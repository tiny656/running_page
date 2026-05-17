"""Regenerate the synthetic GPX/FIT fixtures used by tests/smoke_sync.py.

The fixtures are committed to the repo so the smoke test stays fast and
focused on the parsing/persist path. Re-run this only when you intentionally
want to change fixture shape (e.g. add a new field the parser cares about).

Usage:
    python tests/fixtures/generate_fixtures.py
"""

import datetime
import os
import sys

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.messages.session_message import SessionMessage
from fit_tool.profile.profile_type import FileType, Manufacturer, Sport

HERE = os.path.dirname(os.path.realpath(__file__))
FIT_DIR = os.path.join(HERE, "fit")
GPX_DIR = os.path.join(HERE, "gpx")

# 10 synthetic Shanghai-area points, ~88m apart, ~790m total.
POINTS = [
    (31.2304, 121.4737),
    (31.2310, 121.4743),
    (31.2316, 121.4749),
    (31.2322, 121.4755),
    (31.2328, 121.4761),
    (31.2334, 121.4767),
    (31.2340, 121.4773),
    (31.2346, 121.4779),
    (31.2352, 121.4785),
    (31.2358, 121.4791),
]
START_UTC = datetime.datetime(2024, 1, 1, 8, 0, 0, tzinfo=datetime.timezone.utc)
STEP_S = 5
TOTAL_DISTANCE_M = 800.0
ELEVATION_M = 10.0
HEART_RATE = 150


def _start_unix_ms() -> int:
    return int(START_UTC.timestamp() * 1000)


def write_fit(out_path: str) -> None:
    builder = FitFileBuilder(auto_define=True)

    fid = FileIdMessage()
    fid.type = FileType.ACTIVITY
    fid.manufacturer = Manufacturer.DEVELOPMENT
    fid.product = 0
    fid.time_created = _start_unix_ms()
    fid.serial_number = 0x12345678
    builder.add(fid)

    for i, (lat, lon) in enumerate(POINTS):
        rec = RecordMessage()
        rec.timestamp = _start_unix_ms() + i * STEP_S * 1000
        rec.position_lat = lat
        rec.position_long = lon
        rec.altitude = ELEVATION_M
        rec.heart_rate = HEART_RATE
        builder.add(rec)

    elapsed_s = (len(POINTS) - 1) * STEP_S
    sess = SessionMessage()
    sess.start_time = _start_unix_ms()
    sess.timestamp = _start_unix_ms() + elapsed_s * 1000
    sess.total_elapsed_time = elapsed_s
    sess.total_timer_time = elapsed_s
    sess.total_distance = TOTAL_DISTANCE_M
    sess.sport = Sport.RUNNING
    sess.avg_heart_rate = HEART_RATE
    sess.avg_speed = TOTAL_DISTANCE_M / elapsed_s
    builder.add(sess)

    fit = builder.build()
    fit.to_file(out_path)


def write_gpx(out_path: str) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="running_page-smoke-test" '
        'xmlns="http://www.topografix.com/GPX/1/1">',
        "  <trk>",
        "    <name>smoke-test run</name>",
        "    <type>running</type>",
        "    <trkseg>",
    ]
    for i, (lat, lon) in enumerate(POINTS):
        ts = (START_UTC + datetime.timedelta(seconds=i * STEP_S)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        lines.extend(
            [
                f'      <trkpt lat="{lat}" lon="{lon}">',
                f"        <ele>{ELEVATION_M}</ele>",
                f"        <time>{ts}</time>",
                "      </trkpt>",
            ]
        )
    lines.extend(["    </trkseg>", "  </trk>", "</gpx>", ""])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> int:
    os.makedirs(FIT_DIR, exist_ok=True)
    os.makedirs(GPX_DIR, exist_ok=True)

    fit_path = os.path.join(FIT_DIR, "sample_run.fit")
    gpx_path = os.path.join(GPX_DIR, "sample_run.gpx")

    write_fit(fit_path)
    write_gpx(gpx_path)

    print(f"wrote {fit_path} ({os.path.getsize(fit_path)} bytes)")
    print(f"wrote {gpx_path} ({os.path.getsize(gpx_path)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
