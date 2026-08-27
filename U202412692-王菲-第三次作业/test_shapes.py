"""
test_shapes.py - shapes 模块的单元测试

使用 pytest 框架对 shapes.py 中的所有类和函数进行全面测试。
覆盖范围：
- 工厂函数 create_shape 的正常路径与异常路径
- 各图形子类的 required_fields、area、perimeter 方法
- 基类 Shape 的 validate 校验逻辑（缺失参数、非数字、零值、负值）
- 继承关系
- list_supported_shapes 辅助函数
"""

import math

import pytest

from shapes import (
    Circle,
    Rectangle,
    Shape,
    Square,
    Triangle,
    create_shape,
    list_supported_shapes,
)


# ==================== 工厂函数测试 ====================

class TestCreateShape:
    """测试工厂函数 create_shape 的正常创建和异常处理。"""

    @pytest.mark.parametrize("shape_type, dimensions, expected_class", [
        ("square", {"side": 5.0}, Square),
        ("rectangle", {"length": 5.0, "width": 3.0}, Rectangle),
        ("triangle", {"base": 6.0, "height": 4.0}, Triangle),
        ("circle", {"diameter": 2.0}, Circle),
    ])
    def test_create_correct_subclass(self, shape_type, dimensions, expected_class):
        """create_shape 应返回正确的子类实例。"""
        shape = create_shape(shape_type, dimensions)
        assert isinstance(shape, expected_class)
        assert shape.shape_type == shape_type

    def test_create_invalid_shape_type(self):
        """不支持的图形类型应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不支持的图形类型"):
            create_shape("hexagon", {"side": 5.0})

    def test_create_empty_shape_type(self):
        """空字符串图形类型应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不支持的图形类型"):
            create_shape("", {"side": 5.0})


# ==================== required_fields 测试 ====================

class TestRequiredFields:
    """测试各子类返回正确的字段名元组。"""

    @pytest.mark.parametrize("cls, dimensions, expected", [
        (Square, {"side": 1.0}, ("side",)),
        (Rectangle, {"length": 1.0, "width": 1.0}, ("length", "width")),
        (Triangle, {"base": 1.0, "height": 1.0}, ("base", "height")),
        (Circle, {"diameter": 1.0}, ("diameter",)),
    ])
    def test_required_fields(self, cls, dimensions, expected):
        """各子类应返回正确的所需字段名。"""
        shape = cls(dimensions)
        assert shape.required_fields() == expected


# ==================== 面积计算测试 ====================

class TestArea:
    """测试各图形的面积计算。"""

    def test_square_area(self):
        """正方形面积: side^2。"""
        square = create_shape("square", {"side": 5.0})
        assert square.area() == pytest.approx(25.0)

    def test_rectangle_area(self):
        """长方形面积: length * width。"""
        rectangle = create_shape("rectangle", {"length": 5.0, "width": 3.0})
        assert rectangle.area() == pytest.approx(15.0)

    def test_triangle_area(self):
        """三角形面积: base * height / 2。"""
        triangle = create_shape("triangle", {"base": 6.0, "height": 4.0})
        assert triangle.area() == pytest.approx(12.0)

    def test_circle_area(self):
        """圆形面积: pi * r^2。"""
        circle = create_shape("circle", {"diameter": 2.0})
        assert circle.area() == pytest.approx(math.pi)

    def test_circle_area_with_large_diameter(self):
        """大直径圆形面积验证。"""
        circle = create_shape("circle", {"diameter": 10.0})
        assert circle.area() == pytest.approx(math.pi * 25.0)


# ==================== 周长计算测试 ====================

class TestPerimeter:
    """测试各图形的周长计算。"""

    def test_square_perimeter(self):
        """正方形周长: 4 * side。"""
        square = create_shape("square", {"side": 5.0})
        assert square.perimeter() == pytest.approx(20.0)

    def test_rectangle_perimeter(self):
        """长方形周长: 2 * (length + width)。"""
        rectangle = create_shape("rectangle", {"length": 5.0, "width": 3.0})
        assert rectangle.perimeter() == pytest.approx(16.0)

    def test_triangle_perimeter_not_implemented(self):
        """三角形仅有底和高，周长应抛出 ValueError。"""
        triangle = create_shape("triangle", {"base": 6.0, "height": 4.0})
        with pytest.raises(ValueError, match="三角形周长"):
            triangle.perimeter()

    def test_circle_perimeter(self):
        """圆形周长: pi * diameter。"""
        circle = create_shape("circle", {"diameter": 2.0})
        assert circle.perimeter() == pytest.approx(2 * math.pi)


# ==================== 校验逻辑测试 ====================

class TestValidation:
    """测试基类 validate 的各种异常场景。"""

    def test_missing_field_rectangle(self):
        """缺少 width 参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="缺少必需参数"):
            create_shape("rectangle", {"length": 5.0})

    def test_missing_field_triangle(self):
        """缺少 height 参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="缺少必需参数"):
            create_shape("triangle", {"base": 6.0})

    def test_missing_field_circle(self):
        """缺少 diameter 参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="缺少必需参数"):
            create_shape("circle", {})

    def test_negative_value(self):
        """负值参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="必须大于 0"):
            create_shape("square", {"side": -5.0})

    def test_zero_value(self):
        """零值参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="必须大于 0"):
            create_shape("square", {"side": 0})

    def test_non_numeric_value(self):
        """非数字参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不是有效数字"):
            create_shape("square", {"side": "abc"})

    def test_non_numeric_value_none(self):
        """None 值参数应抛出 ValueError。"""
        with pytest.raises(ValueError, match="不是有效数字"):
            create_shape("square", {"side": None})


# ==================== 继承关系测试 ====================

class TestInheritance:
    """测试类继承关系。"""

    @pytest.mark.parametrize("subclass", [Square, Rectangle, Triangle, Circle])
    def test_subclass_of_shape(self, subclass):
        """所有子类都应继承自 Shape。"""
        assert issubclass(subclass, Shape)

    def test_shape_is_abstract(self):
        """Shape 是抽象类，不能被实例化。"""
        with pytest.raises(TypeError):
            Shape({"side": 1.0})

    @pytest.mark.parametrize("cls, dimensions", [
        (Square, {"side": 1.0}),
        (Rectangle, {"length": 1.0, "width": 1.0}),
        (Triangle, {"base": 1.0, "height": 1.0}),
        (Circle, {"diameter": 1.0}),
    ])
    def test_shape_type_attribute(self, cls, dimensions):
        """每个子类实例的 shape_type 应正确设置。"""
        shape = cls(dimensions)
        assert shape.shape_type != ""
        assert isinstance(shape.shape_type, str)


# ==================== dimensions 属性测试 ====================

class TestDimensions:
    """测试 dimensions 属性的存储和访问。"""

    def test_dimensions_stored(self):
        """dimensions 应正确存储传入的字典。"""
        dims = {"side": 7.5}
        square = create_shape("square", dims)
        assert square.dimensions == dims

    def test_dimensions_independent(self):
        """修改外部字典不应影响已创建的图形（浅拷贝检查）。"""
        dims = {"side": 5.0}
        square = create_shape("square", dims)
        dims["side"] = 999
        assert square.dimensions["side"] == 5.0


# ==================== 辅助函数测试 ====================

class TestListSupportedShapes:
    """测试 list_supported_shapes 辅助函数。"""

    def test_returns_all_shapes(self):
        """应返回所有支持的图形名称。"""
        shapes = list_supported_shapes()
        assert "square" in shapes
        assert "rectangle" in shapes
        assert "triangle" in shapes
        assert "circle" in shapes

    def test_returns_list_type(self):
        """返回值应为列表类型。"""
        assert isinstance(list_supported_shapes(), list)

    def test_count(self):
        """应返回 4 种图形。"""
        assert len(list_supported_shapes()) == 4


# ==================== 综合场景测试 ====================

class TestIntegration:
    """综合场景测试：模拟实际使用流程。"""

    def test_full_workflow_square(self):
        """完整流程: 创建 -> 校验 -> 计算面积 -> 计算周长。"""
        shape = create_shape("square", {"side": 10.0})
        assert shape.shape_type == "square"
        assert shape.area() == pytest.approx(100.0)
        assert shape.perimeter() == pytest.approx(40.0)

    def test_full_workflow_circle(self):
        """圆形完整流程。"""
        shape = create_shape("circle", {"diameter": 4.0})
        assert shape.shape_type == "circle"
        assert shape.area() == pytest.approx(math.pi * 4.0)
        assert shape.perimeter() == pytest.approx(math.pi * 4.0)

    def test_integer_input_accepted(self):
        """整数值也应被接受（int 是 int/float 的子类）。"""
        square = create_shape("square", {"side": 5})
        assert square.area() == pytest.approx(25.0)
