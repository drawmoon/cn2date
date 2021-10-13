import pytest

from cn2date.util import str2digit


str2digit_test_data = [
    ("17", "year", 2017),
    ("2017", "year", 2017),
    ("一七", "year", 2017),
    ("二零一七", "year", 2017),
    ("07", "year", 2007),
    ("12", "month", 12),
    ("十二", "month", 12),
    ("1", "month", 1),
    ("一", "month", 1),
    ("31", "day", 31),
    ("三十一", "day", 31),
    ("1", "day", 1),
    ("一", "day", 1),
]


@pytest.mark.parametrize("input_str,typ,expected", str2digit_test_data, ids=[i[0] for i in str2digit_test_data])
def test_str2digit(input_str: str, typ: str, expected: int):
    rst = str2digit(input_str, typ)
    assert rst == expected

