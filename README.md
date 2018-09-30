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

## Usage 

### Launch
- Place Cozmo on the charger and start the in-app SDK mode
- Launch Redis using `redis-server`
- Launch runner using `python -m nu -h` or `python3.6.6 -m nu -v`
- Launch runner and log using `python3.7 -m nu -v 2>&1 >& log.txt &`

## Contributing

Coming soon. 
