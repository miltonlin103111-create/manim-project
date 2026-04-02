from manim import *

class Day1Vector(Scene):
    def construct(self):
        # 1. 建立座標軸
        axes = Axes(
            x_range=[-12, 12, 1], 
            y_range=[-8, 8, 1], 
            x_length=10.5, 
            y_length=7
        )
        
	#2.建立向量
        vector = Arrow(
	    #3.座標映射到點
            start=axes.c2p(0, 0),
            end=axes.c2p(3, 2),
            buff=0,
            color=BLUE
        )

        self.play(Create(axes))
        self.play(GrowArrow(vector))
        self.wait(2)


