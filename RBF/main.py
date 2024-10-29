from manimlib import *
import cv2

class MainScene(Scene):
    def construct(self):

        lena_img = ImageMobject("lena.bmp")
        lena_img.scale(2)

        self.play(FadeIn(lena_img))

        grid = NumberPlane(
            x_range=(0, 8),
            y_range=(-8, 0),
            axis_config={"stroke_color": "#FFFFFF"},
            background_line_style={"stroke_color": "#FFFFFF", "stroke_width": 1},
            faded_line_ratio=64
        )


        self.play(
            # Set the size with the width of a object
            self.camera.frame.animate.scale(1.5)
        )

        # Label the width and height of the image along with a line to show the width of the image.

        width_label = MarkupText("Ancho y Alto de 512 pixeles").set_color("#D4D4D4").scale(0.5).next_to(grid, direction=UP, buff=0.6)
        width_line = Line(grid.coords_to_point(0, 0.5), grid.coords_to_point(8, 0.5)).set_color("#D4D4D4")
        heigh_line = Line(grid.coords_to_point(-0.5, 0), grid.coords_to_point(-0.5, -8)).set_color("#D4D4D4")

        self.play(Write(width_label), ShowCreation(width_line), ShowCreation(heigh_line))

        self.wait(2)

        self.play(ShowCreation(grid))


        self.play(
            # Set the size with the width of a object
            self.camera.frame.animate.scale(0.1).move_to(lena_img.get_center())
        )

        self.play(self.camera.frame.animate.shift(UP * 2))

        self.play(self.camera.frame.animate.shift(LEFT * 2))

        self.play(self.camera.frame.animate.shift(DOWN * 2))

        self.play(self.camera.frame.animate.shift(RIGHT * 2))





class PixelGrid(Scene):
    def construct(self):

        lena_img = ImageMobject("lena.bmp")
        lena_crop = cv2.imread("lena-crop-small.bmp", cv2.IMREAD_GRAYSCALE)

        grid = NumberPlane(
            x_range=(0, 10),
            y_range=(-10, 0),
            axis_config={"stroke_color": "#434343"},
            background_line_style={"stroke_color": "#434343", "stroke_width": 1.5},
            faded_line_ratio=0
        )

        self.play(ShowCreation(grid))

        y_pos = 0
        pixels = []
        for pixel_row in lena_crop:
            row = VGroup()
            pixel_rectangle = None
            for pixel in pixel_row:
                if pixel_rectangle is None:
                    pixel_rectangle = Rectangle(
                        width=1,
                        height=1,
                        stroke_width=0,
                        fill_color=rgb_to_color([pixel/255, pixel/255, pixel/255]),
                        fill_opacity=1
                    )

                    pixel_rectangle.move_to(grid.coords_to_point(0.5, y_pos-0.5))
                    row.add(pixel_rectangle)
                    #self.play(ShowCreation(pixel_rectangle), run_time=0.01)

                else:
                    pixel_rectangle = Rectangle(
                        width=1,
                        height=1,
                        stroke_width=0,
                        fill_color=rgb_to_color([pixel/255, pixel/255, pixel/255]),
                        fill_opacity=1
                    ).next_to(pixel_rectangle, direction=RIGHT, buff=0)
                    row.add(pixel_rectangle)
                    #self.play(ShowCreation(pixel_rectangle), run_time=0.01)

            y_pos -= 1
            pixels.append(row)

        for row in pixels:
            for pixel in row:
                #self.play(FadeIn(pixel), run_time=0.01)
                self.add(pixel)

        self.remove(grid)

        grid.set_color("#FFFFFF")

        self.play(ShowCreation(grid))

        #self.wait(2)

        pixel_text = MarkupText("Cada pixel tiene un valor de intensidad entre 0 y 255, es decir que se representan con 8 bits de información").set_color("#D4D4D4").scale(0.5).next_to(grid, direction=UP, buff=0.6)
        self.play(Write(pixel_text))

        #self.wait(2)

        for row in pixels:
            for pixel in row:
                pixel_value = int(pixel.fill_color.hsl[2] * 255)
                if pixel_value > 127:
                    pixel_text = MarkupText(f"{pixel_value}").set_color("#000000").scale(0.5).next_to(pixel, direction=IN, buff=0.1)
                else:
                    pixel_text = MarkupText(f"{pixel_value}").set_color("#D4D4D4").scale(0.5).next_to(pixel, direction=IN, buff=0.1)
                self.play(Write(pixel_text), run_time=0.01)



