# result_formatter.py
# 杨婷：结果输出模块
# 负责将已计算完成的原始数值，转换为用户可读的格式化文本
# 输出规范：长度单位统一为厘米，面积单位统一为平方厘米，数值固定保留3位小数
from __future__ import annotations

# ===================== 全局常量配置区 =====================
# 数值保留小数位数，全局统一控制，修改此处即可全局变更输出精度
DECIMAL_PLACES = 3
# 长度输出单位
UNIT_LENGTH = "厘米"
# 面积输出单位
UNIT_AREA = "平方厘米"

# 图形类型标识与中文名称映射字典
# key：程序内部使用的图形英文标识，value：展示给用户的中文图形名称
SHAPE_NAMES = {
    "square": "正方形",
    "rectangle": "长方形",
    "triangle": "三角形",
    "circle": "圆形",
}

# 图形维度标签映射字典
# key：图形类型标识
# value：元组列表，(页面显示的中文标签, dimensions_cm字典中对应的键名)
# 新增图形只需在此处配置，无需新增条件判断分支
SHAPE_DIMENSION_LABELS = {
    "square": [("边长", "side")],
    "rectangle": [("长", "length"), ("宽", "width")],
    "triangle": [("底", "base"), ("高", "height")],
    "circle": [("直径", "diameter")],
}


def format_length(value_cm: float) -> str:
    """
    将厘米单位的原始长度数值，格式化为带单位的展示字符串

    :param value_cm: float，原始长度数值，单位：厘米
    :return: str，格式化完成的文本，示例："5.000 厘米"
    """
    return f"{value_cm:.{DECIMAL_PLACES}f} {UNIT_LENGTH}"


def format_area(value_cm2: float) -> str:
    """
    将平方厘米单位的原始面积数值，格式化为带单位的展示字符串

    :param value_cm2: float，原始面积数值，单位：平方厘米
    :return: str，格式化完成的文本，示例："25.000 平方厘米"
    """
    return f"{value_cm2:.{DECIMAL_PLACES}f} {UNIT_AREA}"


def build_result(shape_type: str, dimensions_cm: dict[str, float], area_cm2: float) -> str:
    """
    组装完整的计算结果多行文本，包含图形类型、输入尺寸、最终面积

    :param shape_type: str，图形类型标识，可选值：square / rectangle / triangle / circle
    :param dimensions_cm: dict[str, float]，图形各维度参数字典，全部数值单位为厘米
    :param area_cm2: float，已经计算完成的面积结果，单位：平方厘米
    :return: str，拼接完成的多行可读结果文本
    """
    # 根据标识获取图形中文名称；未知图形直接使用原始标识兜底
    shape_name = SHAPE_NAMES.get(shape_type, shape_type)
    # 获取当前图形对应的维度标签配置，未知图形返回空列表
    label_list = SHAPE_DIMENSION_LABELS.get(shape_type, [])

    dimension_lines = []
    # 遍历配置，读取对应参数，生成每一行尺寸描述文本
    for display_text, dict_key in label_list:
        val = dimensions_cm.get(dict_key)
        # 做容错判断，字典取不到参数时跳过该行，避免程序抛出异常
        if val is not None:
            dimension_lines.append(f"{display_text}：{format_length(val)}")

    # 将多条尺寸文本使用换行符拼接
    length_text = "\n".join(dimension_lines)

    # 组装全部输出行
    output_lines = [
        f"图形类型：{shape_name}",
        length_text,
        f"面积：{format_area(area_cm2)}"
    ]
    return "\n".join(output_lines)


# ========== 模块自测入口 ==========
# 直接运行本文件时执行自测逻辑；被其他文件import导入时，该段代码不会执行
if __name__ == "__main__":
    # 测试正方形格式化输出
    print("=== 正方形测试 ===")
    print(build_result("square", {"side": 5.0}, 25.0))
    print()

    # 测试长方形格式化输出
    print("=== 长方形测试 ===")
    print(build_result("rectangle", {"length": 4.0, "width": 3.0}, 12.0))
    print()

    # 测试三角形格式化输出
    print("=== 三角形测试 ===")
    print(build_result("triangle", {"base": 6.0, "height": 4.0}, 12.0))
    print()

    # 测试圆形格式化输出，校验浮点数精度处理
    print("=== 圆形测试 ===")
    print(build_result("circle", {"diameter": 4.0}, 12.566370614359172))
    print()

    # 验证小数保留位数功能
    print("=== 保留3位小数验证 ===")
    print(format_length(5.123456))   # 预期输出 "5.123 厘米"
    print(format_area(25.123456))    # 预期输出 "25.123 平方厘米"
