import argparse

from gym_pybullet_drones.envs.BaseAviary import DroneModel, Physics
from gym_pybullet_drones.utils.utils import str2bool


# Задание параметров запуска через консоль через argpasrse
def get_argparse_settings():
    parser = argparse.ArgumentParser(description='Сценарий взлета > поворота > пролета > приземления через Ctrl Aviary')
    parser.add_argument('--drone', default="cf2x", type=DroneModel, help='Модель дрона (default: CF2X)',
                        choices=DroneModel)
    parser.add_argument('--num_drones', default=2, type=int, help='Количество дронов (default: 2)')
    parser.add_argument('--physics', default="pyb", type=Physics, help='Физика Pybullet (default: PYB)',
                        choices=Physics)
    parser.add_argument('--gui', default=True, type=str2bool, help='Использовать ли GUI PyBullet (default: True)')
    parser.add_argument('--obstacles', default=False, type=str2bool, help='Cоздавать ли препятствия (default: False)')
    parser.add_argument('--simulation_freq_hz', default=240, type=int, help='Частота моделирования в Гц (default: 240)')
    parser.add_argument('--control_freq_hz', default=48, type=int, help='Управляющая частота в Гц (default: 240)')
    parser.add_argument('--duration_sec', default=8, type=int, help='Продолжительность моделирования в секундах '
                                                                    '(default: 8)')
    parser.add_argument('--user_debug_gui', default=True, type=str2bool, help='отрисовывать ли оси дронов и ползунки '
                                                                              'оборотов в гуи (default: True)')
    parser.add_argument('--upper_bound', default=1.0, type=float, help='Высота, на которую дрон должен подняться в м '
                                                                       '(default: 1)')

    return parser.parse_args()
