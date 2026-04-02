from manim import *
import numpy as np

class Divergence(MovingCameraScene):
    def construct(self):

        # 1. 建立座標軸與向量場 (建議用一個散度不為常數的場，觀察更有趣)
        axes = Axes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], x_length=8, y_length=8)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers()
        
        def function(point):
            x, y = axes.p2c(point)
            return np.array([x, y])

        func_label = MathTex(r"F[Fx, Fy] = [ x , y ]")
        func_label.scale(1.3)
        func_label.set_color(YELLOW) # 設定為白色或其他醒目的顏色
        func_label.to_edge(UP, buff=0.3)
        func_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        self.add(func_label)

        
        def unit_func (point):
            x, y = axes.p2c(point)
            length= np.linalg.norm(function(point))
            return np.array([x/(length + 1e-8), y/(length + 1e-8), 0])
        
        field = ArrowVectorField(
            function,
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            length_func=lambda norm: norm,
            stroke_width=1, 
            opacity=1.5
        )

        # --- 關鍵修改：根據向量大小設定顏色漸變 ---
        
        max_magnitude = 4

        for vector in field:
            # 獲取箭頭的起始點
            point = vector.get_start()
            
            x, y = axes.p2c(point) # 轉回數學座標來判斷
            # 如果 x 趨近於 0 或 y 趨近於 0 (考慮到浮點數誤差，用 0.1 判斷)
            if abs(x) < 0.1 or abs(y) < 0.1:
                field.remove(vector) # 從物件群組中剔除

            magnitude = np.linalg.norm(function(point))
            
            # 計算顏色比例 (0 ~ 1)，使用 clip 防止超過範圍
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            
            # 設定顏色：從小(BLUE) 到 大(RED) 漸變
            # 你也可以改成 colors=[YELLOW, RED] 等等
            vector.set_color(interpolate_color(BLUE, RED, alpha))


        # 2. 建立散度探測器 (方塊 + 文字)
        start_point= axes.c2p(0,0)
        probe_pos = Dot(color=WHITE).move_to(start_point) # 初始點
        # 探測器方塊
        # 使用 ValueTracker 來控制透明度
        fill_tracker = ValueTracker(0) # 初始透明度為 0
        probe_box = always_redraw(lambda:
            Square(side_length=1)
            .set_fill(PURPLE, opacity=fill_tracker.get_value()) # 動態讀取 tracker
            .set_stroke(WHITE, 2)
            .move_to(probe_pos.get_center())
        )
        target_point= np.array([1, 1])


        self.add(axes, probe_pos, probe_box)
        self.play(Create(field))
        self.bring_to_front(func_label)
        self.wait(2)
        self.play(probe_pos.animate.move_to(axes.c2p(*target_point)),run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.set(width=7).move_to(axes.c2p(2.5,1.3)),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        
        x_plus_p= axes.c2p(1.5,1)
        x_plus_vec = Arrow(
            start=x_plus_p,
            end=axes.c2p(target_point[0] + 0.5 + function(x_plus_p)[0], target_point[1] + function(x_plus_p)[1]),
            buff=0,
            color=GOLD
        )
        x_plus_vec_x_proj = Arrow(
            start=x_plus_p,
            # PURE_BLUE -> BLUE
            end=axes.c2p(target_point[0] + 0.5 + function(x_plus_p)[0], target_point[1]),
            buff=0,
            color=PURE_BLUE
        )
        x_plus_vec_y_proj = Arrow(
            start=x_plus_p,
            # RED -> PURE_RED
            end=axes.c2p(target_point[0] + 0.5, target_point[1] + function(x_plus_p)[1]),
            buff=0,
            color=PURE_RED
        )

        x_min_p = axes.c2p(0.5, 1)
        x_min_vec = Arrow(
            start=x_min_p,
            end=axes.c2p(target_point[0] - 0.5 + function(x_min_p)[0], target_point[1] + function(x_min_p)[1]),
            buff=0,
            color=GOLD
        )
        x_min_vec_x_proj = Arrow(
            start=x_min_p,
            # PURE_BLUE -> BLUE
            end=axes.c2p(target_point[0] - 0.5 + function(x_min_p)[0], target_point[1]),
            buff=0,
            color=PURE_BLUE
        )
        x_min_vec_y_proj = Arrow(
            start=x_min_p,
            # RED -> PURE_RED
            end=axes.c2p(target_point[0] - 0.5, target_point[1] + function(x_min_p)[1]),
            buff=0,
            color=PURE_RED
        )

        right_edge = Line(
            probe_box.get_corner(UR),
            probe_box.get_corner(DR),
            color=RED, # PURE_RED -> RED
            stroke_width=4
        )
        left_edge = Line(
            probe_box.get_corner(UL),
            probe_box.get_corner(DL),
            color=PURE_RED, # RED -> PURE_RED
            stroke_width=4
        )
        line_2dx = Line(
            start=axes.c2p(0.5, 0.5),
            end=axes.c2p(1.5, 0.5),
            buff=0,
            color=BLUE, # PURE_BLUE -> BLUE
            stroke_width=4,
        )
        line_2dx_label = MathTex(r"2", r"dx")
        line_2dx_label[1].set_color(BLUE) # PURE_BLUE -> BLUE
        line_2dx_label.scale(0.5).next_to(line_2dx, DOWN).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        line_2dy = Line(
            start=axes.c2p(0.5, 0.5),
            end=axes.c2p(0.5, 1.5),
            buff=0,
            color=RED, # PURE_RED -> RED
            stroke_width=4,
        )
        line_2dy_label = MathTex(r"2", r"dy")
        line_2dy_label[1].set_color(RED) # PURE_RED -> RED
        line_2dy_label.scale(0.5).next_to(line_2dy, LEFT).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)

        area_label = MathTex(r"4dxdy")
        area_label.scale(0.6).move_to(axes.c2p(*target_point)).set_color(PURPLE).add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)

        x_plus_vecgroup = np.array([function(x_plus_p)[0], 0, 0])
        x_plus_vectors = VGroup(*[
            Arrow(
                start=right_edge.point_from_proportion(alpha),
                end=right_edge.point_from_proportion(alpha) + x_plus_vecgroup,
                buff=0,
                color=PURE_BLUE # BLUE -> PURE_BLUE
            )
            for alpha in np.linspace(0, 1, 5)
        ])
        x_min_vecgroup = np.array([function(x_min_p)[0], 0, 0])
        x_min_vectors = VGroup(*[
            Arrow(
                start=left_edge.point_from_proportion(alpha),
                end=left_edge.point_from_proportion(alpha) + x_min_vecgroup,
                buff=0,
                color=PURE_BLUE # BLUE -> PURE_BLUE
            )
            for alpha in np.linspace(0, 1, 5)
        ])        
        self.play(field.animate.set_opacity(0.5))
        self.play(FadeIn(line_2dx), FadeIn(line_2dy))
        self.play(Write(line_2dx_label), Write(line_2dy_label))
        self.play(fill_tracker.animate.set_value(0.8), Write(area_label))
        self.wait(2)
        self.play(FadeOut(area_label))
        self.play(GrowArrow(x_plus_vec),GrowArrow(x_min_vec))
        self.wait(2)
        self.play(GrowArrow(x_plus_vec_x_proj), GrowArrow(x_plus_vec_y_proj), GrowArrow(x_min_vec_x_proj), GrowArrow(x_min_vec_y_proj),  
            x_plus_vec.animate.set_opacity(0.5), x_min_vec.animate.set_opacity(0.5))
        self.wait(2)
        self.play(FadeOut(x_plus_vec_y_proj), FadeOut(x_min_vec_y_proj), FadeIn(right_edge), run_time=2)
        self.wait()
        self.play(FadeIn(x_plus_vectors), FadeIn(x_min_vectors), run_time=2)
        self.wait(2)

        delta_x_1 = MathTex(r"\Delta Fx =")
        delta_x_2 = MathTex(r"(", r"1+dx", r")", r"\times", r"2dy", r"-", r"(", r"1-dx", r")", r"\times", r"2dy", r"\over", r"4dxdy")
        delta_x_3 = MathTex(r"=1")
        delta_x = VGroup(delta_x_1, delta_x_2, delta_x_3)
        delta_x.arrange(RIGHT, buff=0.2)
        delta_x.scale(0.4).set_color(WHITE).move_to(axes.c2p(3.8, 2.8)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        delta_x_2[1].set_color(BLUE) # BLUE -> PURE_BLUE
        delta_x_2[4].set_color(RED)       # PURE_RED -> RED
        delta_x_2[7].set_color(BLUE) # BLUE -> PURE_BLUE
        delta_x_2[10].set_color(RED)      # PURE_RED -> RED
        delta_x_2[12].set_color(PURPLE)
        self.play(Write(delta_x), run_time=2)
        self.wait(2)

        y_plus_p = axes.c2p(1, 1.5)
        y_plus_vec = Arrow(
            start=y_plus_p,
            end=axes.c2p(target_point[0] + function(y_plus_p)[0], target_point[1] + 0.5 + function(y_plus_p)[1]),
            buff=0,
            color=GOLD
        )
        y_plus_vec_x_proj = Arrow(
            start=y_plus_p,
            # BLUE -> PURE_BLUE
            end=axes.c2p(target_point[0] + function(y_plus_p)[0], target_point[1] + 0.5),
            buff=0,
            color=PURE_BLUE
        )
        y_plus_vec_y_proj = Arrow(
            start=y_plus_p,
            # RED -> PURE_RED
            end=axes.c2p(target_point[0], target_point[1] + 0.5 + function(y_plus_p)[1]),
            buff=0,
            color=PURE_RED
        )

        y_min_p = axes.c2p(1, 0.5)
        y_min_vec = Arrow(
            start=y_min_p,
            end=axes.c2p(target_point[0] + function(y_min_p)[0], target_point[1] - 0.5 + function(y_min_p)[1]),
            buff=0,
            color=GOLD
        )
        y_min_vec_x_proj = Arrow(
            start=y_min_p,
            # BLUE -> PURE_BLUE
            end=axes.c2p(target_point[0] + function(y_min_p)[0], target_point[1] - 0.5),
            buff=0,
            color=PURE_BLUE
        )
        y_min_vec_y_proj = Arrow(
            start=y_min_p,
            # RED -> PURE_RED
            end=axes.c2p(target_point[0], target_point[1] - 0.5 + function(y_min_p)[1]),
            buff=0,
            color=PURE_RED
        )

        up_edge = Line(
            probe_box.get_corner(UR),
            probe_box.get_corner(UL),
            # PURE_BLUE -> BLUE
            color=BLUE,
            stroke_width=4
        )
        down_edge = Line(
            probe_box.get_corner(DR), 
            probe_box.get_corner(DL),
            # RED -> PURE_RED
            color=PURE_RED,
            stroke_width=4
        )
        
        y_plus_vecgroup = np.array([0, function(y_plus_p)[1], 0])
        y_plus_vectors = VGroup(*[
            Arrow(
                start=up_edge.point_from_proportion(alpha), 
                end=up_edge.point_from_proportion(alpha) + y_plus_vecgroup,
                buff=0,
                # RED -> PURE_RED
                color=PURE_RED
            )
            for alpha in np.linspace(0, 1, 5)
        ])
        
        y_min_vecgroup = np.array([0, function(y_min_p)[1], 0])
        y_min_vectors = VGroup(*[
            Arrow(
                start=down_edge.point_from_proportion(alpha), 
                end=down_edge.point_from_proportion(alpha) + y_min_vecgroup,
                buff=0,
                # RED -> PURE_RED
                color=PURE_RED
            )
            for alpha in np.linspace(0, 1, 5)
        ])
        
        self.play(FadeOut(x_plus_vec_x_proj), FadeOut(x_min_vec_x_proj), FadeOut(x_plus_vec), FadeOut(x_min_vec), FadeOut(x_plus_vectors),  
            FadeOut(x_min_vectors), FadeOut(right_edge), run_time=2)
        self.wait(1)
        self.play(GrowArrow(y_plus_vec),GrowArrow(y_min_vec))
        self.wait(2)
        self.play(GrowArrow(y_plus_vec_x_proj), GrowArrow(y_plus_vec_y_proj), GrowArrow(y_min_vec_x_proj), GrowArrow(y_min_vec_y_proj),  
            y_plus_vec.animate.set_opacity(0.5), y_min_vec.animate.set_opacity(0.5))
        self.wait(2)
        self.play(FadeOut(y_plus_vec_x_proj), FadeOut(y_min_vec_x_proj), FadeIn(up_edge),run_time=2)
        self.wait()
        self.play(FadeIn(y_plus_vectors), FadeIn(y_min_vectors), run_time=2)
        self.bring_to_front(delta_x)
        self.wait(2)

        delta_y_1 = MathTex(r"\Delta Fy =")
        delta_y_2 = MathTex(r"(", r"1+dy", r")", r"\times", r"2dx", r"-", r"(", r"1-dy", r")", r"\times", r"2dx", r"\over", r"4dxdy")
        delta_y_3 = MathTex(r"=1")
        delta_y = VGroup(delta_y_1, delta_y_2, delta_y_3)
        delta_y.arrange(RIGHT, buff=0.2)
        delta_y.scale(0.4).set_color(WHITE).move_to(axes.c2p(3.8, 1.8)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        delta_y_2[1].set_color(RED)  # RED -> PURE_RED
        delta_y_2[4].set_color(BLUE)      # PURE_BLUE -> BLUE
        delta_y_2[7].set_color(RED)  # RED -> PURE_RED
        delta_y_2[10].set_color(BLUE)     # PURE_BLUE -> BLUE
        delta_y_2[12].set_color(PURPLE)
        self.play(Write(delta_y))
        self.wait(2)

        self.play(FadeOut(y_plus_vec_y_proj), FadeOut(y_min_vec_y_proj), FadeOut(y_plus_vec), FadeOut(y_min_vec), FadeOut(y_plus_vectors),  
            FadeOut(y_min_vectors),run_time=2)
        divergence_label= MathTex(r"\nabla \cdot F(1,1)=\Delta Fx + \Delta Fy  = 2")
        divergence_label.scale(0.6).set_color(PURE_YELLOW).move_to(axes.c2p(3.8,0.8)).add_background_rectangle(color=BLACK, opacity=0.8, buff=0.1)
        self.play(Write(divergence_label),run_time=2)
        self.wait(3)


