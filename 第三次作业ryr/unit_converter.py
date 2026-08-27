"""
尺寸单位转换模块 unit_converter.py

功能：
    1. 将用户输入的字符串格式尺寸做合法性校验（非空、必须大于0、可转为数字）
    2. 支持 inch / cm 两种单位，统一换算输出为厘米
    3. 支持批量对字典内的多个尺寸字段做校验与单位转换
异常：
    业务输入错误统一抛出自定义异常 DimensionParseError，方便上层区分业务错误与程序异常
依赖：
    Python 3.8+ (使用 Literal 做静态类型提示)
"""

from typing import Dict, Literal

# -------------------------- 常量配置区 --------------------------
# 英寸转厘米换算系数：1英寸 = 2.54厘米
INCH_TO_CM: float = 2.54

# 合法输入单位集合，运行时做单位有效性校验，消除硬编码魔字符串
VALID_UNITS = {"cm", "inch"}

# 静态类型别名：仅允许字符串 "cm" 或 "inch"，IDE/mypy静态检查生效，不影响运行时
UnitType = Literal["cm", "inch"]

# 错误提示常量集中管理，便于统一修改、后期支持国际化
ERR_EMPTY_TEXT = "{field_name}不能为空"
ERR_NOT_POSITIVE = "{field_name}必须大于0"
ERR_INVALID_UNIT = "单位只能是 cm 或者 inch"


class DimensionParseError(ValueError):
    """
    尺寸解析自定义业务异常
    用于区分：用户输入错误（业务异常） vs 程序本身BUG（系统异常）
    上层调用方可以单独捕获此异常，直接取异常信息作为前端提示文案
    """
    pass


def parse_positive_number(text: str, field_name: str) -> float:
    """
    将原始输入字符串解析为大于0的浮点数。
    自动去除字符串首尾空白字符；校验空值、数字合法性、数值必须>0。

    :param text: 原始待解析的输入文本，一般来自表单/外部输入
    :param field_name: 字段名称，用于拼接报错信息，例如 "width"、"高度"
    :return: float，校验通过的正数
    :raises DimensionParseError:
        1. 输入为空或者全空白字符串
        2. 文本无法转换为浮点数（非数字）
        3. 转换后数值小于等于0
    """
    # 去除首尾空格、换行等空白字符
    stripped_text = text.strip()

    # 判断空输入
    if not stripped_text:
        raise DimensionParseError(ERR_EMPTY_TEXT.format(field_name=field_name))

    # 尝试转为浮点数；捕获原生ValueError，包装为业务自定义异常
    try:
        num = float(stripped_text)
    except ValueError as e:
        # 使用 from e 保留原始异常堆栈，调试时可以看到底层报错
        raise DimensionParseError(f"{field_name}不是有效的数字") from e

    # 校验数值必须大于0
    if num <= 0:
        raise DimensionParseError(ERR_NOT_POSITIVE.format(field_name=field_name))

    return num


def to_centimeters(value: float, unit: UnitType) -> float:
    """
    将已经校验完成的数值，根据输入单位换算成厘米。

    :param value: 已经经过 parse_positive_number 校验过的正数浮点数
    :param unit: 输入数值的单位，只允许 "cm" / "inch"
    :return: float，换算完成后的厘米数值
    :raises DimensionParseError: 传入不在VALID_UNITS内的非法单位
    """
    # 运行时校验单位合法性（Literal仅静态提示，运行仍然要校验）
    if unit not in VALID_UNITS:
        raise DimensionParseError(ERR_INVALID_UNIT)

    if unit == "inch":
        return value * INCH_TO_CM
    # cm单位直接返回原值，无需换算
    return value


def parse_dimensions(raw_values: Dict[str, str], unit: UnitType) -> Dict[str, float]:
    """
    批量解析一组尺寸字典：逐个字段校验 + 单位换算，统一输出全部为厘米的字典。

    注意：遇到任意一个字段校验失败会立刻抛出异常终止，不会继续处理剩余字段。
    如果需要收集全部字段错误，可在此基础上改造，捕获每个字段异常存入错误字典。

    :param raw_values: 原始参数字典，key为字段名，value为待解析字符串
    :param unit: raw_values中所有数值对应的原始单位 "cm" / "inch"
    :return: Dict[str, float]，全部数值已转换为厘米
    :raises DimensionParseError: 任意字段校验失败抛出
    """
    result: Dict[str, float] = {}
    for field, raw_text in raw_values.items():
        # 1.字符串解析校验
        num = parse_positive_number(raw_text, field)
        # 2.单位换算到厘米
        cm_value = to_centimeters(num, unit)
        result[field] = cm_value
    return result


# -------------------------- 自测入口 --------------------------
if __name__ == "__main__":
    """
    模块直接运行时执行自测；被import导入时，下面代码不会执行。
    用于快速手工验证功能逻辑，正式自动化测试使用 test_unit_converter.py
    """
    test_cases_text = ["2.5", "2", "5.08", "abc", "", "0", "-3"]
    print("====测试 parse_positive_number====")
    for t in test_cases_text:
        try:
            res = parse_positive_number(t, "长度")
            print(f"输入[{t}] -> {res}")
        except DimensionParseError as e:
            print(f"输入[{t}] 报错: {e}")

    print("\n====测试 to_centimeters====")
    print(f"2 inch → {to_centimeters(2, 'inch')} cm")
    print(f"5  cm → {to_centimeters(5, 'cm')} cm")

    print("\n====测试 parse_dimensions====")
    raw = {"width": "2", "height": "3"}
    out = parse_dimensions(raw, "inch")
    print(out)