from manim import *
import numpy as np

class Day2VectorField(Scene):
    def construct(self):
        # 1. 建立座標軸
        axes = Axes(x_range=[-12, 12, 1], y_range=[-8, 8, 1], x_length=10.5, y_length=7)

        # 2. 定義向量函數
        def vector_field_func(point):
            x, y, _ = point
            return np.array([np.sin(y),-np.cos(x), 0])

        # 3. 建立向量場物件
        field = ArrowVectorField(
            vector_field_func,
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            
            length_func=lambda norm: 0.6 * norm, 
            stroke_width=2, #稍微加粗一點比較好看
        )

        # --- 關鍵修改：根據向量大小設定顏色漸變 ---
        # 估算最大向量大小 (在x=0,y=pi/2)
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

        # 4. 播放動畫
        self.play(Create(axes))
        self.play(Create(field))
        self.wait(2)

