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
            background_line_style={"stroke_color": "#FFFFFF", "stroke_width": 6},
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

        self.wait(1)

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

        image = cv2.imread("pikachu.png", cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_gray = cv2.imread("pikachu.png", cv2.IMREAD_GRAYSCALE)

        grid = NumberPlane(
            x_range=(0, 10),
            y_range=(-10, 0),
            axis_config={"stroke_color": "#434343"},
            background_line_style={"stroke_color": "#434343", "stroke_width": 1.5},
            faded_line_ratio=0
        )

        self.play(ShowCreation(grid), self.camera.frame.animate.scale(1.5))

        # Grid of pixels to draw lena_crop
        y_pos = 0

        pixels = VGroup()

        r_pixels = VGroup()
        g_pixels = VGroup()
        b_pixels = VGroup()

        for pixel_row in image:
            row = VGroup()

            r_row = VGroup()
            g_row = VGroup()
            b_row = VGroup()

            pixel_rectangle = None
            for pixel in pixel_row:
                # First pixel!
                if pixel_rectangle is None:
                    pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([pixel[0]/255, pixel[1]/255, pixel[2]/255]), fill_opacity=1).move_to(grid.coords_to_point(0.5, y_pos-0.5))
                    r_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([pixel[0]/255, 0, 0]), fill_opacity=0.25).move_to(grid.coords_to_point(0.5, y_pos-0.5))
                    g_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([0, pixel[1]/255, 0]), fill_opacity=0.25).move_to(grid.coords_to_point(0.5, y_pos-0.5))
                    b_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([0, 0, pixel[2]/255]), fill_opacity=0.25).move_to(grid.coords_to_point(0.5, y_pos-0.5))

                    row.add(pixel_rectangle)

                    r_row.add(r_pixel_rectangle)
                    g_row.add(g_pixel_rectangle)
                    b_row.add(b_pixel_rectangle)

                # Rest of pixels now have a reference to be positioned
                else:
                    pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([pixel[0]/255, pixel[1]/255, pixel[2]/255]), fill_opacity=1).next_to(pixel_rectangle, direction=RIGHT, buff=0)
                    r_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([pixel[0]/255, 0, 0]), fill_opacity=0.25).next_to(r_pixel_rectangle, direction=RIGHT, buff=0)
                    g_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([0, pixel[1]/255, 0]), fill_opacity=0.25).next_to(g_pixel_rectangle, direction=RIGHT, buff=0)
                    b_pixel_rectangle = Rectangle(width=1, height=1, stroke_width=0,
                        fill_color=rgb_to_color([0, 0, pixel[2]/255]), fill_opacity=0.25).next_to(b_pixel_rectangle, direction=RIGHT, buff=0)

                    row.add(pixel_rectangle)

                    r_row.add(r_pixel_rectangle)
                    g_row.add(g_pixel_rectangle)
                    b_row.add(b_pixel_rectangle)

            y_pos -= 1
            pixels.add(row)

            r_pixels.add(r_row)
            g_pixels.add(g_row)
            b_pixels.add(b_row)

        # Show the drawing px by px!
        for row in pixels:
            for pixel in row:
                self.play(FadeIn(pixel), run_time=0.01)

        for row, pixel_row in enumerate(image_gray):
            for col, pixel in enumerate(pixel_row):
                self.play(pixels[row][col].animate.set_fill(rgb_to_color([pixel/255, pixel/255, pixel/255])), run_time=0.01)

        self.remove(grid)
        grid.set_color("#FFFFFF")
        self.play(ShowCreation(grid))

        pixel_text = MarkupText("Cada pixel tiene un valor de intensidad entre 0 y 255, es decir que se representan con 8 bits de información").set_color("#D4D4D4").scale(0.5).next_to(grid, direction=UP, buff=0.6)
        self.play(Write(pixel_text))

        # Now, write the grayscale value of each pixel
        pixels_value = VGroup()
        for pixel_row in pixels:
            row = VGroup()

            for pixel in pixel_row:
                pixel_value = int(pixel.fill_color.hsl[2] * 255)  # We get the value...

                #Change font color for better legibility...
                if pixel_value > 127:
                    pixel_value = MarkupText(f"{pixel_value}").set_color("#000000").scale(0.5).next_to(pixel, direction=IN, buff=0.1)
                else:
                    pixel_value = MarkupText(f"{pixel_value}").set_color("#D4D4D4").scale(0.5).next_to(pixel, direction=IN, buff=0.1)

                self.play(Write(pixel_value), run_time=0.01)
                row.add(pixel_value)

            pixels_value.add(row)

        self.wait(2)

        # Ok, now clear the drawing and focus only on the first row...
        self.play(FadeOut(pixel_text),
                  FadeOut(grid))

        actual_row_pixels = pixels[0]

        self.play(*[FadeOut(row) for row in pixels[1:]],
                  *[FadeOut(row) for row in pixels_value[1:]],
                  self.camera.frame.animate.move_to(actual_row_pixels.get_center()))

        # Let's group up this row, pixels and values...
        pixel_complete = VGroup()
        for pixel_pair in zip(actual_row_pixels, pixels_value[0]):
            pixel_complete.add(VGroup(pixel_pair[0], pixel_pair[1]))

        # And now separate them...
        self.play(*[pixel[1].animate.shift((pixel[0] + 0.5) * RIGHT) for pixel in enumerate(pixel_complete[5:])],
                  *[pixel[1].animate.shift(abs(pixel[0] - 4.5) * LEFT) for pixel in enumerate(pixel_complete[:5])])

        # First task, show the values in binary...
        binary_pixel_values = [format(int(value.fill_color.hsl[2] * 255), '08b') for value in actual_row_pixels]

        pixel_text = MarkupText("En binario...").set_color("#FFFFFF").scale(0.5).next_to(actual_row_pixels, direction=DOWN, buff=0.6)
        self.play(Write(pixel_text))

        arrows = [Arrow(actual_row_pixels[i].get_bottom() + DOWN, actual_row_pixels[i].get_bottom() + DOWN * 2).set_color("#FFFFFF") for i in range(10)]
        self.play(*[FadeIn(arrow, shift=DOWN) for arrow in arrows])

        binary_values = VGroup()
        lsb_values = VGroup()
        for i, value in enumerate(binary_pixel_values):
            left_portion = MarkupText(f"{value[:4]}").set_color("#FFFFFF").scale(0.5)
            right_portion = MarkupText(f"{value[4:]}").set_color("#828282").scale(0.5).next_to(left_portion, direction=RIGHT, buff=0.1)
            binary_both_portions = VGroup(left_portion, right_portion)

            binary_both_portions.next_to(actual_row_pixels[i], direction=DOWN * 3, buff=0.7)

            binary_values.add(binary_both_portions)
            lsb_values.add(right_portion)

        self.play(FadeIn(binary_values, shift=DOWN))

        self.wait(2)

        # Let's clear off some stuff like the arrows and text...
        self.play(FadeOut(pixel_text),
                  *[FadeOut(arrow) for arrow in arrows],
                  *[value.animate.shift(UP * 1.5) for value in binary_values]
                  )

        # Now introduce the message to hide...
        mensaje = "pizza"

        pixel_text = MarkupText("Para codificar un mensaje cualquiera dentro de cada pixel, debemos de separarlo caracter por caracter").set_color("#FFFFFF").scale(0.5).next_to(actual_row_pixels, direction=DOWN * 2, buff=0.6)
        mensaje_text = MarkupText("Mensaje: ").set_color("#FFFFFF").scale(0.5).next_to(pixel_text, direction=DOWN, buff=0.6)
        mensaje_text_value = MarkupText(f"{mensaje}").set_color("#8bc272").scale(0.5).next_to(mensaje_text, direction=RIGHT, buff=0.3)

        self.play(Write(pixel_text))
        self.play(Write(mensaje_text), Write(mensaje_text_value))

        self.wait(2)

        self.play(FadeOut(pixel_text), FadeOut(mensaje_text), mensaje_text_value.animate.next_to(actual_row_pixels, direction=DOWN * 3, buff=0.6))
        self.play(*[mensaje_text_value[i].animate.next_to(actual_row_pixels[i*2], direction=DOWN * 2, buff=0.6).shift(RIGHT) for i in range(len(mensaje))], run_time=2)

        pixel_text = MarkupText("Recordando que cada caracter (8 bits cada uno) tiene un valor decimal correspondiente al codigo ASCII...").set_color("#FFFFFF").scale(0.5).next_to(mensaje_text_value, direction=DOWN, buff=1)

        self.play(Write(pixel_text))

        ascii_values = [ord(char) for char in mensaje]

        ascii_VGroup = VGroup()
        for value in ascii_values:
            ascii_text = MarkupText(f"{value}").set_color("#8bc272").scale(0.5)
            ascii_VGroup.add(ascii_text)

        for i in range(len(mensaje)):
            ascii_VGroup[i].next_to(mensaje_text_value[i], direction=DOWN, buff=0.5)

        self.play(Write(ascii_VGroup), run_time=4)

        self.wait(2)

        self.play(FadeOut(pixel_text))

        binary_ascii_values = [format(char, '08b') for char in ascii_values]

        binary_ascii = []
        for i, value in enumerate(binary_ascii_values):
            left_portion = MarkupText(f"{value[:4]}").set_color("#61AFEF").scale(0.5)
            right_portion = MarkupText(f"{value[4:]}").set_color("#E06C75").scale(0.5).next_to(left_portion,
                                                                                               direction=RIGHT,
                                                                                               buff=0.1)
            binary_both_portions = VGroup(left_portion, right_portion)

            binary_both_portions.next_to(ascii_VGroup[i], direction=IN, buff=0)

            binary_ascii.append(binary_both_portions)

        pixel_text = MarkupText("La idea está en dividir cada caracter en pares de 4 bits, e insertarlos en los 4 bits menos significativos de cada pixel").set_color("#FFFFFF").scale(0.5).next_to(mensaje_text_value, direction=DOWN, buff=1)

        self.play(Write(pixel_text))
        self.wait(2)

        self.play(Indicate(pixel_text[60:], color="#E5C07B", scale_factor=1.01), Indicate(VGroup(binary_pair[1] for binary_pair in binary_values), color="#E5C07B", scale_factor=1.01), run_time=6)
        self.wait(1)

        self.play(FadeOut(pixel_text))
        self.play(*[Transform(ascii_VGroup[i], binary_ascii[i]) for i in range(len(mensaje))])
        self.wait(1)

        pixel_text = MarkupText("Primero con una sencilla operación AND nos deshacemos de los 4 bits menos significativos de cada pixel").set_color("#FFFFFF").scale(0.5).next_to(pixel_complete, direction=UP, buff=1)

        self.play(Write(pixel_text))
        self.wait(2)

        for i in range(len(binary_pixel_values)):
            binary_pixel_values[i] = binary_pixel_values[i][:4] + "0000"

        self.play(Transform(lsb_values, VGroup(*[MarkupText("0000").set_color("#828282").scale(0.5).next_to(binary_both_portions[1], direction=ORIGIN, buff=0) for binary_both_portions in binary_values])),
                  Transform(pixels_value[0], VGroup(*[MarkupText(f"{int(binary_pixel_values[i], 2)}").set_color(pixels_value[0][i].get_color()).scale(0.5).next_to(pixels_value[0][i], direction=IN, buff=0) for i in range(len(pixels_value[0]))])),
                  *[actual_row_pixels[i].animate.set_fill(rgb_to_color([int(binary_pixel_values[i], 2) / 255, int(binary_pixel_values[i], 2) / 255, int(binary_pixel_values[i], 2) / 255])) for i in range(len(actual_row_pixels))]
                  )

        self.wait(1)

        self.play(Indicate(lsb_values, color="#E5C07B", scale_factor=1), run_time=6)

        self.play(FadeOut(pixel_text))

        pixel_text = Text("Nótese que los pixeles han cambiado ligeramente de color.\nLa elección de usar solo 4 bits ayuda a evitar que los cambios sean notorios.").set_color("#FFFFFF").scale(0.5).next_to(pixel_complete, direction=UP, buff=1)
        self.play(Write(pixel_text))
        self.wait(4)
        self.play(FadeOut(pixel_text))

        pixel_text = MarkupText("Luego con una operación OR insertamos los caracteres, por pares de pixeles").set_color("#FFFFFF").scale(0.5).next_to(pixel_complete, direction=UP, buff=1)
        self.play(Write(pixel_text))
        self.wait(2)

        for i in range(len(binary_ascii_values)):
            binary_pixel_values[i * 2] = binary_pixel_values[i * 2][:4] + binary_ascii_values[i][:4]
            binary_pixel_values[i * 2 + 1] = binary_pixel_values[i * 2 + 1][:4] + binary_ascii_values[i][4:]

        temp = VGroup(*[MarkupText(f"{binary_pixel_values[i][4:]}").set_color("#C678DD").scale(0.5).next_to(binary_both_portions[1], direction=ORIGIN, buff=0) for i, binary_both_portions in enumerate(binary_values)])
        for i in range(0, len(temp), 2):
            temp[i].set_color("#61AFEF")
            temp[i + 1].set_color("#E06C75")

        self.play(
            Transform(lsb_values, temp),
            Transform(pixels_value[0], VGroup(*[MarkupText(f"{int(binary_pixel_values[i], 2)}").set_color(pixels_value[0][i].get_color()).scale(0.5).next_to(pixels_value[0][i], direction=IN, buff=0) for i in range(len(pixels_value[0]))])),
            *[actual_row_pixels[i].animate.set_fill(rgb_to_color([int(binary_pixel_values[i], 2) / 255, int(binary_pixel_values[i], 2) / 255, int(binary_pixel_values[i], 2) / 255])) for i in range(len(actual_row_pixels))],
            FadeOut(ascii_VGroup, shift=UP),
            run_time=2
            )

        self.play(FadeOut(pixel_text))

        pixel_text = MarkupText("¡Ahora el mensaje se encuentra escondido en los pixeles de una imagen!").set_color("#FFFFFF").scale(0.5).next_to(pixel_complete, direction=UP, buff=1)

        self.play(Write(pixel_text))
        self.wait(2)
        self.play(FadeOut(pixel_text), FadeOut(mensaje_text_value))
        self.play(FadeOut(pixels_value[0]), FadeOut(binary_values))

        self.play(
            *[pixel[1].animate.shift((pixel[0] + 0.5) * LEFT) for pixel in enumerate(actual_row_pixels[5:])],
            *[pixel[1].animate.shift(abs(pixel[0] - 4.5) * RIGHT) for pixel in enumerate(actual_row_pixels[:5])],
            )

        self.play(
            *[FadeIn(row) for row in pixels[1:]],
            self.camera.frame.animate.move_to(pixels.get_center()).scale(1.2)
        )

        self.wait(2)

        pixel_text = Text("Para aplicar el mismo procedimiento en una imagen a color, la única diferencia es que se tienen tres canales de colores\nen los que se pueden esconder el mensaje ¡Pero el procedimiento es el mismo!").set_color("#FFFFFF").scale(0.5).next_to(grid, direction=UP, buff=0.6)

        self.play(FadeOut(pixels), Write(pixel_text))

        g_pixels.shift(RIGHT * 0.5 + DOWN * 0.5)
        b_pixels.shift(RIGHT * 1 + DOWN * 1)

        self.play(FadeIn(b_pixels, shift=DOWN))
        self.play(FadeIn(g_pixels, shift=DOWN))
        self.play(FadeIn(r_pixels, shift=DOWN))

        self.wait(2)

        self.play(r_pixels.animate.next_to(pixels, direction=IN, buff=0), g_pixels.animate.next_to(pixels, direction=IN, buff=0), b_pixels.animate.next_to(pixels, direction=IN, buff=0))
