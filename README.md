# Nu

Contributing to the Cozmo community! This framework allows cuztomizing the robot to one's own flavor by creating stackable skills responding to multiple sensory data.

"All life begins with Nu and ends with Nu. This is the truth! This is my belief! ...At least for now."
— "The Mystery of Life," vol. 841, chapter 26

## Installation

### Hardware Dependencies
- [Cozmo](https://www.anki.com/en-us/cozmo) robot
- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b)
  - [Sense HAT](https://www.raspberrypi.org/products/sense-hat) add-on board
  - Microphone module for Pi USB port
  - GPS module for Pi USB port

### Software Dependencies
- [Redis 4.0](https://redis.io/download)
- [Python 3.6.6](https://www.python.org/downloads)
- [Cozmo SDK](http://cozmosdk.anki.com/docs)
- `python -m pip install --upgrade pip && python setup.py install` or
- `python3.6.6 -m pip install missing_dependency`

### Local
- `cd` unto Nu project directory
- Create self-signed certificate `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

### Pi3
- Install Nu project into directory `/home/pi`
- `cd /home/pi/Nu`
- Create self-signed certificate `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
- Copy files from `nu/configs/init.d` into in `/etc/init.d`

## Usage 

### Local
- Connect iOS or Android device to your computer's USB port
- Place Cozmo on the charger and start the in-app SDK mode
- Launch ADB `adb-devices`
- Launch Redis using `redis-server`
- `cd` unto Nu project directory
- Launch Nu using `python -m nu -h` and `python nu/webapp/server.py`
- Launch Nu verbose `python -m nu -vv 2>&1 >& log.txt &` and `python nu/webapp/server.py`

### Pi3
- Connect Android device to a Pi3 USB port
- Place Cozmo on the charger and start the in-app SDK mode
- Launch ADB `adb-devices`
- Launch Redis using `systemctl start redis-server`
- Launch Nu using `systemctl start nu` and `systemctl start nu-webapp`
- Stop using `systemctl stop nu` and `systemctl stop nu-webapp`

## Contributing

Coming soon. 
