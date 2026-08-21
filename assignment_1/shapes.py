"""
shapes.py - 图形类设计（王菲）

使用继承设计图形类：建立图形基类 Shape，以及 Square、Rectangle、Triangle、Circle 四个子类。
提供工厂函数 create_shape，供组长根据用户选择创建对应对象。

数据约定：
- 图形名称：square, rectangle, triangle, circle
- 长度数据：使用字典保存，例如 {"side": 5.0}、{"length": 5.0, "width": 3.0}
- 进入本模块前，所有长度必须已换算为厘米
- 无效输入时抛出 ValueError 并写明原因
"""

from abc import ABC, abstractmethod


class Shape(ABC):
    """图形基类。所有图形子类继承此类。

    属性:
        shape_type: 图形类型名称（如 "square"）
        dimensions: 长度数据字典，所有值应为已换算为厘米的正浮点数
    """

    shape_type: str = ""

    def __init__(self, dimensions: dict[str, float]):
        self.dimensions = dimensions

    @abstractmethod
    def required_fields(self) -> tuple[str, ...]:
        """返回该图形所需的参数名称元组，子类必须实现。"""
        raise NotImplementedError

    def validate(self) -> None:
        """校验 dimensions 是否包含所有必需字段且值为正数。

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
    """正方形。所需参数: side（边长）。"""

    shape_type = "square"

    def required_fields(self) -> tuple[str, ...]:
        return ("side",)


class Rectangle(Shape):
    """长方形。所需参数: length（长）、width（宽）。"""

    shape_type = "rectangle"

    def required_fields(self) -> tuple[str, ...]:
        return ("length", "width")


class Triangle(Shape):
    """三角形。所需参数: base（底）、height（高）。"""

    shape_type = "triangle"

    def required_fields(self) -> tuple[str, ...]:
        return ("base", "height")


class Circle(Shape):
    """圆形。所需参数: diameter（直径）。"""

    shape_type = "circle"

    def required_fields(self) -> tuple[str, ...]:
        return ("diameter",)


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


# ==================== 自测 ====================
if __name__ == "__main__":

    def test_create_shapes():
        """测试 create_shape 能正确返回各子类实例。"""
        square = create_shape("square", {"side": 5.0})
        assert isinstance(square, Square)
        assert square.shape_type == "square"
        assert square.required_fields() == ("side",)

        rectangle = create_shape("rectangle", {"length": 5.0, "width": 3.0})
        assert isinstance(rectangle, Rectangle)
        assert rectangle.shape_type == "rectangle"
        assert rectangle.required_fields() == ("length", "width")

        triangle = create_shape("triangle", {"base": 6.0, "height": 4.0})
        assert isinstance(triangle, Triangle)
        assert triangle.shape_type == "triangle"
        assert triangle.required_fields() == ("base", "height")

        circle = create_shape("circle", {"diameter": 2.0})
        assert isinstance(circle, Circle)
        assert circle.shape_type == "circle"
        assert circle.required_fields() == ("diameter",)

        print("[PASS] create_shape 返回正确的子类实例")

    def test_required_fields():
        """测试各子类返回正确的字段名。"""
        assert Square({"side": 1.0}).required_fields() == ("side",)
        assert Rectangle({"length": 1.0, "width": 1.0}).required_fields() == ("length", "width")
        assert Triangle({"base": 1.0, "height": 1.0}).required_fields() == ("base", "height")
        assert Circle({"diameter": 1.0}).required_fields() == ("diameter",)
        print("[PASS] 各子类返回正确的字段名")

    def test_invalid_shape_type():
        """测试无效图形类型抛出 ValueError。"""
        try:
            create_shape("hexagon", {"side": 5.0})
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert "不支持的图形类型" in str(e)
        print("[PASS] 无效图形类型抛出 ValueError")

    def test_missing_field():
        """测试缺少参数时抛出 ValueError。"""
        try:
            create_shape("rectangle", {"length": 5.0})  # 缺少 width
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert "缺少必需参数" in str(e)
        print("[PASS] 缺少参数时抛出 ValueError")

    def test_non_positive_value():
        """测试参数值非正数时抛出 ValueError。"""
        try:
            create_shape("square", {"side": -5.0})
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert "必须大于 0" in str(e)

        try:
            create_shape("square", {"side": 0})
            assert False, "应抛出 ValueError"
        except ValueError as e:
            assert "必须大于 0" in str(e)
        print("[PASS] 非正数参数抛出 ValueError")

    def test_inheritance():
        """测试继承关系。"""
        assert issubclass(Square, Shape)
        assert issubclass(Rectangle, Shape)
        assert issubclass(Triangle, Shape)
        assert issubclass(Circle, Shape)
        print("[PASS] 继承关系正确")

    test_create_shapes()
    test_required_fields()
    test_invalid_shape_type()
    test_missing_field()
    test_non_positive_value()
    test_inheritance()

    print("\n全部测试通过!")
