from manim import *
import numpy as np

class Gradient(MovingCameraScene):
    def construct(self):
        # 1. 定義座標軸與純量場函數
        axes = ThreeDAxes(x_range=[-5, 5], y_range=[-3, 3], x_length=10, y_length=6)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers()
        def get_val(x, y):
            # 一個簡單的山丘函數
            return x+y

        # 1. 建立函數定義標籤
        # 使用 MathTex 渲染標準數學公式
        func_label = MathTex(r"T(x, y) = x + y")
        func_label.scale(1.3)
        func_label.set_color(YELLOW) # 設定為白色或其他醒目的顏色
        func_label.to_edge(UP, buff=0.3)
        func_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        self.add(func_label)

# --- 定義數值範圍與對應顏色 ---
        
        # 2. 建立數值網格
        grid_labels = VGroup()
        # arange只含下限不含上限，因此(-4, 5) 這是從 -4 ~ 4 的意思
        x_values = np.arange(-5, 6, 1)
        y_values = np.arange(-3, 4, 1)

        # 雙重for迴圈
        for x in x_values:
            for y in y_values:
                val = get_val(x, y)
                if x == 0 or y == 0: continue
                # 建立數字物件 DecimalNumber為專為數值運算設計的文字類別，比text又更廣應用
                # 第一格: 你要存取數值的對象(val)；num_decimal_places: 小數點位數；include_sign: 正數是否加正號
                num = DecimalNumber(val, num_decimal_places=1, include_sign=False)
                num.scale(0.8)
                num.move_to(axes.c2p(x, y, 0))
                
                # --- 關鍵修改：根據數值計算顏色 ---

                max_val = 8  # 最高值
                
                # 步驟 A: 歸一化。計算 val 在 min_val 和 max_val 之間的位置 (0.0 ~ 1.0)
                # 如果 val = 0，alpha = 0；如果 val = 3，alpha = 1
                alpha = np.clip(val/max_val,0,1)
                
                # 步驟 B: 顏色插值。根據 alpha 在藍紅之間調色
                target_color = interpolate_color(BLUE, RED, alpha)
                
                # 步驟 C: 設定顏色
                num.set_color(target_color)
                
                # -----------------------------------
                grid_labels.add(num)

        target_point= axes.c2p(3,1.5)
        target_box= Square(side_length=1).set_stroke(WHITE, 2).move_to(axes.c2p(2,2))

        line_2dx = Line(
            start= axes.c2p(1.5, 1.5),
            end= axes.c2p(2.5, 1.5),
            buff= 0,
            color= BLUE,
            stroke_width=2,
            )
        line_2dx_label= MathTex(r"2", r"dx")
        line_2dx_label[1].set_color(BLUE)
        line_2dx_label.scale(0.5).next_to(line_2dx, DOWN).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        
        line_2dy = Line(
            start= axes.c2p(1.5, 1.5),
            end= axes.c2p(1.5, 2.5),
            buff= 0,
            color= RED,
            stroke_width=2,
            )
        line_2dy_label= MathTex(r"2", r"dy")
        line_2dy_label[1].set_color(RED)
        line_2dy_label.scale(0.5).next_to(line_2dy, LEFT).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

      
        # A. 顯示座標軸與所有網格數值
        self.play(Create(axes))
        self.play(Write(grid_labels), run_time=2)
        self.wait(3)
        
        self.play(self.camera.frame.animate.set(width=7).move_to(target_point),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        self.play(Create(target_box))
        self.play(Create(line_2dx), Create(line_2dy))
        self.play(Write(line_2dx_label), Write(line_2dy_label))
        self.wait(2)

        delta_x_1 = MathTex(r"\Delta Tx = ")
        delta_x_2 = MathTex(r"(4", r"+dx", r")-(4", r"-dx", r")", r"\over", r"2", r"dx")
        delta_x_3 = MathTex(r"=1")
        delta_x_2[1].set_color(BLUE)
        delta_x_2[3].set_color(BLUE)
        delta_x_2[7].set_color(BLUE)
        delta_x_group= VGroup(delta_x_1, delta_x_2, delta_x_3)
        delta_x_group.arrange(RIGHT, buff=0.2)
        delta_x_group.scale(0.5).move_to(axes.c2p(4.5,2.5)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        
        x_plus_dot= Dot(color=BLUE).move_to(axes.c2p(2.5, 2))
        x_min_dot= Dot(color=BLUE).move_to(axes.c2p(1.5, 2))
        self.play(FadeIn(x_plus_dot), FadeIn(x_min_dot))
        self.wait()
        self.play(line_2dx.animate.move_to(axes.c2p(2, 2)))
        self.play(Write(delta_x_group))
        self.wait(2)

        delta_y_1 = MathTex(r"\Delta Ty = ")
        delta_y_2 = MathTex(r"(4", r"+dy", r")-(4", r"-dy", r")", r"\over", r"2", r"dy")
        delta_y_3 = MathTex(r"=1")
        delta_y_2[1].set_color(RED)
        delta_y_2[3].set_color(RED)
        delta_y_2[7].set_color(RED)
        delta_y_group= VGroup(delta_y_1, delta_y_2, delta_y_3)
        delta_y_group.arrange(RIGHT, buff=0.2)
        delta_y_group.scale(0.5).move_to(axes.c2p(4.5,1.5)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        
        y_plus_dot= Dot(color=RED).move_to(axes.c2p(2, 2.5))
        y_min_dot= Dot(color=RED).move_to(axes.c2p(2, 1.5))
        self.play(FadeIn(y_plus_dot), FadeIn(y_min_dot))
        self.wait()
        self.play(line_2dy.animate.move_to(axes.c2p(2, 2)))
        self.play(Write(delta_y_group))
        self.wait(2)

        gradient_label= MathTex(r"\nabla",r" T(2, 2) ", r"=", r" [", r" 1", r"," ,r" 1", r" ]")
        gradient_label.scale(1).set_color(GOLD).move_to(axes.c2p(4.5,0.5)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        gradient_label[5].set_color(BLUE) 
        gradient_label[7].set_color(RED)
        self.play(Write(gradient_label),run_time=2)
        self.wait(3)

        all_objects= VGroup(delta_x_group, delta_y_group, target_box, line_2dx, line_2dx_label, line_2dy, line_2dy_label, x_plus_dot, x_min_dot, y_plus_dot, y_min_dot)
        gradient_vector= Arrow(
            start=axes.c2p(1.5, 1.5),
            end=axes.c2p(2.5,2.5),
            buff=0,
            color=GOLD
        )
        gradient_vector_label= MathTex(r"[1,1]")
        gradient_vector_label.scale(0.6).set_color(GOLD).next_to(axes.c2p(2.5,2.5),UP)
        self.play(FadeOut(all_objects))
        self.play(GrowArrow(gradient_vector))
        self.play(Write(gradient_vector_label),run_time=1)
        self.wait(3)
        