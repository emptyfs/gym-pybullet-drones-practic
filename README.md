# gym-pybullet-drones-practic
Репозиторий практики по библиотеки gym-pybullet-drones (https://github.com/utiasDSL/gym-pybullet-drones)
# Установка библиотеки (Windows)
Существует инструкция по установке (https://github.com/utiasDSL/gym-pybullet-drones/tree/master/assignments#on-windows), здесь она будет продублирована на русском и дополнена

### Необходимые ресурсы

 Visual Studio и [C++ 14.0](https://visualstudio.microsoft.com/downloads/)
- Разработчики рекомендуют the free Community version
- Необходима "Desktop development with C++"

[Python 3](https://www.python.org/downloads/release/python-390/)
- Используется [Windows x86-64 installer](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe) on Windows 10 Home
- Python должен быть 3.9

Python IDE
- Разработчики рекомендуют [PyCharm Community](https://www.jetbrains.com/pycharm/download/#section=windows)

### Установка

Скачайте zip-архив
- Перейдите на https://github.com/utiasDSL/gym-pybullet-drones/releases
- Найдите версию `v0.5.2`, найлите в "Assets" архивы и скачайте на выбор (zip или tar.gz)

![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/97edb206-8ea4-4617-aa06-bf3e77fd3dd8)

Распакуйте скаченный архив и откройте проект `gym-pybullet-drones-v0.5.2` через PyCharm (учтите, что путь к проекту не должен содержать кириллицу - только латиницу, иначе будут вылетать ошибки)

![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/203f6ac6-d59d-49f8-8d5c-835da5dfd457)

В файле `setup.py` перечислены необходимые для установки пакеты (среда PyCharm может вывести список необходимых пакетов в всплывающем окне), пакеты можно установить вручную:
Выберите `File->Settings` и нажмите `Project:gym-pybullet-drones-0.5.2->Python Interpreter`
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/089db82b-6607-4173-953a-fd751b32edce)
- Нажмите `+`, чтобы добавить пакет и `-`, чтобы удалить
Список всех пакетов, которые могут понадобиться:
- `numpy`
- `matplotlib`
- `pybullet`
- `gym`
- `Pillow`
- `сycler`
- `stable_baselines3`
- `ray[rllib]`
- `scipy`

Если все сделано верно, то можно будет запустить следующие файлы проекта и увидеть демонстрируемый разработчиками функционал:
- `assignments.aer1216_fall2020_hw1_sim.py`
- `examples.compare.py`
- `examples.downwash.py`
- `examples.fly.py`
- `examples.physics.py`
