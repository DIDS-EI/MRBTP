from latextable import draw_latex

# 准备数据
data = [
    ["Group 1", "Subgroup A", 10],
    ["", "Subgroup B", 20],
    ["Group 2", "Subgroup A", 15],
    ["", "Subgroup B", 25],
    ["Group 3", "Subgroup A", 30],
]

# 定义表头
header_row = ["Group", "Subgroup", "Value"]

# 使用 latextable 生成 LaTeX 表格
latex_code = draw_latex(data,  caption="Multirow Example", label="table:multirow_example")

# 输出 LaTeX 代码
print(latex_code)
