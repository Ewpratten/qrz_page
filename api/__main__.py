import flask
from webapputils import Webapp
import requests
import os
from .data import *
import timeago
import datetime
import math

# Some metadata
APRS_FI_API_KEY = os.getenv("APRS_FI_API_KEY")
APRS_CALLSIGN = os.getenv("APRS_CALLSIGN")
CALLSIGN = os.getenv("CALLSIGN")
HOME_LATITUDE = math.radians(float(os.getenv("LATITUDE")))
HOME_LONGITUDE = math.radians(float(os.getenv("LONGITUDE")))

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404


@app.route("/")
def index():

    # APRS timestamp
    aprs_timestamp = get_last_position_timestamp(
        APRS_CALLSIGN, APRS_FI_API_KEY)

    # RBN
    rbn_spots = get_recent_rbn_spots(CALLSIGN)
    farthest_distance_abs = 0

    for spot in rbn_spots:
        spotter_lat = math.radians(spot["lat"])
        spotter_lon = math.radians(spot["lon"])
        d_lat = abs(spotter_lat - HOME_LATITUDE)
        d_long = abs(spotter_lon - HOME_LONGITUDE)

        a = math.sin(d_lat / 2)**2 + math.cos(HOME_LATITUDE) * \
            math.cos(spotter_lat) * math.sin(d_long / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = abs(6373.0 * c)

        if distance > farthest_distance_abs:
            farthest_distance_abs = distance

    # Logbook
    recently_logged = get_recent_logs()

    # Data
    last_aprs_humantime = timeago.format(datetime.datetime.fromtimestamp(
        aprs_timestamp, None), datetime.datetime.now()) 
    farthest_distance = f"{round(farthest_distance_abs)} km"
    activity = []

    # Set up rbn data
    for spot in rbn_spots:
        activity.append({
            "type": "spot",
            "other_callsign": spot["spotter"],
            "timestamp": spot["timestamp"],
            "freq": spot["freq"],
            "friendly_time": timeago.format(datetime.datetime.fromtimestamp(spot["timestamp"], None), datetime.datetime.utcnow()) 
        })
    for entry in recently_logged:
        activity.append({
            "type": "contact",
            "other_callsign": entry["other_callsign"],
            "timestamp": entry["timestamp"],
            "freq": "",
            "friendly_time": timeago.format(datetime.datetime.fromtimestamp(entry["timestamp"], None), datetime.datetime.utcnow()) 
        })

    # Sort activity
    activity.sort(key=lambda x: x["timestamp"], reverse=True)

    # Get the last spot time
    if activity:
        last_spot_humantime = timeago.format(datetime.datetime.fromtimestamp(activity[0]["timestamp"], None), datetime.datetime.utcnow())
    else:
        last_spot_humantime = "never"

    # Make response
    res = flask.make_response(flask.render_template('index.html', last_aprs=last_aprs_humantime,
                                                    last_spot=last_spot_humantime, farthest_distance=farthest_distance, activity=activity[:5], age=datetime.datetime.now().year - 2003))
    res.headers.set('Cache-Control', 's-maxage=120, stale-while-revalidate')
    return res


if __name__ == "__main__":
    app.run(debug=True)
