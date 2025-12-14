import sqlite3

def compare_scans(scan_id_1, scan_id_2):
    """Compare two scans and show differences"""
    conn = sqlite3.connect('scan_results.db')
    cursor = conn.cursor()
    
    # Get scan 1 data
    cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id_1,))
    scan1 = cursor.fetchone()
    
    # Get scan 2 data  
    cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id_2,))
    scan2 = cursor.fetchone()
    
    if not scan1 or not scan2:
        print("One or both scans not found!")
        return
    
    print("\n" + "="*60)
    print("SCAN COMPARISON")
    print("="*60)
    
    print(f"\nScan 1: {scan1[1]} ({scan1[3]})")
    print(f"Scan 2: {scan2[1]} ({scan2[3]})")
    
    print(f"\n{'Metric':<20} {'Scan 1':<15} {'Scan 2':<15} {'Difference'}")
    print("-"*60)
    print(f"{'Total Issues':<20} {scan1[5]:<15} {scan2[5]:<15} {scan2[5]-scan1[5]:+d}")
    print(f"{'High Risk':<20} {scan1[6]:<15} {scan2[6]:<15} {scan2[6]-scan1[6]:+d}")
    print(f"{'Medium Risk':<20} {scan1[7]:<15} {scan2[7]:<15} {scan2[7]-scan1[7]:+d}")
    print(f"{'Low Risk':<20} {scan1[8]:<15} {scan2[8]:<15} {scan2[8]-scan1[8]:+d}")
    
    conn.close()

# Usage
if __name__ == "__main__":
    scan_1 = int(input("Enter first scan ID: "))
    scan_2 = int(input("Enter second scan ID: "))
    compare_scans(scan_1, scan_2)
