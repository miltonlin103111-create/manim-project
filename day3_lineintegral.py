from manim import *
import numpy as np

class Day3LineIntegral(Scene):
    def construct(self):
        # 1. 建立座標軸與向量場
        axes = Axes(x_range=[-4, 4], y_range=[-3, 3], x_length=8, y_length=6)

        def func(point):
            x, y, _ = point
            return np.array([x + y, -x, 0]) 
            
        field = ArrowVectorField(
            func, 
            x_range=[-4, 4, 1], 
            y_range=[-3, 3, 1],
            length_func=lambda norm: 0.5 * norm, 
            #---半透明化---
            opacity=0.5
        )

        # 這裡設定一個參考的最大強度值，用來映射顏色
        max_magnitude = np.linalg.norm(func(np.array([4, 3, 0])))

        for vector in field:
            # 獲取箭頭的起始點
            point = vector.get_start()
            magnitude = np.linalg.norm(func(point))
            
            # 計算顏色比例 (0 ~ 1)
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            
            # 設定顏色：從小(BLUE) 到 大(RED) 漸變
            vector.set_color(interpolate_color(BLUE, RED, alpha))
        
        # 2. 定義積分路徑 (正弦波)
        path = ParametricFunction(
            lambda t: np.array([t, np.sin(t * 0.5), 0]),
            t_range=[-3, 3],
            color=WHITE
        )
        path_label = MathTex("C").next_to(path, UR)

        # 3. 建立移動點與跟隨向量

        # 設定t是一個值，從-3開始
        t_tracker = ValueTracker(-3)

        # 移動點移動到路徑的比例
        moving_dot = always_redraw(lambda: 
            Dot(path.point_from_proportion((t_tracker.get_value() + 3) / 6), color=YELLOW)
        )

        # 找到下一刻點的位置，即可找到切線向量
        def get_projection_vector():
            p = moving_dot.get_center()
            dt = 0.01 
            curr_prop = (t_tracker.get_value() + 3) / 6
            next_prop = np.clip(curr_prop + dt, 0, 1)
            
            p_next = path.point_from_proportion(next_prop)
            tangent_vec = p_next - p
            norm = np.linalg.norm(tangent_vec)
            
            if norm < 1e-6:
                return Vector([0, 0, 0])

            # 切線單位向量與內積
            T = tangent_vec / norm
            F = func(p)
            proj_len = np.dot(F, T)
            
            # 將投影向量回傳到get_projection_vector()
            return Arrow(
                start=p,
                end=p + T * proj_len * 0.5,
                buff=0,
                color=GOLD,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.3
            )
        # 不斷重新畫出get_projection_vector
        dr_vector = always_redraw(get_projection_vector)

        # 劃出moving_dot.get_center()處的向量場
        f_vector = always_redraw(lambda:
            Arrow(
                start=moving_dot.get_center(),
                end=moving_dot.get_center() + func(moving_dot.get_center()) * 0.5,
                buff=0, color=RED
            )
        )

        

        # 4. 數值顯示
        work_val = Variable(0, MathTex(r"\int_C \mathbf{F} \cdot d\mathbf{r}"), num_decimal_places=2)
        work_val.to_corner(UL)

        # 5. 播放動畫
        self.add(axes, field, path, path_label)
        self.play(
            Create(moving_dot), 
            Create(f_vector), 
            Create(dr_vector), 
            Write(work_val)
        )
        
        def update_work(mob):
            # 真正的線積分增量是 F · dr
            p = moving_dot.get_center()
            f = func(p)
            # 這裡用一個小的 delta 來模擬
            mob.tracker.set_value(mob.tracker.get_value() + np.linalg.norm(f) * 0.01)

        work_val.add_updater(update_work)
        
        # 讓 t 隨時間以線性增長到3
        self.play(t_tracker.animate.set_value(3), run_time=8, rate_func=linear)
        work_val.remove_updater(update_work)
        self.wait(2)