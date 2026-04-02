from manim import *
import numpy as np

class LineIntegral(Scene):
    def construct(self):

        axes = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 1], x_length=10, y_length=6)

        func_label= MathTex(r"T = f(x,y)")
        func_label.scale(1.5).set_color(PURE_YELLOW).move_to(axes.c2p(0,3)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
       
        def path_func(x):
            return (0.37*(x-0.5))**3

        # 2. 定義積分路徑 (正弦波)
        path = axes.plot(
            lambda x: path_func(x), # 你的函數
            x_range=[-3, 3], # 關鍵：只畫這一小段
            dt=0.05, # 增加採樣點密度
            color=WHITE
        )        
        path_label = MathTex("L").next_to(path, DL)

        def get_val(x, y):
            return 2*np.sin(x)*np.cos(y)+3
        grid_labels = VGroup()
        # arange只含下限不含上限，因此(-4, 5) 這是從 -4 ~ 4 的意思
        x_values = np.arange(-5, 6, 1)
        y_values = np.arange(-3, 4, 1)
        # 雙重for迴圈
        for x in x_values:
            for y in y_values:
                val = get_val(x, y)
                # 建立數字物件 DecimalNumber為專為數值運算設計的文字類別，比text又更廣應用
                # 第一格: 你要存取數值的對象(val)；num_decimal_places: 小數點位數；include_sign: 正數是否加正號
                num = DecimalNumber(val, num_decimal_places=1, include_sign=False)
                num.scale(1)
                num.move_to(axes.c2p(x, y, 0))
                
                # --- 關鍵修改：根據數值計算顏色 ---

                max_val = 5  # 最高值
                
                # 步驟 A: 歸一化。計算 val 在 min_val 和 max_val 之間的位置 (0.0 ~ 1.0)
                # 如果 val = 0，alpha = 0；如果 val = 3，alpha = 1
                alpha = np.clip(val/max_val,0,1)
                
                # 步驟 B: 顏色插值。根據 alpha 在藍紅之間調色
                target_color = interpolate_color(BLUE, RED, alpha)
                
                # 步驟 C: 設定顏色
                num.set_color(target_color)
                
                # -----------------------------------

                num.target_z = val 
                grid_labels.add(num)
                
       

        ds_plus_dot= Dot(color= ORANGE).move_to(axes.c2p(-0.5, path_func(-0.5)))
        ds_min_dot= Dot(color= ORANGE).move_to(axes.c2p(-1, path_func(-1)))
        ds_path= Line(
            start= axes.c2p(-1, path_func(-1)),
            end= axes.c2p(-0.5, path_func(-0.5)),
            buff= 0,
            color= ORANGE,
            stroke_width=4,
            )
        ds_label= MathTex(r"d\ell")
        ds_label.scale(0.9).set_color(ORANGE).next_to(ds_path, UP).add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)

        integral_label_1_old= MathTex(r"\int_{L} f(x, y) \,d",r"\ell")
        integral_label_1_old[1].set_color(ORANGE)
        integral_label_1_old.scale(1.2).move_to(axes.c2p(0,-2)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        self.play( Write(grid_labels), Write(func_label), run_time=2)
        self.bring_to_front(func_label)
        self.wait(2)
        self.play(grid_labels.animate.set_fill(opacity=0.6), Create(path), FadeIn(path_label), run_time=2)
        self.wait(2)
        self.play(FadeIn(ds_plus_dot), FadeIn(ds_min_dot), FadeIn(ds_path), FadeIn(ds_label), run_time=2)
        self.wait(2)       
        self.play(Write(integral_label_1_old))
        self.wait(2)

        some_objects= VGroup(path, path_label, ds_plus_dot, ds_min_dot, ds_path,  ds_label)
        self.play(FadeOut(grid_labels), some_objects.scale(0.9).animate.move_to(axes.c2p(-3,1.5)), integral_label_1_old.animate.move_to(axes.c2p(3.5,1.5)),  
            func_label.animate.move_to(axes.c2p(3.5,3)))
        integral_label_1= MathTex(r"\int_{L} f(x, y) \,d", r"\ell")
        integral_label_1[1].set_color(ORANGE)
        integral_label_1.scale(1.2).move_to(axes.c2p(3.5,1.5))
        self.add(integral_label_1)
        self.play(FadeOut(integral_label_1_old))
        self.wait(2)

        path_eq = MathTex(
            r"L: \begin{cases} {{x}} = {{p}}({{t}}) \\ {{y}} = {{q}}({{t}}) \end{cases}",
            r"({{t}} \in \mathbb{R})"
        )
        path_eq.set_color_by_tex("t", PURE_GREEN)
        path_eq.set_color_by_tex("x", BLUE)
        path_eq.set_color_by_tex("p", BLUE)
        path_eq.set_color_by_tex("y", RED)
        path_eq.set_color_by_tex("q", RED)
        path_eq.scale(1).move_to(axes.c2p(-3.3, -1.5)).add_background_rectangle(opacity=0.8)
        
        self.play(Write(path_eq))
        self.wait(2)
 
        integral_label_2= MathTex(r"\int_{L} f({{p}}, {{q}}) \,d", r"\ell")
        integral_label_2[1].set_color(ORANGE)
        integral_label_2.set_color_by_tex("p", BLUE)
        integral_label_2.set_color_by_tex("q", RED)
        integral_label_2.scale(1.2).move_to(axes.c2p(3.5,1.5))
        self.play(TransformMatchingTex(integral_label_1, integral_label_2))
        integral_label_2_copy= integral_label_2.copy()
        self.add(integral_label_2_copy)
        self.wait()

        point_min_label= MathTex(r"({{p}}, {{q}})")
        d_m_curr= ds_min_dot.get_center()
        point_min_label.set_color_by_tex("p", BLUE)
        point_min_label.set_color_by_tex("q", RED)
        point_min_label.scale(0.8).move_to(axes.c2p(d_m_curr[0], d_m_curr[1]-1.5)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        point_plus_label= MathTex(r"({{p}}+d{{p}}, {{q}}+d{{q}})")
        d_p_curr= ds_plus_dot.get_center()
        point_plus_label.set_color_by_tex("p", BLUE)
        point_plus_label.set_color_by_tex("q", RED)
        point_plus_label.scale(0.8).move_to(axes.c2p(d_p_curr[0]+1.5, d_p_curr[1]-1)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        point_min_vec= Arrow(
            start= axes.c2p(d_m_curr[0], d_m_curr[1]-1.2),
            end= axes.c2p(d_m_curr[0], d_m_curr[1]-0.3),
            buff=0,
            stroke_width=2,
            tip_length=0.2,
            color= WHITE
        )
        point_plus_vec= Arrow(
            start= axes.c2p(d_p_curr[0]+1.5, d_p_curr[1]-0.7),
            end= axes.c2p(d_p_curr[0]+0.2, d_p_curr[1]-0.2),
            buff=0,
            stroke_width=2,
            tip_length=0.2,
            color= WHITE
        )

        self.play(FadeIn(point_min_label), FadeIn(point_min_vec))
        self.play(FadeIn(point_plus_label), FadeIn(point_plus_vec))
        self.wait(2)

        ds_math_label_1= MathTex(r"d", r"\ell", r"=", r"\sqrt{(d{{p}}({{t}}))^2 + (d{{q}}({{t}}))^2}")
        ds_math_label_1[1].set_color(ORANGE)
        ds_math_label_1.set_color_by_tex("p", BLUE)
        ds_math_label_1.set_color_by_tex("t", PURE_GREEN)
        ds_math_label_1.set_color_by_tex("q", RED)
        ds_math_label_1.scale(1).move_to(axes.c2p(3.5, 0))
        ds_math_label_2= MathTex(r"d", r"\ell", r"=", r"\sqrt{(\frac{d{{p}}({{t}})}{d{{t}}})^2 + (\frac{d{{q}}({{t}})}{d{{t}}})^2}", r"d{{t}}")
        ds_math_label_2[1].set_color(ORANGE)
        ds_math_label_2.set_color_by_tex("p", BLUE)
        ds_math_label_2.set_color_by_tex("t", PURE_GREEN)
        ds_math_label_2.set_color_by_tex("q", RED)
        ds_math_label_2.scale(1).move_to(axes.c2p(3.5, 0))
        ds_math_label_3= MathTex(r"d", r"\ell", r"=", r"\sqrt{({{p}}'({{t}}))^2 + ({{q}}'({{t}}))^2}",r"\,", r"d{{t}}")
        ds_math_label_3[1].set_color(ORANGE)
        ds_math_label_3.set_color_by_tex("p", BLUE)
        ds_math_label_3.set_color_by_tex("t", PURE_GREEN)
        ds_math_label_3.set_color_by_tex("q", RED)
        ds_math_label_3.scale(1).move_to(axes.c2p(3.5, 0))
        self.play(Write(ds_math_label_1))
        self.wait(1)
        self.play(TransformMatchingTex(ds_math_label_1, ds_math_label_2))
        self.wait(1)     
        self.play(TransformMatchingTex(ds_math_label_2, ds_math_label_3))
        ds_math_label_3_copy= ds_math_label_3.copy()
        self.add(ds_math_label_3_copy)
        self.wait(2)

        integral_label_3= MathTex(r"\int_{L} f({{p}}, {{q}}) \: \sqrt{({{p}}')^2 + ({{q}}')^2} \, d{{t}}")
        integral_label_3.set_color_by_tex("p", BLUE)
        integral_label_3.set_color_by_tex("q", RED)
        integral_label_3.set_color_by_tex("t", PURE_GREEN)
        integral_label_3.scale(1).move_to(axes.c2p(3.5,-1.8))
        self.play(ReplacementTransform(Group(integral_label_2, ds_math_label_3), integral_label_3))
        self.wait(3)

        all_objects= VGroup(path, path_label, ds_path, ds_plus_dot, ds_min_dot, ds_label, point_min_label, point_plus_label, point_min_vec, point_plus_vec, 
            ds_math_label_3_copy, integral_label_2_copy)
        self.play(FadeOut(all_objects), 
            func_label.animate.move_to(axes.c2p(0,2)), 
            path_eq.animate.move_to(axes.c2p(0,0.5)), 
            integral_label_3.animate.scale(1.2).move_to(axes.c2p(0,-1.5)),
            run_time=2
        )

        integral_label_4 = MathTex(
            r"\int_{",    # [0]
            r"t_0",       # [1]  <-- 這裡就能精準染色了！
            r"}^{",       # [2]
            r"t_1",       # [3]  <-- 這裡也是！
            r"} f(",      # [4]
            r"p",         # [5]
            r",",         # [6]
            r"q",         # [7]
            r") \sqrt{({{p}}')^2 + ({{q}}')^2} \, d{{t}}" # [8] 剩下的
        )

        # 這樣你就不需要 set_color_by_tex 了，直接用索引
        integral_label_4[1].set_color(PURE_GREEN) # 針對 t_0 染色
        integral_label_4[3].set_color(PURE_GREEN) # 針對 t_1 染色
        integral_label_4[5].set_color(BLUE)  # 針對 p 染色
        integral_label_4[7].set_color(RED)   # 針對 q 染色
        integral_label_4.set_color_by_tex("p", BLUE)
        integral_label_4.set_color_by_tex("q", RED)
        integral_label_4.set_color_by_tex("t", PURE_GREEN)
        integral_label_4.scale(1.2).move_to(axes.c2p(0,-1.5))        
        self.play(TransformMatchingTex(integral_label_3, integral_label_4), run_time=2)
        self.wait(2)
        con_rectangle= Rectangle(width=8, height=2).set_stroke(WHITE, 2).move_to(axes.c2p(0, -1.5))
        self.play(Create(con_rectangle))
        self.wait(2)
