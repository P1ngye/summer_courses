# test_result_formatter.py
import unittest
from result_formatter import format_length, format_area, build_result, SHAPE_NAMES


class TestResultFormatter(unittest.TestCase):

    def test_format_length_three_decimal(self):
        """测试长度格式化，保留3位小数，附带单位"""
        self.assertEqual(format_length(5.0), "5.000 厘米")
        self.assertEqual(format_length(5.123456), "5.123 厘米")
        self.assertEqual(format_length(2.6789), "2.679 厘米")

    def test_format_area_three_decimal(self):
        """测试面积格式化，保留3位小数，附带单位"""
        self.assertEqual(format_area(25.0), "25.000 平方厘米")
        self.assertEqual(format_area(25.123456), "25.123 平方厘米")
        self.assertEqual(format_area(12.56637), "12.566 平方厘米")

    def test_build_result_square(self):
        """测试正方形输出文本结构"""
        res = build_result("square", {"side": 5.0}, 25.0)
        self.assertIn("图形类型：正方形", res)
        self.assertIn("边长：5.000 厘米", res)
        self.assertIn("面积：25.000 平方厘米", res)

    def test_build_result_rectangle(self):
        """测试长方形输出文本结构"""
        res = build_result("rectangle", {"length": 4.0, "width": 3.0}, 12.0)
        self.assertIn("图形类型：长方形", res)
        self.assertIn("长：4.000 厘米", res)
        self.assertIn("宽：3.000 厘米", res)
        self.assertIn("面积：12.000 平方厘米", res)

    def test_build_result_triangle(self):
        """测试三角形输出文本结构"""
        res = build_result("triangle", {"base": 6.0, "height": 4.0}, 12.0)
        self.assertIn("图形类型：三角形", res)
        self.assertIn("底：6.000 厘米", res)
        self.assertIn("高：4.000 厘米", res)
        self.assertIn("面积：12.000 平方厘米", res)

    def test_build_result_circle(self):
        """测试圆形输出文本结构，校验小数截断"""
        area_val = 12.566370614359172
        res = build_result("circle", {"diameter": 4.0}, area_val)
        self.assertIn("图形类型：圆形", res)
        self.assertIn("直径：4.000 厘米", res)
        self.assertIn("面积：12.566 平方厘米", res)

    def test_shape_names_mapping(self):
        """校验图形中英文映射字典完整性"""
        expect_keys = {"square", "rectangle", "triangle", "circle"}
        self.assertEqual(set(SHAPE_NAMES.keys()), expect_keys)
        self.assertEqual(SHAPE_NAMES["square"], "正方形")
        self.assertEqual(SHAPE_NAMES["circle"], "圆形")


if __name__ == '__main__':
    unittest.main()
