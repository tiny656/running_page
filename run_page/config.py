import os
from collections import namedtuple

# getting content root directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

OUTPUT_DIR = os.path.join(parent, "activities")
# Sync paths can be overridden via env vars so smoke tests / alternate setups
# can redirect to fixtures or tmp dirs without touching the user's real data.
GPX_FOLDER = os.environ.get("GPX_FOLDER", os.path.join(parent, "GPX_OUT"))
TCX_FOLDER = os.environ.get("TCX_FOLDER", os.path.join(parent, "TCX_OUT"))
FIT_FOLDER = os.environ.get("FIT_FOLDER", os.path.join(parent, "FIT_OUT"))
PNG_FOLDER = os.path.join(parent, "PNG_OUT")
ENDOMONDO_FILE_DIR = os.path.join(parent, "Workouts")
FOLDER_DICT = {
    "gpx": GPX_FOLDER,
    "tcx": TCX_FOLDER,
    "fit": FIT_FOLDER,
}
SQL_FILE = os.environ.get("SQL_FILE", os.path.join(parent, "run_page", "data.db"))
JSON_FILE = os.environ.get(
    "JSON_FILE", os.path.join(parent, "src", "static", "activities.json")
)
SYNCED_FILE = os.environ.get("SYNCED_FILE", os.path.join(parent, "imported.json"))


BASE_TIMEZONE = "Asia/Shanghai"
UTC_TIMEZONE = "UTC"

start_point = namedtuple("start_point", "lat lon")
run_map = namedtuple("polyline", "summary_polyline")
