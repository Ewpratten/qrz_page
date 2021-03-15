import flask
from webapputils import Webapp
import requests

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404
    # return flask.render_template('404.html'), 404


@app.route("/")
def index():

    # Mock data
    last_aprs_humantime = "1 minute ago"
    last_spot_humantime = "1 hour ago"
    farthest_distance = "1000km"
    activity = [
        {
            "type": "contact",
            "other_callsign": "VE3TEST",
            "freq": 7030.0,
            "timestamp": 100023459
        },
        {
            "type": "contact",
            "other_callsign": "V02TEST",
            "freq": 7130.0,
            "timestamp": 100023459
        },
        {
            "type": "spot",
            "other_callsign": "VA1SPOT",
            "freq": 14058.0,
            "timestamp": 10002345
        }
    ]

    # Make response
    res = flask.make_response(flask.render_template('index.html', last_aprs=last_aprs_humantime,
                                                    last_spot=last_spot_humantime, farthest_distance=farthest_distance, activity=activity))
    res.headers.set('Cache-Control', 's-maxage=120, stale-while-revalidate')
    return res


if __name__ == "__main__":
    app.run(debug=True)
