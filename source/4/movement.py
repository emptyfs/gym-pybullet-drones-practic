import time
import numpy as np
import math

from gym_pybullet_drones.utils.utils import sync


def _log_simulation(ARGS, logger, i, env, OBS):  # лог каждого дрона
    for j in range(ARGS.num_drones):
        logger.log(drone=j,
                   timestamp=i / env.SIM_FREQ,
                   state=OBS[str(j)]["state"]
                   )

        """Logs entries for a single simulation step, of a single drone.

        Parameters
        ----------
        drone : int
            Id of the drone associated to the log entry.
        timestamp : float
            Timestamp of the log in simulation clock.
        state : ndarray
            (20,)-shaped array of floats containing the drone's state.
        control : ndarray, optional
            (12,)-shaped array of floats containing the drone's control target.

        """


def _action_turn(action, ctrl, j, OBS, CTRL_EVERY_N_STEPS, env, position, angle):  # поворот через стандартый контроллер
    action[str(j)], _, _ = ctrl[j].computeControl(
        cur_pos=OBS[str(j)]["state"][0:3],
        control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
        target_pos=np.array(position[j]),
        cur_quat=np.array([0, 0, 1, angle]),
        cur_vel=np.zeros(3),
        cur_ang_vel=np.zeros(3), )

    """Computes the PID control action (as RPMs) for a single drone.

          This methods sequentially calls `_dslPIDPositionControl()` and `_dslPIDAttitudeControl()`.

          Parameters
          ----------
          control_timestep : float
              The time step at which control is computed.
          cur_pos : ndarray
              (3,1)-shaped array of floats containing the current position.
          cur_quat : ndarray
              (4,1)-shaped array of floats containing the current orientation as a quaternion.
          cur_vel : ndarray
              (3,1)-shaped array of floats containing the current velocity.
          cur_ang_vel : ndarray
              (3,1)-shaped array of floats containing the current angular velocity.
          target_pos : ndarray
              (3,1)-shaped array of floats containing the desired position.
          target_rpy : ndarray, optional
              (3,1)-shaped array of floats containing the desired orientation as roll, pitch, yaw.
          target_vel : ndarray, optional
              (3,1)-shaped array of floats containing the desired velocity.
          target_ang_vel : ndarray, optional
              (3,1)-shaped array of floats containing the desired angular velocity."""


def _action_pos(action, ctrl, j, CTRL_EVERY_N_STEPS, env, OBS, position):  # передвижение дрона к точке (Точка в 3D)
    action[str(j)], _, _ = ctrl[j].computeControlFromState(
        control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
        state=OBS[str(j)]["state"],
        target_pos=np.array(position[j]),
    )

    """Interface method using `computeControl`.

    It can be used to compute a control action directly from the value of key "state"
    in the `obs` returned by a call to BaseAviary.step().

    Parameters
    ----------
    control_timestep : float
        The time step at which control is computed.
    state : ndarray
        (20,)-shaped array of floats containing the current state of the drone.
    target_pos : ndarray
        (3,1)-shaped array of floats containing the desired position.
    target_rpy : ndarray, optional
        (3,1)-shaped array of floats containing the desired orientation as roll, pitch, yaw.
    target_vel : ndarray, optional
        (3,1)-shaped array of floats containing the desired velocity.
    target_ang_vel : ndarray, optional
        (3,1)-shaped array of floats containing the desired angular velocity.

    """


def turn(logger, ARGS, env, AGGR_PHY_STEPS, action, ctrl, position, stop_time):  # повороты дронов

    """
    Параметры
    ----------
    logger : Logger
        Объект класса Logger
    ARGS : Namespace
        Заполненное пространство имен из argparse
    env : CtrlAviary
        Объект класса CtrlAviary
    AGGR_PHY_STEPS : int
        The number of physics steps within one call to `BaseAviary.step()`.
    action : ndarray | dict[..]
        The input action for one or more drones, translated into RPMs by
        the specific implementation of `_preprocessAction()` in each subclass.
    ctrl : list
        список контроллеров каждого дрона
    position : list
        список координат для перемещения для каждого дрона на каджом шаге симуляции
    stop_time : float
        время на текущее действие (в секундах)
    """

    CTRL_EVERY_N_STEPS = int(np.floor(env.SIM_FREQ / ARGS.control_freq_hz))
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
                _action_turn(action, ctrl, j, OBS, CTRL_EVERY_N_STEPS, env, position, angle)
        elif time.time() - start < 6:  # поворот дронов в обратную сторону, чтобы их затормозить
            for j in range(ARGS.num_drones):
                if j % 2 == 0:
                    angle = -math.pi / 1000
                else:
                    angle = math.pi / 1000
                _action_turn(action, ctrl, j, OBS, CTRL_EVERY_N_STEPS, env, position, angle)
        elif time.time() - start < stop_time:  # время для стабилизации (удержание дрона на одной позиции некоторое
            # время, чтобы он пришел в равновесие)
            for j in range(ARGS.num_drones):
                _action_pos(action, ctrl, j, CTRL_EVERY_N_STEPS, env, OBS, position)
        else:
            _log_simulation(ARGS, logger, i, env, OBS)
            break


def fly_to_position(logger, mode, stop_pos, ARGS, env, AGGR_PHY_STEPS, action, position, takeoff_speed, ctrl,
                    stop_time):  # передвижение дронов

    """
    Параметры
    ----------
    logger : Logger
        Объект класса Logger
    mode : int
        режимы перемещения в пространстве (0 - вверх (по z), 1 - вниз (по z), 2 - параллельно плоскости xy)
    stop_pos : float
        x-\y-\z-координата для остановки перемещения дрона после ее достижения (для mode 0 и mode 1 - z-координата,
        для mode 2 - y-координата)
    ARGS : Namespace
        Заполненное пространство имен из argparse
    env : CtrlAviary
        Объект класса CtrlAviary
    AGGR_PHY_STEPS : int
        The number of physics steps within one call to `BaseAviary.step()`.
    action : ndarray | dict[..]
        The input action for one or more drones, translated into RPMs by
        the specific implementation of `_preprocessAction()` in each subclass.
    position : list
        список координат для перемещения для каждого дрона на каджом шаге симуляции
    takeoff_speed : float
        stop_pos = n * takeoff_speed + начальная позиция (в начале начальная позиция хранитcя в position, потом там
        хранится начальная позиция + takeoff_speed, потом начальная позиция + 2*takeoff_speed и тд до stop_pos)
    ctrl : list
        список контроллеров каждого дрона
    stop_time : float
        время на текущее действие (в секундах)
    """
    CTRL_EVERY_N_STEPS = int(np.floor(env.SIM_FREQ / ARGS.control_freq_hz))
    start = time.time()
    for i in range(0, int(ARGS.duration_sec * env.SIM_FREQ), AGGR_PHY_STEPS):  # взлет
        OBS, _, _, _ = env.step(action)

        if ARGS.gui:
            sync(i, start, env.TIMESTEP)

        for j in range(ARGS.num_drones):
            if mode == 0:
                if position[j][2] < stop_pos:
                    position[j][2] += takeoff_speed
            elif mode == 1:
                if position[j][2] > stop_pos:
                    position[j][2] -= takeoff_speed
            elif mode == 2:
                if j % 2 == 0:
                    if position[j][1] < stop_pos:
                        position[j][1] += takeoff_speed
                else:
                    if position[j][1] > -stop_pos:
                        position[j][1] -= takeoff_speed
            _action_pos(action, ctrl, j, CTRL_EVERY_N_STEPS, env, OBS, position)
        if time.time() - start >= stop_time:
            _log_simulation(ARGS, logger, i, env, OBS)
            break
