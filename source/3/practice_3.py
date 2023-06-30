import numpy as np

import movement
import argparse_settings

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.Logger import Logger

if __name__ == "__main__":

    ARGS = argparse_settings.get_argparse_settings()  # Заполненное пространство имен из argparse
    AGGR_PHY_STEPS = int(ARGS.simulation_freq_hz / ARGS.control_freq_hz)  # The number of physics steps within one call
    # to `BaseAviary.step()`.
    INIT_XYZS = np.array([[0, 0, 0.02]])  # список начальных координат дронов (первый дрон в (0, 0, 0.02))
    for i in range(ARGS.num_drones - 1):  # оставшиеся дроны в линию по x с расстоянием 1
        INIT_XYZS = np.concatenate((INIT_XYZS, np.array([[i + 1, 0, 0.02]])))

    env = CtrlAviary(drone_model=ARGS.drone,  # стандартный контроллер
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

    """Initialization of an aviary environment for control applications.

           Parameters
           ----------
           drone_model : DroneModel, optional
               The desired drone type (detailed in an .urdf file in folder `assets`).
           num_drones : int, optional
               The desired number of drones in the aviary.
           neighbourhood_radius : float, optional
               Radius used to compute the drones' adjacency matrix, in meters.
           initial_xyzs: ndarray | None, optional
               (NUM_DRONES, 3)-shaped array containing the initial XYZ position of the drones.
           initial_rpys: ndarray | None, optional
               (NUM_DRONES, 3)-shaped array containing the initial orientations of the drones (in radians).
           physics : Physics, optional
               The desired implementation of PyBullet physics/custom dynamics.
           freq : int, optional
               The frequency (Hz) at which the physics engine steps.
           aggregate_phy_steps : int, optional
               The number of physics steps within one call to `BaseAviary.step()`.
           gui : bool, optional
               Whether to use PyBullet's GUI.
           record : bool, optional
               Whether to save a video of the simulation in folder `files/videos/`.
           obstacles : bool, optional
               Whether to add obstacles to the simulation.
           user_debug_gui : bool, optional
               Whether to draw the drones' axes and the GUI RPMs sliders.

           """

    logger = Logger(logging_freq_hz=int(ARGS.simulation_freq_hz / AGGR_PHY_STEPS),
                    num_drones=ARGS.num_drones)

    """Logger class __init__ method.

    Parameters
    ----------
    logging_freq_hz : int
        Logging frequency in Hz.
    num_drones : int, optional
        Number of drones.
    duration_sec : int, optional
        Used to preallocate the log arrays (improves performance).

    """

    ctrl = [DSLPIDControl(env) for i in range(ARGS.num_drones)]  # пояснения этих переменных есть в movement.py в
    # описании параметров
    action = {}
    takeoff_speed = 0.01
    position = []
    for i in range(ARGS.num_drones):
        position.append(INIT_XYZS[i])

    # в movement.py есть описание параметров функций
    movement.fly_to_position(logger, 0, ARGS.upper_bound, ARGS, env, AGGR_PHY_STEPS, action, position, takeoff_speed,
                             ctrl, 3)  # полет вверх
    movement.turn(logger, ARGS, env, AGGR_PHY_STEPS, action, ctrl, position, 8.5)  # обороты
    movement.fly_to_position(logger, 1, 0.02, ARGS, env, AGGR_PHY_STEPS, action, position, takeoff_speed, ctrl, 3)
    # посадка дронов

    env.close()
    logger.save()
    logger.plot()  # вывод логов
