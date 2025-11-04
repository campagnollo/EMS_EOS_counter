"""
EMS_counter.py
----------------
This script analyzes recent EMS (Event Management System) export files—specifically
the "Acknowledged" and "Resolved" CSV reports—stored in the user's Downloads directory.
It identifies recent alerts, filters those containing the keyword “WxBB,” and prints
summary counts for Backbone and CCE (non-Backbone) cases.

**Main Workflow:**
1. Searches the user's ~/Downloads directory for the most recent CSV files matching:
   - "EMSv2-export-PCC_-_Acknowledged"
   - "EMSv2-export-PCC_-_Resolved"
2. Loads both CSVs into Pandas DataFrames.
3. Converts the `firingStartTime` column to localized datetimes (America/New_York).
4. Flags rows containing "WxBB" in their `description` field.
5. Calculates counts of Backbone (WxBB) and CCE (non-WxBB) cases received
   within the past 8 hours.
6. Prints a structured summary of EMS and Backbone case totals for both
   Acknowledged and Resolved data sets.
7. Cleans up temporary CSVs after processing.

**Output Example:**
- Number of EMS cases in Acknowledge: N
- Number of Backbone cases in Acknowledge: M
- Number of CCE cases in Acknowledge: (N - M)
- Number of EMS cases in Resolved: X
- Number of Backbone cases in Resolved: Y
- Number of CCE cases in Resolved: (X - Y)

**Error Handling:**
- Gracefully reports missing or malformed files.
- Catches and displays parsing or unexpected runtime errors.

**Dependencies:**
- pandas
- pathlib
- datetime

**Author:** Eric L. Moore
**Last Updated:** November 2025
"""
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone




def main():

    rawtimestamp = datetime.now()



    try:
        ack_path = Path.home() / "Downloads"
        res_path = Path.home() / "Downloads"
        pattern_ack = "EMSv2-export-PCC_-_Acknowledged"
        pattern_res = "EMSv2-export-PCC_-_Resolved"
        matches_ack = [p for p in ack_path.rglob("*") if pattern_ack in p.name]
        matches_res = [p for p in res_path.rglob("*") if pattern_res in p.name]
        if len(matches_ack)==0 and len(matches_res)==0:
            raise Exception(f"No files found for Acknowledge or Resolved")
        matches_tot = [matches_ack[0], matches_res[0]]
        ack_df = pd.read_csv(matches_tot[0])
        res_df = pd.read_csv(matches_tot[1])
        print("✅ File loaded successfully!")


        ack_df['lastReceived'] = pd.to_datetime(ack_df['firingStartTime'], utc=True, errors='coerce')
        ack_df['lastReceived_local'] = ack_df['lastReceived'].dt.tz_convert('America/New_York')
        ack_df['WxBB'] = ack_df['description'].str.contains("WxBB", case=False, na=False)
        ack_wxbb_count = ack_df['WxBB'].sum()


        res_df['lastReceived'] = pd.to_datetime(res_df['firingStartTime'], utc=True, errors='coerce')
        res_df['lastReceived_local'] = res_df['lastReceived'].dt.tz_convert('America/New_York')
        res_df['WxBB'] = res_df['description'].str.contains("WxBB", case=False, na=False)
        res_wxbb_count = ack_df['WxBB'].sum()


        now = datetime.now(timezone.utc).astimezone()
        window = timedelta(hours=8)

        print(f"Checking for entries within 8 hours of {now:%Y-%m-%d %H:%M:%S}")


        ack_recent = ack_df[ack_df['lastReceived_local'] > (now - window)]
        res_recent = res_df[res_df['lastReceived_local'] > (now - window)]


        print(f"Number of EMS cases in Acknowledge:{ack_recent.lastReceived_local.size}")
        print(f"Number of Backbone cases in Acknowledge:{ack_wxbb_count}")
        print(f"Number of CCE cases in Acknowledge:{ack_recent.lastReceived_local.size - ack_wxbb_count}\n")
        print(f"Number of EMS cases in Resolved:{res_recent.lastReceived_local.size}")
        print(f"Number of Backbone cases in Resolved:{res_wxbb_count}")
        print(f"Number of CCE cases in Acknowledge:{res_recent.lastReceived_local.size - res_wxbb_count}\n\n")
        print("")

    except FileNotFoundError:
        print(f"❌ File not found: {ack_path}")
    except pd.errors.ParserError as e:
        print(f"❌ Error parsing CSV: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    finally:
        matches_tot[1].unlink()
        matches_tot[0].unlink()


if __name__ == '__main__':
    main()
