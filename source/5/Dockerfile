FROM python:3.9

WORKDIR /drones-practic

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    freeglut3-dev

COPY ./assignments ./assignments
COPY ./examples ./examples
COPY ./experiments ./experiments
COPY ./files ./files
COPY ./gym_pybullet_drones ./gym_pybullet_drones
COPY ./ros2 ./ros2

ARG GUI
ARG MODE

CMD ["python", "./examples/practice_4.py", "--gui=${GUI}"]