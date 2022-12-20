from manim import *
from math import *
from random import randint

G = 6.6743 * (10 ** (-11))  # гравитационная постоянная
H = 0
earthR = 600000
earthM = 5.29 * 10 ** 22  # масса Земли
marsM = 6.4171 * 10 ** 23  # масса Марса
Tsyn_Mars = 2.135  # синодичечский период Марса
Tsyn_Earth = 1.0  # т.к. взлёт производится с поверзности Земли, о её синодический пероид можно принять за 1


class MathModel:
    def __init__(self):
        pass

    @staticmethod
    def delta_horizontal_speed(P, Ax, v, m):
        """
        dVx / dt

        :param P: сила тяги двигателя
        :param Ax: продольная сила
        :param v: угол тангажа
        :param m: масса летательного аппарата
        :return: dVx / dt
        """
        return (P + Ax) * cos(v) / m

    @staticmethod
    def delta_vertical_speed(P, Ay, v, m):
        """
        dVy / dt

        :param P: сила тяги двигателя
        :param Ay: нормальная сила
        :param v: угол тангажа
        :param m: масса летательного аппарата
        :return: dVy / dt
        """
        return (P + Ay) * sin(v) / m

    first_escape_velocity_formula = r"\sqrt{\frac{GM}{R + h}}"

    @staticmethod
    def get_first_escape_velocity(planetM=earthM, planetR=earthR, H=H):
        """
        Первая космическая скорость

        :param planetM:
        :param planetR:
        :return: вторую космическая скорость
        """
        return sqrt(G * planetM / (planetR + H))

    @staticmethod
    def get_traction_force(Wsec, Va, pa, ph, Sa):
        """
        Сила тяги ракетного двигателя

        :param Wsec: секундный расход массы топлива
        :param Va: скорость выброса Wsec
        :param pa: высота 1
        :param ph: высота 2
        :param Sa: площадь летательного аппарата
        :return: силу тяги ракетного двигателя
        """
        return Wsec * Va + (pa - ph) * Sa

    @staticmethod
    def get_Tsyn_vessel():
        """
        Синодический период

        :return: синодический период тела
        """
        return Tsyn_Earth * Tsyn_Mars / (Tsyn_Mars - Tsyn_Earth)

    @staticmethod
    def tsiolkovsky_formula(u, m0, m):
        """
        Формула Циолковского

        :param u: удельный импульс ракетного двигателя
        :param m0: начальная масса летательного аппарата
        :param m: конечная масса летательного аппарата
        :return: скорость, которую развивает летательный аппарат под воздействием тяги
        """
        return u * log(m0 / m)


class GraphScene(Scene):
    graphCount = 0
    drawnGraphs = []

    def create_graph(
            self,
            x_range, y_range, numbers_to_include_x, numbers_to_include_y,  # axis
            init_x, name_x_axis, name_y_axis, func,  # init values
            end_x_value, math_tex_func,  # end values
    ):
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

        x = ValueTracker(init_x)
        value = name_y_axis

        def create_path(func):
            path = VMobject(color=MAROON)
            dot = Dot(point=[ax.coords_to_point(x.get_value(), func(x.get_value()))], color=MAROON)
            path.set_points_as_corners([dot.get_center(), dot.get_center()])

            graph = ax.plot(func, color=MAROON)

            graph_value_text = DecimalNumber(
                func(x.get_value()),
                num_decimal_places=2,
                stroke_width=2,
            ).next_to(dot, DOWN, buff=0.25)

            path.add_updater(update_path)
            graph_value_text.add_updater(update_func_value_text)

        path = VMobject(color=MAROON)
        dot = Dot(point=[ax.coords_to_point(x.get_value(), func(x.get_value()))], color=MAROON)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        graph = ax.plot(func, color=MAROON)

        graph_value_text = DecimalNumber(
            func(x.get_value()),
            num_decimal_places=2,
            stroke_width=2,
        ).next_to(dot, DOWN, buff=0.25)

        def update_path(path, dot):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

        def update_func_value_text(text, func, dot):
            text.set_value(func(x.get_value())).next_to(dot, DOWN, buff=0.25)

        path.add_updater(update_path)
        graph_value_text.add_updater(update_func_value_text)

        self.add(path, dot, graph_value_text)
        self.play(DrawBorderThenFill(ax), Write(labels), Write(graph_value_text))
        self.play(MoveAlongPath(dot, graph, rate_func=smooth, run_time=5), x.animate.set_value(end_x_value), run_time=5)
        self.remove(path)
        self.add(graph)

        graph_value_text.remove_updater(update_func_value_text)

        graphObj = Mobject()
        graphObj.submobjects = [ax, dot, graph, labels]

        self.wait()

        ax.axis_config["numbers_to_include"] = []
        ax.axis_labels = ["", ""]

        self.play(
            graphObj.animate.scale(0.3),
            graph_value_text.animate.move_to(graphObj.get_center()), rate_func=linear, run_time=1.5
        )

        funcText = MathTex(f"{value} = " + math_tex_func).next_to(graphObj, UP)
        funcText.font_size = DEFAULT_FONT_SIZE

        graph_value_text.set_value(func(x.get_value()))
        graph_value_text.font_size = DEFAULT_FONT_SIZE
        self.play(FadeIn(funcText))

        graphObj.submobjects.append(funcText)
        graphObj.submobjects.append(graph_value_text)
        self.wait()
        self.play(graph_value_text.animate.scale(1.5))

        if self.graphCount <= 0:
            self.play(
                graphObj.animate.to_edge(UR), run_time=2, buff=0.5, rate_func=smooth
            )
        else:
            self.play(
                graphObj.animate.next_to(self.drawnGraphs[-1], DOWN), buff=1
            )
        self.wait()

        self.graphCount += 1
        self.drawnGraphs.append(graphObj)

    def construct(self):
        self.create_graph(
            [100, 1000, 100], [500, 2000, 1000], [100, 300, 700, 1000], [500, 1000, 1500, 2000],
            100, "R", "v(R)", lambda x: MathModel.get_first_escape_velocity(planetR=x * 10000),
            1000, MathModel.first_escape_velocity_formula
        )
# 3*10^20 кг до 3*10^24
# self.create_graph(
#    [0.3, 3000, 100], [0, 3000, 150], np.arange(-1, 1, 1), np.arange(-1, 1, 1),
#    -1, "x", "f(x)", lambda x: MathModel.get_first_escape_velocity(planetM=x),
#    1, MathModel.first_escape_velocity_formula
# )