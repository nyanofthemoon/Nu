# Interface to robot

import time
import asyncio
import logging
from nu import cozmo
from nu.cozmo.util import degrees, distance_inches, distance_mm, speed_mmps, radians
from random import SystemRandom

logger = logging.getLogger()


class Executor:

    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot

    def reset(self):
        self.constitution = 1
        self.energy = 1
        self.happy = 1
        self.robot.world.auto_disconnect_from_cubes_at_end()
        self.robot.world.disconnect_from_cubes()
        self.robot.enable_stop_on_cliff(enable=True)
        self.robot.enable_all_reaction_triggers(should_enable=True)
        self.set_repair_needs(self.constitution)
        self.set_energy_needs(self.energy)
        self.set_play_needs(self.happy)
        self.use_quiet_voice()
        self.become_idle()

    # 0 = 'broken', 1 = 'fully repaired'
    def set_repair_needs(self, value=1):
        self.robot.set_needs_levels(value)

    # 0 = 'no-energy', 1 = 'full energy'
    def set_energy_needs(self, value=1):
        self.robot.set_needs_levels(value)

    # 0 = 'bored', 1 = 'happy'
    def set_play_needs(self, value=1):
        self.robot.set_needs_levels(value)

    def is_charging(self):
        return self.robot.is_charging

    def read_battery(self):
        return self.robot.battery_voltage

    def last_seen_image(self):
        return self.robot.world.latest_image

    def is_airborne(self):
        return self.robot.is_picked_up

    def is_falling(self):
        return self.robot.is_falling

    def is_cliff_ahead(self):
        return self.robot.is_cliff_detected

    def disable_freeplay(self):
        if self.robot.is_freeplay_mode_active == True:
            self.robot.stop_freeplay_behaviors()
            self.robot.enable_facial_expression_estimation(enable=True)
            self.robot.enable_freeplay_cube_lights(enable=False)

    def enable_freeplay(self):
        if self.robot.is_freeplay_mode_active == False:
            self.robot.enable_facial_expression_estimation(enable=False)
            self.robot.enable_freeplay_cube_lights(enable=True)
            self.robot.start_freeplay_behaviors()

    def become_asleep(self):
        self.freeze()
        self._update_sleep_mood()

    def become_idle(self):
        self.freeze()
        self._update_mood()
        self.do_look_around_at_faces()

    def hiccups(self):
        self.robot.execute_custom_behavior(30)

    #def sing(self, song=102):
    #    self.robot.execute_custom_behavior(song)  # SING BINGO

    def acknowledge(self):
        self.robot.execute_custom_behavior(158)
        time.sleep(2)
        self.freeze()

    def freeze(self):
        self.robot._set_none_behavior()
        self.robot.clear_idle_animation()

    # Will dance for duration seconds
    def dance(self, duration=10):
        self.robot.execute_custom_behavior(7)
        time.sleep(duration)
        self.freeze()

    # Will look at closest face and rush to it, idefinitely.
    def rush_to_visible_person(self):
        self.robot.execute_custom_behavior(159)

    def speak_slowly(self, text, excited=False):
        self.robot.say_text(text, in_parallel=True, num_retries=1, voice_pitch=-0.15, duration_scalar=1.25, play_excited_animation=excited).wait_for_completed()

    def speak(self, text, excited=False):
        self.robot.say_text(text, in_parallel=True, num_retries=1, play_excited_animation=excited).wait_for_completed()

    def speak_quickly(self, text, excited=False):
        self.robot.say_text(text, in_parallel=True, num_retries=1, voice_pitch=0.15, duration_scalar=0.75, play_excited_animation=excited).wait_for_completed()

    # http://cozmosdk.anki.com/docs/generated/cozmo.anim.html
    def emote_single(self, type):
        trigger = getattr(Emote, type)()
        self.robot.play_anim_trigger(trigger).wait_for_completed()

    def emote_chain(self, type):
        triggers = getattr(EmoteChain, type)()
        for trigger in triggers:
            self.robot.play_anim_trigger(trigger).wait_for_completed()

    def set_head_angle(self, angle):
        self.robot.set_head_angle(degrees(angle)).wait_for_completed()

    def set_lift_height(self, height):
        self.robot.set_lift_height(height).wait_for_completed()

    def turn(self, angle):
        self.robot.turn_in_place(degrees(angle)).wait_for_completed()

    def turn_right(self):
        self.turn(-90)

    def turn_left(self):
        self.turn(90)

    def turn_around(self):
        self.turn(180)

    def open_lights(self, color='white'):
        # 'green', 'red', 'blue', 'white'
        color = color + '_light'
        light = cozmo.lights[color].flash()
        self.robot.set_backpack_lights(light1=light, light2=light, light3=light, light4=light, light5=light)

    def close_lights(self):
        self.robot.set_backpack_lights_off()

    def open_side_lights(self, color='red'):
        light = cozmo.lights[color]
        self.robot.set_backpack_lights(light1=light, light5=light)

    def close_side_lights(self):
        self.robot.set_backpack_lights(light1=cozmo.lights.off_light, light5=cozmo.lights.off_light)

    def open_front_light(self, color='white'):
        self.robot.set_backpack_lights(light2=cozmo.lights[color])

    def close_front_light(self):
        self.robot.set_backpack_lights(light2=cozmo.lights.off_light)

    def open_center_light(self,  color='white'):
        self.robot.set_backpack_lights(light3=cozmo.lights[color])

    def close_center_light(self):
        self.robot.set_backpack_lights(light3=cozmo.lights.off_light)

    def open_rear_light(self, color='white'):
        self.robot.set_backpack_lights(light4=cozmo.lights[color])

    def close_rear_light(self):
        self.robot.set_backpack_lights(light4=cozmo.lights.off_light)

    def turn_random(self):
        self.turn(SystemRandom().choice([
            -90,
            -180,
            -270,
            90,
            180,
            270
        ]))

    def look_up(self):
        self.set_head_angle(44.5)

    def look_down(self):
        self.set_head_angle(-25.0)

    def lift_up(self):
        self.set_lift_height(92.0)

    def lift_down(self):
        self.set_lift_height(0.0)

    def undock_from_charger(self):
        if self.robot.is_on_charger == True or self.is_charging():
            self.robot.drive_off_charger_contacts(num_retries=3).wait_for_completed()
            self.move_forward(4.5)

    def move_forward(self, distance_in=1.0):
        self.robot.drive_straight(distance_inches(distance_in), speed_mmps(25)).wait_for_completed()

    def move_backward(self, distance_in=1.0):
        self.robot.drive_straight(distance_inches((distance_in*-1)), speed_mmps(25)).wait_for_completed()

    def go_to_charger(self):
        if (self.robot.is_on_charger == False):
            charger = async_run_until_complete(self._locate_charger())
            return self._go_to_object(charger)
        else:
            return False

    def go_to_any_cube(self):
        cube = async_run_until_complete(self._locate_any_cube())
        return self._go_to_object(cube)

    def be_silent(self):
        self.robot.set_robot_volume(0.0)

    def use_quiet_voice(self):
        self.robot.set_robot_volume(0.33)

    def use_normal_voice(self):
        self.robot.set_robot_volume(0.67)

    def use_loud_voice(self):
        self.robot.set_robot_volume(1.0)

    def last_seen_face(self):
        last_seen_face = None
        if self.robot.world.visible_face_count() > 0:
            visible_faces_iterator = iter(self.robot.world.visible_faces)
            try:
                last_seen_face = max(enumerate(visible_faces_iterator))[1]
            finally:
                del visible_faces_iterator
        return last_seen_face

    def last_seen_pet(self):
        last_seen_pet = None
        if self.robot.world.visible_pet_count() > 0:
            visible_pets_iterator = iter(self.robot.world.visible_pets)
            try:
                last_seen_pet = max(enumerate(visible_pets_iterator))[1]
            finally:
                del visible_pets_iterator
        return last_seen_pet

    def do_look_around(self):
        return self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    def do_look_for_face(self):
        return self.robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

    # Will look around and look at faces, indefinitely.
    def do_look_around_at_faces(self):
        self.robot.execute_custom_behavior(27)

    def _update_mood(self):
        happy = self.happy
        energy = self.energy
        constitution = self.constitution
        animation = Emote.idle()
        if constitution < 0.5:
            animation = cozmo.anim.Triggers.NeedsSevereLowRepairIdle
        if energy < 0.5:
            animation = cozmo.anim.Triggers.NeedsSevereLowRepairIdle
        if happy < 0.5:
            animation = cozmo.anim.Triggers.NothingToDoBoredIdle
        self.robot.set_idle_animation(animation)

    def _update_sleep_mood(self):
        self.robot.set_idle_animation(Emote.sleep())

    def constitution(self):
        return self.constitution

    def update_constitution(self, amount: 0.25):
        self.set_repair_needs( (self.constitution + amount) )
        self._update_mood()

    def energy(self):
        return self.energy

    def update_energy(self, amount: 0.25):
        self.set_energy_needs( (self.energy + amount) )
        self._update_mood()

    def happiness(self):
        return self.happy

    def update_happiness(self, amount: 0.25):
        self.set_play_needs( (self.happy + amount) )
        self._update_mood()

    ###
    def dock_and_recharge(self):
        if self.go_to_charger():
            self.turn_around()
            async_run_until_complete(self.robot.backup_onto_charger(max_drive_time=10))
        return self.robot.is_charging

    def _turn_towards_face(self, face):
        try:
            self.robot.turn_towards_face(face, num_retries=1).wait_for_completed()
            return True
        except:
            return False

    async def _locate_face(self, face):
        located = False
        find_face = self.do_look_for_face()
        for retry in range(3):
            try:
                visible_face = await self.robot.world.wait_for_observed_face(timeout=10)
                if visible_face.face_id == face.face_id:
                    located = True
                    break
            except:
                pass
        find_face.stop()
        return located

    async def _locate_any_face(self):
        find_face = self.do_look_for_face()
        try:
            face = await self.robot.world.wait_for_observed_face(timeout=25)
        finally:
            find_face.stop()
            return face

    async def _locate_any_pet(self):
        find_pet = self.do_look_for_face()
        try:
            pet = await self.robot.world.wait_for_observed_pet(timeout=25)
        finally:
            find_pet.stop()
            return pet

    async def _locate_any_cube(self):
        find_cube = self.do_look_around()
        try:
            cube = await self.robot.world.wait_for_observed_light_cube(timeout=25)
        finally:
            find_cube.stop()
            return cube

    async def _locate_charger(self, charger=None):
        self.set_head_angle(0)
        self.set_lift_height(0)
        look_around = self.do_look_around()
        try:
            charger = await self.robot.world.wait_for_observed_charger(timeout=25)
        finally:
            look_around.stop()
            return charger

    def _go_to_object(self, observed):
        if observed != None:
            self.robot.go_to_object(observed, distance_mm(70.0)).wait_for_completed()
            return True
        else:
            return False


def async_run_until_complete(coroutine):
    loop = None
    result = None
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        done, pending = loop.run_until_complete(asyncio.wait([asyncio.ensure_future(coroutine)]))
        for future in done:
            result = future.result()
    finally:
        loop.close()
        return result


class ExecutableActions:
    SPEAK_SLOW = 'speak_slowly'
    SPEAK = 'speak'
    SPEAK_FAST = 'speak_quickly'
    EMOTE_SINGLE = 'emote_single'
    EMOTE_CHAIN = 'emote_chain'
    MOVE_HEAD = 'set_head_angle'
    MOVE_LIFT = 'set_lift_height'
    LOOK_UP = 'look_up'
    LOOK_DOWN = 'look_down'
    LIFT_UP = 'lift_up'
    LIFT_DOWN = 'lift_dow'
    MOVE_FORWARD = 'move_forward'
    MOVE_BACKWARD = 'move_backward'
    TURN = 'turn'
    TURN_AROUND = 'turn_around'
    TURN_RIGHT = 'turn_right'
    TURN_LEFT = 'turn_left'
    TURN_RANDOM = 'turn_random'
    UNDOCK_FROM_CHARGER = 'undock_from_charger'
    DOCK_AND_RECHARGE = 'dock_and_recharge'
    GO_TO_CHARGER = 'go_to_charger'
    GO_TO_ANY_CUBE = 'go_to_any_cube'
    OPEN_LIGHTS = 'open_lights'
    CLOSE_LIGHTS = 'close_lights'
    OPEN_FRONT_LIGHT = 'open_front_light'
    CLOSE_FRONT_LIGHT = 'close_front_light'
    OPEN_CENTER_LIGHT = 'open_center_light'
    CLOSE_CENTER_LIGHT = 'close_center_light'
    OPEN_REAR_LIGHT = 'open_rear_light'
    CLOSE_REAR_LIGHT = 'close_rear_light'
    OPEN_WARNING_LIGHTS = 'open_side_lights'
    CLOSE_WARNING_LIGHTS = 'close_side_lights'
    BE_SILENT = 'be_silent'
    USE_QUIET_VOICE = 'use_quiet_voice'
    USE_NORMAL_VOICE = 'use_normal_voice'
    USE_LOUD_VOICE = 'use_loud_voice'
    DO_LOOK_AROUND = 'do_look_around'
    DO_LOOK_FOR_PERSON = 'do_look_for_face'
    DO_LOOK_AROUND_AT_PEOPLE = 'do_look_around_at_faces'
    ENABLE_FREEPLAY = 'enable_freeplay'
    DISABLE_FREEPLAY = 'disable_freeplay'
    ACKNOWLEDGE = 'acknowledge'
    DANCE = 'dance'
    FREEZE = 'freeze'
    RUSH_TO_VISIBLE_PERSON = 'rush_to_visible_person'
    HICCUPS = 'hiccups'
    BECOME_IDLE = 'become_idle'
    BECOME_ASLEEP = 'become_asleep'
    UPDATE_CONSTITUTION = 'update_constitution'
    UPDATE_ENERGY = 'update_energy'
    UPDATE_HAPPINESS = 'update_happiness'


class ExecutableSingleEmotes:
    UPSET = 'upset'
    ANNOYED = 'annoyed'
    CURIOUS = 'curious'
    HAPPY = 'happy'
    EXCITED = 'excited'
    UNHAPPY = 'unhappy'
    SURPRISED = 'surprised'
    SCARED = 'scared'
    BORED = 'bored'
    IDLE = 'idle'
    TIRED = 'tired'
    WAKEUP = 'wake_up'
    SLEEP = 'sleep'

class ExecutableChainEmotes:
    FALL_ASLEEP = 'fall_asleep'

class EmoteChain:

    @staticmethod
    def fall_asleep():
        return [
            SystemRandom().choice([
                cozmo.anim.Triggers.GoToSleepGetIn,
                cozmo.anim.Triggers.StartSleeping,
                cozmo.anim.Triggers.GoToSleepSleeping
            ]),
            SystemRandom().choice([
                cozmo.anim.Triggers.CodeLabSleep,
                cozmo.anim.Triggers.GuardDogSleepLoop,
                cozmo.anim.Triggers.Sleeping
            ])
        ]


class Emote:

    @staticmethod
    def annoyed():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabFrustrated,
            cozmo.anim.Triggers.CozmoSaysBadWord,
            cozmo.anim.Triggers.CubeMovedUpset,
        ])

    @staticmethod
    def upset():
        return SystemRandom().choice([
            cozmo.anim.Triggers.MajorFail,
            cozmo.anim.Triggers.FrustratedByFailureMajor,
            cozmo.anim.Triggers.CozmoSaysBadWord,
            cozmo.anim.Triggers.FrustratedByFailure
        ])

    @staticmethod
    def curious():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabThinking,
            cozmo.anim.Triggers.CodeLabWondering,
            cozmo.anim.Triggers.CodeLabCurious
        ])

    @staticmethod
    def excited():
        return SystemRandom().choice([
            cozmo.anim.Triggers.MajorWin,
            cozmo.anim.Triggers.CodeLabExcited,
        ])

    @staticmethod
    def happy():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabWin,
            cozmo.anim.Triggers.CodeLabHappy,
            cozmo.anim.Triggers.CodeLabReactHappy,
            cozmo.anim.Triggers.DriveLoopHappy
        ])

    @staticmethod
    def surprised():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabSurprise,
            cozmo.anim.Triggers.CodeLabWhoa,
            cozmo.anim.Triggers.OnSawNewNamedFace,
            cozmo.anim.Triggers.OnSawNewUnnamedFace
        ])

    @staticmethod
    def scared():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabWhew
        ])

    @staticmethod
    def unhappy():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabUnhappy
        ])

    @staticmethod
    def bored():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabBored,
            cozmo.anim.Triggers.CodeLabChatty,
            cozmo.anim.Triggers.NothingToDoBoredEvent
        ])

    @staticmethod
    def idle():
        return SystemRandom().choice([
            cozmo.anim.Triggers.DroneModeIdle,
            cozmo.anim.Triggers.CodeLabIdle,
            cozmo.anim.Triggers.CodeLabStaring,
            cozmo.anim.Triggers.GameSetupIdle,
            cozmo.anim.Triggers.IdleOnCharger,
            cozmo.anim.Triggers.CozmoSaysIdle,
            cozmo.anim.Triggers.MeetCozmoScanningIdle,
            cozmo.anim.Triggers.InteractWithFaceTrackingIdle,
            cozmo.anim.Triggers.SparkIdle
        ])

    @staticmethod
    def tired():
        return SystemRandom().choice([
            cozmo.anim.Triggers.ConnectWakeUp_SevereEnergy,
            cozmo.anim.Triggers.ConnectWakeUp_SevereRepair
        ])

    @staticmethod
    def sleep():
        return SystemRandom().choice([
            cozmo.anim.Triggers.CodeLabSleep,
            cozmo.anim.Triggers.GuardDogSleepLoop,
            cozmo.anim.Triggers.Sleeping
        ])

    @staticmethod
    def wake_up():
        return SystemRandom().choice([
            cozmo.anim.Triggers.GoToSleepGetOut,
            cozmo.anim.Triggers.GoToSleepOff,
            cozmo.anim.Triggers.ConnectWakeUp,
            cozmo.anim.Triggers.VC_StartledWakeup
        ])
