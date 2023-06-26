import time
import argparse
import numpy as np
import math

from gym_pybullet_drones.envs.BaseAviary import DroneModel, Physics
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.utils.utils import sync, str2bool
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl

if __name__ == "__main__":
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
    ARGS = parser.parse_args()
    AGGR_PHY_STEPS = int(ARGS.simulation_freq_hz / ARGS.control_freq_hz)
    INIT_XYZS = np.array([[0, 0, 0.02]])
    for i in range(ARGS.num_drones - 1):
        INIT_XYZS = np.concatenate((INIT_XYZS, np.array([[i + 1, 0, 0.02]])))

    env = CtrlAviary(drone_model=ARGS.drone,
                     num_drones=ARGS.num_drones,
                     initial_xyzs=INIT_XYZS,
                     initial_rpys=None,
                     physics=ARGS.physics,
                     neighbourhood_radius=10,
                     freq=ARGS.simulation_freq_hz,
                     aggregate_phy_steps=AGGR_PHY_STEPS,
                     gui=ARGS.gui,
                     obstacles=ARGS.obstacles,
                     user_debug_gui=ARGS.user_debug_gui
                     )

    ctrl = [DSLPIDControl(env) for i in range(ARGS.num_drones)]
    states = []
    action = {}
    CTRL_EVERY_N_STEPS = int(np.floor(env.SIM_FREQ / ARGS.control_freq_hz))
    takeoff_speed = 0.01
    position = []
    for i in range(ARGS.num_drones):
        position.append(INIT_XYZS[i])

    start = time.time()
    for i in range(0, int(ARGS.duration_sec * env.SIM_FREQ), AGGR_PHY_STEPS):  # взлет

        OBS, _, _, _ = env.step(action)

        if ARGS.gui:
            sync(i, start, env.TIMESTEP)

        for j in range(ARGS.num_drones):
            if position[j][2] < ARGS.upper_bound:
                position[j][2] += takeoff_speed
            action[str(j)], _, _ = ctrl[j].computeControlFromState(
                control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                state=OBS[str(j)]["state"],
                target_pos=np.array(position[j]),
            )
        if time.time() - start >= 3:
            break

    start = time.time()
    for i in range(0, int(ARGS.duration_sec * env.SIM_FREQ), AGGR_PHY_STEPS):  # повороты

        OBS, _, _, _ = env.step(action)

        if ARGS.gui:
            sync(i, start, env.TIMESTEP)

        if time.time() - start < 3:  # 2 поворота (1-ый дрон по часовой, 2-ой - против)
            for j in range(ARGS.num_drones):
                if j % 2 == 0:
                    angle = math.pi / 1000
                else:
                    angle = -math.pi / 1000
                action[str(j)], _, _ = ctrl[j].computeControl(
                    cur_pos=OBS[str(j)]["state"][0:3],
                    control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                    target_pos=np.array(position[j]),
                    cur_quat=np.array([0, 0, 1, angle]),
                    cur_vel=np.zeros(3),
                    cur_ang_vel=np.zeros(3), )
        elif time.time() - start < 6:  # поворот дронов в обратную сторону, чтобы их затормозить
            for j in range(ARGS.num_drones):
                if j % 2 == 0:
                    angle = -math.pi / 1000
                else:
                    angle = math.pi / 1000
                action[str(j)], _, _ = ctrl[j].computeControl(
                    cur_pos=OBS[str(j)]["state"][0:3],
                    control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                    target_pos=np.array(position[j]),
                    cur_quat=np.array([0, 0, 1, angle]),
                    cur_vel=np.zeros(3),
                    cur_ang_vel=np.zeros(3), )
        elif time.time() - start < 9:  # время для стабилизации
            for j in range(ARGS.num_drones):
                action[str(j)], _, _ = ctrl[j].computeControlFromState(
                    control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                    state=OBS[str(j)]["state"],
                    target_pos=np.array(position[j]),
                )
            else:
                break

    start = time.time()
    for i in range(0, int(ARGS.duration_sec * env.SIM_FREQ), AGGR_PHY_STEPS):  # приземление
        OBS, _, _, _ = env.step(action)

        if ARGS.gui:
            sync(i, start, env.TIMESTEP)

        for j in range(ARGS.num_drones):
            if position[j][2] > 0.02:
                position[j][2] -= takeoff_speed
            action[str(j)], _, _ = ctrl[j].computeControlFromState(
                control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                state=OBS[str(j)]["state"],
                target_pos=np.array(position[j]),
            )

    env.close()
