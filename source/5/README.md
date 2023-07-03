# Инструция по установке и запуску образа Docker

- `Dockerfile` для сборки данного образа расположен в этой же директории

# Установка
### Необходимые ресурсы
- [Docker](https://www.docker.com/)
- [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/)
### Скачивание образа
Образ хранится на [DockerHub](https://hub.docker.com/r/emptyfs/practice-drones-korsunov)

Команда для скачивания - `docker pull emptyfs/practice-drones-korsunov`

### Запуск (настройка X Server)
Для использования GUI понадобится скачать и насроить X Server (мной использовался VcXsrv)

Далее нужно запустить `xlaunch` для насройки сервера
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/6263c173-fdad-4675-8de7-5549b994dd6e)

Настройки должны соответствовать настройкам на следующих скриншотах
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/0b7d4514-82b3-4248-8ad3-db12ca581d7f)
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/e823c03b-ca7b-4113-aec2-8ff23f4ceab1)
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/f532c8f6-7bd1-4b09-b717-6246525f7657)

После этого должен появится значок сервера:

![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/70705a14-d665-4162-9590-856b2da6b792)

Теперь понадобится ваш IP-адрес, его можно узнать командой `ipconfig`:

![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/32ee3caf-f701-4928-bf24-f69ed6e455b7)

IP-адрес устанавливается в переменную среды командой `set-variable -name DISPLAY -value <ваш IP-адрес>:0.0`

### Запуск (без и с GUI)
Для запуска предусмотрены 2 флага:
- `GUI`, который отвечает за наличие графического отображения (к команде запуска нужно добавить `-e GUI=False` (вместо 'False' предусмотрено использование 'false' или '0') - для запуска без GUI и любое другое значение для запуска с GUI (например, `-e GUI=True`))
- `MODE`, который отвечает за сценарий полета дронов (к команде запуска нужно добавить `-e MODE=4` - для сценария полета на оценку 'Хорошо' и любое другое значение для сценария полета на оценку 'Удовлетворительно' (например, `-e MODE=3`))

Все варианты команд запуска:
- `docker run -ti --rm -e DISPLAY=$DISPLAY -e GUI=True -e MODE=4 emptyfs/practice-drones-korsunov` - с GUI и сценарием на 4
- `docker run -ti --rm -e DISPLAY=$DISPLAY -e GUI=False -e MODE=4 emptyfs/practice-drones-korsunov` - без GUI и сценарием на 4
- `docker run -ti --rm -e DISPLAY=$DISPLAY -e GUI=True -e MODE=3 emptyfs/practice-drones-korsunov` - с GUI и сценарием на 3
- `docker run -ti --rm -e DISPLAY=$DISPLAY -e GUI=False -e MODE=3 emptyfs/practice-drones-korsunov` - без GUI и сценарием на 3

Демонстрация запуска
![image](https://github.com/emptyfs/gym-pybullet-drones-practic/assets/54939750/80e487aa-e733-4c05-9a8d-add20547e791)

Если возникает ошибка `cannot connect to X server`, то значит вы не подключились к серверу, чтобы исправить ошибку нужно снова задайте свой IP-адрес в переменную `DISPLAY` (учтите, что VcXsrv должен быть включен) - эти действия описаны выше в пункте `Запуск (настройка X Server)`





















