from manim import *
import numpy as np

class SphericalDivergence(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-15 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4], x_length=8, y_length=8, z_length=8)  

        func_label_1 = MathTex(r"\text{F}[F_{x}, F_{y}, F_{z}]\Rightarrow \text{F}[", r"F_{r}", r",", r"F_{\theta}", r",", r"F_{\phi}", r"]")
        func_label_2= MathTex(r"\nabla \cdot \text{F}= ", r"\Delta ", r"F_{r}", r" +",r" \Delta ", r"F_{\theta}", r" +", r" \Delta ", r"F_{\phi}")

        func_label_1[1].set_color(ORANGE)
        func_label_1[3].set_color(PURPLE)
        func_label_1[5].set_color(GREEN)
        func_label_2[2].set_color(ORANGE)
        func_label_2[5].set_color(PURPLE)
        func_label_2[7].set_color(GREEN)

        func_label= VGroup(func_label_1, func_label_2)
        func_label.arrange(DOWN, buff=0.1)
        func_label.scale(1).move_to(axes.c2p(0, 0, 3)).add_background_rectangle(color=BLACK, opacity=0.6, buff=0.1).rotate(self.camera.get_phi(), 
            axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

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
        outer_sphere = get_sphere_surface(r_min+1).set_fill(WHITE)

        def get_sphere_surface_r(r):
            return Surface(
                lambda u, v: np.array([r * np.sin(u) * np.cos(v), r * np.sin(u) * np.sin(v), r * np.cos(u)]),
                u_range=[theta_min, theta_min+ d_theta],
                v_range=[phi_min, phi_min+ d_phi],
                resolution=(8, 8),
            )
        r_surf_plus= get_sphere_surface_r(r_min+ dr).set_fill(RED_A).set_opacity(0.4)
        r_surf_min= get_sphere_surface_r(r_min).set_fill(RED_A).set_opacity(0.4)

        def get_sphere_surface_theta(theta):
            return Surface(
                lambda u, v: np.array([u * np.sin(theta) * np.cos(v), u * np.sin(theta) * np.sin(v), u * np.cos(theta)]),
                u_range=[r_min+dr, r_min],
                v_range=[phi_min, phi_min+ d_phi],
                resolution=(8, 8),
            )
        theta_surf_plus= get_sphere_surface_theta(theta_min+ d_theta).set_fill(PURPLE_E).set_opacity(0.4)
        theta_surf_min= get_sphere_surface_theta(theta_min).set_fill(PURPLE_E).set_opacity(0.4)

        def get_sphere_surface_phi(phi):
            return Surface(
                lambda u, v: np.array([u * np.sin(v) * np.cos(phi), u * np.sin(v) * np.sin(phi), u * np.cos(v)]),
                u_range=[r_min, r_min+ dr],
                v_range=[theta_min, theta_min+ d_theta],
                resolution=(8, 8),
            )
        phi_surf_plus= get_sphere_surface_phi(phi_min+ d_phi).set_fill(GREEN_A).set_opacity(0.4)
        phi_surf_min= get_sphere_surface_phi(phi_min).set_fill(GREEN_A).set_opacity(0.4)

        block = VGroup(
            r_surf_plus, r_surf_min, 
            theta_surf_plus, theta_surf_min,        
            phi_surf_plus, phi_surf_min
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
            stroke_opacity= 0.6
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
            stroke_opacity= 0.6
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
        dr_label= MathTex(r"dr")
        dr_label.next_to(dr_radius).scale(0.6).set_color(ORANGE).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        d_theta_arc = ArcBetweenPoints(
            start= axes.c2p(1 * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                1 * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                1 * np.cos(theta_min+d_theta)),
            end= axes.c2p(1 * np.sin(theta_min) * np.cos(phi_min), 
                1 * np.sin(theta_min) * np.sin(phi_min), 
                1 * np.cos(theta_min)),
            radius=0.8,
            color=PURPLE
        )
        d_theta_label= MathTex(r"d\theta")
        d_theta_label.move_to(axes.c2p(1.5 * np.sin(theta_min+d_theta/2) * np.cos(phi_min), 
                1.5 * np.sin(theta_min+d_theta/2) * np.sin(phi_min), 
                1.5 * np.cos(theta_min+d_theta/2))).set_color(PURPLE).scale(0.6).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES,  
                axis=OUT)

        d_phi_arc = Arc(
            radius=0.8,
            start_angle= phi_min,                      
            angle= d_phi,          
            arc_center=ORIGIN,
            color= GREEN
        )
        d_phi_label= MathTex(r"d\phi").move_to(axes.c2p(                      
                1.5 * np.cos(phi_min+d_phi/2),
                1.5 * np.sin(phi_min+d_phi/2),
                0
            )).scale(0.6).set_color(GREEN).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)


        self.play(Create(outer_sphere))
        self.play(FadeIn(block), FadeIn(line_UR), FadeIn(line_UL), FadeIn(line_DR), FadeIn(line_DL), FadeIn(line_PR), FadeIn(line_PL), FadeIn(line_PDL), FadeIn(line_PDR))
        self.play(Create(dr_radius), Write(dr_label), Create(d_theta_arc), Write(d_theta_label), Create(d_phi_arc), Write(d_phi_label))
        all_objects= VGroup(axes, block, line_UR, line_UL, line_DR, line_DL, line_PR, line_PL, line_PDL, line_PDR, dr_radius, dr_label, d_theta_arc, d_theta_label,  
            d_phi_arc, d_phi_label, outer_sphere)
        self.play(all_objects.animate.shift(LEFT * 1.6+ DOWN*1.6*(2+np.sqrt(3))+IN*3), func_label.animate.scale(0.8),
            func_label.animate.shift(RIGHT*0.6+ UP*0.6*(2+np.sqrt(3))))
        self.play(all_objects.animate.scale(1.5))
        self.play(FadeOut(outer_sphere))
        
        r_plus_surf= get_sphere_surface_r(r_min+dr).set_fill(BLUE).scale(1.5).match_points(block[0])
        r_min_surf= get_sphere_surface_r(r_min).set_fill(RED).scale(1.5).match_points(block[1])
        theta_plus_surf=  get_sphere_surface_theta(theta_min+ d_theta).scale(1.5).set_fill(BLUE).match_points(block[2])
        theta_min_surf=  get_sphere_surface_theta(theta_min).set_fill(RED).scale(1.5).match_points(block[3])
        phi_plus_surf= get_sphere_surface_phi(phi_min+ d_phi).set_fill(BLUE).scale(1.5).match_points(block[4])
        phi_min_surf= get_sphere_surface_phi(phi_min).set_fill(RED).scale(1.5).match_points(block[5])

        delta_r_label_1 = MathTex(r"\Delta", r"F_{r}", r" = ")
        delta_r_label_2 = MathTex(r"F_{r}(r+dr)", r"\times", r"Area(", r"r+dr", r")", r"-", r"F_{r}(r)", r"\times", r"Area(", r"r", r")", r"\over", r"volume")
        area_r_plus_label= MathTex(r"Area(", r"r+dr", r")", r" = ")
        area_r_min_label= MathTex(r"Area(", r"r", r")", r" = ")
        volume_r_label = MathTex(r"volume = ", r"(", r"\frac{4}{3}", r"\pi(", r"r+dr", r")^{3} - ", r"\frac{4}{3}", r"\pi", r"r", r"^{3}) \times \alpha = ")
        area_r_plus_eff= MathTex(r" 4\pi(", r"r+dr", r")^{2}", r"\times", r"\alpha")
        area_r_min_eff= MathTex(r" 4\pi", r"r", r"^{2}", r"\times", r"\alpha")
        volume_r_eff= MathTex(r"4\pi", r"r", r"^{2} d", r"r", r"\times", r"\alpha")
        delta_r_label_3 = MathTex(r"F_{r}(r+dr)", r"\times", r"4\pi(", r"r+dr", r")^{2}  \alpha", r"-", r"F_{r}(r)", r"\times",  r"4\pi", r"r", 
            r"^{2}  \alpha", r"\over",r"4\pi", r"r", r"^{2} d", r"r", r"\times \alpha")
        equal_r_label= MathTex(r"=\:")
        delta_r_label_4= MathTex(r"1", r"\over", r"r", r"^2")
        delta_r_label_5= MathTex(r"F_{r}(r+dr)", r"(", r"r+dr", r")^{2}", r"-", r"F_{r}(r)", r"r", r"^{2}", r"\over", r"r", r"^{2}d", r"r")
        delta_r_label_6= MathTex(r"\partial", r"\over", r"\partial", r"r")
        delta_r_label_7= MathTex(r"(", r"r", r"^{2}", r"F_{r}", r")")
       
        delta_r_label_1.set_color_by_tex(r"F_{r}", ORANGE)
        delta_r_label_2.set_color_by_tex(r"F_{r}(r+dr)", ORANGE)
        delta_r_label_2.set_color_by_tex(r"r+dr", ORANGE)
        delta_r_label_2.set_color_by_tex(r"r", ORANGE)
        delta_r_label_2.set_color_by_tex(r"F_{r}(r)", ORANGE)
        delta_r_label_2[2].set_color(BLUE)
        delta_r_label_2[4].set_color(BLUE)
        delta_r_label_2[8].set_color(RED)
        delta_r_label_2[10].set_color(RED)
        area_r_plus_label[0].set_color(BLUE)
        area_r_plus_label[1].set_color(ORANGE)
        area_r_plus_label[2].set_color(BLUE)
        area_r_plus_eff[1].set_color(ORANGE)
        area_r_min_label[0].set_color(RED)
        area_r_min_label[1].set_color(ORANGE)
        area_r_min_label[2].set_color(RED)
        area_r_min_eff[1].set_color(ORANGE)
        volume_r_label[4].set_color(ORANGE)
        volume_r_label[8].set_color(ORANGE)
        volume_r_eff[1].set_color(ORANGE)
        delta_r_label_3.set_color_by_tex(r"F_{r}(r+dr)", ORANGE)
        delta_r_label_3.set_color_by_tex(r"r+dr", ORANGE)
        delta_r_label_3.set_color_by_tex(r"F_{r}(r)", ORANGE)
        delta_r_label_3.set_color_by_tex(r"r", ORANGE)
        delta_r_label_4[2].set_color(ORANGE)
        delta_r_label_5.set_color_by_tex(r"F_{r}(r+dr)", ORANGE)
        delta_r_label_5.set_color_by_tex(r"r+dr", ORANGE)
        delta_r_label_5.set_color_by_tex(r"F_{r}(r)", ORANGE)
        delta_r_label_5.set_color_by_tex(r"r", ORANGE)
        delta_r_label_6[3].set_color(ORANGE)
        delta_r_label_7[1].set_color(ORANGE)
        delta_r_label_7[3].set_color(ORANGE)

        delta_r_group_1= VGroup(delta_r_label_1, delta_r_label_2)
        delta_r_group_1.arrange(RIGHT, buff=0.1)
        delta_r_group_1.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_r_plus_group= VGroup(area_r_plus_label, area_r_plus_eff)
        area_r_plus_group.arrange(RIGHT, buff=0.1)
        area_r_plus_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 2.3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_r_min_group= VGroup(area_r_min_label, area_r_min_eff)
        area_r_min_group.arrange(RIGHT, buff=0.1)
        area_r_min_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 1.65)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        volume_r_group= VGroup(volume_r_label, volume_r_eff)
        volume_r_group.arrange(RIGHT, buff=0.1)
        volume_r_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 1)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_r_label_3.scale(0.8).move_to(axes.c2p(1.5, 1.5*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
            
        delta_r_label_5.scale(0.8).move_to(axes.c2p(1.5, 1.5*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_r_group_2= VGroup(delta_r_label_4, delta_r_label_6, delta_r_label_7) 
        delta_r_group_2.arrange(RIGHT, buff=0.1)
        delta_r_group_2.scale(0.8).move_to(axes.c2p(2.05, 2.05*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        equal_r_label.scale(0.8).move_to(axes.c2p(1.8, 1.8*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.play(FadeIn(r_min_surf), FadeIn(r_plus_surf), run_time=2)
        self.wait(1)
        self.play(Write(delta_r_group_1))
        self.wait(2)
        area_r_plus_group_copy= area_r_plus_group.copy()
        self.play(Write(area_r_plus_group), Write(area_r_plus_group_copy))
        self.wait(2)
        area_r_min_group_copy= area_r_min_group.copy()
        self.play(Write(area_r_min_group), Write(area_r_min_group_copy))
        self.wait(1)
        volume_r_group_copy= volume_r_group.copy()
        self.play(Write(volume_r_group), Write(volume_r_group_copy))
        self.wait(2)
# 步驟 A: 將所有零件匯聚成那串最長、未約分的公式 (delta_r_label_3)
        self.play(
            TransformMatchingTex(Group(delta_r_label_2, area_r_plus_eff, area_r_min_eff, volume_r_eff) , delta_r_label_3),
            run_time=2)
        self.wait(2)

# 步驟 B: 執行約分，飛向最終形式
        self.play(
            TransformMatchingTex(delta_r_label_3, delta_r_label_5) # 相同字元會飛過去，消失的會淡出
            , run_time=2)
        self.wait(2)
        self.play(delta_r_label_5.animate.move_to(axes.c2p(1.3, 1.3*(2+np.sqrt(3)), 3)))
        self.play(Write(equal_r_label), Write(delta_r_group_2))
        self.wait(2)
        self.play(
            FadeOut(delta_r_label_5),
            FadeOut(equal_r_label),
            FadeOut(area_r_plus_group),
            FadeOut(area_r_plus_group_copy),
            FadeOut(area_r_min_group),
            FadeOut(area_r_min_group_copy),
            FadeOut(volume_r_group),
            FadeOut(volume_r_group_copy),
            delta_r_label_1.animate.move_to(axes.c2p(1.3, 1.3*(2+np.sqrt(3)), 1.3)),
            delta_r_group_2.animate.move_to(axes.c2p(1.7, 1.7*(2+np.sqrt(3)), 1.3)),
            run_time=2)
        self.play(delta_r_label_1.animate.scale(1.3),
            delta_r_group_2.animate.scale(1.3),
            run_time=2)

        con_rectangle_r= Rectangle(width= 5, height= 2).set_stroke(WHITE, 2).move_to(axes.c2p(1.55, 1.55*(2+np.sqrt(3)), 1.3)).rotate(self.camera.get_phi(),  
            axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        self.play(Create(con_rectangle_r), run_time=1)
        self.wait(3)
        div_r_group= VGroup(delta_r_label_1, delta_r_group_2, con_rectangle_r)
        self.play(div_r_group.animate.scale(0.6))
        self.play(div_r_group.animate.move_to(axes.c2p(0.44, 0.44*(2+np.sqrt(3)), 4.2)), run_time=2)
        self.wait(2)
        self.play(FadeOut(r_min_surf, r_plus_surf))

        r_sup_l= Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= ORANGE,
            stroke_width=3,
            stroke_opacity= 1
            )
        r_sup_r= Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= ORANGE,
            stroke_width=3,
            stroke_opacity= 1
            )
        r_sup_label= MathTex(r"r")
        r_sup_label.scale(0.8).set_color(ORANGE).move_to(axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min)/2, 
                (r_min) * np.sin(theta_min) * np.sin(phi_min)/2, 
                (r_min) * np.cos(theta_min)/2-0.2)).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        theta_sup_arc=  ArcBetweenPoints(
            start= axes.c2p(0.8 * np.sin(theta_min) * np.cos(phi_min), 
                0.8 * np.sin(theta_min) * np.sin(phi_min), 
                0.8 * np.cos(theta_min)),
            end= axes.c2p(0, 0, 0.8),
            radius= 0.8,
            color=PURPLE
        )
        theta_sup_label= MathTex(r"\theta")
        theta_sup_label.set_color(PURPLE).move_to(axes.c2p(1.1 * np.sin((theta_min)/2) * np.cos(phi_min), 
                1.1 * np.sin((theta_min)/2) * np.sin(phi_min), 
                1.1 * np.cos((theta_min)/2))).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        line_sup_l=  DashedLine(
            start= axes.c2p(0, 0, (r_min) * np.cos(theta_min)),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= ORANGE,
            dashed_ratio=0.5,
            stroke_width=4,
            stroke_opacity= 0.8
            )
        line_sup_r=  DashedLine(
            start= axes.c2p(0, 0, (r_min) * np.cos(theta_min)),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min)),
            buff= 0,
            color= ORANGE,
            dashed_ratio=0.5,
            stroke_width=4,
            stroke_opacity= 0.8
            )
        line_sup_label= MathTex( r"r", r"sin", r"\theta")
        line_sup_label[0].set_color(ORANGE)
        line_sup_label[2].set_color(PURPLE)
        line_sup_label.move_to(axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min)/2, 
                (r_min) * np.sin(theta_min) * np.sin(phi_min)/2, 
                (r_min) * np.cos(theta_min)-0.2)).scale(0.8).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        theta_arc_path=  ArcBetweenPoints(
            start= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min+d_phi), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min+d_phi), 
                (r_min) * np.cos(theta_min)),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            radius=r_min,
            color=PURE_YELLOW
        )
        theta_arc_path_label= MathTex( r"r", r"sin", r"\theta", r"d\phi")
        theta_arc_path_label.set_color(PURE_YELLOW).scale(0.8).move_to(axes.c2p(1.5*(r_min) * np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                1.5*(r_min) * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                (r_min) * np.cos(theta_min)+0.2)).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        
        dr_sup_radius= Line(
            start= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            end= axes.c2p((r_min+dr) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min+dr) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min+dr) * np.cos(theta_min)),
            buff= 0,
            color= ORANGE,
            )

        r_theta_arc_path= ArcBetweenPoints(
            start= axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min+d_theta)),
            end= axes.c2p((r_min) * np.sin(theta_min) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min)),
            radius=r_min,
            color= PURE_CYAN
        )
        r_theta_arc_path_label= MathTex( r"r", r"d\theta")
        r_theta_arc_path_label.set_color(PURE_CYAN).scale(0.8).move_to(axes.c2p((r_min) * np.sin(theta_min+d_theta) * np.cos(phi_min), 
                (r_min) * np.sin(theta_min+d_theta) * np.sin(phi_min), 
                (r_min) * np.cos(theta_min+d_theta)-0.2)).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)


        delta_theta_label_1 = MathTex(r"\Delta", r"F_{\theta}", r" = ")
        delta_theta_label_2 = MathTex(r"F_{\theta}(\theta+d\theta)", r"\times", r"Area(", r"\theta+d\theta", r")", r"-", r"F_{\theta}(\theta)", r"\times", 
            r"Area(", r"\theta", r")", r"\over", r"volume")
        area_theta_plus_label= MathTex(r"Area(", r"\theta+d\theta", r")", r" = ")
        area_theta_min_label= MathTex(r"Area(", r"\theta", r")", r" = ")
        volume_theta_label = MathTex(r"volume = ", r"r sin \theta d\phi", r"\times", r"dr" , r"\times", r"r d\theta", r"=")
        area_theta_plus_eff= MathTex(r"r", r"sin(", r"\theta+d\theta", r")", r"d\phi", r"\times", r"dr")
        area_theta_min_eff= MathTex(r"r", r"sin(", r"\theta", r")", r"d\phi", r"\times", r"dr")
        volume_theta_eff= MathTex(r"r", r"^{2}", r"sin", r"\theta", r"dr", r"d\theta", r"d\phi")
        delta_theta_label_3 = MathTex(r"F_{\theta}(\theta+d\theta)", r"\times", r"r", r"sin(", r"\theta+d\theta", r")", r"d\phi", r"dr", r"-",
            r"F_{\theta}(\theta)", r"\times", r"r", r"sin(", r"\theta", r")", r"d\phi", r"dr", r"\over", r"r", r"^{2}", r"sin", r"\theta", r"dr", r"d\theta", r"d\phi")
        delta_theta_label_4= MathTex(r"F_{\theta}(\theta+d\theta)", r"sin(", r"\theta+d\theta", r")", r"-",
            r"F_{\theta}(\theta)", r"sin(", r"\theta", r")", r"\over", r"r", r"sin", r"\theta", r"\:", r"d\theta")
        delta_theta_label_5= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        delta_theta_label_6= MathTex(r"\partial", r"\over", r"\partial", r"\theta")
        delta_theta_label_7= MathTex(r"(", r"sin", r"\theta", r"F_{\theta}", r")")
        equal_theta_label= MathTex(r"=\:")

        delta_theta_label_1[1].set_color(PURPLE)
        delta_theta_label_2[0].set_color(PURPLE)
        delta_theta_label_2[2].set_color(BLUE)
        delta_theta_label_2[3].set_color(PURPLE)
        delta_theta_label_2[4].set_color(BLUE)
        delta_theta_label_2[6].set_color(PURPLE)
        delta_theta_label_2[8].set_color(RED)
        delta_theta_label_2[9].set_color(PURPLE)
        delta_theta_label_2[10].set_color(RED)
        area_theta_plus_label[0].set_color(BLUE)
        area_theta_plus_label[1].set_color(PURPLE)
        area_theta_plus_label[2].set_color(BLUE)
        area_theta_plus_eff[0].set_color(PURE_YELLOW)
        area_theta_plus_eff[1].set_color(PURE_YELLOW)
        area_theta_plus_eff[2].set_color(PURE_YELLOW)
        area_theta_plus_eff[3].set_color(PURE_YELLOW)
        area_theta_plus_eff[4].set_color(PURE_YELLOW)
        area_theta_plus_eff[6].set_color(ORANGE)
        area_theta_min_label[0].set_color(RED)
        area_theta_min_label[1].set_color(PURPLE)
        area_theta_min_label[2].set_color(RED)
        area_theta_min_eff[0].set_color(PURE_YELLOW)
        area_theta_min_eff[1].set_color(PURE_YELLOW)
        area_theta_min_eff[2].set_color(PURE_YELLOW)
        area_theta_min_eff[3].set_color(PURE_YELLOW)
        area_theta_min_eff[4].set_color(PURE_YELLOW)
        area_theta_min_eff[6].set_color(ORANGE)
        volume_theta_label[1].set_color(PURE_YELLOW)
        volume_theta_label[3].set_color(ORANGE)
        volume_theta_label[5].set_color(PURE_CYAN)
        volume_theta_eff[0].set_color(ORANGE)
        volume_theta_eff[3].set_color(PURPLE)
        volume_theta_eff[4].set_color(ORANGE)
        volume_theta_eff[5].set_color(PURPLE)
        volume_theta_eff[6].set_color(GREEN)
        delta_theta_label_3.set_color_by_tex(r"r", ORANGE)
        delta_theta_label_3.set_color_by_tex(r"dr", ORANGE)
        delta_theta_label_3.set_color_by_tex(r"d\phi", GREEN)
        delta_theta_label_3.set_color_by_tex(r"\theta", PURPLE)
        delta_theta_label_3.set_color_by_tex(r"d\theta", PURPLE)
        delta_theta_label_3.set_color_by_tex(r"\theta+d\theta", PURPLE)
        delta_theta_label_3[0].set_color(PURPLE)
        delta_theta_label_3[9].set_color(PURPLE)
        delta_theta_label_4[0].set_color(PURPLE)
        delta_theta_label_4[2].set_color(PURPLE)
        delta_theta_label_4[5].set_color(PURPLE)
        delta_theta_label_4[7].set_color(PURPLE)
        delta_theta_label_4[10].set_color(ORANGE)
        delta_theta_label_4[12].set_color(PURPLE)
        delta_theta_label_4[14].set_color(PURPLE)
        delta_theta_label_5[2].set_color(ORANGE)
        delta_theta_label_5[4].set_color(PURPLE)
        delta_theta_label_6[3].set_color(PURPLE)
        delta_theta_label_7[2].set_color(PURPLE)
        delta_theta_label_7[3].set_color(PURPLE)

        delta_theta_group_1= VGroup(delta_theta_label_1, delta_theta_label_2)
        delta_theta_group_1.arrange(RIGHT, buff=0.1)
        delta_theta_group_1.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_theta_plus_group= VGroup(area_theta_plus_label, area_theta_plus_eff)
        area_theta_plus_group.arrange(RIGHT, buff=0.1)
        area_theta_plus_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 2.3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_theta_min_group= VGroup(area_theta_min_label, area_theta_min_eff)
        area_theta_min_group.arrange(RIGHT, buff=0.1)
        area_theta_min_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 1.65)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        volume_theta_group= VGroup(volume_theta_label, volume_theta_eff)
        volume_theta_group.arrange(RIGHT, buff=0.1)
        volume_theta_group.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 1)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_theta_label_3.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
            
        delta_theta_label_4.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_theta_group_2= VGroup(delta_theta_label_5, delta_theta_label_6, delta_theta_label_7) 
        delta_theta_group_2.arrange(RIGHT, buff=0.1)
        delta_theta_group_2.scale(0.8).move_to(axes.c2p(1.95, 1.95*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        equal_theta_label.scale(0.8).move_to(axes.c2p(1.65, 1.65*(2+np.sqrt(3)), 3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.camera.light_source.move_to( 6 * RIGHT + 6 * UP + 2 * OUT)
        self.play(FadeIn(theta_min_surf), FadeIn(theta_plus_surf), FadeOut(theta_surf_plus), FadeOut(theta_surf_min), run_time=2)
        self.wait(1)
        self.play(Write(delta_theta_group_1))
        self.wait(2)

        self.play(Create(r_sup_l), Create(r_sup_r), FadeIn(r_sup_label))
        self.play(Create(theta_sup_arc), FadeIn(theta_sup_label))
        self.play(dr_label.animate.move_to(axes.c2p((r_min+dr/2) * np.sin(theta_min/1.3) * np.cos(phi_min), 
                (r_min+dr/2) * np.sin(theta_min/1.3) * np.sin(phi_min), 
                (r_min+dr/2) * np.cos(theta_min/1.3))), FadeOut(dr_radius), FadeIn(dr_sup_radius)) 
        self.play(Create(line_sup_l), Create(line_sup_r), FadeIn(line_sup_label))
        self.play(d_phi_arc.animate.move_to(axes.c2p(0.8 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                0.8 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                (r_min) * np.cos(theta_min))), 
            d_phi_label.animate.move_to(axes.c2p(0.5 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                0.5 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                1.1 *(r_min)* np.cos(theta_min))))
        self.play(d_phi_arc.animate.scale(0.6).move_to(axes.c2p(0.6 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                0.6 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                (r_min) * np.cos(theta_min))))
        self.play(Create(theta_arc_path), Write(theta_arc_path_label))
        self.wait(1)
        self.play(FadeOut(r_sup_l), FadeOut(r_sup_r), FadeOut(r_sup_label), FadeOut(theta_sup_arc), FadeOut(theta_sup_label))
        area_theta_plus_group_copy= area_theta_plus_group.copy()
        self.play(Write(area_theta_plus_group), Write(area_theta_plus_group_copy))
        self.wait(2)
        area_theta_min_group_copy= area_theta_min_group.copy()
        self.play(Write(area_theta_min_group), Write(area_theta_min_group_copy))
        self.wait(2)
        self.play(Create(r_theta_arc_path), FadeIn(r_theta_arc_path_label))
        self.wait(2)
        volume_theta_group_copy= volume_theta_group.copy()
        self.play(Write(volume_theta_group), Write(volume_theta_group_copy))
        self.wait(2)
# 步驟 A: 將所有零件匯聚成那串最長、未約分的公式 (delta_r_label_3)
        self.play(delta_theta_label_1.animate.move_to(axes.c2p(0.48, 0.48*(2+np.sqrt(3)), 3)),
            TransformMatchingTex(Group(delta_theta_label_2, area_theta_plus_eff, area_theta_min_eff, volume_theta_eff), delta_theta_label_3),
            run_time=2)
        self.wait(2)

# 步驟 B: 執行約分，飛向最終形式
        self.play(
            TransformMatchingTex(delta_theta_label_3, delta_theta_label_4) # 相同字元會飛過去，消失的會淡出
            , run_time=2)
        self.wait(2)
        self.play(delta_theta_label_1.animate.move_to(axes.c2p(0.33, 0.33*(2+np.sqrt(3)), 3)), 
            delta_theta_label_4.animate.move_to(axes.c2p(1.03, 1.03*(2+np.sqrt(3)), 3)))
        self.play(Write(equal_theta_label), Write(delta_theta_group_2))
        self.wait(2)
        self.play(
            FadeOut(delta_theta_label_4),
            FadeOut(equal_theta_label),
            FadeOut(area_theta_plus_group),
            FadeOut(area_theta_plus_group_copy),
            FadeOut(area_theta_min_group),
            FadeOut(area_theta_min_group_copy),
            FadeOut(volume_theta_group),
            FadeOut(volume_theta_group_copy),
            delta_theta_label_1.animate.move_to(axes.c2p(1.2, 1.2*(2+np.sqrt(3)), 1.3)),
            delta_theta_group_2.animate.move_to(axes.c2p(1.7, 1.7*(2+np.sqrt(3)), 1.3)),
            run_time=2)
        self.play(delta_theta_label_1.animate.scale(1.3),
            delta_theta_group_2.animate.scale(1.3),
            run_time=2)

        con_rectangle_theta= Rectangle(width= 6.5, height= 2).set_stroke(WHITE, 2).move_to(axes.c2p(1.53, 1.53*(2+np.sqrt(3)), 1.3)).rotate(self.camera.get_phi(),  
            axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        self.play(Create(con_rectangle_theta), run_time=1)
        self.wait(3)
        div_theta_group= VGroup(delta_theta_label_1, delta_theta_group_2, con_rectangle_theta)
        self.play(div_theta_group.animate.scale(0.6))
        self.play(div_theta_group.animate.move_to(axes.c2p(0.44, 0.44*(2+np.sqrt(3)), 3.2)), run_time=2)
        self.wait(2)
        self.play(
            FadeOut(theta_arc_path), FadeOut(theta_arc_path_label), 
            FadeOut(line_sup_l), FadeOut(line_sup_r), FadeOut(line_sup_label), 
            FadeOut(d_phi_arc), FadeOut(d_phi_label),
            FadeOut(theta_plus_surf), FadeOut(theta_min_surf),
            FadeIn(theta_surf_plus), FadeIn(theta_surf_min))
        self.play(d_phi_arc.animate.move_to(axes.c2p(0.6 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                0.6 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                0)), 
            d_phi_label.animate.move_to(axes.c2p(1.3 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                1.3 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                0)))
        self.play(d_phi_arc.animate.scale(0.8).move_to(axes.c2p(0.8 *np.sin(theta_min) * np.cos(phi_min+d_phi/2), 
                0.8 * np.sin(theta_min) * np.sin(phi_min+d_phi/2), 
                0)))
        self.wait(1)


        delta_phi_label_1 = MathTex(r"\Delta", r"F_{\phi}", r" = ")
        delta_phi_label_2 = MathTex(r"F_{\phi}(\phi+d\phi)", r"\times", r"Area(", r"\phi+d\phi", r")", r"-", r"F_{\phi}(\phi)", r"\times", 
            r"Area(", r"\phi", r")", r"\over", r"volume")
        area_phi_plus_label= MathTex(r"Area(", r"\phi+d\phi", r")", r" = ")
        area_phi_min_label= MathTex(r"Area(", r"\phi", r")", r" = ")
        volume_phi_label = MathTex(r"volume = ")
        area_phi_plus_eff= MathTex(r"dr", r"\times",r"r d\theta")
        area_phi_min_eff= MathTex(r"dr", r"\times",r"r d\theta")
        volume_phi_eff= MathTex(r"r", r"^{2}", r"sin", r"\theta", r"dr", r"d\theta", r"d\phi")
        delta_phi_label_3 = MathTex(r"F_{\phi}(\phi+d\phi)", r"\times", r"dr", r"\times",r"r", r"d\theta", r"-",
            r"F_{\phi}(\phi)", r"\times", r"dr", r"\times",r"r", r"d\theta", r"\over", r"r", r"^{2}", r"sin", r"\theta", r"dr", r"d\theta", r"d\phi")
        delta_phi_label_4= MathTex(r"F_{\phi}(\phi+d\phi)", r"-", r"F_{\phi}(\phi)", r"\over", r"r", r"sin", r"\theta", r"\:", r"d\phi")
        delta_phi_label_5= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        delta_phi_label_6= MathTex(r"\partial", r"\over", r"\partial", r"\phi")
        delta_phi_label_7= MathTex(r"F_{\phi}")
        equal_phi_label= MathTex(r"=\:")

        # 定義顏色常量
        COL_R = ORANGE      # r, dr
        COL_THETA = PURPLE  # theta, dtheta
        COL_PHI = GREEN     # phi, dphi
        color_map = {
            "r": COL_R, "dr": COL_R,
            "theta": COL_THETA, r"\theta": COL_THETA, r"d\theta": COL_THETA,
            "phi": COL_PHI, r"\phi": COL_PHI, r"d\phi": COL_PHI, "\phi+d\phi": COL_PHI,
            "F_{\phi}": COL_PHI, "F_{\phi}(\phi+d\phi)": COL_PHI, "F_{\phi}(\phi)": COL_PHI
        }
        labels_to_color = [
            delta_phi_label_1, delta_phi_label_2, area_phi_plus_label, 
            area_phi_min_label,  
            volume_phi_eff, delta_phi_label_3, delta_phi_label_4, 
            delta_phi_label_5, delta_phi_label_6, delta_phi_label_7
        ]
        for label in labels_to_color:
            label.set_color_by_tex_to_color_map(color_map)
        
        delta_phi_label_2[2].set_color(BLUE)
        delta_phi_label_2[4].set_color(BLUE)
        delta_phi_label_2[8].set_color(RED)
        delta_phi_label_2[10].set_color(RED)
        area_phi_plus_label[0].set_color(BLUE)
        area_phi_plus_label[2].set_color(BLUE)
        area_phi_plus_eff[0].set_color(ORANGE)
        area_phi_plus_eff[2].set_color(PURE_CYAN)
        area_phi_min_label[0].set_color(RED)
        area_phi_min_label[2].set_color(RED)
        area_phi_min_eff[0].set_color(ORANGE)
        area_phi_min_eff[2].set_color(PURE_CYAN)

        delta_phi_group_1 = VGroup(delta_phi_label_1, delta_phi_label_2)
        delta_phi_group_1.arrange(RIGHT, buff=0.1)
        delta_phi_group_1.scale(0.8).move_to(axes.c2p(1.4, 1.4*(2+np.sqrt(3)), 2)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_phi_plus_group = VGroup(area_phi_plus_label, area_phi_plus_eff)
        area_phi_plus_group.arrange(RIGHT, buff=0.1)
        area_phi_plus_group.scale(0.8).move_to(axes.c2p(1.5, 1.5*(2+np.sqrt(3)), 1.3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        area_phi_min_group = VGroup(area_phi_min_label, area_phi_min_eff)
        area_phi_min_group.arrange(RIGHT, buff=0.1)
        area_phi_min_group.scale(0.8).move_to(axes.c2p(1.5, 1.5*(2+np.sqrt(3)), 0.65)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        volume_phi_group = VGroup(volume_phi_label, volume_phi_eff)
        volume_phi_group.arrange(RIGHT, buff=0.1)
        volume_phi_group.scale(0.8).move_to(axes.c2p(1.5, 1.5*(2+np.sqrt(3)), 0)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_phi_label_3.scale(0.8).move_to(axes.c2p(1.55, 1.55*(2+np.sqrt(3)), 2)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_phi_label_4.scale(0.8).move_to(axes.c2p(1.45, 1.45*(2+np.sqrt(3)), 2)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        delta_phi_group_2 = VGroup(delta_phi_label_5, delta_phi_label_6, delta_phi_label_7) 
        delta_phi_group_2.arrange(RIGHT, buff=0.1)
        delta_phi_group_2.scale(0.8).move_to(axes.c2p(2.07, 2.07*(2+np.sqrt(3)), 2)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        equal_phi_label.scale(0.8).move_to(axes.c2p(1.84, 1.84*(2+np.sqrt(3)), 2)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.play(FadeIn(phi_min_surf), FadeIn(phi_plus_surf), FadeOut(phi_surf_plus), FadeOut(phi_surf_min), run_time=2)
        self.wait(1)
        self.play(Write(delta_phi_group_1))
        self.wait(2)
        area_phi_plus_group_copy = area_phi_plus_group.copy()
        self.play(Write(area_phi_plus_group), Write(area_phi_plus_group_copy))
        self.wait(2)
        area_phi_min_group_copy = area_phi_min_group.copy()
        self.play(Write(area_phi_min_group), Write(area_phi_min_group_copy))
        self.wait(2)
        volume_phi_group_copy = volume_phi_group.copy()
        self.play(Write(volume_phi_group), Write(volume_phi_group_copy))
        self.wait(2)
        self.play(
            delta_phi_label_1.animate.move_to(axes.c2p(0.73, 0.73*(2+np.sqrt(3)), 2)),
            TransformMatchingTex(Group(delta_phi_label_2, area_phi_plus_eff, area_phi_min_eff, volume_phi_eff), delta_phi_label_3),
            run_time=2
        )
        self.wait(2)
        # 步驟 B: 執行約分，飛向最終形式
        self.play(
            delta_phi_label_1.animate.move_to(axes.c2p(1, 1*(2+np.sqrt(3)), 2)),
            TransformMatchingTex(delta_phi_label_3, delta_phi_label_4), # 相同字元會飛過去，消失的會淡出
            run_time=2
        )
        self.wait(2)
        self.play(Write(equal_phi_label), Write(delta_phi_group_2))
        self.wait(2)
        self.play(
            FadeOut(delta_phi_label_4),
            FadeOut(equal_phi_label),
            FadeOut(area_phi_plus_group),
            FadeOut(area_phi_plus_group_copy),
            FadeOut(area_phi_min_group),
            FadeOut(area_phi_min_group_copy),
            FadeOut(volume_phi_group),
            FadeOut(volume_phi_group_copy),
            delta_phi_label_1.animate.move_to(axes.c2p(1.3, 1.3*(2+np.sqrt(3)), 1.3)),
            delta_phi_group_2.animate.move_to(axes.c2p(1.7, 1.7*(2+np.sqrt(3)), 1.3)),
            run_time=2
        )
        self.play(
            delta_phi_label_1.animate.scale(1.3),
            delta_phi_group_2.animate.scale(1.3),
            run_time=2
        )
        con_rectangle_phi = Rectangle(width=5.5, height=2).set_stroke(WHITE, 2).move_to(axes.c2p(1.55, 1.55*(2+np.sqrt(3)), 1.3)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)
        self.play(Create(con_rectangle_phi), run_time=1)
        self.wait(3)
        self.play(
            FadeOut(phi_plus_surf), FadeOut(phi_min_surf),
            FadeOut(all_objects), FadeOut(dr_sup_radius),
            FadeOut(r_theta_arc_path), FadeOut(r_theta_arc_path_label),
            run_time=1
        )
        self.wait(1)
        div_phi_group= VGroup(delta_phi_label_1, delta_phi_group_2, con_rectangle_phi)
        self.play(div_phi_group.animate.scale(0.6))


        self.play(
            div_r_group.animate.scale(1.1).move_to(axes.c2p(0.26, 0.26*(2+np.sqrt(3)), 3.2)),
            div_theta_group.animate.scale(1.1).move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 3.2)),
            div_phi_group.animate.scale(1.1).move_to(axes.c2p(1.83, 1.83*(2+np.sqrt(3)), 3.2)),
            FadeOut(func_label_1), func_label_2.animate.move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 1.5)),
            run_time=2)
        div_r_group_copy= div_r_group.copy()
        div_theta_group_copy= div_theta_group.copy()
        div_phi_group_copy= div_phi_group.copy()
        self.add(div_r_group_copy, div_theta_group_copy, div_phi_group_copy)
        self.wait(3)
        
        div_label_1_1= MathTex(r"\nabla \cdot \text{F}= ")
        div_label_1_2= MathTex(r"1", r"\over", r"r", r"^2")
        div_label_1_3= MathTex(r"\partial", r"\over", r"\partial", r"r")
        div_label_1_4= MathTex(r"(", r"r", r"^{2}", r"F_{r}", r")", r"+")
        div_label_1_5= MathTex(r" \Delta ", r"F_{\theta}", r"+")
        div_label_1_6= MathTex(r" \Delta ", r"F_{\phi}")
        div_label_group_1= VGroup(div_label_1_1, div_label_1_2, div_label_1_3, div_label_1_4, div_label_1_5, div_label_1_6)
        div_label_group_1.arrange(RIGHT, buff=0.1)
        div_label_group_1.move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 1.5)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta() + 90*DEGREES, axis=OUT)

        div_label_2_1= MathTex(r"\nabla \cdot \text{F}= ")
        div_label_2_2= MathTex(r"1", r"\over", r"r", r"^2")
        div_label_2_3= MathTex(r"\partial", r"\over", r"\partial", r"r")
        div_label_2_4= MathTex(r"(", r"r", r"^{2}", r"F_{r}", r")", r"+")
        div_label_2_5= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        div_label_2_6= MathTex(r"\partial", r"\over", r"\partial", r"\theta")
        div_label_2_7= MathTex(r"(", r"sin", r"\theta", r"F_{\theta}", r")", r" +")
        div_label_2_8= MathTex(r" \Delta ", r"F_{\phi}")
        div_label_group_2= VGroup(div_label_2_1, div_label_2_2, div_label_2_3, div_label_2_4, div_label_2_5, div_label_2_6, div_label_2_7, div_label_2_8)
        div_label_group_2.arrange(RIGHT, buff=0.1)
        div_label_group_2.move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 1.5)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta() + 90*DEGREES, axis=OUT)

        div_label_3_1= MathTex(r"\nabla \cdot \text{F}= ")
        div_label_3_2= MathTex(r"1", r"\over", r"r", r"^2")
        div_label_3_3= MathTex(r"\partial", r"\over", r"\partial", r"r")
        div_label_3_4= MathTex(r"(", r"r", r"^{2}", r"F_{r}", r")", r"+")
        div_label_3_5= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        div_label_3_6= MathTex(r"\partial", r"\over", r"\partial", r"\theta")
        div_label_3_7= MathTex(r"(", r"sin", r"\theta", r"F_{\theta}", r")", r" +")
        div_label_3_8= MathTex(r"1", r"\over", r"r", r"sin", r"\theta")
        div_label_3_9= MathTex(r"\partial", r"\over", r"\partial", r"\phi")
        div_label_3_10= MathTex(r"F_{\phi}")
        div_label_group_3= VGroup(div_label_3_1, div_label_3_2, div_label_3_3, div_label_3_4, div_label_3_5,
            div_label_3_6, div_label_3_7, div_label_3_8, div_label_3_9, div_label_3_10)
        div_label_group_3.arrange(RIGHT, buff=0.1)
        div_label_group_3.move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 1.5)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta() + 90*DEGREES, axis=OUT)

        COL_R = ORANGE      # r, dr
        COL_THETA = PURPLE  # theta, dtheta
        COL_PHI = GREEN     # phi, dphi
        color_map_2 = {
            "r": COL_R, "F_{r}": COL_R,
            r"\theta": COL_THETA, r"F_{\theta}": COL_THETA,
            r"\phi": COL_PHI, r"F_{\phi}": COL_PHI 
        }
        labels_to_color_2 = [
            # 第一組 (r 分量完成時)
            div_label_1_1, div_label_1_2, div_label_1_3, div_label_1_4, div_label_1_5, div_label_1_6,
            # 第二組 (theta 分量完成時)
            div_label_2_1, div_label_2_2, div_label_2_3, div_label_2_4, div_label_2_5, div_label_2_6, div_label_2_7, div_label_2_8,
            # 第三組 (完整散度公式)
            div_label_3_1, div_label_3_2, div_label_3_3, div_label_3_4, div_label_3_5, div_label_3_6, div_label_3_7, div_label_3_8, div_label_3_9, div_label_3_10
            ]
        for label in labels_to_color_2:
            label.set_color_by_tex_to_color_map(color_map_2)

        self.play(TransformMatchingTex(Group(func_label_2, *delta_r_group_2), div_label_group_1))
        self.wait(1)
        self.play(TransformMatchingTex(Group(*div_label_group_1, *delta_theta_group_2), div_label_group_2))
        self.wait(1)
        self.play(TransformMatchingTex(Group(*div_label_group_2, *delta_phi_group_2), div_label_group_3))
        self.wait(1)

        div_rectangle= Rectangle(width=12.5, height=1.8).set_stroke(WHITE, 2).move_to(axes.c2p(1.05, 1.05*(2+np.sqrt(3)), 1.5)).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT)

        self.play(Create(div_rectangle), FadeOut(div_r_group), FadeOut(div_r_group_copy), 
            FadeOut(div_theta_group), FadeOut(div_theta_group_copy), 
            FadeOut(div_phi_group), FadeOut(div_phi_group_copy))

        final_group= VGroup(div_label_group_3, div_rectangle)
        self.play(final_group.animate.shift(OUT*1))
        self.wait(3)
       