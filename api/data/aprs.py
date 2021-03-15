import requests
from typing import Optional


def get_last_position_timestamp(callsign: str, api_key: str) -> Optional[float]:

    res = requests.get(f"https://api.aprs.fi/api/get?name={callsign}&what=loc&apikey={api_key}&format=json", headers={
        "User-Agent": "hambadges/1.x (https://github.com/Ewpratten/hambadges)"
    })

    if int(res.status_code / 100) != 2:
        return None

    res_json = res.json()

    if res_json["result"] != "ok":
        return None

    if not res_json["entries"]:
        return None

    # NOTE: There is more information to be had from this API. Maybe extend this"
    return int(res_json["entries"][0]["time"])