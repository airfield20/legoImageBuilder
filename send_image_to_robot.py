import cv2, sys, numpy as np
from time import sleep

img_res = 32

colors = {
    'red': ([27, 40, 196], 2),
    'green': ([74, 151, 75], 6),
    'blue': ([171, 105, 13], 4),
    'white': ([242, 243, 242], 0),
    'yellow': ([47, 205, 245], 5),
    'black': ([52, 42, 27], 1),
    'orange': ([-1, -1, -1], 3)
}

gpio_map = [5, 6, 12, 13]  # output, output, output, input


def activate_gpio(color):
    if color in colors.keys():
        binary = [int(x) for x in list('{0:0b}'.format(colors[color][1]))]
        if len(binary) == 2:
            binary.insert(0, 0)
        if len(binary) == 1:
            binary.insert(0, 0)
            binary.insert(0, 0)
        print("Binary color code for " + str(colors[color][1]) + ": " + str(binary))
        for index, bit in enumerate(binary):
            if bit:
                print("Setting GPIO pin " + str(gpio_map[index]) + " ON")
            else:
                print("Setting GPIO pin " + str(gpio_map[index]) + " OFF")


def place_color(color):
    print("waiting for signal")
    # sleep(.5)
    print("Signal received, setting color: " + color)
    activate_gpio(color)


def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        print("Processing: " + fname)
    else:
        sys.stderr.write("Usage: python send_image_to_robot.py <imageFile>\n")
        return
    img = cv2.imread(fname)
    if img.shape[0] != img_res and img.shape[1] != img_res and img.shape[2] != 3:
        raise Exception("Image must be " + str(img_res) + "x" + str(img_res) + " in resolution")
    else:
        print("Image is correct resolution: " + str(img_res) + "x" + str(img_res))
    for i in xrange(img.shape[0]):
        for j in xrange(img.shape[1]):
            [r, g, b] = [img.item(i, j, 0), img.item(i, j, 1), img.item(i, j, 2)]
            pix = [r, g, b]
            for key in colors.keys():
                if pix == colors[key][0]:
                    place_color(key)
    print("Done")


if __name__ == '__main__':
    main()
