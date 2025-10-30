import gdstk

# 參數設定
line_width = 1.0
spacing = 4 * line_width  # 疊代間距
radius_start = 5 * line_width
num_shapes = 6  # 產生幾個不同R角的L型

lib = gdstk.Library()
cell = lib.new_cell("L_SHAPES")

# 從 (0, 0) 開始逐漸往右上排列
for i in range(num_shapes):
    r = radius_start + i * line_width  # R角逐漸增加
    offset_y = i * spacing * 2  # 每次往上移以避免重疊

    # 建立路徑
    path = gdstk.RobustPath((0, offset_y), line_width, layer=1)
    path.segment((10, offset_y))  # 向右走一段
    path.arc(r, 0, gdstk.pi / 2, final_width=line_width)  # 加上R角 (90度彎曲)
    path.segment((10 + r, offset_y + r))  # 向上延伸一段

    cell.add(path)

# 輸出 GDS
lib.write_gds("L_shapes.gds")
print("已產生 L_shapes.gds")

# 示意圖（需裝 matplotlib）
try:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    for element in cell.polygons:
        polygon = element.points
        ax.plot(polygon[:, 0], polygon[:, 1], 'b-')
    ax.set_aspect('equal')
    ax.set_title("L-shaped paths with increasing bend radius")
    plt.show()
except ImportError:
    print("若要顯示示意圖請安裝 matplotlib：pip install matplotlib")
