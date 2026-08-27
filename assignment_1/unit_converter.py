INCH_TO_CM = 2.54


def parse_positive_number(text: str, field_name: str) -> float:
    """将文本转为大于 0 的浮点数；失败时抛出带字段名的 ValueError。"""
    text = text.strip()
    if not text:
        raise ValueError(f"{field_name}不能为空")
    num = float(text)
    if num <= 0:
        raise ValueError(f"{field_name}必须大于0")
    return num


def to_centimeters(value: float, unit: str) -> float:
    """unit 仅接受 'cm' 或 'inch'；返回厘米数。"""
    if unit == "cm":
        return value
    elif unit == "inch":
        return value * INCH_TO_CM
    else:
        raise ValueError("单位只能是 cm 或者 inch")


def parse_dimensions(raw_values: dict[str, str], unit: str) -> dict[str, float]:
    """校验并换算一组输入，返回所有值均为厘米的字典。"""
    result = {}
    for key, text in raw_values.items():
        num = parse_positive_number(text, key)
        cm_val = to_centimeters(num, unit)
        result[key] = cm_val
    return result


# --------下面是自测代码，可以直接运行测试---------
if __name__ == "__main__":
    # 测试用例
    test_cases_text = ["2.5", "2", "5.08", "abc", "", "0", "-3"]
    print("====测试 parse_positive_number====")
    for t in test_cases_text:
        try:
            res = parse_positive_number(t, "长度")
            print(f"输入[{t}] -> {res}")
        except ValueError as e:
            print(f"输入[{t}] 报错: {e}")

    print("\n====测试 to_centimeters====")
    print(f"2 inch → {to_centimeters(2, 'inch')} cm")   # 5.08
    print(f"5  cm → {to_centimeters(5, 'cm')} cm")

    print("\n====测试 parse_dimensions====")
    raw = {"width": "2", "height": "3"}
    out = parse_dimensions(raw, "inch")
    print(out)