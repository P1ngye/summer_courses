# 通用面积计算器——面积计算部分

![通用面积计算器运行截图](images/calculator-interface.jpg)

## Project Title

本项目是一个使用 Python 编写的通用面积计算器，可以计算正方形、长方形、三角形和圆形的面积。完整程序使用 Tkinter 图形界面，支持厘米和英寸输入。

我负责 `area_calculator.py`。这个文件只处理面积公式，接收的长度已经换算成厘米，返回的面积单位为平方厘米。

## Getting Started

### Prerequisites

- Python 3.9 或更高版本
- 不需要安装第三方库

### Installing

下载完整的 `assignment_1` 文件夹，在该目录运行：

```bash
python main.py
```

程序启动后，在窗口中选择图形、单位并填写长度，然后点击“计算面积”。

## Running the Tests

在 `assignment_1` 目录执行：

```bash
python -m unittest discover -s tests -v
```

当前共有 10 项测试，主要检查四种面积公式、缺少参数、未知图形以及无效长度。

几个简单结果如下：

| 图形 | 输入 | 面积 |
| --- | --- | --- |
| 正方形 | 边长 2 | 4 |
| 长方形 | 长 3、宽 4 | 12 |
| 三角形 | 底 6、高 4 | 12 |
| 圆形 | 直径 2 | 约 3.1416 |

## Usage

四个公式函数可以单独使用：

```python
from area_calculator import (
    square_area,
    rectangle_area,
    triangle_area,
    circle_area,
)

print(square_area(2))          # 4.0
print(rectangle_area(3, 4))    # 12.0
print(triangle_area(6, 4))     # 12.0
print(circle_area(2))          # 3.141592...
```

程序其他模块使用统一接口：

```python
from area_calculator import calculate_area

area = calculate_area("rectangle", {
    "length": 3.0,
    "width": 4.0,
})
print(area)  # 12.0
```

圆形参数是直径。计算模块保留完整浮点精度，不在公式中提前四舍五入，三位小数由结果输出模块处理。

## Contributing

小组采用分模块开发方式。我完成面积公式与统一计算入口，其他成员分别负责界面、图形类、单位换算和结果格式化。

## Versioning

当前版本为 **v1.0.0**，已完成四种图形的面积计算和输入合法性检查。

## Authors

- **姓名**：喻麒麟
- **学号**：U202412699
- **负责文件**：`area_calculator.py`

## License

本项目仅用于课程学习和作业提交。

## Acknowledgments

感谢老师的指导，也感谢组员共同确定模块接口和测试数据。
