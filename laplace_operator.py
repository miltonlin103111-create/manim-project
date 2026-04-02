from manim import *
import numpy as np

class LaplaceOperator(MovingCameraScene):
    def construct(self):
        case_label = MathTex(r"\text{if } \nabla \cdot(\nabla T) > 0 \\ \text{then } \nabla T \text{ looks like}", tex_environment="gather*")        
        case_label.scale(1.3).set_color(YELLOW).to_edge(UP, buff=0.3).add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1)
        self.add(case_label)
        self.wait(1)
 
        case1_dot= Dot(color= WHITE).move_to([-3,0,0])
        case2_dot= Dot(color= WHITE).move_to([3,0,0])
        self.add(case1_dot, case2_dot)
        self.wait(1)

        case1_vector1_1= Arrow(
            start= [-4.2,0.5,0],
            end= [-3.2,0.5,0],
            buff=0,
            color= BLUE
            )
        case1_vector1_2= Arrow(
            start= [-4.2,0,0],
            end= [-3.2,0,0],
            buff=0,
            color= BLUE
            )
        case1_vector1_3= Arrow(
            start= [-4.2,-0.5,0],
            end= [-3.2,-0.5,0],
            buff=0,
            color= BLUE
            )
        case1_vector2_1= Arrow(
            start= [-2.8,0.5,0],
            end= [-0.8,0.5,0],
            buff=0,
            color= RED
            )
        case1_vector2_2= Arrow(
            start= [-2.8,0,0],
            end= [-0.8,0,0],
            buff=0,
            color= RED
            )
        case1_vector2_3= Arrow(
            start= [-2.8,-0.5,0],
            end= [-0.8,-0.5,0],
            buff=0,
            color= RED
            )
        box1= Rectangle(width=5, height= 5).set_stroke(WHITE, 2).move_to([-2.5,-1,0])
        self.play(Create(box1))
        self.play(FadeIn(case1_vector1_1), FadeIn(case1_vector1_2), FadeIn(case1_vector1_3), FadeIn(case1_vector2_1), FadeIn(case1_vector2_2), FadeIn(case1_vector2_3))
  

        case2_vector1_1= Arrow(
            start= [3, 0.2, 0],
            end= [3, 1, 0],
            buff=0,
            color= RED
            )
        case2_vector1_2= Arrow(
            start= [3.173,0.1,0],
            end= [3.866,0.5,0],
            buff=0,
            color= RED
            )
        case2_vector1_3= Arrow(
            start= [3.173,-0.1,0],
            end= [3.866,-0.5,0],
            buff=0,
            color= RED
            )
        case2_vector1_4= Arrow(
            start= [3, -0.2, 0],
            end= [3, -1, 0],
            buff=0,
            color= RED
            )
        case2_vector1_5= Arrow(
            start= [2.827,-0.1,0],
            end= [2.134,-0.5,0],
            buff=0,
            color= RED
            )
        case2_vector1_6= Arrow(
            start= [2.827,0.1,0],
            end= [2.134,0.5,0],
            buff=0,
            color= RED
            )
        box2= Rectangle(width=5, height= 5).set_stroke(WHITE, 2).move_to([3,-1,0])
        self.play(Create(box2))
        self.play(GrowArrow(case2_vector1_1), GrowArrow(case2_vector1_2), GrowArrow(case2_vector1_3), GrowArrow(case2_vector1_4), GrowArrow(case2_vector1_5),  
            GrowArrow(case2_vector1_6), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate.set(width=6).move_to([-2.5, 0, 0]),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        self.wait(2)

        case1_label= MathTex(r"\text{value of T may look like}")
        case1_label.scale(0.6).set_color(YELLOW).move_to([-2.5, 1.2, 0])
        case1_dots_1= MathTex(r"0\\0\\0")
        case1_dots_1.scale(0.8).set_color(BLUE).move_to([-4, 0, 0])
        case1_dots_2= MathTex(r"1\\1\\1")
        case1_dots_2.scale(0.8).set_color(WHITE).move_to([-3, 0, 0])
        case1_dots_3= MathTex(r"10\\10\\10")
        case1_dots_3.scale(0.8).set_color(RED).move_to([-2, 0, 0])

        self.play(Write(case1_label))
        self.wait()
        self.play(case1_vector1_1.animate.set_opacity(0.6), case1_vector1_2.animate.set_opacity(0.6), case1_vector1_3.animate.set_opacity(0.6), 
            case1_vector2_1.animate.set_opacity(0.6), case1_vector2_2.animate.set_opacity(0.6), case1_vector2_3.animate.set_opacity(0.6), 
            case1_dot.animate.set_opacity(0.6), run_time=1)
        self.play(FadeIn(case1_dots_1), FadeIn(case1_dots_2), FadeIn(case1_dots_3), run_time=1)
        self.wait(3)

        def func1(t):
            x = t 
            y = 0.5* np.exp(t)  
            return np.array([x, y, 0])
        path1 = ParametricFunction(
            func1,
            t_range=[-1.3, 1.3],
            stroke_width=5,
          )
 
        path1.move_to([-4, -3.2, 0], aligned_edge=DL).set_color_by_gradient([PURE_RED,WHITE, PURE_BLUE])
 
        path1_label= MathTex(r"\text{graph}")
        path1_label.scale(0.6).set_color(YELLOW).move_to([-2.5, -1.2, 0])

        self.play(self.camera.frame.animate.move_to([-2.5, -2, 0]),
            run_time=2,
            rate_func=smooth)
        self.wait(1)
        self.play(Write(path1_label))
        self.wait(1)
        self.play(Create(path1))
        self.wait(3)       
        self.play(self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        self.wait(2)
        self.play(self.camera.frame.animate.set(width=6).move_to([3, 0, 0]),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑

        case2_label= MathTex(r"\text{value of T may look like}")
        case2_label.scale(0.6).set_color(YELLOW).move_to([3, 1.2, 0])
        case2_dots_0= MathTex(r"0")
        case2_dots_0.scale(0.8).set_color(BLUE).move_to([3, 0, 0])
        case2_dots_1= MathTex(r"10")
        case2_dots_1.scale(0.8).set_color(RED).move_to([3, 0.6 , 0])
        case2_dots_2= MathTex(r"10")
        case2_dots_2.scale(0.8).set_color(RED).move_to([3.52, 0.3, 0])
        case2_dots_3= MathTex(r"10")
        case2_dots_3.scale(0.8).set_color(RED).move_to([3.52, -0.3, 0])
        case2_dots_4= MathTex(r"10")
        case2_dots_4.scale(0.8).set_color(RED).move_to([3, -0.6, 0])
        case2_dots_5= MathTex(r"10")
        case2_dots_5.scale(0.8).set_color(RED).move_to([2.48, -0.3, 0])
        case2_dots_6= MathTex(r"10")
        case2_dots_6.scale(0.8).set_color(RED).move_to([2.48, 0.3, 0])

        self.play(Write(case2_label))
        self.wait()
        self.play(case2_vector1_1.animate.set_opacity(0.6), case2_vector1_2.animate.set_opacity(0.6), case2_vector1_3.animate.set_opacity(0.6), 
            case2_vector1_4.animate.set_opacity(0.6), case2_vector1_5.animate.set_opacity(0.6), case2_vector1_6.animate.set_opacity(0.6), 
            case2_dot.animate.set_opacity(0.6), run_time=1)
        self.play(FadeIn(case2_dots_0), FadeIn(case2_dots_1), FadeIn(case2_dots_2), FadeIn(case2_dots_3), FadeIn(case2_dots_4), FadeIn(case2_dots_5), 
            FadeIn(case2_dots_6), run_time=1)
        self.wait(3)

        def func2(t):
            x = t 
            y = 0.8 * t**2  
            return np.array([x, y, 0])

        path2= ParametricFunction(func2, t_range=[-1.3, 1.3], stroke_width=5)
        path2.move_to([3, -3.2, 0], aligned_edge=DOWN)
        path2.set_sheen_direction([0, 1, 0]).set_color([BLUE, RED]) 

        path2_label= MathTex(r"\text{graph}")
        path2_label.scale(0.6).set_color(YELLOW).move_to([3, -1.2, 0])

        self.play(self.camera.frame.animate.move_to([3, -2, 0]),
            run_time=2,
            rate_func=smooth)
        self.wait(1)
        self.play(Write(path2_label))
        self.wait(1)
        self.play(Create(path2))
        self.wait(3)       
        self.play(self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN),
            run_time=2,
            rate_func=smooth) # 讓移動過程平滑
        self.wait(3)
