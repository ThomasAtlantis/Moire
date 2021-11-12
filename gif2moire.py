import os
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def parseGIF(GIF_file, frame_num=8):
	
	img_it = ImageSequence.Iterator(Image.open(GIF_file))
	frames = [np.array(frame.copy().convert("L")) for frame in img_it]
	frames = frames[::len(frames) // frame_num]
	
	patern = np.ones_like(frames[0])
	index = lambda i: (slice(None), slice(i, None, frame_num))
	for i, frame in enumerate(frames): patern[index(i)] = frame[index(i)]

	# Image.fromarray(255 - patern[100:-100, 250:-250]).convert("L").save('1.png')

	fig = plt.figure()
	plt.xticks([])
	plt.yticks([])

	def card_when(t):
		card = np.zeros_like(patern)
		card[:, t::frame_num] = 1
		return card
	# to_save = 255 * np.repeat(np.expand_dims(1 - card_when(0), -1), 4, axis=-1)
	# to_save[card_when(0) == 1][-1] = 0
	# print(to_save.shape)
	# Image.fromarray(to_save).convert("RGBA").save('3.png')
	canvas = plt.imshow(patern * card_when(t=0))
	animat = animation.FuncAnimation(
		fig, lambda t: canvas.set_data(patern * card_when(t=t%100)), interval=200)
	plt.show()
	# animat.save("/Users/liushangyu/Desktop/out.gif")  # 谨慎使用，输出文件巨大

if __name__ == "__main__":
	parseGIF("/Users/liushangyu/Downloads/walk.gif", frame_num=7)