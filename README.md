# cn2date

[![Pypi Version][pypi-image]][pypi-url]

中文日期 、口语 转换为 日期字符串

## 安装

```bash
pip install cn2date
```

## 使用

```python
from cn2date import parse

result = parse("2021年")
# 输出结果：('2021-01-01 00:00:00', '2022-01-01 00:00:00')

result = parse("二零二一年九月十七日")
# 输出结果：('2021-09-17 00:00:00', '2021-09-18 00:00:00')

result = parse("今天")
# 输出结果：('2022-02-23 00:00:00', '2022-02-24 00:00:00')

result = parse("本季度")
# 输出结果：('2022-01-01 00:00:00', '2022-04-01 00:00:00')
```

## 许可证

[MIT License](LICENSE)

[pypi-image]: https://badge.fury.io/py/cn2date.svg
[pypi-url]: https://pypi.org/project/cn2date/
