"""
Web Application Security Scanner
Using OWASP ZAP for automated vulnerability detection
"""

import time
import json
from datetime import datetime
from zapv2 import ZAPv2
import sqlite3
from pathlib import Path

class SecurityScanner:
    def __init__(self, zap_api_key='changeme', zap_proxy='http://127.0.0.1:8080'):
        """Initialize ZAP connection"""
        self.zap = ZAPv2(apikey=zap_api_key, proxies={'http': zap_proxy, 'https': zap_proxy})
        self.db_path = 'scan_results.db'
        self.init_database()
    
    def init_database(self):
        """Create database for storing scan results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_alerts INTEGER DEFAULT 0,
                high_risk INTEGER DEFAULT 0,
                medium_risk INTEGER DEFAULT 0,
                low_risk INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                alert_name TEXT,
                risk_level TEXT,
                confidence TEXT,
                url TEXT,
                description TEXT,
                solution TEXT,
                reference TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("[+] Database initialized successfully")
    
    def start_scan(self, target_url, scan_type='quick'):
        """Start a new security scan"""
        print(f"\n[+] Starting {scan_type} scan for: {target_url}")
        
        # Save scan info to database
        scan_id = self.save_scan_info(target_url, scan_type)
        
        try:
            # Step 1: Access the target
            print("[+] Accessing target URL...")
            self.zap.urlopen(target_url)
            time.sleep(2)
            
            # Step 2: Spider the target
            print("[+] Spidering the target...")
            spider_id = self.zap.spider.scan(target_url)
            
            while int(self.zap.spider.status(spider_id)) < 100:
                print(f"    Spider progress: {self.zap.spider.status(spider_id)}%")
                time.sleep(2)
            
            print("[+] Spider completed")
            
            # Step 3: Passive scan (automatic)
            print("[+] Running passive scan...")
            time.sleep(5)
            
            # Step 4: Active scan (if not quick scan)
            if scan_type != 'quick':
                print("[+] Starting active scan...")
                active_scan_id = self.zap.ascan.scan(target_url)
                
                while int(self.zap.ascan.status(active_scan_id)) < 100:
                    print(f"    Active scan progress: {self.zap.ascan.status(active_scan_id)}%")
                    time.sleep(5)
                
                print("[+] Active scan completed")
            
            # Step 5: Get results
            print("[+] Collecting results...")
            alerts = self.zap.core.alerts(baseurl=target_url)
            
            # Process and save results
            self.process_results(scan_id, alerts)
            
            print(f"[+] Scan completed! Found {len(alerts)} vulnerabilities")
            return scan_id
            
        except Exception as e:
            print(f"[!] Error during scan: {str(e)}")
            self.update_scan_status(scan_id, 'failed')
            return None
    
    def save_scan_info(self, target_url, scan_type):
        """Save scan information to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scans (target_url, scan_type, start_time, status)
            VALUES (?, ?, ?, 'running')
        ''', (target_url, scan_type, datetime.now().isoformat()))
        
        scan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return scan_id
    
    def process_results(self, scan_id, alerts):
        """Process and save vulnerability results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        high_count = 0
        medium_count = 0
        low_count = 0
        
        for alert in alerts:
            risk = alert.get('risk', 'Informational')
            
            if risk == 'High':
                high_count += 1
            elif risk == 'Medium':
                medium_count += 1
            elif risk == 'Low':
                low_count += 1
            
            cursor.execute('''
                INSERT INTO vulnerabilities 
                (scan_id, alert_name, risk_level, confidence, url, description, solution, reference)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                scan_id,
                alert.get('alert', 'Unknown'),
                alert.get('risk', 'Informational'),
                alert.get('confidence', 'Unknown'),
                alert.get('url', ''),
                alert.get('description', ''),
                alert.get('solution', ''),
                alert.get('reference', '')
            ))
        
        # Update scan summary
        cursor.execute('''
            UPDATE scans 
            SET end_time = ?, total_alerts = ?, high_risk = ?, 
                medium_risk = ?, low_risk = ?, status = 'completed'
            WHERE id = ?
        ''', (datetime.now().isoformat(), len(alerts), high_count, 
              medium_count, low_count, scan_id))
        
        conn.commit()
        conn.close()
    
    def update_scan_status(self, scan_id, status):
        """Update scan status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE scans SET status = ? WHERE id = ?', (status, scan_id))
        conn.commit()
        conn.close()
    
    def generate_report(self, scan_id, output_file='security_report.html'):
        """Generate HTML report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get scan info
        cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
        scan = cursor.fetchone()
        
        if not scan:
            print("[!] Scan not found")
            return
        
        # Get vulnerabilities
        cursor.execute('SELECT * FROM vulnerabilities WHERE scan_id = ?', (scan_id,))
        vulns = cursor.fetchall()
        
        # Generate HTML report
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Security Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 30px; border-radius: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .high {{ border-left: 5px solid #e74c3c; }}
        .medium {{ border-left: 5px solid #f39c12; }}
        .low {{ border-left: 5px solid #3498db; }}
        .vuln-item {{ background: white; padding: 20px; margin: 10px 0; border-radius: 10px; }}
        .risk-high {{ color: #e74c3c; }}
        .risk-medium {{ color: #f39c12; }}
        .risk-low {{ color: #3498db; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Web Application Security Report</h1>
        <p><strong>Target:</strong> {scan[1]}</p>
        <p><strong>Scan Type:</strong> {scan[2]}</p>
        <p><strong>Date:</strong> {scan[3]}</p>
    </div>
    
    <div class="summary">
        <div class="card">
            <h3>Total Issues</h3>
            <h1>{scan[5]}</h1>
        </div>
        <div class="card high">
            <h3>High Risk</h3>
            <h1 class="risk-high">{scan[6]}</h1>
        </div>
        <div class="card medium">
            <h3>Medium Risk</h3>
            <h1 class="risk-medium">{scan[7]}</h1>
        </div>
        <div class="card low">
            <h3>Low Risk</h3>
            <h1 class="risk-low">{scan[8]}</h1>
        </div>
    </div>
    
    <h2>Detailed Findings</h2>
'''
        
        for vuln in vulns:
            risk_class = f"risk-{vuln[3].lower()}"
            html += f'''
    <div class="vuln-item {vuln[3].lower()}">
        <h3>{vuln[2]} <span class="{risk_class}">[{vuln[3]}]</span></h3>
        <p><strong>URL:</strong> {vuln[5]}</p>
        <p><strong>Description:</strong> {vuln[6]}</p>
        <p><strong>Solution:</strong> {vuln[7]}</p>
        <p><strong>Confidence:</strong> {vuln[4]}</p>
    </div>
'''
        
        html += '''
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[+] Report generated: {output_file}")
        conn.close()
    
    def get_scan_history(self, limit=10):
        """Get scan history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scans ORDER BY id DESC LIMIT ?', (limit,))
        scans = cursor.fetchall()
        conn.close()
        return scans
    
    def print_summary(self, scan_id):
        """Print scan summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
        scan = cursor.fetchone()
        
        if scan:
            print("\n" + "="*60)
            print("SCAN SUMMARY")
            print("="*60)
            print(f"Target URL: {scan[1]}")
            print(f"Scan Type: {scan[2]}")
            print(f"Total Vulnerabilities: {scan[5]}")
            print(f"High Risk: {scan[6]}")
            print(f"Medium Risk: {scan[7]}")
            print(f"Low Risk: {scan[8]}")
            print(f"Status: {scan[9]}")
            print("="*60 + "\n")
        
        conn.close()


# Main execution
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        Web Application Security Scanner v1.0             ║
    ║              Powered by OWASP ZAP                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize scanner
    scanner = SecurityScanner()
    
    # Example usage
    print("\n[*] Make sure ZAP is running on localhost:8080")
    print("[*] ZAP API Key should be set (default: changeme)\n")
    
    # Get user input
    target_url = input("Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()
    
    if not target_url:
        target_url = "http://testphp.vulnweb.com"
        print(f"[*] Using default test site: {target_url}")
    
    print("\nScan Types:")
    print("1. Quick Scan (Spider + Passive)")
    print("2. Standard Scan (Spider + Passive + Active)")
    print("3. Deep Scan (Full scan with all checks)")
    
    choice = input("\nSelect scan type (1-3): ").strip()
    
    scan_types = {'1': 'quick', '2': 'standard', '3': 'deep'}
    scan_type = scan_types.get(choice, 'quick')
    
    # Start scan
    scan_id = scanner.start_scan(target_url, scan_type)
    
    if scan_id:
        # Print summary
        scanner.print_summary(scan_id)
        
        # Generate report
        report_file = f"security_report_{scan_id}.html"
        scanner.generate_report(scan_id, report_file)
        
        print(f"[+] All done! Check {report_file} for detailed report")
    else:
        print("[!] Scan failed. Please check ZAP connection and try again.")
