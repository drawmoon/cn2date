from datetime import datetime

import pytest

from cn2date.util import (date_add, date_build, date_lens, date_sub,
                          date_trunc, now, to_datepart)


def test_now():
    assert now() == datetime(2021, 9, 1)


def test_date_build():
    y = date_build(2021)
    assert y == datetime(2021, 1, 1)

    m = date_build(2021, 9)
    assert m == datetime(2021, 9, 1)

    d = date_build(2021, 9, 15)
    assert d == datetime(2021, 9, 15)

    with pytest.raises(ValueError):
        date_build(None)


def test_date_trunc():
    dt = datetime(2021, 9, 15)

    y = date_trunc(dt, "y")
    assert y == datetime(2021, 1, 1)

    fhoy = date_trunc(dt, "fhoy")
    assert fhoy == datetime(2021, 1, 1)

    shoy = date_trunc(dt, "shoy")
    assert shoy == datetime(2021, 7, 1)

    q = date_trunc(dt, "q")
    assert q == datetime(2021, 7, 1)

    fq = date_trunc(dt, "fq")
    assert fq == datetime(2021, 1, 1)

    sq = date_trunc(dt, "sq")
    assert sq == datetime(2021, 4, 1)

    tq = date_trunc(dt, "tq")
    assert tq == datetime(2021, 7, 1)

    foq = date_trunc(dt, "foq")
    assert foq == datetime(2021, 10, 1)

    m = date_trunc(dt, "m")
    assert m == datetime(2021, 9, 1)

    w = date_trunc(dt, "w")
    assert w == datetime(2021, 9, 13)

    d = date_trunc(dt, "d")
    assert d == datetime(2021, 9, 15)

    am = date_trunc(dt, "am")
    assert am == datetime(2021, 9, 15, 0, 0, 0)

    pm = date_trunc(dt, "pm")
    assert pm == datetime(2021, 9, 15, 12, 0, 0)

    with pytest.raises(ValueError):
        date_trunc(dt, "x")


def test_date_lens():
    dt = datetime(2021, 9, 15)

    y = date_lens(dt, "y")
    assert y == datetime(2022, 9, 15)

    fhoy = date_lens(dt, "fhoy")
    assert fhoy == datetime(2021, 7, 1)

    shoy = date_lens(dt, "shoy")
    assert shoy == datetime(2022, 1, 1)

    q = date_lens(dt, "q")
    assert q == datetime(2021, 12, 15)

    fq = date_lens(dt, "fq")
    assert fq == datetime(2021, 4, 1)

    sq = date_lens(dt, "sq")
    assert sq == datetime(2021, 7, 1)

    tq = date_lens(dt, "tq")
    assert tq == datetime(2021, 10, 1)

    foq = date_lens(dt, "foq")
    assert foq == datetime(2022, 1, 1)

    m = date_lens(dt, "m")
    assert m == datetime(2021, 10, 15)

    w = date_lens(dt, "w")
    assert w == datetime(2021, 9, 22)

    d = date_lens(dt, "d")
    assert d == datetime(2021, 9, 16)

    am = date_lens(dt, "am")
    assert am == datetime(2021, 9, 15, 12, 0, 0)

    pm = date_lens(dt, "pm")
    assert pm == datetime(2021, 9, 15, 19, 0, 0)

    with pytest.raises(ValueError):
        date_lens(dt, "x")


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
    ("year", "07", 2007),
    ("year", "17", 2017),
    ("year", "2017", 2017),
    ("year", "一七", 2017),
    ("year", "二零一七", 2017),
    ("month", "1", 1),
    ("month", "12", 12),
    ("month", "一", 1),
    ("month", "十二", 12),
    ("day", "1", 1),
    ("day", "31", 31),
    ("day", "一", 1),
    ("day", "三十一", 31),
]


@pytest.mark.parametrize(
    "typ,text,expected",
    to_datepart_testdata,
    ids=[i[0] for i in to_datepart_testdata],
)
def test_to_datepart(typ: str, text: str, expected: int):
    n = to_datepart(text, typ)

    assert n == expected
