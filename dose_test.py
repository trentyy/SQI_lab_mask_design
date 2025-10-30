import gdstk
import matplotlib.pyplot as plt
import math

lib = gdstk.Library()

# === 參數設定 ===
line_width = 1.0     # µm
gap = 1.0            # µm
length = 50.0        # µm (直/橫線長)
rect_len = 30.0      # µm (第三圖形中每條長方形長度)
num_lines = 10
cell_size = 80       # 每個方格大小 (µm)

# === 1. 直的 10 條線 (vertical) ===
cell1 = lib.new_cell("VERTICAL_LINES")
for i in range(num_lines):
    x0 = i * (line_width + gap)
    rect = gdstk.rectangle((x0, 0), (x0 + line_width, length))
    cell1.add(rect)

# === 2. 橫的 10 條線 (horizontal) ===
cell2 = lib.new_cell("HORIZONTAL_LINES")
for i in range(num_lines):
    y0 = i * (line_width + gap)
    rect = gdstk.rectangle((0, y0), (length, y0 + line_width))
    cell2.add(rect)

# === 3. 夾角變化的雙長方形（pivot 在第一條右端）===
cell3 = lib.new_cell("ANGLE_LINES")
x_offset = 0.0
y_offset = 0.0
# 我把單位矩形建在原點，從 x=0 延伸到 x=rect_len，垂直方向以 y=0 為中心：
# rect_base 範圍為 (0, -w/2) -> (rect_len, w/2)
for angle_deg in range(0, 91, 15):  # 15°,30°,...,180°
    angle_rad = math.radians(angle_deg)

    # 第一條：不旋轉，從 x=0 到 x=rect_len，垂直以 0 為中心；再平移到 y_offset
    r1 = gdstk.rectangle((0.0, -line_width/2.0), (rect_len, line_width/2.0))
    r1 = r1.translate(0.0 + x_offset, y_offset)
    cell3.add(r1)

    # 第二條：在原點建立相同長的矩形，先以原點旋轉，再把原點移到 pivot=(rect_len, y_offset)
    r2 = gdstk.rectangle((0.0, -line_width/2.0), (rect_len, line_width/2.0))
    r2 = r2.rotate(angle_rad, (0.0, -line_width/2.0))           # 以左端 (x=0) 當旋轉中心
    r2 = r2.translate(rect_len + x_offset, y_offset)          # 把左端移到第一條的右端 (pivot)
    cell3.add(r2)

    # 每次往下移動 4 個線寬 (避免重疊)
    x_offset -= 4.0 * line_width
    y_offset += 4.0 * line_width

# === 4. 棋盤格 ===
cell4 = lib.new_cell("CHECKERBOARD")
square_size = 5.0
rows = cols = 6
for i in range(rows):
    for j in range(cols):
        if (i + j) % 2 == 0:
            x0 = j * square_size
            y0 = i * square_size
            rect = gdstk.rectangle((x0, y0), (x0 + square_size, y0 + square_size))
            cell4.add(rect)

# === 把四個 cell 排到 TOP cell (由上到下) ===
top = lib.new_cell("TOP")
top.add(gdstk.Reference(cell1, (0, 3 * cell_size)))
top.add(gdstk.Reference(cell2, (0, 2 * cell_size)))
top.add(gdstk.Reference(cell3, (0, 1 * cell_size)))
top.add(gdstk.Reference(cell4, (0, 0)))

# === 輸出 GDS 檔 ===
lib.write_gds("patterns_fixed_angle.gds")
print("已產生 patterns_fixed_angle.gds（包含修正後的第3圖形）。")

# === 畫示意圖（matplotlib）===
def polys_from_cell(cell):
    # 取 cell 的 polygon 與 rectangle 轉為多邊形點 (gdstk 對象)
    polys = []
    # polygons
    for poly in cell.polygons:
        polys.append(poly.points)
    # rectangles / paths 等會被當成 polygons 也包含在 polygons 屬性
    return polys

fig, axs = plt.subplots(4, 1, figsize=(6, 12))

cells = [cell1, cell2, cell3, cell4]
titles = ["直的 10 條線", "橫的 10 條線", "雙長方形夾角 (15°→180°)", "棋盤格"]

for ax, c, title in zip(axs, cells, titles):
    polys = polys_from_cell(c)
    for p in polys:
        xs, ys = zip(*p)
        ax.fill(xs, ys, edgecolor=None, color="black")
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
