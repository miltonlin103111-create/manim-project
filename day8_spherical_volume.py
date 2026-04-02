from manim import *
import numpy as np

class SphericalCoordinate(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        axes = ThreeDAxes(x_range=[-5, 5], y_range=[-5, 5], z_range=[-4, 4], x_length=10, y_length=10, z_length=8)        

        # 範圍設定
        r_min = ValueTracker(2)
        theta_min = ValueTracker(30*DEGREES)
        phi_min = ValueTracker(30*DEGREES)
        
        # 修正：將 dr, d_theta, d_phi 提到最前面，確保後面的函數都讀得到
        dr = 0.98
        d_theta = 20 * DEGREES
        d_phi = 30 * DEGREES

        # 修正：將函數名稱改為 get_sphere_surface 以符合你原本 inner_sphere 的呼叫
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
        
        inner_sphere = always_redraw(lambda: get_sphere_surface(r_min.get_value()).set_fill(GRAY_B))
 
        # 修正：將 start_p 變成動態獲取，否則你的 Dot 和 Line 會留在原位不動
        def get_current_start_p():
            return np.array([
                r_min.get_value() * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                r_min.get_value() * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                r_min.get_value() * np.cos(theta_min.get_value())
            ])
        
        # 修正：start_dot 必須用 always_redraw
        start_dot = always_redraw(lambda: Dot(color=WHITE).move_to(axes.c2p(*get_current_start_p())))

        self.add(axes)
        self.play(Create(inner_sphere))
        self.play(inner_sphere.animate.set_opacity(0.8),run_time= 2)
        self.add(start_dot)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(2)

        # 修正：radius 的 end 要連動
        radius = always_redraw(lambda: Line(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*get_current_start_p()),
            buff=0,
            color=ORANGE
        ))
        
        # 保留你的標籤定義
        radius_label = always_redraw(lambda: MathTex(r"r").move_to(axes.c2p(                      
                r_min.get_value()/2 * np.sin(theta_min.get_value()+9*DEGREES) * np.cos(phi_min.get_value()),
                r_min.get_value()/2 * np.sin(theta_min.get_value()+9*DEGREES) * np.sin(phi_min.get_value()),
                r_min.get_value()/2 * np.cos(theta_min.get_value()+9*DEGREES)
            )).set_color(ORANGE).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        theta_arc = always_redraw(lambda: ArcBetweenPoints(
            start=axes.c2p(0, 0, 1),
            end=axes.c2p(                      
                1 * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()),
                1 * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()),
                1 * np.cos(theta_min.get_value())
            ),
            radius=1,
            color=PURPLE
        ))
        theta_label = always_redraw(lambda: MathTex(r"\theta").move_to(axes.c2p(                      
                1.5 * np.sin(theta_min.get_value()/2) * np.cos(phi_min.get_value()),
                1.5 * np.sin(theta_min.get_value()/2) * np.sin(phi_min.get_value()),
                1.5 * np.cos(theta_min.get_value()/2)
            )).set_color(PURPLE).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        phi_arc = always_redraw(lambda: Arc(
            radius=1,
            start_angle=0,                      
            angle=phi_min.get_value(),          
            arc_center=axes.c2p(0,0,0),
            color=GREEN
        ))
        phi_label = always_redraw(lambda: MathTex(r"\phi").move_to(axes.c2p(                      
                1.3 * np.cos(phi_min.get_value()/2),
                1.3 * np.sin(phi_min.get_value()/2),
                0
            )).set_color(GREEN).rotate(
            self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        line_P= always_redraw(lambda: DashedLine(
            start= axes.c2p(*get_current_start_p()),
            end= axes.c2p(get_current_start_p()[0], get_current_start_p()[1], 0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5
            ))

        line_PD= always_redraw(lambda: Line(
            start= axes.c2p(0,0,0),
            end= axes.c2p(get_current_start_p()[0], get_current_start_p()[1], 0),
            buff= 0,
            color= WHITE,
            stroke_width=3
            ))

        self.wait()
        self.play(Create(radius), Write(radius_label))
        self.play(Create(theta_arc), Write(theta_label))
        self.play(FadeIn(line_P), FadeIn(line_PD))
        self.play(Create(phi_arc), Write(phi_label))
        # 向量連動修正
        r_vector = always_redraw(lambda: Arrow(
            start=axes.c2p(*get_current_start_p()),
            end=axes.c2p(
                (r_min.get_value() + 1) * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                (r_min.get_value() + 1) * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                (r_min.get_value() + 1) * np.cos(theta_min.get_value())
            ),
            buff=0, color=ORANGE
        ))
        
        r_vec_label = always_redraw(lambda: MathTex(r"\hat{r}").set_color(ORANGE).move_to(axes.c2p(
                (r_min.get_value() + 1.5) * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                (r_min.get_value() + 1.5) * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                (r_min.get_value() + 1.5) * np.cos(theta_min.get_value())
            )).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        theta_vector = always_redraw(lambda: Arrow(
            start=axes.c2p(*get_current_start_p()),
            end=axes.c2p(
                get_current_start_p()[0] + 1 * np.cos(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                get_current_start_p()[1] + 1 * np.cos(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                get_current_start_p()[2] - 1 * np.sin(theta_min.get_value())
            ),
            buff=0, color=PURPLE
        ))
        
        theta_vec_label = always_redraw(lambda: MathTex(r"\hat{\theta}").set_color(PURPLE).move_to(axes.c2p(
                get_current_start_p()[0] + 1 * np.cos(theta_min.get_value()+15*DEGREES) * np.cos(phi_min.get_value()), 
                get_current_start_p()[1] + 1 * np.cos(theta_min.get_value()+15*DEGREES) * np.sin(phi_min.get_value()), 
                get_current_start_p()[2] - 1 * np.sin(theta_min.get_value()+15*DEGREES)
            )).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        phi_vector = always_redraw(lambda: Arrow(
            start=axes.c2p(*get_current_start_p()),
            end=axes.c2p(
                r_min.get_value() * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()) - np.sin(phi_min.get_value()),            
                r_min.get_value() * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()) + np.cos(phi_min.get_value()), 
                r_min.get_value() * np.cos(theta_min.get_value())
            ),
            buff=0, color=GREEN
        ))

        phi_vec_label = always_redraw(lambda: MathTex(r"\hat{\phi}").set_color(GREEN).move_to(axes.c2p(
                (r_min.get_value()) * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value())- np.sin(phi_min.get_value())-0.3 ,            
                (r_min.get_value()) * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value())+ np.cos(phi_min.get_value())+0.3, 
                (r_min.get_value()) * np.cos(theta_min.get_value())
            )).rotate(self.camera.get_phi(), axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        self.wait()
        self.begin_ambient_camera_rotation(rate=-0.1)
        self.wait(2)
        self.play(FadeIn(r_vector), Write(r_vec_label), run_time=2)
        self.wait(2)
        self.play(FadeIn(theta_vector), Write(theta_vec_label), run_time=2)
        self.wait(2)
        self.play(FadeIn(phi_vector), Write(phi_vec_label), run_time=2)
        self.wait(2)

        self.play(r_min.animate.set_value(3.5), run_time=2)
        self.play(r_min.animate.set_value(2), run_time=2)
        self.play(theta_min.animate.set_value(145 * DEGREES), run_time=2)
        self.play(theta_min.animate.set_value(30 * DEGREES), run_time=2)
        self.play(phi_min.animate.set_value(270 * DEGREES), run_time=4)
        self.play(phi_min.animate.set_value(30 * DEGREES), run_time=2)


        # 體積塊定義面 (修正 u,v 內部的 tracker 呼叫)
        def get_sphere_surface_r(r):
            return Surface(
                lambda u, v: np.array([r * np.sin(u) * np.cos(v), r * np.sin(u) * np.sin(v), r * np.cos(u)]),
                u_range=[theta_min.get_value(), theta_min.get_value()+ d_theta],
                v_range=[phi_min.get_value(), phi_min.get_value()+ d_phi],
                resolution=(8, 8), fill_opacity=0.6,
            )
        def get_sphere_surface_theta(theta):
            return Surface(
                lambda u, v: np.array([u * np.sin(theta) * np.cos(v), u * np.sin(theta) * np.sin(v), u * np.cos(theta)]),
                u_range=[r_min.get_value(), r_min.get_value()+dr],
                v_range=[phi_min.get_value(), phi_min.get_value()+ d_phi],
                resolution=(8, 8), fill_opacity=0.6,
            )
        def get_sphere_surface_phi(phi):
            return Surface(
                lambda u, v: np.array([u * np.sin(v) * np.cos(phi), u * np.sin(v) * np.sin(phi), u * np.cos(v)]),
                u_range=[r_min.get_value(), r_min.get_value()+ dr],
                v_range=[theta_min.get_value(), theta_min.get_value()+ d_theta],
                resolution=(8, 8), fill_opacity=0.6,
            )

        block = always_redraw(lambda: VGroup(
            get_sphere_surface_r(r_min.get_value()+ dr).set_fill(BLUE_A), get_sphere_surface_r(r_min.get_value()).set_fill(BLUE_E), 
            get_sphere_surface_theta(theta_min.get_value()+ d_theta).set_fill(PURPLE_E), get_sphere_surface_theta(theta_min.get_value()).set_fill(PURPLE_A),        
            get_sphere_surface_phi(phi_min.get_value()+ d_phi).set_fill(GREEN_E), get_sphere_surface_phi(phi_min.get_value()).set_fill(GREEN_A)
        ))

        outer_sphere = always_redraw(lambda: get_sphere_surface(r_min.get_value()+1).set_fill(WHITE))

        # 修正 DashedLine 語法錯誤 (補逗號)
        line_UR= always_redraw(lambda: Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.cos(theta_min.get_value())),
            buff= 0,
            color= WHITE,
            stroke_width=3,
            ))
        line_UL= always_redraw(lambda: Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                (r_min.get_value()) * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                (r_min.get_value()) * np.cos(theta_min.get_value())),
            buff= 0,
            color= WHITE,
            stroke_width=3,
            ))
        line_DL= always_redraw(lambda: Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()), 
                (r_min.get_value()) * np.cos(theta_min.get_value()+d_theta)),
            buff= 0,
            color= WHITE,
            stroke_width=3
            ))
        line_DR= always_redraw(lambda: Line(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.cos(theta_min.get_value()+d_theta)),
            buff= 0,
            color= WHITE,
            stroke_width=3
            ))
        line_PL= always_redraw(lambda: DashedLine(
            start= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()), 
                (r_min.get_value()) * np.cos(theta_min.get_value()+d_theta)),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5
            ))
        line_PR= always_redraw(lambda: DashedLine(
            start= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.cos(theta_min.get_value()+d_theta)),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()+d_phi), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5
            ))
        line_PDL= always_redraw(lambda: DashedLine(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5
            ))
        line_PDR= always_redraw(lambda: DashedLine(
            start= axes.c2p(0, 0, 0),
            end= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()+d_phi), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()+d_phi), 
                0),
            buff= 0,
            color= WHITE,
            dashed_ratio=0.5
            ))

        dr_radius= always_redraw(lambda: Line(
            start= axes.c2p((r_min.get_value()) * np.sin(theta_min.get_value()+d_theta/2) * np.cos(phi_min.get_value()+d_phi/2), 
                (r_min.get_value()) * np.sin(theta_min.get_value()+d_theta/2) * np.sin(phi_min.get_value()+d_phi/2), 
                (r_min.get_value()) * np.cos(theta_min.get_value()+d_theta/2)),
            end= axes.c2p((r_min.get_value()+dr) * np.sin(theta_min.get_value()+d_theta/2) * np.cos(phi_min.get_value()+d_phi/2), 
                (r_min.get_value()+dr) * np.sin(theta_min.get_value()+d_theta/2) * np.sin(phi_min.get_value()+d_phi/2), 
                (r_min.get_value()+dr) * np.cos(theta_min.get_value()+d_theta/2)),
            buff= 0,
            color= ORANGE,
            ))
        dr_label= always_redraw(lambda : MathTex(r"dr").next_to(dr_radius).set_color(ORANGE).rotate(self.camera.get_phi(), axis=RIGHT)
            .rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        d_theta_arc = always_redraw(lambda: ArcBetweenPoints(
            start= axes.c2p(1 * np.sin(theta_min.get_value()) * np.cos(phi_min.get_value()), 
                1 * np.sin(theta_min.get_value()) * np.sin(phi_min.get_value()), 
                1 * np.cos(theta_min.get_value())),
            end= axes.c2p(1 * np.sin(theta_min.get_value()+d_theta) * np.cos(phi_min.get_value()), 
                1 * np.sin(theta_min.get_value()+d_theta) * np.sin(phi_min.get_value()), 
                1 * np.cos(theta_min.get_value()+d_theta)),
            radius=1,
            color=PURPLE
        ))
        d_theta_label= always_redraw(lambda : MathTex(r"d\theta").next_to(d_theta_arc).set_color(PURPLE).rotate(self.camera.get_phi(), 
            axis=RIGHT).rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        d_phi_arc = always_redraw(lambda: Arc(
            radius=1,
            start_angle= phi_min.get_value(),                     
            angle= d_phi,          
            arc_center=ORIGIN,
            color= GREEN
        ))
        d_phi_label= always_redraw(lambda :MathTex(r"d\phi").next_to(d_phi_arc).set_color(GREEN).rotate(self.camera.get_phi(), axis=RIGHT)
            .rotate(self.camera.get_theta()+ 90*DEGREES, axis=OUT))

        self.play(Create(outer_sphere), FadeOut(inner_sphere))
        self.play(FadeIn(block), FadeIn(line_UR), FadeIn(line_UL), FadeIn(line_DR), FadeIn(line_DL), FadeIn(line_PR), FadeIn(line_PL), FadeIn(line_PDL), FadeIn(line_PDR),    
            FadeOut(r_vector), FadeOut(theta_vector), FadeOut(phi_vector), FadeOut(r_vec_label), FadeOut(theta_vec_label), FadeOut(phi_vec_label), 
            FadeOut(radius), FadeOut(theta_arc), FadeOut(phi_arc), FadeOut(radius_label), FadeOut(theta_label), FadeOut(phi_label), FadeOut(start_dot), FadeOut(line_P),
            FadeOut(line_PD) )
        self.play(Create(dr_radius), Write(dr_label), Create(d_theta_arc), Write(d_theta_label), Create(d_phi_arc), Write(d_phi_label))
        self.wait(2)
        self.begin_ambient_camera_rotation(rate= -0.2)
        self.wait(2)
        self.play(r_min.animate.set_value(3.5), run_time=2)
        self.play(r_min.animate.set_value(2), run_time=2)
        self.play(theta_min.animate.set_value(145 * DEGREES), run_time=2)
        self.play(theta_min.animate.set_value(30 * DEGREES), run_time=2)
        self.play(phi_min.animate.set_value(270 * DEGREES), run_time=4)
        self.play(phi_min.animate.set_value(30 * DEGREES), run_time=2)
        self.wait(4)
