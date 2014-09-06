#coding=utf8
from PIL import Image
import math
import unittest
import dafiti_image


#000 BLACK
#F00 RED
#0F0 GREEN
#00F BLUE
#0FF CYAN
#F0F MAGENTA
#FF0 YELLOW
#FFF WHITE
COLORS = {
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
}


class TestInternetMethod1(unittest.TestCase):
    def process_file(self, filename):
        return dafiti_image.colorz(filename, 3, (1/3, 1/3, 2/3, 2/3))

    def test_simple_file_processing1(self):
        self.assertEqual(
            self.process_file("test_images/verde.jpeg"),
            'CYAN')

    def test_super_simple_file_processing(self):
        self.assertEqual(
            self.process_file("test_images/verde_quad.jpeg"),
            'GREEN')

    def test_simple_file_processing2(self):
        self.assertEqual(
            self.process_file("test_images/DSC099522.jpg"),
            'RED')

    def test_complex_file_processing1(self):
        self.assertEqual(
            self.process_file("test_images/white_lady.jpeg"),
            'WHITE')

    def test_unknown_color_file_processing2(self):
        self.assertEqual(
            self.process_file("test_images/phoebe.jpeg"),
            'BLACK')


class TestDafitiMethod(unittest.TestCase):

    def find_color(self, mycolor):
        color_found = None
        min_dist = 999999999

        for color_name, color in COLORS.items():
            dist = math.sqrt(
                math.pow(mycolor[0] - color[0], 2) +
                math.pow(mycolor[1] - color[1], 2) +
                math.pow(mycolor[2] - color[2], 2))
            # print color_name, dist
            if color_found is None or dist < min_dist:
                color_found = color_name
                min_dist = dist

        # print color_found
        return color_found

    def process_file(self, filename):
        myimage = Image.open(filename)
        myimage.load()

        # print(myimage.format, myimage.size, myimage.mode)

        hist = dict(zip(COLORS.keys(), [0]*len(COLORS)))
        for x in xrange(1, myimage.size[0]):
            for y in xrange(1, myimage.size[1]):
                if x > myimage.size[0]/3 and x < 2*myimage.size[0]/3 and \
                        y > myimage.size[1]/3 and y < 2*myimage.size[1]/3:
                    hist[self.find_color(myimage.getpixel((x, y)))] += 1

        print sorted(hist.items(), key=lambda x: -x[1])
        return sorted(hist.items(), key=lambda x: -x[1])[0][0]

    def test_simple_file_processing1(self):
        self.assertEqual(
            self.process_file("test_images/verde.jpeg"),
            'CYAN')

    def test_super_simple_file_processing(self):
        self.assertEqual(
            self.process_file("test_images/verde_quad.jpeg"),
            'GREEN')

    def test_simple_file_processing2(self):
        self.assertEqual(
            self.process_file("test_images/DSC099522.jpg"),
            'RED')

    def test_complex_file_processing1(self):
        self.assertEqual(
            self.process_file("test_images/white_lady.jpeg"),
            'WHITE')

    def test_unknown_color_file_processing2(self):
        self.assertEqual(
            self.process_file("test_images/phoebe.jpeg"),
            'BLACK')

if __name__ == '__main__':
    unittest.main()
