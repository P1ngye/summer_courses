"""
shapes.py - 图形类设计

使用继承设计图形类：建立图形基类 Shape，以及 Square、Rectangle、Triangle、Circle 四个子类。
提供工厂函数 create_shape，根据用户选择创建对应对象。

数据约定：
- 图形名称：square, rectangle, triangle, circle
- 长度数据：使用字典保存，例如 {"side": 5.0}、{"length": 5.0, "width": 3.0}
- 进入本模块前，所有长度必须已换算为厘米
- 无效输入时抛出 ValueError 并写明原因

重构说明（第三次作业）：
- 新增 area() 和 perimeter() 抽象方法，各子类实现具体计算逻辑
- 完善类型注解和文档字符串，支持自动文档生成
- 对 __init__ 增加 dict 浅拷贝，防止外部修改影响内部状态
- 单元测试从 if __name__ 自测迁移为 pytest 框架，覆盖更全面
"""

from abc import ABC, abstractmethod
from math import pi

class Shape(ABC):
    """图形基类。所有图形子类继承此类。

    属性:
        shape_type: 图形类型名称（如 "square"）
        dimensions: 长度数据字典，所有值应为已换算为厘米的正浮点数
    """

    shape_type: str = ""

    def __init__(self, dimensions: dict[str, float]):
        """初始化图形实例。

        对传入的 dimensions 做浅拷贝，避免外部修改字典影响内部状态。

        参数:
            dimensions: 长度数据字典，所有值必须已换算为厘米
        """
        self.dimensions = dict(dimensions)

    @abstractmethod
    def required_fields(self) -> tuple[str, ...]:
        """返回该图形所需的参数名称元组，子类必须实现。

        返回:
            所需参数名称的元组，如 ("side",) 或 ("length", "width")
        """
        ...

    @abstractmethod
    def area(self) -> float:
        """计算并返回图形面积（平方厘米），子类必须实现。

        返回:
            图形面积，单位为平方厘米
        """
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """计算并返回图形周长（厘米），子类必须实现。

        返回:
            图形周长，单位为厘米
        """
        ...

    def validate(self) -> None:
        """校验 dimensions 是否包含所有必需字段且值为正数。

        在构造对象后调用此方法，确保所有参数合法。

        抛出:
            ValueError: 当缺少必需参数、值非数字或值非正数时
        """
        for field in self.required_fields():
            if field not in self.dimensions:
                raise ValueError(
                    f"缺少必需参数: {field}（图形类型: {self.shape_type}）"
                )
            value = self.dimensions[field]
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"参数 {field} 的值不是有效数字: {value}"
                )
            if value <= 0:
                raise ValueError(
                    f"参数 {field} 的值必须大于 0，当前为: {value}"
                )


class Square(Shape):
    """正方形。

    所需参数: side（边长）
    面积公式: side * side
    周长公式: 4 * side
    """

    shape_type = "square"

    def required_fields(self) -> tuple[str, ...]:
        return ("side",)

    def area(self) -> float:
        side = self.dimensions["side"]
        return side * side

    def perimeter(self) -> float:
        side = self.dimensions["side"]
        return 4 * side


class Rectangle(Shape):
    """长方形。

    所需参数: length（长）、width（宽）
    面积公式: length * width
    周长公式: 2 * (length + width)
    """

    shape_type = "rectangle"

    def required_fields(self) -> tuple[str, ...]:
        return ("length", "width")

    def area(self) -> float:
        length = self.dimensions["length"]
        width = self.dimensions["width"]
        return length * width

    def perimeter(self) -> float:
        length = self.dimensions["length"]
        width = self.dimensions["width"]
        return 2 * (length + width)


class Triangle(Shape):
    """三角形。

    所需参数: base（底）、height（高）
    面积公式: base * height / 2
    周长公式: 需三条边数据，仅给定底和高时无法计算，调用 perimeter() 将抛出 ValueError
    """

    shape_type = "triangle"

    def required_fields(self) -> tuple[str, ...]:
        return ("base", "height")

    def area(self) -> float:
        base = self.dimensions["base"]
        height = self.dimensions["height"]
        return base * height / 2

    def perimeter(self) -> float:
        raise ValueError(
            "三角形周长需要三条边的长度，当前仅提供底和高，无法计算周长"
        )


class Circle(Shape):
    """圆形。

    所需参数: diameter（直径）
    面积公式: pi * (diameter / 2) ** 2
    周长公式: pi * diameter
    """

    shape_type = "circle"

    def required_fields(self) -> tuple[str, ...]:
        return ("diameter",)

    def area(self) -> float:
        radius = self.dimensions["diameter"] / 2
        return pi * radius ** 2

    def perimeter(self) -> float:
        diameter = self.dimensions["diameter"]
        return pi * diameter


# 图形类型 -> 子类的映射表
_SHAPE_REGISTRY: dict[str, type[Shape]] = {
    "square": Square,
    "rectangle": Rectangle,
    "triangle": Triangle,
    "circle": Circle,
}


def create_shape(shape_type: str, dimensions: dict[str, float]) -> Shape:
    """工厂函数：根据图形名称返回对应子类对象。

    参数:
        shape_type: 图形名称，可选值: square, rectangle, triangle, circle
        dimensions: 长度数据字典，所有值必须已换算为厘米

    返回:
        对应的 Shape 子类实例

    抛出:
        ValueError: 当图形名称无效、参数缺失或参数值非正数时
    """
    if shape_type not in _SHAPE_REGISTRY:
        raise ValueError(
            f"不支持的图形类型: '{shape_type}'，"
            f"支持的类型: {', '.join(_SHAPE_REGISTRY.keys())}"
        )

    shape = _SHAPE_REGISTRY[shape_type](dimensions)
    shape.validate()
    return shape


def list_supported_shapes() -> list[str]:
    """返回当前支持的所有图形类型名称列表。

    返回:
        支持的图形名称列表，如 ["square", "rectangle", "triangle", "circle"]
    """
    return list(_SHAPE_REGISTRY.keys())


if __name__ == "__main__":

    def demo():
        """演示各图形的创建、面积和周长计算。"""
        shapes = [
            create_shape("square", {"side": 5.0}),
            create_shape("rectangle", {"length": 5.0, "width": 3.0}),
            create_shape("triangle", {"base": 6.0, "height": 4.0}),
            create_shape("circle", {"diameter": 2.0}),
        ]

        for shape in shapes:
            print(f"[{shape.shape_type}] 面积: {shape.area():.2f} cm^2", end="")
            try:
                print(f", 周长: {shape.perimeter():.2f} cm")
            except ValueError as e:
                print(f", 周长: 不可计算 ({e})")

    demo()
