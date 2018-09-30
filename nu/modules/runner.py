# Runner

import logging
import threading
from distutils.util import strtobool
from time import sleep
from nu import cozmo

from .scheduler import Scheduler
from .body import Executor
from .body.senses import *
from .brain import SMemoryQueue, SMemoryPubSub, SMemoryStorage
from .brain import LMemory
from .brain import Operator
from .brain.senses import *
from .config import runner_config
from .config import sense_config
from .config import skill_config
from .skills import *

runnerConfig = runner_config()
senseConfig = sense_config()
skillConfig = skill_config()


class Runner:

    smemory = None
    lmemory = None
    operator = None
    executor = None
    scheduler = None
    schedulerThread = None
    pubsubThread = None

    def __init__(self):
        self.recognizer = None
        self.audioData = None
        self.scheduler = Scheduler()

    def scheduleTasks(self, sensors=[], exclusions=[]):
        for sensor in sensors:
            if sensor not in exclusions:
              self.scheduler.add(int(senseConfig.get('refresh', sensor)), getattr(globals()[sensor], 'publish'))

    def startScheduledTasks(self):
        self.schedulerThread = threading.Thread(daemon=True, target=self.scheduler.start)
        self.schedulerThread.start()
        self.schedulerThread.join()

    def stopScheduledTasks(self):
        self.scheduler.stop()
        self.schedulerThread._stop()

    def startShortTermMemory(self):
        SMemoryStorage.flushdb()
        SMemoryQueue.flush()
        SMemoryQueue.start(self.operator.handle_entry)

    def stopShortTermMemory(self):
        SMemoryQueue.stop()

    def startLongTermMemory(self):
        self.lmemory = LMemory()

    def stopLongTermMemory(self):
        return True

    def bindSensoryCallback(self, robot: cozmo.robot.Robot, sensors):
        if 'BodySenseAirborne' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseAirborne'))/2, self._sensorCallbackBodySenseAirborne)
        if 'BodySenseBattery' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseBattery'))/2, self._sensorCallbackBodySenseBattery)
        if 'BodySenseCliff' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseCliff'))/2, self._sensorCallbackBodySenseCliff)
        if 'BodySenseFalling' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseFalling'))/2, self._sensorCallbackBodySenseFalling)
        if 'BodySenseFace' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseFace'))/2, self._sensorCallbackBodySenseFace)
        if 'BodySensePet' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySensePet'))/2, self._sensorCallbackBodySensePet)
        if 'BodySenseRecharging' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseRecharging'))/2, self._sensorCallbackBodySenseRecharging)
        if 'BodySenseVision' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseVision'))/2, self._sensorCallbackBodySenseVision)
        if 'BrainSenseSound' in sensors:
            BrainSenseSound.listen(int(senseConfig.get('refresh', 'BrainSenseSound')))
        if 'BrainSenseText2Speech' in sensors:
            BrainSenseText2Speech.listen(int(senseConfig.get('refresh', 'BrainSenseText2Speech')))

    def _sensorCallbackBodySenseAirborne(self):
        BodySenseAirborne.set(str(self.executor.is_airborne()))
    def _sensorCallbackBodySenseBattery(self):
        BodySenseBattery.set(str(self.executor.read_battery()))
    def _sensorCallbackBodySenseCliff(self):
        BodySenseCliff.set(str(self.executor.is_cliff_ahead()))
    def _sensorCallbackBodySenseFalling(self):
        BodySenseFalling.set(str(self.executor.is_falling()))
    def _sensorCallbackBodySenseFace(self):
        BodySenseFace.set(str(self.executor.last_seen_face()))
    def _sensorCallbackBodySensePet(self):
        BodySensePet.set(str(self.executor.seen_pet()))
    def _sensorCallbackBodySenseRecharging(self):
        BodySenseRecharging.set(str(self.executor.is_charging()))
    def _sensorCallbackBodySenseVision(self):
        BodySenseVision.set(str(self.executor.last_seen_image()))

    def unbindSensoryCallback(self):
        self.scheduler.empty()
        return True

    def bindMessageCallback(self, skills):
        for skill in skills:
            skillClass = globals()[skill]
            for subscription in getattr(skillClass, 'SUBSCRIPTIONS'):
                sensorClass = globals()[subscription]
                sensorClass.subscribe(skillClass.handle_message)

        self.pubsubThread = SMemoryPubSub.run_in_thread(sleep_time=0.5, daemon=True)

    def unbindMessageCallback(self):
        SMemoryPubSub.punsubscribe('*')
        self.pubsubThread.stop()

    def startLogicalOperator(self):
        self.operator = Operator(self.executor)

    def stopLogicalOperator(self):
        # @TODO
        # self.operator = None
        return True

    def startPhysicalExecutor(self, robot: cozmo.robot.Robot):
        # @TODO
        self.executor = Executor(robot)
        return True

    def stopPhysicalExecutor(self):
        # @TODO
        self.executor = None
        return True

logger = logging.getLogger()
runner = None

def main_function():
    global runner
    runner = Runner()
    run_cozmo_program()

def run_cozmo_program():
    logger.info('Contacting Cozmo SDK')
    try:
        cozmo.robot.Robot.drive_off_charger_on_connect = strtobool(runnerConfig.get('options', 'DriveOffChargerOnConnect'))
        cozmo.run_program(
            cozmo_connect_callback,
            use_viewer=strtobool(runnerConfig.get('options', 'UseViewer')),
            use_3d_viewer=strtobool(runnerConfig.get('options', 'Use3DViewer')),
            force_viewer_on_top=strtobool(runnerConfig.get('options', 'ForceViewerOnTop')),
            show_viewer_controls=strtobool(runnerConfig.get('options', 'ShowViewerControls'))
        )
    except SystemExit as e:
        logger.error(str(e))
        alog = logging.getLogger('cozmo.general')
        alog.disabled = True
        logger.critical('Cozmo SDK Connection Timeout')
        sleep(1.5)
        run_cozmo_program()

def cozmo_connect_callback(robot: cozmo.robot.Robot):
    alog = logging.getLogger('cozmo.general')
    alog.disabled = True
    global runner

    skills = []
    for name, status in skillConfig.items('status'):
        if strtobool(status):
            skills.append(name)

    sensors = []
    ex_sensors = ['BrainSenseSound', 'BrainSenseText2Speech']
    for skill in skills:
        for sensor in getattr(globals()[skill], 'SUBSCRIPTIONS'):
            if sensor not in sensors:
                sensors.append(sensor)

    logger.info('Connected to Cozmo SDK')
    logger.info('Contacting Long Term Memory')
    runner.startLongTermMemory()
    logger.info('Starting Physical Executor')
    runner.startPhysicalExecutor(robot)
    logger.info('Starting Logical Operator')
    runner.startLogicalOperator()
    logger.info('Contacting Short Term Memory')
    runner.startShortTermMemory()
    logger.info('Finding Required Sensors ' + str(sensors))
    logger.info('Excluding Sensors ' + str(ex_sensors))
    runner.bindSensoryCallback(robot, sensors)
    runner.bindMessageCallback(skills)
    logger.info('Initializing Skills ' + str(skills))
    runner.scheduleTasks(sensors, ex_sensors)
    runner.startScheduledTasks()


def cozmo_disconnect_callback():
    global runner
    logger.critical('Disconnected from Cozmo SDK')
    logger.warning('Unscheduling Recurrent Tasks')
    runner.stopScheduledTasks()
    logger.warning('Disconnecting from Sensors')
    runner.unbindSensoryCallback()
    runner.unbindMessageCallback()
    logger.warning('Forgetting Short Term Memory')
    runner.stopShortTermMemory()
    logger.warning('Stopping Logical Operator')
    runner.stopLogicalOperator()
    logger.warning('Stopping Physical Executor')
    runner.stopPhysicalExecutor()
    run_cozmo_program()
