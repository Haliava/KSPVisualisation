from manim import *
from math import *
from random import randint

G = 6.6743 / (10 ** 11)  # гравитационная постоянная
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
        return int(sqrt(G * planetM / (planetR + H)))


for i in range(100000, 1000000):
    print(MathModel.get_first_escape_velocity(planetR=i))