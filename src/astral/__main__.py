import argparse
import datetime
import json
from typing import Any, Dict

from astral import LocationInfo, Observer, sun

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo  # type: ignore

options = argparse.ArgumentParser()
options.add_argument(
    "-n",
    "--name",
    dest="name",
    default="Somewhere",
    help="Location name (free-form text)",
)
options.add_argument(
    "-r", "--region", dest="region", default="On Earth", help="Region (free-form text)"
)
options.add_argument(
    "-d", "--date",
    dest="date",
    type=datetime.date.fromisoformat,
    default=datetime.date.today(),
    help="Date to compute times for (yyyy-mm-dd)",
)
options.add_argument("-t", "--tzname", help="Timezone name")
options.add_argument("latitude", type=float, help="Location latitude (float)")
options.add_argument("longitude", type=float, help="Location longitude (float)")
options.add_argument(
    "elevation", nargs="?", type=float, default=0, help="Elevation in metres (float)"
)
args = options.parse_args()

loc = LocationInfo(
    args.name,
    args.region,
    args.tzname,
    args.latitude,
    args.longitude,
)

obs = Observer(args.latitude, args.longitude, args.elevation)

kwargs: Dict[str, Any] = {}
kwargs["observer"] = obs
kwargs["date"] = args.date

sun_as_str = {}
format_str = "%Y-%m-%dT%H:%M:%S"
if args.tzname is None:
    kwargs["tzinfo"] = datetime.timezone.utc
    format_str += "Z"
else:
    kwargs["tzinfo"] = zoneinfo.ZoneInfo(loc.timezone)
    format_str += "%z"


s = sun.sun(**kwargs)

for key, value in s.items():
    sun_as_str[key] = s[key].strftime(format_str)

sun_as_str["timezone"] = kwargs["tzinfo"].tzname
sun_as_str["location"] = f"{loc.name}, {loc.region}"

print(json.dumps(sun_as_str))
