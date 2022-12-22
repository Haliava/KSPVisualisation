import numpy as np
from manim import *
from math import *
from random import randint

G = 6.6743 * (10 ** (-11))  # гравитационная постоянная
H = 0
earthR = 600000
earthM = 5.29 * 10 ** 22  # масса Земли
marsM = 6.4171 * 10 ** 23  # масса Марса


class MathModel:
    def __init__(self):
        pass

    @staticmethod
    def get_first_escape_velocity(planetM=earthM, planetR=earthR, H=H):
        """
        Первая космическая скорость

        :param planetM:
        :param planetR:
        :return: первую космическая скорость
        """
        return sqrt(G * planetM / (planetR + H))

    @staticmethod
    def get_second_escape_velocity(planetM=earthM, planetR=earthR, H=H):
        """
        Вторая космическая скорость

        :param planetM:
        :param planetR:
        :return: вторую космическая скорость
        """
        return sqrt(G * planetM / (planetR + H)) * sqrt(2)


class GraphScene(Scene):
    graphCount = 0
    drawnGraphs = []

    def create_graph(
            self,
            x_range, y_range, numbers_to_include_x, numbers_to_include_y,  # axis
            init_x, end_x_value, name_x_axis, name_y_axis,  # values
            func, func2  # funcs
    ):
        """
        Создаёт ось с друмя графиками

        :param x_range: начало, конец, частота засечек оси абсцисс
        :param y_range: начало, конец, частота засечек оси ординат
        :param numbers_to_include_x: какие из значений оси абсцисс подписать
        :param numbers_to_include_y:какие из значений оси ординат подписать
        :param init_x: стартовый X
        :param end_x_value: конечный X
        :param name_x_axis: как подписать ось абсцисс
        :param name_y_axis: как подписать ось ординат
        :param func: первая функция
        :param func2: вторая функция
        :return: график + его анимации
        """

        ax = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={
                "include_tip": False,
                "numbers_to_include": numbers_to_include_y,
            },
            x_axis_config={
                "include_tip": False,
                "numbers_to_include": numbers_to_include_x,
            },
            tips=False
        )
        labels = ax.get_axis_labels(x_label=name_x_axis, y_label=name_y_axis)

        def create_path(func, color):
            value_tracker = ValueTracker(init_x)
            path = VMobject(color=color)
            dot = Dot(point=[ax.coords_to_point(value_tracker.get_value(), func(value_tracker.get_value()))],
                      color=color)
            path.set_points_as_corners([dot.get_center(), dot.get_center()])

            graph = ax.plot(func, color=color)

            graph_value_text = DecimalNumber(
                func(value_tracker.get_value()),
                num_decimal_places=2,
                stroke_width=2,
            ).next_to(dot, DOWN, buff=0.25)

            path.add_updater(lambda x: update_path(x, dot))
            graph_value_text.add_updater(lambda x: update_func_value_text(x, func, dot, value_tracker))

            return [graph, graph_value_text, path, dot, value_tracker]

        def update_path(path, dot):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

        def update_func_value_text(text, func, dot, value_tracker):
            text.set_value(func(value_tracker.get_value())).next_to(dot, DOWN, buff=0.25)

        graph1, graph_value_text1, path1, dot1, value_tracker1 = create_path(func, RED)
        graph2, graph_value_text2, path2, dot2, value_tracker2 = create_path(func2, RED)

        self.add(path1, dot1, graph_value_text1)
        self.play(DrawBorderThenFill(ax), Write(labels), Write(graph_value_text1))
        self.play(MoveAlongPath(dot1, graph1, rate_func=smooth),
                  value_tracker1.animate.set_value(end_x_value), run_time=5)
        self.remove(path1)
        self.add(graph1)

        self.add(path2, dot2, graph_value_text2)
        self.play(FadeIn(dot2, graph_value_text2))
        self.play(MoveAlongPath(dot2, graph2, rate_func=smooth, run_time=5),
                  value_tracker2.animate.set_value(end_x_value),
                  run_time=5)
        self.remove(path2)
        self.add(graph2)

        graph_value_text1.remove_updater(update_func_value_text)
        graph_value_text2.remove_updater(update_func_value_text)

        graphObj = Mobject()
        graphObj.submobjects = [ax, dot1, dot2, graph1, graph2, labels]

        self.wait()

        ax.axis_config["numbers_to_include"] = []
        ax.axis_labels = ["", ""]

    def construct(self):
        '''self.create_graph(
           [100, 1000, 100], [500, 3000, 1000], [100, 300, 700, 900], [500, 1000, 1500, 2000, 2500, 3000],
           100, 1000, "R,m*1000", "v(R),m/s", lambda x: MathModel.get_first_escape_velocity(planetR=x * 10000),
           lambda x: MathModel.get_second_escape_velocity(planetR=x * 10000)
        )'''

        '''self.create_graph(
           [3, 30000, 5000], [500, 25000, 5000], np.arange(500, 30000 + 1, 5000), np.arange(500, 25000 + 1, 5000),
           3, 30000, "M,kg*10^{20}", "v(M),m/s", lambda x: MathModel.get_first_escape_velocity(planetM=x * 10 ** 20),
           lambda x: MathModel.get_second_escape_velocity(planetM=x * 10 ** 20)
        )'''

        self.create_graph(
            [70000, 200000, 20000], [2700, 3500, 200], np.arange(70000, 200001, 20000), np.arange(2700, 3500, 200),
            70000, 200000, "H,m", "v(H),m/s", lambda x: MathModel.get_second_escape_velocity(H=x),
            lambda x: MathModel.get_first_escape_velocity(H=x)
        )
