from manim import *
import numpy as np

class SphericalGradient(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-15 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4], x_length=8, y_length=8, z_length=8)  

        func_label = MathTex(r"\text{T}(x, y, z)\Rightarrow \text{T}(", r"r", r",", r" \theta", r",", r" \phi", r") \\"
            r"\nabla \text{T}= [\Delta T", r"_{r}", r" , \Delta T", r"_{\theta}", r" , \Delta T", r"_{\phi}", r"]", tex_environment="gather*" )
        func_label.scale(1.3).set_color(WHITE).move_to(axes.c2p(0, 0, 3)).add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1).rotate(self.camera.get_phi(), 
            axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
            
        func_label[2].set_color(ORANGE)
        func_label[4].set_color(PURPLE)
        func_label[6].set_color(GREEN)
        func_label[8].set_color(ORANGE)
        func_label[10].set_color(PURPLE)
        func_label[12].set_color(GREEN)
        self.add(func_label)
        self.wait(2)


        self.add(axes)      
        # 範圍設定
        r_min = 2
        theta_min = 30*DEGREES
        phi_min = 30*DEGREES
        
        # 修正：將 dr, d_theta, d_phi 提到最前面，確保後面的函數都讀得到
        dr = 0.98
        d_theta = 20 * DEGREES
        d_phi = 30 * DEGREES


        def get_sphere_surface(r_val):
            return Surface(
                lambda u, v: np.array([
                    r_val * np.sin(u) * np.cos(v),
                    r_val * np.sin(u) * np.sin(v), # 修正：原本漏了 np.sin(u)
                    r_val * np.cos(u)
                ]),
                u_range=[0, np.pi],
                v_range=[0, 2 * np.pi],
                fill_opacity=0.1
            )

        def get_sphere_surface_r(r):
            return Surface(
                lambda u, v: np.array([r * np.sin(u) * np.cos(v), r * np.sin(u) * np.sin(v), r * np.cos(u)]),
                u_range=[theta_min, theta_min+ d_theta],
                v_range=[phi_min, phi_min+ d_phi],
                resolution=(8, 8), fill_opacity=0.6,
            )

        outer_sphere = get_sphere_surface(r_min+1).set_fill(WHITE)

        def get_sphere_surface_theta(theta):
            return Surface(
                lambda u, v: np.array([u * np.sin(theta) * np.cos(v), u * np.sin(theta) * np.sin(v), u * np.cos(theta)]),
                u_range=[r_min, r_min+dr],
                v_range=[phi_min, phi_min+ d_phi],
                resolution=(8, 8), fill_opacity=0.6,
            )
        def get_sphere_surface_phi(phi):
            return Surface(
                lambda u, v: np.array([u * np.sin(v) * np.cos(phi), u * np.sin(v) * np.sin(phi), u * np.cos(v)]),
                u_range=[r_min, r_min+ dr],
                v_range=[theta_min, theta_min+ d_theta],
                resolution=(8, 8), fill_opacity=0.6,
            )

        block = VGroup(
            get_sphere_surface_r(r_min+ dr).set_fill(RED_A), get_sphere_surface_r(r_min).set_fill(RED_A), 
            get_sphere_surface_theta(theta_min+ d_theta).set_fill(PURPLE_E), get_sphere_surface_theta(theta_min).set_fill(PURPLE_A),        
            get_sphere_surface_phi(phi_min+ d_phi).set_fill(BLUE_A), get_sphere_surface_phi(phi_min).set_fill(BLUE_E)
        )

        # 修正 DashedLine 語法錯誤 (補逗號)
        line_UR= Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= WHITE,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_UL= Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= WHITE,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_DL=  Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min+d_theta)),
            buff= 0,
            color= WHITE,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_DR=  Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min+d_theta)),
            buff= 0,
            color= WHITE,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_PL=  DashedLine(
            start= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min+d_theta)),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_PR=  DashedLine(
            start= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min+d_theta)),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min+d_phi), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_PDL=  DashedLine(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5,
            stroke_width=2,
            stroke_opacity= 0.8
            )
        line_PDR=  DashedLine(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min+d_phi), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5,
            stroke_width=2,
            stroke_opacity= 0.8
            )

        dr_radius=  Line(
            start= axes.c2p((r_min) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                (r_min) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min) * np.cos(theta_min+d_theta/2)),
            end= axes.c2p((r_min+dr) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                (r_min+dr) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min+dr) * np.cos(theta_min+d_theta/2)),
            buff= 0,
            color= ORANGE,
            )
        dr_label= MathTex(r"dr").next_to(dr_radius).set_color(ORANGE).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        d_theta_arc = ArcBetweenPoints(
            start= axes.c2p(1 * np.sin(theta_min) * np.cos(phi_min), 
                1 * np.sin(theta_min) * np.sin(phi_min), 
                1 * np.cos(theta_min)),
            end= axes.c2p(1 * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                1 * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                1 * np.cos(theta_min+d_theta)),
            radius=1,
            color=PURPLE
        )
        d_theta_label= MathTex(r"d\theta").move_to(axes.c2p(1.5 * np.sin(theta_min+d_theta/2) * np.cos(phi_min), 
                1.5 * np.sin(theta_min+d_theta/2) * np.sin(phi_min), 
                1.5 * np.cos(theta_min+d_theta/2))).set_color(PURPLE).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        d_phi_arc = Arc(
            radius=1,
            start_angle= phi_min,                      
            angle= d_phi,          
            arc_center=ORIGIN,
            color= GREEN
        )
        d_phi_label= MathTex(r"d\phi").move_to(axes.c2p(                      
                1.5 * np.cos(phi_min+d_phi/2),
                1.5 * np.sin(phi_min+d_phi/2),
                0
            )).set_color(GREEN).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.play(Create(outer_sphere))
        self.play(FadeIn(block), FadeIn(line_UR), FadeIn(line_UL), FadeIn(line_DR), FadeIn(line_DL), FadeIn(line_PR), FadeIn(line_PL), FadeIn(line_PDL), FadeIn(line_PDR))
        self.play(Create(dr_radius), Write(dr_label), Create(d_theta_arc), Write(d_theta_label), Create(d_phi_arc), Write(d_phi_label))
        all_objects= VGroup(axes, block, line_UR, line_UL, line_DR, line_DL, line_PR, line_PL, line_PDL, line_PDR, dr_radius, dr_label, d_theta_arc, d_theta_label,  
            d_phi_arc, d_phi_label, outer_sphere)
        self.play(all_objects.animate.shift(LEFT * 1.3+ DOWN*1.3*(2+np.sqrt(3))+IN*0.7),func_label.animate.shift(RIGHT*0.85+ UP*0.85*(2+np.sqrt(3))))
        self.play(all_objects.animate.scale(1.5))
 
        r_plus_dot= Dot(color= PURE_BLUE).move_to(axes.c2p((r_min+dr) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                (r_min+dr) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min+dr) * np.cos(theta_min+d_theta/2))).rotate(theta_min+d_theta/2, axis= UP).rotate(phi_min+d_phi/2, axis= OUT)
        r_min_dot= Dot(color= PURE_RED).move_to(axes.c2p((r_min) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                (r_min) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min) * np.cos(theta_min+d_theta/2))).rotate(theta_min+d_theta/2, axis= UP).rotate(phi_min+d_phi/2, axis= OUT)
        delta_r_label_1 = MathTex(r"\Delta T", r"_{r}", r" =")
        delta_r_label_2 = MathTex(r"T(", r"r+dr", r",", r" \theta", r",", r" \phi", r")", r"-", r"T(", r"r", r",", r" \theta", r",", r" \phi", r")", r"\over",
            r"dr") 
        delta_r_label_3 = MathTex(r"=")
        delta_r_label_4 = MathTex(r"\partial T", r"\over", r"\partial", r"r")
        delta_r_label_1[1].set_color(ORANGE)
        delta_r_label_2[0].set_color(BLUE)
        delta_r_label_2[1].set_color(ORANGE)
        delta_r_label_2[3].set_color(PURPLE)
        delta_r_label_2[5].set_color(GREEN)
        delta_r_label_2[6].set_color(BLUE)
        delta_r_label_2[8].set_color(RED)
        delta_r_label_2[9].set_color(ORANGE)
        delta_r_label_2[11].set_color(PURPLE)
        delta_r_label_2[13].set_color(GREEN)
        delta_r_label_2[14].set_color(RED)
        delta_r_label_2[16].set_color(ORANGE)
        delta_r_label_4[3].set_color(ORANGE)
        delta_r_group = VGroup(
            delta_r_label_1, 
            delta_r_label_2, 
            delta_r_label_3, 
            delta_r_label_4
        )
        delta_r_group.arrange(RIGHT, buff=0.1)
        delta_r_group.scale(0.8).move_to(axes.c2p(1.45, 1.45*(2+np.sqrt(3)), 1.2)).add_background_rectangle(color=BLACK, opacity=0.6, 
            buff= 0.1).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        self.play(FadeIn(r_plus_dot), FadeIn(r_min_dot))
        self.wait(1)
        self.play(Write(delta_r_group),run_time=2)
        self.wait(2)
        self.play(FadeOut(r_plus_dot), FadeOut(r_min_dot), delta_r_label_2[0].animate.set_color(WHITE), delta_r_label_2[6].animate.set_color(WHITE), 
            delta_r_label_2[8].animate.set_color(WHITE), delta_r_label_2[14].animate.set_color(WHITE))

        theta_plus_dot= Dot(color= PURE_BLUE).move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min+d_theta) * np.cos(phi_min+d_phi/2), 
                (r_min+dr/2) * np.sin(theta_min+d_theta) * np.sin(phi_min+d_phi/2), 
                (r_min+dr/2) * np.cos(theta_min+d_theta))).rotate(theta_min+d_theta-90*DEGREES, axis= UP).rotate(phi_min+d_phi/2, axis= OUT)
        theta_min_dot= Dot(color= PURE_RED).move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                (r_min+dr/2) * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                (r_min+dr/2) * np.cos(theta_min))).rotate(theta_min-90*DEGREES, axis= UP).rotate(phi_min+d_phi/2, axis= OUT)
        delta_theta_label_1 = MathTex(r"\Delta T", r"_{\theta}", r" =")
        delta_theta_label_2 = MathTex(r"T(", r"r", r",", r" \theta+d\theta", r",", r" \phi", r")", r"-", r"T(", r"r", r",", r" \theta", r",", r" \phi", r")", r"\over",
            r"r", r"d\theta") 
        delta_theta_label_3 = MathTex(r"=")
        delta_theta_label_4 = MathTex(r"1", r"\over", r"r")
        delta_theta_label_5 = MathTex(r"\partial T", r"\over", r"\partial", r"\theta")
        delta_theta_label_1[1].set_color(PURPLE)
        delta_theta_label_2[0].set_color(BLUE)
        delta_theta_label_2[1].set_color(ORANGE)
        delta_theta_label_2[3].set_color(PURPLE)
        delta_theta_label_2[5].set_color(GREEN)
        delta_theta_label_2[6].set_color(BLUE)
        delta_theta_label_2[8].set_color(RED)
        delta_theta_label_2[9].set_color(ORANGE)
        delta_theta_label_2[11].set_color(PURPLE)
        delta_theta_label_2[13].set_color(GREEN)
        delta_theta_label_2[14].set_color(RED)
        delta_theta_label_2[16].set_color(ORANGE)
        delta_theta_label_2[17].set_color(PURPLE)
        delta_theta_label_4[2].set_color(ORANGE)
        delta_theta_label_5[3].set_color(PURPLE)
        delta_theta_group = VGroup(
            delta_theta_label_1, 
            delta_theta_label_2, 
            delta_theta_label_3, 
            delta_theta_label_4,
            delta_theta_label_5
        )
        delta_theta_group.arrange(RIGHT, buff=0.1)
        delta_theta_group.scale(0.8).move_to(axes.c2p(1.45, 1.45*(2+np.sqrt(3)), 0.2)).add_background_rectangle(color=BLACK, opacity=0.6, 
            buff= 0.1).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        theta_arc_path=  ArcBetweenPoints(
            start= theta_plus_dot.get_center(),
            end= theta_min_dot.get_center(),
            radius=r_min+dr/2,
            color=PURPLE
        )
        theta_arc_path_label= MathTex(r"r", r"d\theta")
        theta_arc_path_label[0].set_color(ORANGE)
        theta_arc_path_label[1].set_color(PURPLE)
        theta_arc_path_label.move_to(axes.c2p((r_min+dr-0.1) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                (r_min+dr-0.1) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min+dr-0.1) * np.cos(theta_min+d_theta/2))).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        self.play(FadeIn(theta_plus_dot), FadeIn(theta_min_dot))
        self.play(FadeIn(theta_arc_path), FadeIn(theta_arc_path_label), FadeOut(dr_label), FadeOut(dr_radius))
        self.wait(1)
        self.play(Write(delta_theta_group),run_time=2)
        self.wait(2)
        self.play(FadeOut(theta_plus_dot), FadeOut(theta_min_dot), FadeOut(theta_arc_path), FadeOut(theta_arc_path_label), 
            delta_theta_label_2[0].animate.set_color(WHITE), delta_theta_label_2[6].animate.set_color(WHITE), 
            delta_theta_label_2[8].animate.set_color(WHITE), delta_theta_label_2[14].animate.set_color(WHITE))


        phi_plus_dot= Dot(color= PURE_BLUE).move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi), 
                (r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi), 
                (r_min+dr/2) * np.cos(theta_min+d_theta/2))).rotate(90*DEGREES, axis= UP).rotate(90*DEGREES-phi_min-d_phi, axis= OUT)
        phi_min_dot= Dot(color= PURE_RED).move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.cos(phi_min), 
                (r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.sin(phi_min), 
                (r_min+dr/2) * np.cos(theta_min+d_theta/2))).rotate(90*DEGREES, axis= UP).rotate(90*DEGREES-phi_min, axis= OUT)
        delta_phi_label_1 = MathTex(r"\Delta T", r"_{\phi}", r" =")
        delta_phi_label_2 = MathTex(r"T(", r"r", r",", r" \theta", r",", r" \phi+d\phi", r")", r"-", r"T(", r"r", r",", r" \theta", r",", r" \phi", r")", r"\over",
            r"r", r"sin", r"\theta", r"d\phi") 
        delta_phi_label_3 = MathTex(r"=")
        delta_phi_label_4 = MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        delta_phi_label_5 = MathTex(r"\partial T", r"\over", r"\partial", r"\phi")
        delta_phi_label_1[1].set_color(GREEN)
        delta_phi_label_2[0].set_color(BLUE)
        delta_phi_label_2[1].set_color(ORANGE)
        delta_phi_label_2[3].set_color(PURPLE)
        delta_phi_label_2[5].set_color(GREEN)
        delta_phi_label_2[6].set_color(BLUE)
        delta_phi_label_2[8].set_color(RED)
        delta_phi_label_2[9].set_color(ORANGE)
        delta_phi_label_2[11].set_color(PURPLE)
        delta_phi_label_2[13].set_color(GREEN)
        delta_phi_label_2[14].set_color(RED)
        delta_phi_label_2[16].set_color(ORANGE)
        delta_phi_label_2[18].set_color(PURPLE)
        delta_phi_label_2[19].set_color(GREEN)
        delta_phi_label_4[2].set_color(ORANGE)
        delta_phi_label_4[4].set_color(PURPLE)
        delta_phi_label_5[3].set_color(GREEN)
        delta_phi_group = VGroup(
            delta_phi_label_1, 
            delta_phi_label_2, 
            delta_phi_label_3, 
            delta_phi_label_4,
            delta_phi_label_5
        )
        delta_phi_group.arrange(RIGHT, buff=0.1)
        delta_phi_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), -0.8)).add_background_rectangle(color=BLACK, opacity=0.6, 
            buff= 0.1).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        phi_arc_path=  ArcBetweenPoints(
            start= phi_plus_dot.get_center(),
            end= phi_min_dot.get_center(),
            radius=r_min+dr,
            color=GREEN
        )
        phi_arc_path_label= MathTex(r"r",r"sin", r"\theta", r"d\phi")
        phi_arc_path_label[0].set_color(ORANGE)
        phi_arc_path_label[2].set_color(PURPLE)
        phi_arc_path_label[3].set_color(GREEN)
        phi_arc_path_label.scale(1.2).move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2)*1.5, 
                (r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2)*1.5, 
                (r_min+dr/2) * np.cos(theta_min+d_theta/2))).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        line_sup_l=  DashedLine(
            start= axes.c2p(0, 0, (r_min+dr/2) * np.cos(theta_min+d_theta/2)),
            end= phi_min_dot.get_center(),
            buff= 0,
            color= ORANGE,
            dashed_ratio=0.5,
            stroke_width=4,
            stroke_opacity= 0.8
            )
        line_sup_r= DashedLine(
            start= axes.c2p(0, 0, (r_min+dr/2) * np.cos(theta_min+d_theta/2)),
            end= phi_plus_dot.get_center(),
            buff= 0,
            color= ORANGE,
            dashed_ratio=0.5,
            stroke_width=4,
            stroke_opacity= 0.8
            )
        line_sup_label= MathTex(r"r",r"sin", r"\theta")
        line_sup_label[0].set_color(ORANGE)
        line_sup_label[2].set_color(PURPLE)
        line_sup_label.move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.cos(phi_min)/2, 
                (r_min+dr/2) * np.sin(theta_min+d_theta/2) * np.sin(phi_min)/2, 
                (r_min+dr/2) * np.cos(theta_min+d_theta/2)-0.2)).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        r_sup= Line(
            start= axes.c2p(0, 0, 0),
            end= phi_min_dot.get_center(),
            buff= 0,
            color= ORANGE,
            stroke_width=3,
            stroke_opacity= 1
            )
        r_sup_label= MathTex(r"r")
        r_sup_label.set_color(ORANGE).move_to(axes.c2p((r_min+dr) * np.sin(theta_min+d_theta/2) * np.cos(phi_min)/2, 
                (r_min+dr) * np.sin(theta_min+d_theta/2) * np.sin(phi_min)/2, 
                (r_min+dr) * np.cos(theta_min+d_theta/2)/2-0.2)).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        theta_sup_arc=  ArcBetweenPoints(
            start= axes.c2p(0.8 * np.sin(theta_min+d_theta/2) * np.cos(phi_min), 
                0.8 * np.sin(theta_min+d_theta/2) * np.sin(phi_min), 
                0.8 * np.cos(theta_min+d_theta/2)),
            end= axes.c2p(0, 0, 0.8),
            radius= 0.8,
            color=PURPLE
        )
        theta_sup_label= MathTex(r"\theta")
        theta_sup_label.set_color(PURPLE).move_to(axes.c2p(1.1 * np.sin((theta_min+d_theta/2)/2) * np.cos(phi_min), 
                1.1 * np.sin((theta_min+d_theta/2)/2) * np.sin(phi_min), 
                1.1 * np.cos((theta_min+d_theta/2)/2))).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)


        self.play(FadeIn(phi_plus_dot), FadeIn(phi_min_dot))
        self.play(FadeIn(phi_arc_path))
        self.play(FadeOut(line_UR), FadeOut(line_UL), FadeOut(line_DR), FadeOut(line_DL), FadeOut(d_theta_label), FadeOut(d_theta_arc), d_phi_label.animate.scale(0.8))
        self.play(Create(r_sup), FadeIn(r_sup_label))
        self.play(Create(theta_sup_arc), FadeIn(theta_sup_label))
        self.play(Create(line_sup_l), Create(line_sup_r), FadeIn(line_sup_label))
        self.play(
            d_phi_arc.animate.scale(0.6).move_to(axes.c2p(
                0.6*np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                0.6 * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                (r_min+dr/2)* np.cos(theta_min+d_theta/2))), 
            d_phi_label.animate.scale(0.8).move_to(axes.c2p(1*np.sin(theta_min+d_theta/2) * np.cos(phi_min+d_phi/2), 
                1 * np.sin(theta_min+d_theta/2) * np.sin(phi_min+d_phi/2), 
                1.1 *(r_min+dr/2)* np.cos(theta_min+d_theta/2))))
        self.play(Write(phi_arc_path_label))
        self.wait(1)
        self.play(Write(delta_phi_group),run_time=2)
        self.wait(3)
        self.play(delta_phi_label_2[0].animate.set_color(WHITE), delta_phi_label_2[6].animate.set_color(WHITE), 
            delta_phi_label_2[8].animate.set_color(WHITE), delta_phi_label_2[14].animate.set_color(WHITE))


        all_objects_s= VGroup(phi_plus_dot, phi_min_dot, phi_arc_path, r_sup, r_sup_label, theta_sup_arc, theta_sup_label, line_sup_l, line_sup_r, line_sup_label, 
            phi_arc_path_label, func_label)
        self.play(FadeOut(all_objects), FadeOut(all_objects_s))
        all_labels= VGroup( delta_r_group, delta_theta_group, delta_phi_group)
        self.play(all_labels.animate.shift(LEFT*0.85+ DOWN*0.85*(2+np.sqrt(3))+OUT*1.5))
        self.wait(2)

        con_label_1= MathTex(r"\nabla \text{T}= [")
        con_label_2= MathTex(r"\partial T", r"\over", r"\partial", r"r")
        con_label_3= MathTex(r",")
        con_label_4= MathTex(r"1", r"\over", r"r")
        con_label_5= MathTex(r"\partial T", r"\over", r"\partial", r"\theta")
        con_label_6= MathTex(r",")
        con_label_7= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        con_label_8= MathTex(r"\partial T", r"\over", r"\partial", r"\phi")
        con_label_9= MathTex(r"]")
        con_label_2[3].set_color(ORANGE)
        con_label_4[2].set_color(ORANGE)
        con_label_5[3].set_color(PURPLE)
        con_label_7[2].set_color(ORANGE)
        con_label_7[4].set_color(PURPLE)
        con_label_8[3].set_color(GREEN)

        con_group= VGroup(con_label_1, con_label_2, con_label_3, con_label_4, con_label_5, con_label_6, con_label_7, con_label_8, con_label_9)
        con_group.arrange(RIGHT, buff=0.2)
        con_label_3.align_to(con_label_2, DOWN)
        con_label_6.align_to(con_label_5, DOWN)
        con_group.scale(1.5).move_to([0, 0, -2.5]).add_background_rectangle(color=BLACK, opacity=0.6, 
            buff= 0.2).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.play(Write(con_group))
        self.wait(3)

