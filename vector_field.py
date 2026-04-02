from manim import *
import numpy as np

class VectorField(Scene):
    def construct(self):
        # 1. 建立座標軸
        axes = Axes(x_range=[-6, 6, 1], y_range=[-3, 3, 1], x_length=12, y_length=6)
        

        # 2. 定義向量函數
        def vector_field_func(point):
            x, y, _ = point
            return np.array([x+y,y, 0])

        func_label = MathTex(r"F[Fx, Fy] = [x+y, y]")
        func_label.scale(1.3)
        func_label.set_color(YELLOW) # 設定為白色或其他醒目的顏色
        func_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)

        # 2. 定位在螢幕正上方
        # UP 代表螢幕頂端，再稍微往下偏移 (buff=0.3)
        func_label.to_edge(UP, buff=0.3)
        # 3. 鎖定在螢幕框架上 (HUD)
        self.add(func_label)


        # 3. 建立向量場物件
        field = ArrowVectorField(
            vector_field_func,
            x_range=[-3, 3, 0.5],
            y_range=[-1, 1, 0.5],
            
            length_func=lambda norm: norm, 
            stroke_width=2, 
            opacity=0.7
        )

        # --- 關鍵修改：根據向量大小設定顏色漸變 ---
        
        max_magnitude = np.linalg.norm([5,2]) 

        for vector in field:
            # 獲取箭頭的起始點
            point = vector.get_start()
            # 計算該點的向量數值大小
            magnitude = np.linalg.norm(vector_field_func(point))
            
            # 計算顏色比例 (0 ~ 1)，使用 clip 防止超過範圍
            alpha = np.clip(magnitude / max_magnitude, 0, 1)
            
            # 設定顏色：從小(BLUE) 到 大(RED) 漸變
            # 你也可以改成 colors=[YELLOW, RED] 等等
            vector.set_color(interpolate_color(BLUE, RED, alpha))
        # ---------------------------------------

        target1 = Dot(color=PINK).move_to(axes.c2p(1,1))
        target1_label = MathTex(r"(1,1)")
        target1_label.scale(0.6)
        target1_label.set_color(PINK) 
        target1_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        target1_label.next_to(target1, DOWN)

        target2 = Dot(color=GREEN).move_to(axes.c2p(0,-1))
        target2_label = MathTex(r"(0,-1)")
        target2_label.scale(0.6)
        target2_label.set_color(GREEN) 
        target2_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        target2_label.next_to(target2, UP)

        vector1 = Arrow(
            start=axes.c2p(1,1),
            end=axes.c2p(3, 2),
            buff=0,
            color=PINK
        )
        vector1_label= MathTex(r"[2,1]").scale(0.6).set_color(PINK).next_to(axes.c2p(3,2), UP)
        
        vector2 = Arrow(
	    #3.座標映射到點
            start=axes.c2p(0,-1),
            end=axes.c2p(-1,-2),
            buff=0,
            color=GREEN
        )
        vector2_label= MathTex(r"[-1,-1]").scale(0.6).set_color(GREEN).next_to(axes.c2p(-1,-2), DOWN)


        # 4. 播放動畫
        self.play(Create(axes))
        self.play(Create(field))
        self.bring_to_front(func_label)
        self.wait(2)

        self.add(target1)
        self.play(Write(target1_label))
        self.wait(1)
        self.play(GrowArrow(vector1))
        self.play(Write(vector1_label))
        self.wait(2)

        self.add(target2)
        self.play(Write(target2_label))
        self.wait(1)
        self.play(GrowArrow(vector2))
        self.play(Write(vector2_label))
        self.wait(2)

