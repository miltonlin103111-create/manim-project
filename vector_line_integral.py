from manim import *
import numpy as np

class LineIntegral(MovingCameraScene):
    def construct(self):

        axes = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 1], x_length=10, y_length=6)
        func_label= MathTex(r"\vec{F} = [Fx, Fy]")
        func_label.scale(1.5).set_color(PURE_YELLOW).move_to(axes.c2p(0,3)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
       
        def path_func(x):
            return (0.37*(x-0.5))**3

        # 2. 定義積分路徑 
        path = axes.plot(
            lambda x: path_func(x), # 你的函數
            x_range=[-3, 3], # 關鍵：只畫這一小段
            dt=0.05, # 增加採樣點密度
            color=WHITE
        )        
        path_label = MathTex("L").next_to(path, DL)

        def function(point):
            x, y = axes.p2c(point)
            return np.array([-y+0.5*x, x+1, 0])

        field = ArrowVectorField(
            function,
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            length_func=lambda norm: 1.5,
            stroke_width=1, 
            color= GOLD,
            opacity=1
        )


        self.play(Create(field), Write(func_label), run_time=2)
        self.bring_to_front(func_label)
        self.wait(2)
        self.play(field.animate.set_opacity(0.4), Create(path), FadeIn(path_label), run_time=2)
        self.wait(2)
        
        ex_vec = VGroup(*[
            Arrow(
                start=(p_start := path.point_from_proportion(alpha)), 
                end=p_start + 1.5*function(p_start)/np.linalg.norm(function(p_start)),
                buff=0,
                stroke_width=4,
                color= PINK
            )
            for alpha in np.linspace(0, 1, 8)
            ])
        self.play(Create(ex_vec))
        self.wait(2)

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

        wrong_integral= MathTex(r"\int_{L} \lvert", r"\vec{F}", r" \rvert \,d", r"\ell")
        wrong_integral.scale(1.2).move_to(axes.c2p(0,-2)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        wrong_integral[4].set_color(ORANGE)
        wrong_integral[2].set_color(PINK)

        self.play(FadeIn(ds_plus_dot), FadeIn(ds_min_dot), FadeIn(ds_path), FadeIn(ds_label), run_time=2)
        self.wait(2)       
        self.play(Write(wrong_integral))
        self.wait(2)
        self.play(FadeOut(wrong_integral), FadeOut(ds_plus_dot), FadeOut(ds_min_dot), FadeOut(ds_path), FadeOut(ds_label))     

        ex_vec_parallel = VGroup()
        ex_vec_vertical = VGroup()

        for alpha in np.linspace(0, 1, 8):
            # 1. 取得起點與場向量
            p_start = path.point_from_proportion(alpha)
            f_vec = 1.5*function(p_start)/np.linalg.norm(function(p_start))  # 假設這已經是 3D 向量
    
            # 2. 計算單位切向量 T
            # 取得極小位移後的點來估計切線
            dt = 0.001
            # 處理邊界，避免 alpha+dt > 1
            alpha_next = min(alpha + dt, 1)
            alpha_prev = max(alpha - dt, 0)
            p_next = path.point_from_proportion(alpha_next)
            p_prev = path.point_from_proportion(alpha_prev)
    
            tangent = p_next - p_prev
            unit_tangent = tangent / np.linalg.norm(tangent)
    
            # 3. 計算投影
            # 切向分量 = (F 點積 T) * T
            v_para = np.dot(f_vec, unit_tangent) * unit_tangent
            # 法向分量 = F - 切向分量
            v_vert = f_vec - v_para
    
            # 4. 建立箭頭 (加上 0.3 的縮放)
            para_arrow = Arrow(
                start=p_start, end=p_start + v_para ,
                buff=0, 
                color=BLUE, 
                stroke_width=10
            )
            vert_arrow = Arrow(
                start=p_start,
                end=p_start + v_vert ,
                buff=0, 
                color=RED, 
                stroke_width=3
            )
    
            ex_vec_parallel.add(para_arrow)
            ex_vec_vertical.add(vert_arrow)

        self.play(ex_vec.animate.set_opacity(0.6), Create(ex_vec_parallel), Create(ex_vec_vertical), run_time=2)
        self.wait(2)
        self.play(FadeOut(ex_vec_vertical), FadeOut(ex_vec))
        ex_vec.set_opacity(1)
        self.wait(2)
        right_integral= MathTex(r"W=\int_{L}", r"F_{\parallel}", r"\,d", r"\ell")
        right_integral.scale(1.2).move_to(axes.c2p(0,-2))
        right_integral[3].set_color(ORANGE)
        right_integral[1].set_color(BLUE)
        right_integral_copy= right_integral.copy()
        right_integral.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        self.play(Write(right_integral), run_time=2)
        self.wait(2)
        self.play(FadeOut(field), FadeOut(ex_vec_parallel), FadeIn(ex_vec), FadeOut(right_integral))
        self.wait(2)
        self.play(self.camera.frame.animate.set(width=6).move_to([1.5, 0.5, 0]),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        self.wait(2)

        F_label= MathTex(r"\vec{F}")
        F_label.scale(0.8).move_to(axes.c2p(1.5,1.8)).set_color(PINK)
        self.play(FadeIn(F_label))
        self.wait(1)

        p_start = path.point_from_proportion(5/7)
        dt=0.001
        p_plus= path.point_from_proportion(5/7+dt)
        tangent= p_plus-p_start
        unit_tangent= tangent / np.linalg.norm(tangent)
        
        u_vec= Arrow(
            start= p_start,
            end= p_start+ unit_tangent,
            buff=0,
            stroke_width= 5,
            color= ORANGE
            )
        u_vec_label= MathTex(r"\vec{u}")
        u_vec_label.set_color(ORANGE).scale(0.8).move_to(axes.c2p(1.7,-0.3))

        self.play(Create(u_vec))
        self.play(FadeIn(u_vec_label))
        self.wait(1)
        self.play(self.camera.frame.animate.set(width=6).move_to([3, 0.5, 0]),
            run_time=1,
            rate_func=smooth) # 讓移動過程平滑
        self.wait(2)        

        dot_label= MathTex(r"\vec{F}", r"\cdot", r"\vec{u}", r"=", r"F_{\parallel}")
        dot_label[0].set_color(PINK)
        dot_label[2].set_color(ORANGE)
        dot_label[4].set_color(BLUE)
        dot_label.scale(0.9).move_to(axes.c2p(3.8,1.5))
        dot_label_copy= dot_label.copy()
        dot_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        ds_vec_label= MathTex(r"d\vec{\ell}",r"=[dx,dy,dz]")
        ds_vec_label[0].set_color(ORANGE)
        ds_vec_label.scale(0.8).move_to(axes.c2p(3.8,0.5)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        u_ds_label_1= MathTex(r"\vec{u}", r"=")
        u_ds_label_2= MathTex(r"d\vec{\ell}", r"\over", r"\lvert", r"d\vec{\ell}", r"\rvert")
        u_ds_label_1[0].set_color(ORANGE)
        u_ds_label_2[0].set_color(ORANGE)
        u_ds_label_2[3].set_color(ORANGE)
        u_ds_label= VGroup(u_ds_label_1, u_ds_label_2)
        u_ds_label.arrange(RIGHT, buff=0.1)
        u_ds_label.scale(0.9).move_to(axes.c2p(3.8,-0.5))
        u_ds_label_copy= u_ds_label.copy()
        u_ds_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        self.play(Write(dot_label))
        self.add(dot_label_copy)
        self.wait(2)
        self.play(Write(ds_vec_label))
        self.wait(2)
        self.play(Write(u_ds_label))
        self.add(u_ds_label_copy)
        self.wait(2)
        
        dot_re_label_1= MathTex(r"\vec{F}", r"\cdot") 
        dot_re_label_2= MathTex(r"d\vec{\ell}", r"\over", r"\lvert", r"d\vec{\ell}", r"\rvert")
        dot_re_label_3= MathTex(r"=", r"F_{\parallel}")
        dot_re_label_1[0].set_color(PINK)
        dot_re_label_2[0].set_color(ORANGE)
        dot_re_label_2[3].set_color(ORANGE)
        dot_re_label_3[1].set_color(BLUE)
        dot_re_label= VGroup(dot_re_label_1, dot_re_label_2, dot_re_label_3)
        dot_re_label.arrange(RIGHT, buff=0.2)
        dot_re_label.scale(0.9).move_to(axes.c2p(3.8,1.5))
        dot_re_label_1.shift(UP * 0.1)
        dot_re_label_copy= dot_re_label.copy()
        dot_re_label.add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        self.play(TransformMatchingTex(Group(dot_label_copy, u_ds_label_copy), dot_re_label_copy), FadeOut(dot_label), FadeOut(u_ds_label))
        self.add(dot_re_label)
        self.wait(2)        
        
        right_integral_copy.scale(0.8).move_to(axes.c2p(3.8,-0.5))
        self.play(Write(right_integral_copy))
        self.wait(2)
        right_re_integral_1= MathTex(r"W=\int_{L}",r"\vec{F}", r"\cdot")
        right_re_integral_2= MathTex(r"d\vec{\ell}", r"\over", r"\lvert", r"d\vec{\ell}", r"\rvert")
        right_re_integral_3= MathTex(r"\,d", r"\ell")
        right_re_integral_1[1].set_color(PINK)
        right_re_integral_2[0].set_color(ORANGE)
        right_re_integral_2[3].set_color(ORANGE)
        right_re_integral_3[1].set_color(ORANGE)
        right_re_integral= VGroup(right_re_integral_1, right_re_integral_2, right_re_integral_3)
        right_re_integral.arrange(RIGHT, buff=0.2)
        right_re_integral.scale(0.9).move_to(axes.c2p(3.8,-0.5))
        self.play(TransformMatchingTex(Group(dot_re_label_copy, right_integral_copy), right_re_integral), FadeOut(dot_re_label))
        self.wait(2)

        right_con_integral= MathTex(r"W=\int_{L}", r"\vec{F}", r"\cdot", r"d", r"\vec{\ell}")
        right_con_integral[1].set_color(PINK)
        right_con_integral[4].set_color(ORANGE)
        right_con_integral.scale(0.9).move_to(axes.c2p(3.8,-0.5))
        con_rectangle= Rectangle(width=4, height=1.6).set_stroke(WHITE, 2).move_to(axes.c2p(3, 0.5))
        self.play(TransformMatchingTex(right_re_integral, right_con_integral))
        self.wait(2)
        all_objects= VGroup(path, path_label, ex_vec, u_vec, u_vec_label, F_label, ds_vec_label)
        self.play(FadeOut(all_objects))
        self.play(right_con_integral.animate.scale(1.2).move_to(axes.c2p(3, 0.5)))
        self.play(Create(con_rectangle))
        self.wait(2)

        con= VGroup(right_con_integral, con_rectangle)
        if_tex= Text("如果 L 是一個閉環，則在積分符號打一個圈", font="Microsoft JhengHei", weight=BOLD) 
        if_tex.scale(0.3).move_to(axes.c2p(3, 0.35))   
        loop_integral= MathTex(r"W=\oint_{L}", r"\vec{F}", r"\cdot", r"d", r"\vec{\ell}")
        loop_integral[1].set_color(PINK)
        loop_integral[4].set_color(ORANGE)
        loop_integral.scale(0.65).move_to(axes.c2p(3,-0.3))
        loop_rectangle= Rectangle(width=4, height=1.6).scale(0.6).set_stroke(WHITE, 2).move_to(axes.c2p(3, -0.3))
        self.play(con.animate.scale(0.6).move_to(axes.c2p(3, 1.3)))
        self.play(Write(if_tex))
        self.play(Create(loop_rectangle), Write(loop_integral))
        self.wait(5)

        