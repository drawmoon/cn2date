# cn2date

[![image](https://img.shields.io/pypi/v/cn2date.svg)](https://pypi.python.org/pypi/cn2date)
[![image](https://img.shields.io/pypi/l/cn2date.svg)](https://github.com/drawmoon/cn2date/blob/main/LICENSE)

中文日期 、口语 转换为 日期字符串

## 安装

```bash
pip install cn2date
```

## 使用

```python
from cn2date import parse


def parse_input(input: str):
    between = parse(input)
    if not between:
        raise RuntimeError()

    print([str(d.datetime()) for d in between])


if __name__ == "__main__":
    for x in ["2023年", "二零二三年十二月二十一日", "今年", "本季度"]:
        parse_input(x)


# 输出结果
# ['2023-01-01 00:00:00', '2023-12-31 23:59:59.999999']
# ['2023-12-21 00:00:00', '2023-12-21 23:59:59.999999']
# ['2025-01-01 00:00:00', '2025-12-31 23:59:59.999999']
# ['2025-07-01 00:00:00', '2025-09-30 23:59:59.999999']

```

## 许可证

[MIT License](LICENSE)
