from manim import *
import numpy as np

class StreamLine(Scene):
    def construct(self):
        # 1. 建立座標軸 
        axes = Axes(
            x_range=[-12, 12, 1], 
            y_range=[-8, 8, 1], 
            x_length=10.5, 
            y_length=7
        )

        # 2. 定義向量函數 (格子渦流)
        def vector_field_func(point):
            x, y, _ = point
            # np.array是生成一個陣列，這裡用來存放向量場
            return np.array([np.sin(y), -np.cos(x), 0])

        func_label = MathTex(r"F [ Fx, Fy ] = [ sin(y), -cos(x) ]")
        func_label.scale(1.3)
        func_label.set_color(YELLOW) # 設定為白色或其他醒目的顏色
        func_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        func_label.to_edge(UP, buff=0.3)
        self.add(func_label)


        # 3. 建立向量場物件
        field = ArrowVectorField(
            vector_field_func,
            x_range=[-5.25, 5.25, 0.7],
            y_range=[-3.5, 3.5, 0.7],
            
            length_func=lambda norm: 0.6 * norm, 
            stroke_width=1, 
            opacity=0.5
        )

        # --- 關鍵修改：根據向量大小設定顏色漸變 ---
        
        max_magnitude = np.linalg.norm([0,1.57]) 

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

        # 3. 建立 StreamLines
        # 密度設為 0.4，避免線條過多導致渲染太慢
        stream_lines = StreamLines(
            vector_field_func,
            x_range=[-5.25, 5.25, 0.4],
            y_range=[-3.5, 3.5, 0.4],
            stroke_width=3,
            # 線條延伸
            padding=1,
            # 自動根據強度套色
            colors=[BLUE, RED, WHITE]
        )

        # 4. 播放動畫
        self.add(axes, field, stream_lines)
          # start_animation 會讓流線動起來
        # warm_up=FALSE 讓動畫一開始就是流動狀態，不會從靜止開始
        stream_lines.start_animation(warm_up=True, flow_speed=1, time_width=0.6)
        self.bring_to_front(func_label,)
        self.wait(10)