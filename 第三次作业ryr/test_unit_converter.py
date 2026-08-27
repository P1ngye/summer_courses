import unittest
from unit_converter import (
    parse_positive_number,
    to_centimeters,
    parse_dimensions,
    DimensionParseError
)


class TestUnitConverter(unittest.TestCase):
    # ========== parse_positive_number 测试 ==========
    def test_parse_positive_number_valid(self):
        """合法正数文本，返回正确浮点数，包含首尾空格的输入"""
        self.assertEqual(parse_positive_number("2.5", "长度"), 2.5)
        self.assertEqual(parse_positive_number("  3  ", "宽度"), 3.0)
        self.assertEqual(parse_positive_number("5.08", "高度"), 5.08)

    def test_parse_positive_number_empty(self):
        """空字符串抛出异常：字段不能为空"""
        with self.assertRaisesRegex(DimensionParseError, "不能为空"):
            parse_positive_number("", "长度")

    def test_parse_positive_number_non_number(self):
        """非数字文本抛出DimensionParseError"""
        with self.assertRaisesRegex(DimensionParseError, "不是有效的数字"):
            parse_positive_number("abc", "长度")

    def test_parse_positive_number_zero(self):
        """输入0，抛出必须大于0"""
        with self.assertRaisesRegex(DimensionParseError, "必须大于0"):
            parse_positive_number("0", "长度")

    def test_parse_positive_number_negative(self):
        """负数抛出必须大于0"""
        with self.assertRaisesRegex(DimensionParseError, "必须大于0"):
            parse_positive_number("-3", "长度")

    # ========== to_centimeters 单位换算测试 ==========
    def test_to_centimeters_cm(self):
        """cm单位直接返回原值"""
        self.assertEqual(to_centimeters(5, "cm"), 5)
        self.assertEqual(to_centimeters(10.5, "cm"), 10.5)

    def test_to_centimeters_inch(self):
        """inch换算厘米 *2.54"""
        self.assertEqual(to_centimeters(2, "inch"), 5.08)
        self.assertEqual(to_centimeters(1, "inch"), 2.54)

    def test_to_centimeters_bad_unit(self):
        """非法单位抛出异常"""
        with self.assertRaisesRegex(DimensionParseError, "单位只能是 cm 或者 inch"):
            to_centimeters(10, "mm")

    # ========== parse_dimensions 批量解析字典 ==========
    def test_parse_dimensions_inch(self):
        """输入inch的字符串字典，输出厘米浮点字典"""
        raw = {"width": "2", "height": "3"}
        result = parse_dimensions(raw, "inch")
        self.assertEqual(result["width"], 5.08)
        self.assertEqual(result["height"], 7.62)

    def test_parse_dimensions_cm(self):
        """输入cm的字符串字典，数值不变"""
        raw = {"w": "10", "h": "20.5"}
        result = parse_dimensions(raw, "cm")
        self.assertEqual(result["w"], 10.0)
        self.assertEqual(result["h"], 20.5)

    def test_parse_dimensions_bad_negative_value(self):
        """字典里面包含负数，向上抛出异常"""
        raw = {"width": "-5", "height": "10"}
        with self.assertRaisesRegex(DimensionParseError, "必须大于0"):
            parse_dimensions(raw, "cm")

    def test_parse_dimensions_bad_text_value(self):
        """字典里面包含非数字字符串"""
        raw = {"width": "abc", "height": "10"}
        with self.assertRaisesRegex(DimensionParseError, "不是有效的数字"):
            parse_dimensions(raw, "cm")

    def test_parse_dimensions_empty_field_value(self):
        """字典字段值为空字符串"""
        raw = {"width": "", "height": "10"}
        with self.assertRaisesRegex(DimensionParseError, "不能为空"):
            parse_dimensions(raw, "cm")


if __name__ == "__main__":
    unittest.main()

