import os
from PIL import Image, ImageSequence


def parseGIF(GIF_file):
	frames = []
	GIF_name = GIF_file.split('.')[0]
	for i, frame in enumerate(ImageSequence.Iterator(Image.open(GIF_file))):
		if i % 4 == 0:
			frame.save(f"imgs/{GIF_name}-{i}.png")
			frames.append(frame.copy())
	frames[0].save("out.gif", save_all=True, append_images=frames[1:])
if __name__ == "__main__":
	parseGIF("walk.gif")