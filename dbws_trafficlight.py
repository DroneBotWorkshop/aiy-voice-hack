#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# dbws_trafficlight.py
# Voice Controlled Traffic Light
# Modified by DroneBot Workshop
# 2018-02-20
#

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import subprocess
import sys

import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def red_led_on():
    aiy.audio.say('Red light on')
    GPIO.output(26,True)

def red_led_off():
    aiy.audio.say('Red light off')
    GPIO.output(26,False)

def yellow_led_on():
    aiy.audio.say('Yellow light on')
    GPIO.output(6,True)

def yellow_led_off():
    aiy.audio.say('Yellow light off')
    GPIO.output(6,False)

def green_led_on():
    aiy.audio.say('Green light on')
    GPIO.output(13,True)

def green_led_off():
    aiy.audio.say('Green light off')
    GPIO.output(13,False)
    
def all_led_on():
    aiy.audio.say('Turning all lights on')
    GPIO.output(26,True)
    GPIO.output(6,True)
    GPIO.output(13,True)

def all_led_off():
    aiy.audio.say('Turning all lights off')
    GPIO.output(26,False)
    GPIO.output(6,False)
    GPIO.output(13,False)

def traffic_go():
    aiy.audio.say('Green light. You can go')
    GPIO.output(26,False)
    GPIO.output(6,False)
    GPIO.output(13,True)

def traffic_stop():
    aiy.audio.say('Red light. You must stop')
    GPIO.output(26,True)
    GPIO.output(6,False)
    GPIO.output(13,False)

def traffic_caution():
    aiy.audio.say('Yellow light. Be careful')
    GPIO.output(26,False)
    GPIO.output(6,True)
    GPIO.output(13,False)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'red light on':
            assistant.stop_conversation()
            red_led_on()
        elif text == 'red light off':
            assistant.stop_conversation()
            red_led_off()
        elif text == 'yellow light on':
            assistant.stop_conversation()
            yellow_led_on()
        elif text == 'yellow light off':
            assistant.stop_conversation()
            yellow_led_off()
        elif text == 'green light on':
            assistant.stop_conversation()
            green_led_on()
        elif text == 'green light off':
            assistant.stop_conversation()
            green_led_off()
        elif text == 'traffic go':
            assistant.stop_conversation()
            traffic_go()
        elif text == 'traffic stop':
            assistant.stop_conversation()
            traffic_stop()
        elif text == 'traffic caution':
            assistant.stop_conversation()
            traffic_caution()
        elif text == 'all lights on':
            assistant.stop_conversation()
            all_led_on()
        elif text == 'all lights off':
            assistant.stop_conversation()
            all_led_off()
        
        

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
