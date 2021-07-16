import requests
from typing import List
import datetime
import calendar

def get_recent_rbn_spots(callsign: str) -> List[dict]:

    res = requests.get(f"http://www.reversebeacon.net/dxsd1/sk.php?s=0&r=100&cdx={callsign}", headers={
        "Host": "www.reversebeacon.net",
        "Referer": f"http://www.reversebeacon.net/dxsd1/dxsd1.php?f=0&t=dx&c={callsign}"
    })

    if int(res.status_code / 100) != 2:
        return []

    res_json = res.json()

    output = []

    if "s"  in res_json:
        for entry in res_json["s"]:

            # Get obfuscated "diff" value
            # diff = round(datetime.datetime.now(tz = datetime.timezone.utc).timestamp() /
            #              1000) - res_json["s"][entry][6]

            raw_time = res_json["s"][entry][5].split(" ")
            raw_t = raw_time[0].replace("z", "")
            hour = raw_t[:2]
            minute = raw_t[2:]
            day_num = raw_time[1]
            month_name = calendar.month_name[list(calendar.month_abbr).index(raw_time[2])]
            year = datetime.datetime.now().year

            # Construct a parsable time string
            time_str = f"{hour}:{minute} {day_num} {month_name}, {year}"

            # Build obj
            output.append({
                "spotter": res_json["s"][entry][0],
                "freq": res_json["s"][entry][1],
                "timestamp": datetime.datetime.strptime(time_str, "%H:%M %d %B, %Y").timestamp(),
                "lat": float(res_json["ci"][res_json["s"][entry][0]][6]),
                "lon": float(res_json["ci"][res_json["s"][entry][0]][7]),
            })

    return output
