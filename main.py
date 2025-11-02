import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone

from numpy.f2py.auxfuncs import throw_error


def main():

    rawtimestamp = datetime.now()
    timestamp = f"{rawtimestamp.hour}:{rawtimestamp.minute}:{rawtimestamp.second}"
    #ack_path = Path.home() / "Downloads" / "ack.csv"
    #res_path = Path.home() / "Downloads" / "res.csv"

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

        # Parse ISO8601 timestamps (UTC) and convert to local timezone
        ack_df['lastReceived'] = pd.to_datetime(ack_df['firingStartTime'], utc=True, errors='coerce')
        ack_df['lastReceived_local'] = ack_df['lastReceived'].dt.tz_convert('America/New_York')
        res_df['lastReceived'] = pd.to_datetime(res_df['firingStartTime'], utc=True, errors='coerce')
        res_df['lastReceived_local'] = res_df['lastReceived'].dt.tz_convert('America/New_York')

        # Current local time (aware)
        now = datetime.now(timezone.utc).astimezone()  # same zone as tz_convert
        window = timedelta(hours=8)

        print(f"Checking for entries within 8 hours of {now:%Y-%m-%d %H:%M:%S}")

        # Filter rows newer than (now - 8 hours)
        ack_recent = ack_df[ack_df['lastReceived_local'] > (now - window)]
        res_recent = res_df[res_df['lastReceived_local'] > (now - window)]

        # for t in recent['lastReceived_local']:
        #     print(t)
        print(f"Number of EMS cases in Acknowledge:{ack_recent.lastReceived_local.size}")
        print(f"Number of EMS cases in Resolved:{res_recent.lastReceived_local.size}")
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
