from manim import *
from PIL import Image
import numpy as np
import random

class MovingAround(Scene):
	def construct(self):
		self.add_sound("0.wav")
		pad = VGroup()
		for i in range(6):
			pad_line = VGroup(*[Text("BARRIER-GRID ANIMATION", fill_opacity=0.2, stroke_width=2, color=WHITE).scale(2) for i in range(10)])
			pad_line.arrange_in_grid(rows=1, buff=0.2)
			pad.add(pad_line)
		pad.arrange_in_grid(rows=6, buff=0.2)
		animate_tmp = []
		for i in range(6):
			if i % 2 == 0:
				animate_tmp.append(pad.submobjects[i].animate.shift(LEFT * random.random() * 5))
			else:
				animate_tmp.append(pad.submobjects[i].animate.shift(RIGHT * random.random() * 5))
		self.play(*animate_tmp)
		with register_font("/System/Library/Fonts/PingFang.ttc"):
			title = Text("栅格动画原理", font="PingFang", color=BLUE, weight=BOLD, fill_opacity=1)
		self.play(Write(title), pad.animate.set_opacity(0.2))
		self.play(title.animate.scale(1.5), run_time=0.5)
		self.play(title.animate.scale(1.5), run_time=0.5)
		author = Text("清川@Zhihu", font="PingFang", color=WHITE, fill_opacity=1).scale(0.8).next_to(title, DOWN * 0.5)
		website = Text("https://liushangyu.xyz", font="PingFang", color=WHITE, fill_opacity=1).scale(0.5).next_to(author, DOWN * 0.1)
		self.play(Write(author), Write(website))
		self.add_sound("1.mp3")
		self.wait(5)
		self.clear()
		
		line = Line(LEFT * 7, LEFT * 6)

		patern = Image.open('/Users/liushangyu/Desktop/1.png').convert("RGBA")
		patern = ImageMobject(np.array(patern).astype(np.uint8))
		patern.scale(3)

		raster = Image.open('/Users/liushangyu/Desktop/3.png').convert("RGBA")
		raster = ImageMobject(np.array(raster).astype(np.uint8)).shift(LEFT * 7)
		raster.scale(3)

		circles = [Circle(radius=1, color=BLUE, fill_opacity=0.5, stroke_width=1).shift(UP) for i in range(2)]
		circles_t = [Circle(radius=1, color=BLUE, fill_opacity=0.5, stroke_width=1).shift(UP) for i in range(4)]
		circles_t_text = [MathTex(f"t={i}").shift(RIGHT * 4).shift(UP) for i in range(4)]
		for i in range(4): 
			circles_t[i].shift(DOWN * i)
			circles_t_text[i].shift(DOWN * i)
		
		self.play(FadeIn(circles[0]))
		self.add_sound("2.mp3")
		self.wait(3)
		self.play(circles[0].animate.shift(DOWN * 3), run_time=1)
		self.play(FadeOut(circles[0]), run_time=0.2)
		self.play(FadeIn(circles[1]))
		self.play(circles[1].animate.shift(DOWN * 3), run_time=1)
		self.play(FadeOut(circles[1]), run_time=0.2)
		self.add_sound("3.mp3")
		self.wait(3)

		for i in range(4):
			self.play(FadeIn(circles_t[i]), Write(circles_t_text[i]))
		self.play(
			circles_t[0].animate.shift(LEFT * 1.5 * 3), 
			circles_t_text[0].animate.shift(LEFT * 1.5 * 3).shift(UP * 2).shift(LEFT * 4),
			circles_t[1].animate.shift(LEFT * 0.5 * 3),
			circles_t_text[1].animate.shift(LEFT * 0.5 * 3).shift(UP * 3).shift(LEFT * 4),
			circles_t[2].animate.shift(RIGHT * 0.5 * 3), 
			circles_t_text[2].animate.shift(RIGHT * 0.5 * 3).shift(UP * 4).shift(LEFT * 4),
			circles_t[3].animate.shift(RIGHT * 1.5 * 3),
			circles_t_text[3].animate.shift(RIGHT * 1.5 * 3).shift(UP * 5).shift(LEFT * 4),
		)
		rectans = VGroup(*[Rectangle(width=0.1, height=2.0, color=RED, fill_opacity=0.2, stroke_width=1) for i in range(20)])
		rectans.arrange_in_grid(rows=1, buff=0)
		rectans_copies = [rectans.copy().shift(circles_t[i].get_center() - rectans.get_center()) for i in range(4)]
		self.add_sound("4.mp3")
		self.wait(4)
		self.play(*[FadeIn(r) for r in rectans_copies], run_time=1)
		self.add_sound("5.mp3")
		self.wait(8)
		for i in range(4):
			animate_tmp = []
			for j in range(20):
				if (j - i) % 4 == 0: continue
				animate_tmp.append(rectans_copies[i].submobjects[j].animate.set_fill(BLACK).set_opacity(1))
			self.play(*animate_tmp, run_time=1.5)
			if i == 0:
				self.add_sound("6.mp3")
				self.wait(5.2)
		self.add_sound("7.mp3")
		self.wait(4)
		grided_circles = [VGroup(circles_t[i], rectans_copies[i]) for i in range(4)]
		animate_tmp = []
		for i in range(4):
			for j in range(20):
				if (j - i) % 4 == 0:
					animate_tmp.append(rectans_copies[i].submobjects[j].animate.set_opacity(0))
				animate_tmp.append(rectans_copies[i].submobjects[j].animate.set_stroke(width=0))
		self.play(*animate_tmp, run_time=1.5)
		grided_circles_img = [np.array(g.get_image().convert("RGBA")) for g in grided_circles]
		for c in grided_circles_img:
			for x in range(c.shape[0]):
				for y in range(c.shape[1]):
					if np.mean(c[x, y][:3]) < 30:
						c[x, y][-1] = 0
		grided_circles_img = [ImageMobject(g.astype(np.uint8)).scale_to_fit_height(8) for g in grided_circles_img]
		self.play(*[FadeOut(g) for g in grided_circles], run_time=0)
		self.play(*[FadeOut(t) for t in circles_t_text], run_time=0)
		self.play(
			MoveAlongPath(grided_circles_img[0], 
				Line(grided_circles_img[0].get_center(), grided_circles_img[0].get_center() + RIGHT * 1.5 * 3),
				rate_func=rate_functions.linear),
			MoveAlongPath(grided_circles_img[1], 
				Line(grided_circles_img[1].get_center(), grided_circles_img[1].get_center() + RIGHT * 0.5 * 3),
				rate_func=rate_functions.linear),
			MoveAlongPath(grided_circles_img[2], 
				Line(grided_circles_img[2].get_center(), grided_circles_img[1].get_center() + LEFT * 0.5 * 3),
				rate_func=rate_functions.linear),
			MoveAlongPath(grided_circles_img[3], 
				Line(grided_circles_img[3].get_center(), grided_circles_img[1].get_center() + LEFT * 1.5 * 3),
				rate_func=rate_functions.linear)
		)
		rectans_raster = VGroup(*[Rectangle(width=0.3, height=8.0, color=GREY, fill_opacity=1, stroke_width=1) for i in range(40)])
		rectans_raster.arrange_in_grid(rows=1, buff=0.1).shift(LEFT * 6)
		self.add_sound("8.mp3")
		self.wait(7.5)
		self.play(FadeIn(rectans_raster))
		self.play(MoveAlongPath(rectans_raster, Line(LEFT * 6, LEFT * 2.96), rate_func=rate_functions.linear), run_time=5)
		self.add_sound("9.mp3")
		self.wait(3.7)
		self.add_sound("10.mp3")
		self.wait(12.5)
		self.play(rectans_raster.animate.set_fill(RED_B))
		self.play(rectans_raster.animate.set_opacity(0.2))
		self.play(MoveAlongPath(rectans_raster, Line(LEFT * 2.96, LEFT * 0.04), rate_func=rate_functions.linear), run_time=5)
		self.add_sound("11.mp3")
		self.wait(13.8)
		self.play(rectans_raster.animate.set_opacity(1))
		self.play(rectans_raster.animate.set_fill(GREY))
		self.play(MoveAlongPath(rectans_raster, Line(LEFT * 0.04, RIGHT * 3.03), rate_func=rate_functions.linear), run_time=3)
		self.wait()
		self.add_sound("12.mp3")
		self.wait(10)
		self.clear()

		self.play(FadeIn(patern))
		self.play(FadeIn(raster))
		self.play(MoveAlongPath(raster, line, rate_func=rate_functions.ease_in_bounce), run_time=5)
		self.play(FadeOut(raster, shift=DOWN * 2, scale=2))
		self.wait()
		self.clear()

		main_page = Image.open('0.png').convert("RGB")
		main_page = ImageMobject(np.array(main_page).astype(np.uint8))
		main_page.height = 7
		self.play(FadeIn(main_page))
		self.add_sound("13.mp3")
		self.wait(21)
		self.add_sound("1.wav")
		self.wait(1)

