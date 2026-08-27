# result_formatter.py
# 杨婷：结果输出模块
# 负责将已计算好的数据整理成用户可读的文本
# 所有长度输出为厘米，面积输出为平方厘米，统一保留3位小数

from __future__ import annotations

SHAPE_NAMES = {
    "square": "正方形",
    "rectangle": "长方形",
    "triangle": "三角形",
    "circle": "圆形",
}


def format_length(value_cm: float) -> str:
    """
    将长度值格式化为带单位的字符串，保留3位小数
    """
    return f"{value_cm:.3f} 厘米"


def format_area(value_cm2: float) -> str:
    """
    将面积值格式化为带单位的字符串，保留3位小数
    """
    return f"{value_cm2:.3f} 平方厘米"


def build_result(shape_type: str, dimensions_cm: dict[str, float], area_cm2: float) -> str:
    """
    构建完整的结果输出文本，包含图形类型、各输入长度和最终面积

    参数：
        shape_type: 图形类型标识（"square", "rectangle", "triangle", "circle"）
        dimensions_cm: 各边长（单位为厘米），如 {"side": 5.0} 或 {"length": 5.0, "width": 3.0}
        area_cm2: 面积（单位为平方厘米）

    返回：
        多行文本结果
    """
    # 获取中文图形名称
    shape_name = SHAPE_NAMES.get(shape_type, shape_type)

    # 构建输入长度描述
    if shape_type == "square":
        length_text = f"边长：{format_length(dimensions_cm['side'])}"
    elif shape_type == "rectangle":
        length_text = f"长：{format_length(dimensions_cm['length'])}\n宽：{format_length(dimensions_cm['width'])}"
    elif shape_type == "triangle":
        length_text = f"底：{format_length(dimensions_cm['base'])}\n高：{format_length(dimensions_cm['height'])}"
    elif shape_type == "circle":
        length_text = f"直径：{format_length(dimensions_cm['diameter'])}"
    else:
        length_text = ""

    # 组装最终结果
    result = f"图形类型：{shape_name}\n"
    result += f"{length_text}\n"
    result += f"面积：{format_area(area_cm2)}"

    return result


# ========== 自测代码（可直接运行测试） ==========
if __name__ == "__main__":
    # 测试正方形
    print("=== 正方形测试 ===")
    print(build_result("square", {"side": 5.0}, 25.0))
    print()

    # 测试长方形
    print("=== 长方形测试 ===")
    print(build_result("rectangle", {"length": 4.0, "width": 3.0}, 12.0))
    print()

    # 测试三角形
    print("=== 三角形测试 ===")
    print(build_result("triangle", {"base": 6.0, "height": 4.0}, 12.0))
    print()

    # 测试圆形
    print("=== 圆形测试 ===")
    print(build_result("circle", {"diameter": 4.0}, 12.566370614359172))
    print()

    # 验证保留3位小数
    print("=== 保留3位小数验证 ===")
    print(format_length(5.123456))   # 应输出 "5.123 厘米"
    print(format_area(25.123456))    # 应输出 "25.123 平方厘米"