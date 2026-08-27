"""通用面积计算器图形界面。

组长王澔博负责本文件：收集用户输入、调用各组员模块并显示结果。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from area_calculator import calculate_area
from result_formatter import build_result
from shapes import create_shape
from unit_converter import parse_dimensions


# 中文名称 ->（内部图形类型、需要输入的字段）
SHAPE_OPTIONS: dict[str, tuple[str, tuple[tuple[str, str], ...]]] = {
    "正方形": ("square", (("side", "边长"),)),
    "长方形": ("rectangle", (("length", "长"), ("width", "宽"))),
    "三角形": ("triangle", (("base", "底"), ("height", "高"))),
    "圆形": ("circle", (("diameter", "直径"),)),
}

UNIT_OPTIONS = {
    "厘米（cm）": "cm",
    "英寸（inch）": "inch",
}


class AreaCalculatorApp:
    """负责图形选择、输入收集、模块调用和结果展示。"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("通用面积计算器")
        self.root.geometry("660x590")
        self.root.minsize(600, 540)

        self.shape_var = tk.StringVar(value="正方形")
        self.unit_var = tk.StringVar(value="厘米（cm）")
        self.result_var = tk.StringVar(value="请选择图形并输入长度。")
        self.input_vars: dict[str, tk.StringVar] = {}

        self._configure_style()
        self._build_interface()
        self._refresh_inputs()

    def _configure_style(self) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Microsoft YaHei UI", 10))
        style.configure("Field.TLabel", font=("Microsoft YaHei UI", 11))
        style.configure("Action.TButton", font=("Microsoft YaHei UI", 11, "bold"), padding=8)
        style.configure("Result.TLabel", font=("Microsoft YaHei UI", 12), padding=14)

    def _build_interface(self) -> None:
        container = ttk.Frame(self.root, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="通用面积计算器", style="Title.TLabel").pack()
        ttk.Label(
            container,
            text="支持正方形、长方形、三角形和圆形",
            style="Subtitle.TLabel",
        ).pack(pady=(4, 20))

        selection_frame = ttk.LabelFrame(container, text="计算设置", padding=16)
        selection_frame.pack(fill="x")
        selection_frame.columnconfigure(1, weight=1)

        ttk.Label(selection_frame, text="图形类型：", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=6
        )
        shape_box = ttk.Combobox(
            selection_frame,
            textvariable=self.shape_var,
            values=tuple(SHAPE_OPTIONS),
            state="readonly",
            font=("Microsoft YaHei UI", 10),
        )
        shape_box.grid(row=0, column=1, sticky="ew", pady=6)
        shape_box.bind("<<ComboboxSelected>>", self._refresh_inputs)

        ttk.Label(selection_frame, text="输入单位：", style="Field.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=6
        )
        unit_box = ttk.Combobox(
            selection_frame,
            textvariable=self.unit_var,
            values=tuple(UNIT_OPTIONS),
            state="readonly",
            font=("Microsoft YaHei UI", 10),
        )
        unit_box.grid(row=1, column=1, sticky="ew", pady=6)

        self.input_frame = ttk.LabelFrame(container, text="长度输入", padding=16)
        self.input_frame.pack(fill="x", pady=16)
        self.input_frame.columnconfigure(1, weight=1)

        ttk.Button(
            container,
            text="计算面积",
            command=self._calculate,
            style="Action.TButton",
        ).pack(fill="x")

        result_frame = ttk.LabelFrame(container, text="计算结果", padding=10)
        result_frame.pack(fill="both", expand=True, pady=(16, 0))
        ttk.Label(
            result_frame,
            textvariable=self.result_var,
            style="Result.TLabel",
            justify="left",
            anchor="nw",
        ).pack(fill="both", expand=True)

    def _refresh_inputs(self, _event: object | None = None) -> None:
        """根据当前图形创建对应的长度输入框。"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.input_vars.clear()
        _shape_type, fields = SHAPE_OPTIONS[self.shape_var.get()]

        for row, (field_name, display_name) in enumerate(fields):
            ttk.Label(
                self.input_frame,
                text=f"{display_name}：",
                style="Field.TLabel",
            ).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=7)

            value_var = tk.StringVar()
            entry = ttk.Entry(
                self.input_frame,
                textvariable=value_var,
                font=("Microsoft YaHei UI", 11),
            )
            entry.grid(row=row, column=1, sticky="ew", pady=7)
            self.input_vars[field_name] = value_var

            if row == 0:
                entry.focus_set()

        self.result_var.set("请输入大于 0 的长度，然后点击“计算面积”。")

    def _calculate(self) -> None:
        """调用组员模块完成校验、换算、建模、计算和格式化。"""
        shape_type, _fields = SHAPE_OPTIONS[self.shape_var.get()]
        unit = UNIT_OPTIONS[self.unit_var.get()]
        raw_values = {
            field_name: value_var.get()
            for field_name, value_var in self.input_vars.items()
        }

        try:
            dimensions_cm = parse_dimensions(raw_values, unit)
            shape = create_shape(shape_type, dimensions_cm)
            area_cm2 = calculate_area(shape.shape_type, shape.dimensions)
            result_text = build_result(
                shape.shape_type,
                shape.dimensions,
                area_cm2,
            )
        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror("输入错误", str(error), parent=self.root)
            return

        self.result_var.set(result_text)


def main() -> None:
    root = tk.Tk()
    AreaCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
