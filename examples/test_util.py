import pytest

from util import merge
from typing import List, Tuple


merge_testdata = [
    ([("2017年", "DATE", 0, 1), ("2021年", "DATE", 3, 4)], [("2017年", "DATE", 0, 1), ("2021年", "DATE", 3, 4)]),
    ([("第四", "ORDINAL", 0, 1), ("季度", "DATE", 1, 2)], [("第四季度", "DATE", 0, 2)]),
    ([("2021年7月28日", "DATE", 4, 7), ("当天", "DATE", 7, 8)], [("2021年7月28日当天", "DATE", 4, 8)]),
    ([("4", "CARDINAL", 0, 1), ("季度", "DATE", 1, 2)], [("4季度", "DATE", 0, 2)])
]


@pytest.mark.parametrize("ner,expected_ner", merge_testdata)
def test_merge(ner: List[Tuple[str, str, int, int]], expected_ner: List[Tuple[str, str, int, int]]):
    rst = merge(ner)
    assert len(rst) == len(expected_ner)
    for i, t in enumerate(expected_ner):
        assert rst[i] == t
