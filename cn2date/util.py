from .conf import NUMERAL_CN2NUM, NUMERAL_NUM2CN, UNIT_CN2NUM


def num2cn(s: str, strict: bool = False) -> str:
    """数值字符转换为中文

    Args:
        s (str): 需要转换的字符串
        strict (bool, optional): 严格模式；
        当值为 `True` 时，严格按照中文标准翻译，例如：`10 -> 十`，
        否则则按照简单映射翻译，例如：`10 -> 一零`. 默认值为 `False`。

    Returns:
        str: 数字转换为中文的字符串
    """
    han_str = s.translate(str.maketrans(NUMERAL_NUM2CN))
    if not strict:
        return han_str

    str_list: list[str] = []
    if len(han_str) == 2:
        # 处理 "十x" 的字符串
        if han_str[0] != "零":
            if han_str[1] == "零":
                str_list.append(han_str[0])
                str_list.append("十")
            else:
                str_list.append(han_str[0])
                str_list.append("十")
                str_list.append(han_str[1])
            return "".join(str_list[1:]) if str_list[0] == "一" else "".join(str_list)

    return han_str


def cn2num(s: str) -> int:
    """中文字符转换为数字

    Args:
        s (str): 需要转换的字符串

    Returns:
        str: 中文转换为数字的字符串
    """
    if s in UNIT_CN2NUM:
        return UNIT_CN2NUM[s]

    num_str = s.translate(str.maketrans(NUMERAL_CN2NUM))
    if num_str[0] in ["十", "拾"]:
        num_str = f"1{num_str[1:]}"
    elif len(num_str) > 1 and num_str[1] == "十":
        str_list: list[str] = []
        if len(num_str) == 2:
            str_list.append(num_str[:-1])
            str_list.append("0")
        else:
            str_list.append(num_str[0])
            str_list.append(num_str[2])
        num_str = "".join(str_list)

    return int(num_str)
