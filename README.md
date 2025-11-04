# EMS Counter

A Python utility that scans and analyzes **Event Management System (EMS)** export reports to count recent alerts, detect Backbone-related issues (`WxBB`), and summarize event statistics.  

This tool is designed to help NOC and infrastructure engineers quickly understand EMS case volume and event distribution between **Backbone (WxBB)** and **CCE (non-WxBB)** events.

---

## 🧠 Overview

`EMS_counter.py` automates the following tasks:

1. Searches your `~/Downloads` folder for the latest EMS export CSV files:
   - `EMSv2-export-PCC_-_Acknowledged`
   - `EMSv2-export-PCC_-_Resolved`
2. Loads the files into Pandas DataFrames.
3. Converts timestamps (`firingStartTime`) to local time (`America/New_York`).
4. Identifies cases that contain **"WxBB"** in their description.
5. Filters cases received within the **last 8 hours**.
6. Prints a summary table showing counts of total EMS, Backbone, and CCE cases.
7. Cleans up the processed CSV files automatically.

---

## 📊 Example Output

```bash
✅ File loaded successfully!
Checking for entries within 8 hours of 2025-11-04 13:45:22

Number of EMS cases in Acknowledge: 34
Number of Backbone cases in Acknowledge: 17
Number of CCE cases in Acknowledge: 17

Number of EMS cases in Resolved: 29
Number of Backbone cases in Resolved: 14
Number of CCE cases in Resolved: 15
```

## Dependency	Purpose
pandas	Data processing and filtering
pathlib	File path management
datetime	Time zone conversion and time window logic

Export the latest Acknowledged and Resolved EMS CSV files into your Downloads folder.

Run the script:
```
python EMS_counter.py
```

View the console output for counts and case summaries.

🧩 File Cleanup

After processing, the script automatically deletes the matched CSVs to prevent clutter in your Downloads directory.

If you prefer to keep the files for auditing, you can comment out the following lines at the bottom of the script:
```
matches_tot[1].unlink()
matches_tot[0].unlink()
```

⚠️ Error Handling

If no matching files are found, you’ll see:

❌ Unexpected error: No files found for Acknowledge or Resolved

If CSVs are malformed or missing fields, Pandas will raise a ParserError, which the script will report gracefully.

🧑‍💻 Author

Eric L. Moore
Network & Automation Engineer
Raleigh, NC
Fluent in Python, Ansible, Kubernetes, and Infrastructure as Code (IaC).
