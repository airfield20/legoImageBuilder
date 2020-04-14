import cv2
import sys
import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# Based on official lego color codes here http://www.peeron.com/cgi-bin/invcgis/colorguide.cgi
red = sRGBColor(27, 40, 196, is_upscaled=True)
green = sRGBColor(74, 151, 75, is_upscaled=True)
blue = sRGBColor(171, 105, 13, is_upscaled=True)
white = sRGBColor(242, 243, 242, is_upscaled=True)
yellow = sRGBColor(47,205,245, is_upscaled=True)
black = sRGBColor(52,42,27, is_upscaled=True)

new_res = 16

colors = [red, green, blue, white, yellow, black]

def sRGBToList(obj):
    return [int(obj.rgb_r * 255),int(obj.rgb_g *255),int(obj.rgb_b*255)]

def sRGBFromList(c):
    return sRGBColor(c[0],c[1],c[2],is_upscaled=True)

def color_distance(color1_rgb, color2_rgb):
    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)
    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)
    # Find the color difference
    return delta_e_cie2000(color1_lab, color2_lab)


def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        print(fname)
    else:
        sys.stderr.write("Usage: python legoImage.py <imageFile>\n")
        return
    img = cv2.imread(fname)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, channels = img.shape
    print("height, width = " + str(height) + ", " + str(width))
    if width > height:
        img = img[0:height, 0:height]
    elif height > width:
        img = img[0:width, 0:width]
    small_img = cv2.resize(img, (new_res, new_res))
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
    for row in range(new_res):
        for col in range(new_res):
            min_dist = 999999999999999999999
            interpolated_color = sRGBColor(0, 0, 0)
            for color in colors:
                if color_distance(color, sRGBFromList(small_img[row, col])) <= min_dist:
                    min_dist = color_distance(color, sRGBFromList(small_img[row, col]))
                    interpolated_color = color
            small_img[row, col] = sRGBToList(interpolated_color)

    print interpolated_color
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", 600, 600)
    cv2.imshow("image", small_img)
    cv2.imwrite(fname + ".processed.png", small_img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
