"""End-to-end smoke test for the GPX and FIT sync entry points.

Runs ``run_page/fit_sync.py`` and ``run_page/gpx_sync.py`` against the tiny
synthetic fixtures under ``tests/fixtures/``, with all output paths redirected
to a temporary directory via environment variables so the user's real
``data.db`` and ``activities.json`` are never touched.

Asserts that the resulting JSON contains one activity per fixture, that the
``summary_polyline`` is non-empty, and that the decoded start/end coordinates
match the fixture endpoints within a small tolerance. The endpoint check is
what catches the polyline-trimming regression class of bugs (see commits
``b8dd923d`` and ``1e58d6fd``) -- a silent trim would shift the endpoints
inward by several metres.

Exits non-zero on any failure so CI fails loudly.
"""

import json
import os
import subprocess
import sys
import tempfile
from math import asin, cos, radians, sin, sqrt

HERE = os.path.dirname(os.path.realpath(__file__))
REPO_ROOT = os.path.dirname(HERE)
FIXTURE_DIR = os.path.join(HERE, "fixtures")

# These must match tests/fixtures/generate_fixtures.py's POINTS[0] and [-1].
EXPECTED_START = (31.2304, 121.4737)
EXPECTED_END = (31.2358, 121.4791)
ENDPOINT_TOLERANCE_M = 5.0


def haversine_m(p1, p2):
    lat1, lon1 = radians(p1[0]), radians(p1[1])
    lat2, lon2 = radians(p2[0]), radians(p2[1])
    a = (
        sin((lat2 - lat1) / 2) ** 2
        + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * 6371000 * asin(sqrt(a))


def fail(label, msg):
    print(f"[{label}] FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def run_case(label, sync_script, folder_env_key, fixture_subdir):
    """Run one sync entry point against its fixture dir, assert on the JSON."""
    with tempfile.TemporaryDirectory(prefix=f"running_page_smoke_{label}_") as tmp:
        empty = os.path.join(tmp, "_empty")
        os.mkdir(empty)

        env = os.environ.copy()
        # Point every input folder somewhere safe; override only the one we want.
        env["GPX_FOLDER"] = empty
        env["FIT_FOLDER"] = empty
        env["TCX_FOLDER"] = empty
        env[folder_env_key] = os.path.join(FIXTURE_DIR, fixture_subdir)
        env["SQL_FILE"] = os.path.join(tmp, "data.db")
        env["JSON_FILE"] = os.path.join(tmp, "activities.json")
        env["SYNCED_FILE"] = os.path.join(tmp, "imported.json")

        proc = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, "run_page", sync_script)],
            env=env,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            fail(label, f"{sync_script} exited {proc.returncode}")

        json_path = env["JSON_FILE"]
        if not os.path.exists(json_path):
            fail(label, f"sync did not write {json_path}")

        with open(json_path) as f:
            activities = json.load(f)

        if len(activities) != 1:
            fail(label, f"expected 1 activity, got {len(activities)}")

        a = activities[0]
        if a.get("type") != "Run":
            fail(label, f"expected type='Run', got {a.get('type')!r}")
        if not a.get("distance") or a["distance"] <= 0:
            fail(label, f"expected positive distance, got {a.get('distance')!r}")

        poly = a.get("summary_polyline")
        if not poly:
            fail(label, "summary_polyline is empty (possible polyline-trim regression)")

        # Local import so we don't require polyline at module import time.
        import polyline

        pts = polyline.decode(poly)
        if len(pts) < 2:
            fail(label, f"polyline decoded to {len(pts)} points (<2)")

        start_drift = haversine_m(pts[0], EXPECTED_START)
        end_drift = haversine_m(pts[-1], EXPECTED_END)
        if start_drift > ENDPOINT_TOLERANCE_M:
            fail(
                label,
                f"start drifted {start_drift:.2f}m from fixture "
                f"(>{ENDPOINT_TOLERANCE_M}m; polyline-trim regression?)",
            )
        if end_drift > ENDPOINT_TOLERANCE_M:
            fail(
                label,
                f"end drifted {end_drift:.2f}m from fixture "
                f"(>{ENDPOINT_TOLERANCE_M}m; polyline-trim regression?)",
            )

        print(
            f"[{label}] OK: 1 activity, {len(pts)} polyline points, "
            f"start drift {start_drift:.2f}m, end drift {end_drift:.2f}m"
        )


def main():
    run_case("fit", "fit_sync.py", "FIT_FOLDER", "fit")
    run_case("gpx", "gpx_sync.py", "GPX_FOLDER", "gpx")
    print("sync smoke: all checks passed")


if __name__ == "__main__":
    main()
