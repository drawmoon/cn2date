from datetime import datetime

import pytest

from cn2date.util import DateBuilder, date_add, date_part, date_sub, endof, startof


def test_date_builder():
    bdr = DateBuilder()
    bdr.year(2021)
    assert bdr.build() == datetime(2021, 1, 1)

    bdr.month(2)
    assert bdr.build() == datetime(2021, 2, 1)

    bdr.day(15)
    assert bdr.build() == datetime(2021, 2, 15)

    # with pytest.raises(ValueError):
    #     dbr.year(None)


def test_startof():
    dt = datetime(2021, 9, 15)

    y = startof(dt, "y")
    assert y == datetime(2021, 1, 1)

    fhoy = startof(dt, "fhoy")
    assert fhoy == datetime(2021, 1, 1)

    shoy = startof(dt, "shoy")
    assert shoy == datetime(2021, 7, 1)

    q = startof(dt, "q")
    assert q == datetime(2021, 7, 1)

    fq = startof(dt, "fq")
    assert fq == datetime(2021, 1, 1)

    sq = startof(dt, "sq")
    assert sq == datetime(2021, 4, 1)

    tq = startof(dt, "tq")
    assert tq == datetime(2021, 7, 1)

    foq = startof(dt, "foq")
    assert foq == datetime(2021, 10, 1)

    m = startof(dt, "m")
    assert m == datetime(2021, 9, 1)

    w = startof(dt, "w")
    assert w == datetime(2021, 9, 13)

    d = startof(dt, "d")
    assert d == datetime(2021, 9, 15)

    am = startof(dt, "am")
    assert am == datetime(2021, 9, 15, 0, 0, 0)

    pm = startof(dt, "pm")
    assert pm == datetime(2021, 9, 15, 12, 0, 0)

    with pytest.raises(ValueError):
        startof(dt, "x")


def test_endof():
    dt = datetime(2021, 9, 15)

    y = endof(dt, "y")
    assert y == datetime(2022, 9, 15)

    fhoy = endof(dt, "fhoy")
    assert fhoy == datetime(2021, 7, 1)

    shoy = endof(dt, "shoy")
    assert shoy == datetime(2022, 1, 1)

    q = endof(dt, "q")
    assert q == datetime(2021, 12, 15)

    fq = endof(dt, "fq")
    assert fq == datetime(2021, 4, 1)

    sq = endof(dt, "sq")
    assert sq == datetime(2021, 7, 1)

    tq = endof(dt, "tq")
    assert tq == datetime(2021, 10, 1)

    foq = endof(dt, "foq")
    assert foq == datetime(2022, 1, 1)

    m = endof(dt, "m")
    assert m == datetime(2021, 10, 15)

    w = endof(dt, "w")
    assert w == datetime(2021, 9, 22)

    d = endof(dt, "d")
    assert d == datetime(2021, 9, 16)

    am = endof(dt, "am")
    assert am == datetime(2021, 9, 15, 12, 0, 0)

    pm = endof(dt, "pm")
    assert pm == datetime(2021, 9, 15, 19, 0, 0)

    with pytest.raises(ValueError):
        endof(dt, "x")


def test_date_add():
    dt = datetime(2021, 9, 15)

    y = date_add(dt, 1, "y")
    assert y == datetime(2022, 9, 15)

    q = date_add(dt, 1, "q")
    assert q == datetime(2021, 12, 15)

    m = date_add(dt, 1, "m")
    assert m == datetime(2021, 10, 15)

    w = date_add(dt, 1, "w")
    assert w == datetime(2021, 9, 22)

    d = date_add(dt, 1, "d")
    assert d == datetime(2021, 9, 16)

    with pytest.raises(ValueError):
        date_add(dt, 1, "x")


def test_date_sub():
    dt = datetime(2021, 9, 15)

    y = date_sub(dt, 1, "y")
    assert y == datetime(2020, 9, 15)

    q = date_sub(dt, 1, "q")
    assert q == datetime(2021, 6, 15)

    m = date_sub(dt, 1, "m")
    assert m == datetime(2021, 8, 15)

    w = date_sub(dt, 1, "w")
    assert w == datetime(2021, 9, 8)

    d = date_sub(dt, 1, "d")
    assert d == datetime(2021, 9, 14)

    with pytest.raises(ValueError):
        date_sub(dt, 1, "x")


to_datepart_testdata = [
    ("y", "07", 2007),
    ("y", "17", 2017),
    ("y", "2017", 2017),
    ("y", "一七", 2017),
    ("y", "二零一七", 2017),
    ("m", "1", 1),
    ("m", "12", 12),
    ("m", "一", 1),
    ("m", "十二", 12),
    ("d", "1", 1),
    ("d", "31", 31),
    ("d", "一", 1),
    ("d", "三十一", 31),
]


@pytest.mark.parametrize(
    "typ,text,expected",
    to_datepart_testdata,
    ids=[i[1] for i in to_datepart_testdata],
)
def test_date_part(typ, text: str, expected: int):
    n = date_part(text, typ)

    assert n == expected
