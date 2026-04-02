from manim import *
import numpy as np

class ScalarField(ThreeDScene):
    def construct(self):
        # 1. 定義座標軸與純量場函數
        axes = ThreeDAxes(x_range=[-6, 6], y_range=[-3, 3], z_range=[-4, 4], x_length=10, y_length=5)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers()
        def get_val(x, y):
            # 一個簡單的山丘函數
            return x+y

        # 1. 建立函數定義標籤
        # 使用 MathTex 渲染標準數學公式
        func_label = MathTex(r"T(x, y) = x + y")
        func_label.scale(1.5)
        func_label.set_color(WHITE) # 設定為白色或其他醒目的顏色

        # 2. 定位在螢幕正上方
        # UP 代表螢幕頂端，再稍微往下偏移 (buff=0.3)
        func_label.to_edge(UP, buff=0.3)

        # 3. 鎖定在螢幕框架上 (HUD)
        self.add_fixed_in_frame_mobjects(func_label)

# --- 定義數值範圍與對應顏色 ---
        
        # 2. 建立數值網格
        grid_labels = VGroup()
        # arange只含下限不含上限，因此(-4, 5) 這是從 -4 ~ 4 的意思
        x_values = np.arange(-6, 7, 2)
        y_values = np.arange(-3, 4, 2)

        # 雙重for迴圈
        for x in x_values:
            for y in y_values:
                val = get_val(x, y)
                if x == 0 or y == 0: continue
                # 建立數字物件 DecimalNumber為專為數值運算設計的文字類別，比text又更廣應用
                # 第一格: 你要存取數值的對象(val)；num_decimal_places: 小數點位數；include_sign: 正數是否加正號
                num = DecimalNumber(val, num_decimal_places=1, include_sign=False)
                num.scale(1)
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

        # A. 顯示座標軸與所有網格數值
        self.add(axes)
        self.play(Write(grid_labels), run_time=2)
        self.wait(3)
