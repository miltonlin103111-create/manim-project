from manim import *
import numpy as np

class Day4Divergence(Scene):
    def construct(self):
        # 1. 建立座標軸與向量場 (建議用一個散度不為常數的場，觀察更有趣)
        axes = Axes(x_range=[-4, 4], y_range=[-3, 3])
        
        def function (point):
            x, y, _ = point
            # 場函數：F = [x^2, y^2, 0] -> div(F) = 2x + 2y
            return np.array([x**2, y**2, 0])
        def func (point):
            x, y, _ = point
            length = np.linalg.norm(function(point))
            return np.array([x**2/length, y**2/length, 0])

        # 3. 建立 StreamLines
        # 密度設為 0.4，避免線條過多導致渲染太慢
        stream_lines = StreamLines(
            func,
            x_range=[-4, 4, 0.6],
            y_range=[-3, 3, 0.6],
            stroke_width=2,
            padding=1,
        )

        # --- 顏色邏輯修正 ---
        # 函數 [x^2, y^2]最大值為
        max_magnitude = 25

        for line in stream_lines:
            start_point = line.get_start()
            # 根據起始點的向量長度決定顏色
            magnitude = np.linalg.norm(func(start_point))
            
            # alpha 越接近 1 代表流速越快 (紅色)，越接近 0 代表越慢 (藍色)
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            line.set_color(interpolate_color(BLUE, RED, alpha))


        # 2. 建立散度探測器 (方塊 + 文字)
        probe_pos = Dot(color=WHITE).move_to(axes.c2p(-2, -2)) # 初始點
        
        # 散度計算函式
        def get_div_at_point(point):
            eps = 0.001
            # 數值偏微分
            dfx_dx = (func(point + [eps, 0, 0])[0] - func(point - [eps, 0, 0])[0]) / (2 * eps)
            dfy_dy = (func(point + [0, eps, 0])[1] - func(point - [0, eps, 0])[1]) / (2 * eps)
            return dfx_dx + dfy_dy

        # 探測器方塊
        probe_box = always_redraw(lambda:
            Square(side_length=0.8)
            .set_stroke(WHITE, 2)
            .move_to(probe_pos.get_center())
        )

        # 散度數值標籤
        div_label = always_redraw(lambda:
            VGroup(
                MathTex(r"\nabla \cdot \mathbf{F} = "),
                DecimalNumber(get_div_at_point(probe_pos.get_center()), num_decimal_places=2)
            ).arrange(RIGHT).scale(0.7).next_to(probe_box, UP)
        )

        self.add(axes, stream_lines, probe_pos, probe_box, div_label)
        stream_lines.start_animation(warm_up=True, flow_speed=0.8, time_width=0.4)

        # 3. 讓方塊移動到不同的點
        # 移動到右上方 (2, 2)
        self.play(probe_pos.animate.move_to(axes.c2p(2, 2)), run_time=4)
        self.wait()
        
        # 移動到左上方 (-2, 2)
        self.play(probe_pos.animate.move_to(axes.c2p(-2, 2)), run_time=3)
        self.wait()