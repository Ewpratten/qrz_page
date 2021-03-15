import requests
from typing import List
import dateutil.parser


def get_recent_logs() -> List[dict]:

    res = requests.get(
        "https://cloudlog.i.retrylife.ca/index.php/logbook/qso_map/10")

    if int(res.status_code / 100) != 2:
        return []

    res_json = res.json()

    output = []
    for entry in res_json["markers"]:

        # Parse out date
        html = entry["html"].split("<br />")
        date_str = html[1].split(": ")[1]
        timestamp = dateutil.parser.parse(date_str).timestamp()

        output.append({
            "other_callsign": entry["label"],
            "timestamp": timestamp
        })

    return output