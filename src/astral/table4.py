from math import cos, sin
from typing import Callable, Dict, List, NamedTuple


class Table4Row(NamedTuple):
    coefficient: float
    t: bool
    sincos: Callable[[float], float]
    argument_multiplers: Dict[int, int]


Gm = 2  # Moon mean anomoly
Fm = 3  # Moon argument of latitude
D = 4  # Moon mean elongation from sun
Om = 5  # Longitude of the lunar ascending node
Ls = 7  # Sun mean longitude
Gs = 8  # Sun mean anomoly
L2 = 12  # Venus mean longitude

table4_v: List[Table4Row] = [
    Table4Row(0.39558, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.08200, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.03257, False, sin, {Gm: 1, Fm: -1, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.01092, False, sin, {Gm: 1, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00666, False, sin, {Gm: 1, Fm: -1, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00644, False, sin, {Gm: 1, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00331, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00304, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(
        -0.00240, False, sin, {Gm: 1, Fm: -1, D: -2, Om: -1, Ls: 0, Gs: 0, L2: 0}
    ),
    Table4Row(0.00226, False, sin, {Gm: 1, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00108, False, sin, {Gm: 1, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00079, False, sin, {Gm: 0, Fm: 1, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00078, False, sin, {Gm: 0, Fm: 1, D: 2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00066, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00062, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00050, False, sin, {Gm: 1, Fm: -1, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00045, False, sin, {Gm: 2, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00031, False, sin, {Gm: 2, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00027, False, sin, {Gm: 1, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00024, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00021, True, sin, {Gm: 0, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00018, False, sin, {Gm: 0, Fm: 1, D: -1, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00016, False, sin, {Gm: 0, Fm: 1, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00016, False, sin, {Gm: 1, Fm: -1, D: 0, Om: -1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00016, False, sin, {Gm: 2, Fm: -1, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00015, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(
        -0.00012, False, sin, {Gm: 1, Fm: -1, D: -2, Om: -1, Ls: 0, Gs: 1, L2: 0}
    ),
    Table4Row(-0.00011, False, sin, {Gm: 1, Fm: -1, D: 0, Om: -1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00009, False, sin, {Gm: 1, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00009, False, sin, {Gm: 2, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00008, False, sin, {Gm: 2, Fm: -1, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00008, False, sin, {Gm: 1, Fm: 1, D: 2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00008, False, sin, {Gm: 0, Fm: 3, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00007, False, sin, {Gm: 1, Fm: -1, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(
        -0.00007, False, sin, {Gm: 2, Fm: -1, D: -2, Om: -1, Ls: 0, Gs: 0, L2: 0}
    ),
    Table4Row(-0.00007, False, sin, {Gm: 1, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00006, False, sin, {Gm: 0, Fm: 1, D: 1, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00006, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00006, False, sin, {Gm: 1, Fm: -1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00006, False, sin, {Gm: 0, Fm: 1, D: 2, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00005, False, sin, {Gm: 1, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00004, False, sin, {Gm: 2, Fm: 1, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00004, False, sin, {Gm: 1, Fm: -3, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00004, False, sin, {Gm: 1, Fm: -1, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 1, Fm: -1, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 0, Fm: 1, D: -1, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 0, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 0, Fm: 1, D: -2, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 1, Fm: 1, D: -2, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 0, Fm: 1, D: -1, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: -1, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 0, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 1, Fm: 1, D: -1, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: 1, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 3, Fm: 1, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(
        -0.00002, False, sin, {Gm: 2, Fm: -1, D: -4, Om: -1, Ls: 0, Gs: 0, L2: 0}
    ),
    Table4Row(
        0.00002, False, sin, {Gm: 1, Fm: -1, D: -2, Om: -1, Ls: 0, Gs: -1, L2: 0}
    ),
    Table4Row(-0.00002, True, sin, {Gm: 1, Fm: -1, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(
        -0.00002, False, sin, {Gm: 1, Fm: -1, D: -4, Om: -1, Ls: 0, Gs: 0, L2: 0}
    ),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: 1, D: -4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 2, Fm: -1, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 1, Fm: 1, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 1, Fm: 1, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
]

table4_u: List[Table4Row] = [
    Table4Row(1, False, cos, {Gm: 0, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.10828, False, cos, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.01880, False, cos, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.01479, False, cos, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00181, False, cos, {Gm: 2, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00147, False, cos, {Gm: 2, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00105, False, cos, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00075, False, cos, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00067, False, cos, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00057, False, cos, {Gm: 0, Fm: 0, D: 1, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00055, False, cos, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00046, False, cos, {Gm: 1, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00041, False, cos, {Gm: 1, Fm: -2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00024, False, cos, {Gm: 0, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00017, False, cos, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00013, False, cos, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00010, False, cos, {Gm: 1, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00009, False, cos, {Gm: 0, Fm: 0, D: 1, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00007, False, cos, {Gm: 2, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00006, False, cos, {Gm: 3, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00006, False, cos, {Gm: 0, Fm: 2, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00005, False, cos, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -2, L2: 0}),
    Table4Row(-0.00005, False, cos, {Gm: 2, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00005, False, cos, {Gm: 1, Fm: 2, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00005, False, cos, {Gm: 1, Fm: 0, D: -1, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00004, False, cos, {Gm: 1, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00004, False, cos, {Gm: 3, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00003, False, cos, {Gm: 1, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00003, False, cos, {Gm: 2, Fm: -2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00003, False, cos, {Gm: 0, Fm: 2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
]


table4_w: List[Table4Row] = [
    Table4Row(0.10478, False, sin, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.04105, False, sin, {Gm: 0, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.02130, False, sin, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.01779, False, sin, {Gm: 0, Fm: 2, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.01774, False, sin, {Gm: 0, Fm: 0, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00987, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00338, False, sin, {Gm: 1, Fm: -2, D: 0, Om: -2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00309, False, sin, {Gm: 0, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00190, False, sin, {Gm: 0, Fm: 2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00144, False, sin, {Gm: 1, Fm: 0, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00144, False, sin, {Gm: 1, Fm: -2, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00113, False, sin, {Gm: 1, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00094, False, sin, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00092, False, sin, {Gm: 2, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00071, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00070, False, sin, {Gm: 2, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00067, False, sin, {Gm: 1, Fm: 2, D: -2, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00066, False, sin, {Gm: 0, Fm: 2, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00066, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00061, False, sin, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00058, False, sin, {Gm: 0, Fm: 0, D: 1, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00049, False, sin, {Gm: 1, Fm: 2, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00049, False, sin, {Gm: 1, Fm: 0, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00042, False, sin, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00034, False, sin, {Gm: 0, Fm: 2, D: -2, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00026, False, sin, {Gm: 0, Fm: 2, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00025, False, sin, {Gm: 1, Fm: -2, D: -2, Om: -2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00024, False, sin, {Gm: 1, Fm: -2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00023, False, sin, {Gm: 1, Fm: 2, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00023, False, sin, {Gm: 1, Fm: 0, D: -2, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00019, False, sin, {Gm: 1, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00012, False, sin, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00011, False, sin, {Gm: 1, Fm: 0, D: -2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00011, False, sin, {Gm: 1, Fm: -2, D: -2, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00010, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00009, False, sin, {Gm: 1, Fm: 0, D: -1, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00008, False, sin, {Gm: 0, Fm: 0, D: 1, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00008, False, sin, {Gm: 0, Fm: 2, D: 2, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00008, False, sin, {Gm: 0, Fm: 0, D: 0, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00007, False, sin, {Gm: 0, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00006, False, sin, {Gm: 0, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00005, False, sin, {Gm: 1, Fm: 2, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00005, False, sin, {Gm: 3, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(
        -0.00005, False, sin, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 16, Gs: 0, L2: -18}
    ),
    Table4Row(-0.00005, False, sin, {Gm: 2, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00004, True, sin, {Gm: 0, Fm: 2, D: 0, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00004, False, cos, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 16, Gs: 0, L2: -18}),
    Table4Row(-0.00004, False, sin, {Gm: 1, Fm: -2, D: 2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00004, False, sin, {Gm: 1, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00004, False, sin, {Gm: 3, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00004, False, sin, {Gm: 0, Fm: 2, D: 2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00004, False, sin, {Gm: 0, Fm: 0, D: 2, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 0, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: 2, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 1, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 2, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 0, Fm: 2, D: -2, Om: 1, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 1, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 2, Fm: 2, D: -2, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 0, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -2, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 2, Fm: 0, D: -2, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00003, False, sin, {Gm: 1, Fm: 2, D: -2, Om: 2, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00003, False, sin, {Gm: 2, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 0, Fm: 2, D: -2, Om: 2, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 2, Fm: 2, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 2, Fm: 0, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, True, cos, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 16, Gs: 0, L2: -18}),
    Table4Row(0.00002, False, sin, {Gm: 0, Fm: 0, D: 4, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 0, Fm: 2, D: -1, Om: 2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: 2, D: -2, Om: 0, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 2, Fm: 0, D: 0, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 2, Fm: -2, D: 0, Om: -1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 1, Fm: 0, D: 2, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(0.00002, False, sin, {Gm: 2, Fm: 0, D: 0, Om: 0, Ls: 0, Gs: -1, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: 0, D: -4, Om: 0, Ls: 0, Gs: 1, L2: 0}),
    Table4Row(0.00002, True, sin, {Gm: 1, Fm: 0, D: 0, Om: 0, Ls: 16, Gs: 0, L2: -18}),
    Table4Row(
        -0.00002, False, sin, {Gm: 1, Fm: -2, D: 0, Om: -2, Ls: 0, Gs: -1, L2: 0}
    ),
    Table4Row(0.00002, False, sin, {Gm: 2, Fm: -2, D: 0, Om: -2, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: 0, D: 2, Om: 1, Ls: 0, Gs: 0, L2: 0}),
    Table4Row(-0.00002, False, sin, {Gm: 1, Fm: -2, D: 2, Om: -1, Ls: 0, Gs: 0, L2: 0}),
]
