import datetime
import json
import argparse

from astral import LocationInfo
from astral.sun import local

options = argparse.ArgumentParser()
options.add_argument("-n", "--name", dest="name", help="Location name (free-form text)")
options.add_argument(
    "--lat", dest="latitude", type=float, help="Location latitude (float)"
)
options.add_argument(
    "--lng", dest="longitude", type=float, help="Location longitude (float)"
)
options.add_argument(
    "-d", "--date", dest="date", help="Date to compute times for (yyyy-mm-dd)"
)
options.add_argument("-t", "--tzname", help="Timezone name")
args = options.parse_args()

loc = LocationInfo(args.name or "Somewhere", None, args.tzname, args.latitude, args.longitude, 0)

kwargs = {}
if args.date is not None:
    try:
        kwargs["date"] = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    except:  # noqa: E0722
        kwargs["date"] = datetime.date.today()

if args.tzname is None:
    kwargs["local"] = False

sun = local.sun(**kwargs)

sun_as_str = {}
for key, value in sun.items():
    sun_as_str[key] = sun[key].strftime("%Y-%m-%dT%H:%M:%S")

print(json.dumps(sun_as_str))
