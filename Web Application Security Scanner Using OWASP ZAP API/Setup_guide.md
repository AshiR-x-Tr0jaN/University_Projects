# 🛡️ Web Application Security Scanner - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [ZAP Installation (Windows)](#zap-installation)
3. [Python Setup](#python-setup)
4. [Project Installation](#project-installation)
5. [Running the Scanner](#running-the-scanner)
6. [Project Report Guidelines](#project-report)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Prerequisites

### Required Software:
- **Windows 10/11**
- **Java 11 or higher** (for ZAP)
- **Python 3.8+**
- **Internet connection**

---

## 📦 ZAP Installation (Windows)

### Step 1: Download ZAP
1. Visit: https://www.zaproxy.org/download/
2. Download **"ZAP 2.14.0 Windows (64) Installer"**
3. File size: ~300MB

### Step 2: Install ZAP
1. Run the installer (.exe file)
2. Click **Next** through installation
3. Choose installation directory (default: `C:\Program Files\ZAP`)
4. Complete installation

### Step 3: First Launch
1. Open **OWASP ZAP**
2. Select **"No, I do not want to persist this session"**
3. ZAP will start on `localhost:8080` by default

### Step 4: Get API Key
1. In ZAP menu: **Tools → Options → API**
2. Note down the **API Key** (or set it to `changeme` for testing)
3. Keep ZAP running in background

---

## 🐍 Python Setup

### Step 1: Install Python
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check ✅ **"Add Python to PATH"** during installation
3. Verify installation:
```bash
python --version
```

### Step 2: Install Required Libraries
Open Command Prompt and run:

```bash
# Install Python ZAP library
pip install python-owasp-zap-v2.4

# Install other dependencies
pip install flask
pip install requests
```

---

## 🚀 Project Installation

### Step 1: Create Project Folder
```bash
mkdir SecurityScanner
cd SecurityScanner
```

### Step 2: Save Python Script
1. Create file: `scanner.py`
2. Copy the Python code I provided above
3. Save it in the SecurityScanner folder

### Step 3: Create Test Website (Optional)
You can use these safe testing sites:
- http://testphp.vulnweb.com
- http://testhtml5.vulnweb.com
- http://testasp.vulnweb.com

**⚠️ WARNING**: Only scan websites you own or have permission to test!

---

## ▶️ Running the Scanner

### Method 1: Command Line

1. **Start ZAP** (keep it running)
2. **Open Command Prompt** in project folder
3. **Run the scanner**:
```bash
python scanner.py
```

4. **Enter details when prompted**:
   - Target URL: `http://testphp.vulnweb.com`
   - Scan type: Choose 1, 2, or 3

### Method 2: Custom Script

Create `run_scan.py`:
```python
from scanner import SecurityScanner

# Initialize
scanner = SecurityScanner(
    zap_api_key='changeme',
    zap_proxy='http://127.0.0.1:8080'
)

# Scan a website
scan_id = scanner.start_scan(
    target_url='http://testphp.vulnweb.com',
    scan_type='quick'
)

# Generate report
if scan_id:
    scanner.print_summary(scan_id)
    scanner.generate_report(scan_id, 'my_report.html')
```

Run it:
```bash
python run_scan.py
```

---

## 📊 Understanding the Results

### Risk Levels:
- **🔴 High**: Critical vulnerabilities (SQL Injection, XSS)
- **🟡 Medium**: Moderate issues (Missing headers, weak configs)
- **🔵 Low**: Minor issues (Info disclosure, outdated versions)

### Common Vulnerabilities Found:
1. **SQL Injection** - Database manipulation attacks
2. **Cross-Site Scripting (XSS)** - Script injection
3. **CSRF** - Cross-site request forgery
4. **Security Headers Missing** - X-Frame-Options, CSP, etc.
5. **Directory Listing** - Exposed file structure

---

## 📝 Project Report Guidelines

### University Project Structure:

#### 1. **Title Page**
- Project Title: "Web Application Security Scanner using OWASP ZAP"
- Your Name & Roll Number
- Course & Department
- Date

#### 2. **Abstract** (1 page)
- Problem statement
- Proposed solution
- Key features
- Results summary

#### 3. **Introduction** (2-3 pages)
- Background on web security
- Need for automated scanners
- OWASP ZAP overview
- Project objectives

#### 4. **Literature Review** (3-4 pages)
- Existing security tools
- Vulnerabilities types (OWASP Top 10)
- ZAP vs other tools
- Research papers

#### 5. **System Design** (5-6 pages)
- Architecture diagram
- Component details
- Technology stack
- Database schema
- Flowcharts

#### 6. **Implementation** (8-10 pages)
- Code explanation (key functions)
- Screenshots of code
- ZAP configuration
- Database design
- UI screenshots

#### 7. **Testing & Results** (5-6 pages)
- Test cases on 3-5 websites
- Before/after vulnerability comparisons
- Performance metrics
- Sample reports (screenshots)
- Graphs and charts

#### 8. **Conclusion** (1-2 pages)
- What you achieved
- Limitations
- Future enhancements

#### 9. **References**
- OWASP documentation
- Research papers
- Python libraries documentation

---

## 🎨 Making Your Project Stand Out

### Add These Features:

1. **Dashboard UI** (Use the React code I provided)
2. **Email Reports** - Send reports via email
3. **Scheduled Scans** - Automatic daily/weekly scans
4. **Comparison Feature** - Compare multiple scans
5. **Export to PDF** - Professional PDF reports
6. **Vulnerability Prioritization** - Rank by severity

### Extra Credit Ideas:
- Multi-website batch scanning
- False positive detection
- Custom vulnerability rules
- Integration with Slack/Discord for alerts
- Mobile app notification system

---

## 🔧 Troubleshooting

### Problem 1: "Cannot connect to ZAP"
**Solution**: 
- Make sure ZAP is running
- Check if port 8080 is free
- Verify API key is correct

### Problem 2: "Module not found: zapv2"
**Solution**:
```bash
pip uninstall python-owasp-zap-v2.4
pip install python-owasp-zap-v2.4
```

### Problem 3: Scan takes too long
**Solution**:
- Use 'quick' scan type for testing
- Reduce scan scope in ZAP settings
- Use smaller test websites

### Problem 4: No vulnerabilities found
**Solution**:
- Use vulnerable test sites (testphp.vulnweb.com)
- Enable active scanning
- Check ZAP is properly configured

### Problem 5: Database error
**Solution**:
```bash
# Delete old database
del scan_results.db
# Run scanner again
python scanner.py
```

---

## 📚 Useful Resources

### Documentation:
- ZAP Official Docs: https://www.zaproxy.org/docs/
- Python ZAP API: https://github.com/zaproxy/zap-api-python
- OWASP Top 10: https://owasp.org/www-project-top-ten/

### Learning Resources:
- ZAP Getting Started: https://www.zaproxy.org/getting-started/
- Web Security Academy: https://portswigger.net/web-security
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/

### Test Sites (Safe to Scan):
- http://testphp.vulnweb.com
- http://testhtml5.vulnweb.com
- http://testasp.vulnweb.com
- https://juice-shop.herokuapp.com

---

## ✅ Project Checklist

Before submitting your project, make sure:

- [ ] ZAP installed and working
- [ ] Python script runs successfully
- [ ] Successfully scanned at least 3 websites
- [ ] Generated HTML reports
- [ ] Database stores results properly
- [ ] Screenshots documented
- [ ] Code commented properly
- [ ] Report written (20-25 pages)
- [ ] Presentation slides ready (10-15 slides)
- [ ] Demo video recorded (5-10 minutes)

---

## 🎓 Presentation Tips

### What to Show in Demo:
1. **Introduction** (1 min)
   - What is the problem?
   - Why this project?

2. **Live Demo** (3-4 min)
   - Start ZAP
   - Run scanner
   - Show real-time scanning
   - Display results

3. **Results Analysis** (2 min)
   - Show vulnerability report
   - Explain severity levels
   - Show fix recommendations

4. **Technical Architecture** (2 min)
   - System design
   - Technologies used
   - Key features

5. **Q&A** (2 min)

---

## 🎯 Grading Criteria (Typical University Project)

| Component | Weightage |
|-----------|-----------|
| Code Quality & Functionality | 30% |
| Report Documentation | 25% |
| Innovation & Features | 20% |
| Presentation & Demo | 15% |
| Testing & Results | 10% |

---

## 💡 Pro Tips

1. **Start Early**: Testing can reveal unexpected issues
2. **Document Everything**: Take screenshots at every step
3. **Test Multiple Sites**: Shows versatility
4. **Add Visualizations**: Graphs make reports impressive
5. **Explain Security**: Don't just scan, understand vulnerabilities
6. **Compare Tools**: Show why ZAP is good
7. **Real-world Application**: Suggest how companies can use it

---

## 📞 Need Help?

If you face any issues:
1. Check the troubleshooting section
2. Read ZAP documentation
3. Search on Stack Overflow
4. Check ZAP community forums

---

**Good Luck with Your Project! 🚀**

Remember: This tool is for **educational purposes** and **ethical testing only**. Never scan websites without permission!

---

## 📄 License & Disclaimer

This project is for **educational purposes only**. Unauthorized scanning of websites is illegal. Always obtain proper authorization before testing any web application.
