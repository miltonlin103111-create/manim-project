from manim import *
import numpy as np

class Mountain(ThreeDScene):
    def construct(self):
        # 1. 定義座標軸與純量場函數
        axes = ThreeDAxes(x_range=[-5, 5], y_range=[-3, 3], z_range=[-8, 8], x_length=10, y_length=6, z_length=16)
        def get_val(x, y):
            # 一個簡單的山丘函數
            return x+y

        func_label = MathTex(r"T(x, y) = x + y")
        func_label.scale(1.3)
        func_label.set_color(YELLOW) # 設定為白色或其他醒目的顏色

        # 2. 定位在螢幕正上方
        # UP 代表螢幕頂端，再稍微往下偏移 (buff=0.3)
        func_label.to_edge(UP, buff=0.3)
        func_label.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        # 3. 鎖定在螢幕框架上 (HUD)
        self.add_fixed_in_frame_mobjects(func_label)


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

                num.target_z = val 
                grid_labels.add(num)

        # 3. 建立曲面(u,v為參數式，可直接當成x,y)
        mountain = Surface(
            lambda u, v: axes.c2p(u, v, get_val(u, v)),
            u_range=[-8, 8],
            v_range=[-5, 5],
            resolution=(30, 30),
            fill_opacity=0.6
        )
        mountain.set_fill_by_value(axes=axes, colors=[(PURE_BLUE, -8), (PURE_RED, 8)])

        # 4.算出梯度向量
        def get_gradient(point):
            x, y, z = axes.p2c(point) # 轉回數學座標
            f_val = get_val(x, y)
            # 梯度公式：df/dx = 1, df/dy = 1
            return np.array([1, 1, 0])
        
        initial_p= np.array([2, 1, 0])
        target = Dot(color=GOLD).move_to(axes.c2p(*initial_p)) # 初始點
        
	
        # 建立梯度向量
        def scalor_vector() : 
            p= axes.p2c(target.get_center())
            return Arrow(
            start= axes.c2p(p[0]-0.5, p[1]-0.5, p[2]),
            end= axes.c2p(p[0]+0.5, p[1]+0.5, p[2]),
            buff=0,
            color=GOLD
            )
        vector= always_redraw(scalor_vector)
        
        # 標示梯度
        gradient_label = always_redraw(lambda:
            MathTex(
                fr"\nabla T({axes.p2c(target.get_center())[0]:.1f}, "
                fr"{axes.p2c(target.get_center())[1]:.1f}) = [1, 1, 0]"
            ).arrange(RIGHT, aligned_edge=DOWN).scale(0.8).next_to(target, LEFT).set_color(GOLD).add_background_rectangle(color=BLACK, opacity=0.6, buff=
            0.1).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        )
               
     
        
        # --- 動畫播放 ---
        
        # A. 顯示座標軸與所有網格數值
        self.add(axes)
        self.play(Write(grid_labels), run_time=2)
        self.add(target)
        self.wait()
        self.play(GrowArrow(vector))
        self.play(Write(gradient_label))
        self.wait(2)

        # B. 轉動視角到 3D
        self.move_camera(phi=75 * DEGREES, theta=-95 * DEGREES, run_time=2)
        
        self.wait()

        # C. 關鍵動作：讓數字「升到」對應的高度
        # 我們遍歷剛剛建立的每個數字，讓它們移動到 (x, y, z)
        animations = []
        for num in grid_labels:
            # 獲取它目前的 x, y
            curr_pos = axes.p2c(num.get_center())
            # 移動到正確的 3D 高度
            animations.append(
                num.animate.move_to(axes.c2p(curr_pos[0], curr_pos[1], num.target_z))
            )
       
        # *animations前面有*，代表全部動畫一起執行
        self.play(*animations, run_time=2)
        self.wait()

        # D. 最後顯現完整的曲面
        self.play(Create(mountain))
        self.wait()

        # E. 向量變成平行斜面
        self.play(target.animate.move_to(axes.c2p(initial_p[0], initial_p[1], get_val(initial_p[0], initial_p[1]))), run_time=2)
        self.wait()
        
        # --- 建立斜面向量 (金色：真正的 3D 切線方向) ---
        def get_dynamic_vector3d():
            # 1. 取得目前點的數學座標
            curr_math = axes.p2c(target.get_center())
            x, y, z = curr_math
            
            # 2. 取得數學上的梯度
            grad = get_gradient(curr_math)
            mag_sq = np.linalg.norm(grad)**2 # z 軸的增量為梯度的平方
            
            # 3. 回傳箭頭 (起點與終點都必須轉換成螢幕座標)
            return Arrow(
                start = axes.c2p(x, y, z), # 這是重點！必須用 c2p 轉回去
                end = axes.c2p(
                    x + grad[0], 
                    y + grad[1], 
                    z + mag_sq 
                ),
                buff=0,
                color=GREEN,
                stroke_width=6
            )

        vector3D = always_redraw(get_dynamic_vector3d) 
        # --- 建立動態梯度數值標籤 ---
        self.play(GrowArrow(vector3D))
        self.wait(2)

        self.play(target.animate.move_to(axes.c2p(-2, 1, get_val(-2, 1))), run_time=5)
        self.wait()
