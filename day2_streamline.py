from manim import *
import numpy as np

class Day2StreamLine(Scene):
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

        # 3. 建立 StreamLines
        # 密度設為 0.4，避免線條過多導致渲染太慢
        stream_lines = StreamLines(
            vector_field_func,
            x_range=[-5, 5, 0.5],
            y_range=[-3, 3, 0.5],
            stroke_width=2,
            # 線條延伸
            padding=1,
            # 自動根據強度套色
            colors=[BLUE, RED, WHITE]
        )

        # 4. 播放動畫
        self.play(Create(axes))
        self.add(stream_lines)
        
        # start_animation 會讓流線動起來
        # warm_up=FALSE 讓動畫一開始就是流動狀態，不會從靜止開始
        stream_lines.start_animation(warm_up=FALSE, flow_speed=0.8, time_width=0.4)
        
        self.wait(8)