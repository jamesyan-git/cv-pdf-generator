import os, sys
from PIL import Image

size = (115, 115)
for infile in os.listdir("images/missed/"):
    outfile = "small_" + infile
    # print(infile)
    if infile != outfile:
        try:

            im = Image.open("images/missed/" + infile)

            width, height = im.size

            if width < height:   # portrait image
                ratio = height / 115
                temp_height = 115
                temp_width = width / ratio
                size = (temp_width, temp_height)
            elif height > width: # Landscape image
                ratio = width / 115
                temp_height = height / ratio
                temp_width = 115
                size = (temp_height, temp_width)
            else:                # equal
                size = (115, 115)

            im.thumbnail(size, Image.ANTIALIAS)
            im.save("images/resized/" + outfile, "JPEG")
        except IOError:
            print("Error\n", infile)