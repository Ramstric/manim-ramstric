from manimlib import *


class MainScene(Scene):
    def construct(self):
        grid = NumberPlane(
            x_range=(0, 8),
            y_range=(0, 25, 5),
            height=5,
            axis_config={"stroke_color": "#434343"},
            background_line_style={"stroke_color": "#434343", "stroke_width": 1.5},
            faded_line_ratio=0
        )

        # Number labels for the grid on the x-axis and y-axis.
        labels = VGroup()

        for value in range(0, 9):
            value_label = MarkupText(f"{value} s").set_color("#D4D4D4").scale(0.3)
            labels.add(value_label.copy().next_to(grid.coords_to_point(value, 0), direction=DOWN, buff=0.2))

        for value in range(0, 26, 5):
            value_label = MarkupText(f"{value} °C").set_color("#D4D4D4").scale(0.3)
            labels.add(value_label.copy().next_to(grid.coords_to_point(0, value), direction=LEFT, buff=0.2))

        # Remove top and right lines from the grid.
        grid.background_lines[4].set_stroke(width=0)
        grid.background_lines[12].set_stroke(width=0)

        # Labels for the x-axis and y-axis.
        y_label = MarkupText("Temperature").set_color("#D4D4D4").scale(0.35).rotate(90 * DEGREES).next_to(grid, direction=LEFT, buff=0.85)
        x_label = MarkupText("Time").set_color("#D4D4D4").scale(0.35).next_to(grid, direction=DOWN, buff=0.6)
        grid_labels = VGroup(x_label, y_label)

        self.play(ShowCreation(grid), ShowCreation(grid_labels), Write(labels)) # Show the grid, labels, and number labels.

        # Plot the temperature function and its equation.
        temperature_plot = grid.get_graph(lambda x: 10 * np.log(x + 0.2) + 0.5 * x ** 2 - 7.5 * x + 25, x_range=(0, 8))
        temperature_plot.set_color_by_xyz_func(glsl_snippet="y", colormap='inferno', min_value=-0.75, max_value=1.5)

        temperature_equation = Tex("T(t) = 10 \\ln(t + 0.2) + 0.5t^2 - 7.5t + 25")
        temperature_equation.set_color("#fbf591")
        temperature_equation.scale(0.5)

        temperature_equation.next_to(grid.coords_to_point(4, 23), direction=ORIGIN+UP, buff=0)

        self.play(ShowCreation(temperature_plot), Write(temperature_equation))  # Show the temperature plot and its equation.

        # Derivative of the temperature function.
        slope_tangent = grid.get_tangent_line(0, temperature_plot, length=1).set_color("#ed5858")
        slope_label = Tex("T'(t) =", font_size=24).set_color("#ed5858").next_to(slope_tangent, direction=np.array([1., 0., 0.]))
        slope_value = DecimalNumber(0, color="#ed5858", num_decimal_places=2, font_size=20, text_config={"font": "LM Roman 10"}).next_to(slope_label, direction=RIGHT)

        self.play(ShowCreation(slope_tangent), Write(slope_label), Write(slope_value))   # Show the tangent line and its label.

        tracker = ValueTracker(0)

        slope_tangent.add_updater(lambda m: m.become(grid.get_tangent_line(tracker.get_value(), temperature_plot, length=1)).set_color(slope_value.get_color()))
        slope_label.add_updater(lambda m: m.next_to(slope_tangent, direction=np.array([1., 0., 0.])).set_color(slope_value.get_color()))

        def slope_value_updater(mob):
            mob.set_value(10 / (tracker.get_value() + 0.2) + tracker.get_value() - 7.5).next_to(slope_label, direction=RIGHT, buff=0.1)
            if mob.get_value() < 0:
                mob.set_color("#7bb0ed")
            else:
                mob.set_color("#ed5858")

        slope_value.add_updater(slope_value_updater)

        self.play(tracker.animate.set_value(8), run_time=10)
        self.play(tracker.animate.set_value(0), run_time=10)
