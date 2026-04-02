from manim import *
import numpy as np

class Day4Divergence(Scene):
    def construct(self):
        # 1. 建立座標軸與向量場 (建議用一個散度不為常數的場，觀察更有趣)
        axes = Axes(x_range=[-12, 12, 1], y_range=[-8, 8, 1], x_length=10.5, y_length=7)
        
        def function(point):
            x, y = axes.p2c(point)
            return np.array([np.sin(x/2), np.sin(y/2), 0])
        
        def unit_func (point):
            x, y, = axes.p2c(point)
            length= np.linalg.norm(function(point))
            return np.array([np.sin(x/2)/(length + 1e-8), np.sin(y/2)/(length + 1e-8), 0])

        # 3. 建立 StreamLines
        # 密度設為 0.4，避免線條過多導致渲染太慢
        stream_lines = StreamLines(
            function,
            x_range=[-6, 6, 0.4],
            y_range=[-4, 4, 0.4],
            colors=[BLUE, RED, WHITE],
            stroke_width=3,
            padding=1
        )


        # --- 關鍵修改：根據向量大小設定顏色漸變 ---
        
        max_magnitude = np.sqrt(2) 

        for vector in field:
            # 獲取箭頭的起始點
            point = vector.get_start()
            # 計算該點的向量數值大小
            magnitude = np.linalg.norm(function(point))
            
            # 計算顏色比例 (0 ~ 1)，使用 clip 防止超過範圍
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            
            # 設定顏色：從小(BLUE) 到 大(RED) 漸變
            # 你也可以改成 colors=[YELLOW, RED] 等等
            vector.set_color(interpolate_color(BLUE, RED, alpha))

        # --- 顏色邏輯修正 ---
  

        probe_pos = Dot(color=WHITE).move_to(axes.c2p(0,0)) # 初始點
        
        def get_div_at_point(m_point):
            # 將螢幕像素座標轉回數學座標
            p = axes.p2c(m_point)
            eps = 0.01 # 單位場在奇點附近變化極大，eps 不宜太小否則會跳動
            
            # 計算單位場在 x 和 y 方向的數值偏微分
            p_x_plus = axes.c2p(p[0] + eps, p[1], 0)
            p_x_minus = axes.c2p(p[0] - eps, p[1], 0)
            dfx_dx = (unit_func(p_x_plus)[0] - unit_func(p_x_minus)[0]) / (2 * eps)
            
            p_y_plus = axes.c2p(p[0], p[1] + eps, 0)
            p_y_minus = axes.c2p(p[0], p[1] - eps, 0)
            dfy_dy = (unit_func(p_y_plus)[1] - unit_func(p_y_minus)[1]) / (2 * eps)
            
            res = dfx_dx + dfy_dy
            # 限制數值顯示，防止出現 999999 這種破壞畫面的數字
            return np.clip(res, -100, 100)

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
        self.play(probe_pos.animate.move_to(axes.c2p(0, 0)), run_time=3)
        self.wait()

        # 移動到右上方 (np.pi, np.pi)
        self.play(probe_pos.animate.move_to(axes.c2p(2*np.pi, 2*np.pi)), run_time=4)
        self.wait()
        
        # 移動到左上方 (np.pi, 0)
        self.play(probe_pos.animate.move_to(axes.c2p(2*np.pi, 0)), run_time=3)
        self.wait()