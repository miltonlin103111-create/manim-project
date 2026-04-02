from manim import *
import numpy as np

class Day5Curl(Scene):
    def construct(self):
        # 1. 建立座標軸
        axes = Axes(x_range=[-12, 12, 1], y_range=[-8, 8, 1], x_length=10.5, y_length=7)
        
        # --- 旋度場函數定義 ---
        # 為了有旋轉感，我們讓 x 分量受 y 影響，y 分量受 x 影響
        def function(point):
            x, y = axes.p2c(point)
            return np.array([-np.sin(y / 2), np.sin(x / 2), 0])
        
        def unit_func(point):
            raw_v = function(point)
            length = np.linalg.norm(raw_v)
            return raw_v / (length + 1e-8)

        # 2. 建立流線 (StreamLines) - 展現旋轉路徑
        stream_lines = StreamLines(
            function,
            x_range=[-5, 5, 0.4],
            y_range=[-4, 4, 0.4],
            colors=[BLUE, RED, WHITE],
            stroke_width=1.5,
            padding=1
        )

        # 3. 建立向量場 (ArrowVectorField) - 展現單位方向
        field = ArrowVectorField(
            unit_func,
            x_range=[-5, 5, 0.5],
            y_range=[-3.5, 3.5, 0.5],
            length_func=lambda norm: 0.6,
            stroke_width=1,
            opacity=0.5
        )

        # 為單位向量場著色 (根據原始場強度)
        max_magnitude = 1.0 
        for vector in field:
            point = vector.get_start()
            magnitude = np.linalg.norm(function(point))
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            vector.set_color(interpolate_color(BLUE, RED, alpha))

        # --- 關鍵修改：計算旋度 (Curl) ---
        def get_curl_at_point(m_point):
            p = axes.p2c(m_point)
            eps = 0.01 
            
            # 計算 dFy/dx
            p_x_plus = axes.c2p(p[0] + eps, p[1], 0)
            p_x_minus = axes.c2p(p[0] - eps, p[1], 0)
            dfy_dx = (unit_func(p_x_plus)[1] - unit_func(p_x_minus)[1]) / (2 * eps)
            
            # 計算 dFx/dy
            p_y_plus = axes.c2p(p[0], p[1] + eps, 0)
            p_y_minus = axes.c2p(p[0], p[1] - eps, 0)
            dfx_dy = (unit_func(p_y_plus)[0] - unit_func(p_y_minus)[0]) / (2 * eps)
            
            # 二維旋度公式: dFy/dx - dFx/dy
            res = dfy_dx - dfx_dy
            return np.clip(res, -100, 100)

        # 4. 探測器與標籤
        probe_pos = Dot(color=WHITE).move_to(axes.c2p(0, 0))
        probe_box = Square(side_length=0.8).set_stroke(WHITE, 2)

        def update_box(mob, dt):
            # A. 讓方塊跟隨探測點的位置
            mob.move_to(probe_pos.get_center())
            
            # B. 獲取當前位置的旋度值
            curl_val = get_curl_at_point(probe_pos.get_center())
            
            # C. 關鍵：使用 .rotate() 進行「增量旋轉」
            # 角度 = 角速度 (curl_val) * 時間差 (dt)
            mob.rotate(curl_val/30 * dt)

        # 3. 將更新函式掛載到方塊上
        probe_box.add_updater(update_box)

        # 旋度標籤 (使用交叉乘積符號)
        curl_label = always_redraw(lambda:
            VGroup(
                MathTex(r"(\nabla \times \mathbf{F}) \cdot \hat{\mathbf{k}} = "),
                DecimalNumber(get_curl_at_point(probe_pos.get_center()), num_decimal_places=2)
            ).arrange(RIGHT).scale(0.7).next_to(probe_box, UP)
        )

        # 5. 動畫播放
        self.add(axes, stream_lines, field, probe_pos, probe_box, curl_label)
        stream_lines.start_animation(warm_up=FALSE, flow_speed=0.8, time_width=0.4)
        
        # 移動路徑：觀察正旋、零旋、負旋
        self.play(probe_pos.animate.move_to(axes.c2p(0, 0)), run_time=2) # 中心旋轉最強
        self.wait()

        self.play(probe_pos.animate.move_to(axes.c2p(2*np.pi, 0)), run_time=3)
        self.wait(2)
        
        self.play(probe_pos.animate.move_to(axes.c2p(2*np.pi, 2*np.pi)), run_time=3) 
        self.wait(2)

        self.play(probe_pos.animate.move_to(axes.c2p(np.pi, np.pi)), run_time=3) 
        self.wait(3)

        
