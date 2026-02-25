import json
import re
from pathlib import Path

_UNIT_CODES_PATH = Path(__file__).parent / "data" / "unit_codes.json"

with open(_UNIT_CODES_PATH) as _f:
    _CODE_DICT: dict[str, str] = json.load(_f)


def get_codes(units_enjoyed_most: str):
    if "(" not in units_enjoyed_most and "-" not in units_enjoyed_most:
        match_indices = [(m.start(0), m.end(0)) for m in re.finditer("[A-Za-z]{3}[0-9]{4}", units_enjoyed_most)]

        if match_indices:
            new_str = units_enjoyed_most[:match_indices[0][0]]
            for i in range(1, len(match_indices) - 1):
                start = match_indices[i][0]
                end = start + 7
                match = units_enjoyed_most[start:end]
                unit_title = _CODE_DICT[match]
                new_str += unit_title + units_enjoyed_most[end: match_indices[i + 1][0]]

            new_str += _CODE_DICT[units_enjoyed_most[match_indices[-1][0]:match_indices[-1][0] + 7]] + units_enjoyed_most[match_indices[-1][0] + 7:]
            return new_str


if __name__ == "__main__":
    pass
