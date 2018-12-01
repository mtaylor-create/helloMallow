# Copyright (C) 2017 Google Inc.
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

"""Sample that implements a gRPC client for the Google Assistant API."""

import concurrent.futures
import json
import logging
import os
import os.path
import pathlib2 as pathlib
import sys
import uuid

import click
import grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

import aiy.audio
import random

import snowboydecoder
import signal
import time

from google.assistant.embedded.v1alpha2 import (
		embedded_assistant_pb2,
		embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception

try:
		from . import (
				assistant_helpers,
				audio_helpers,
				device_helpers
		)
except (SystemError, ImportError):
		import assistant_helpers
		import audio_helpers
		import device_helpers

#-------------------------

interrupted=False
model="models/heyMallow.pmdl"

def signal_handler(signal, frame):
 global interrupted
 interrupted=True

def interrupt_callback():
 global interrupted
 return interrupted

#signal.signal(signal.SIGINT, signal_handler)

detector=snowboydecoder.HotwordDetector(model, sensitivity=0.5)

def detect_callback():
	#detector.terminate()
	print("I heard you!")
	global interrupted
	interrupted=True
#  detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)


#-------------------------

greetings=["mush mush?","Snootle doo?","mush?","mush mush?","hi!","may I help?","me?","yes friend?","mush?","hi!","Presdent Reagan?","hum?","mo she mo she? Mollow des"]

moods=["I'm alright.","A little bored","Just mushin.","Hum? Sorry, I was reading.","Cheebly.","All is well with the cosmos.","A little peckish.","I took a nice nap.","I ate some of your food. Sorry."]

friends=["Gregor ","Bartlett ","Maple "]
feels=["wants to come.","was feeling bored earlier.","and I are going to hang out.","would like to see something new.","is ready for an adventure!","never lets you down!","thinks you might need help today.","maybe?"]

def mallowSpeak(userQuery, gResponse):
	if "pineapple" in userQuery:
		return "pineapple pineapple?"

	elif "how are you" in userQuery:
		return moods[random.randint(0,len(moods)-1)]

	elif "nap" in userQuery:
		aiy.audio.say("A nap? I'll nap for 10 minutes!")
		time.sleep(60*10)
		return "That was a nice nap. Did you miss me?"

	elif "i'm busy" in userQuery or "on the phone" in userQuery:
		aiy.audio.say("Oops.  I'll be quiet.")
		time.sleep(60*60)
		return "Is it ok for me to come back now?"

	elif "who " in userQuery and ("bring" in userQuery or "come" in userQuery or "take" in userQuery):
		return friends[random.randint(0,len(friends)-1)] + feels[random.randint(0,len(feels)-1)]

	elif "goodnight" in userQuery or "good night" in userQuery:
		return "Good night friend.  Sweet dreams for you."

	else:
		return gResponse







#-------------------------

def main():
	wait_for_user_trigger = True
	while True:
			print("woober")
			detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)
			print("dooooooooo")
			if wait_for_user_trigger:
					print("Waiting for mush...")
					detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)
					print("Mush detector cleared")
					#detector.terminate()
					#aiy.audio.say("mush mush?")
					#aiy.audio.say(greetings[random.randint(0,len(greetings)-1)])

					#print("dooooooooo")
					#click.pause(info='Press Enter to send a new request...')
			#continue_conversation = assistant.assist()
			# wait for user trigger if there is no follow-up turn in
			# the conversation.
			#wait_for_user_trigger = not continue_conversation

			global interrupted
			interrupted=False


if __name__ == '__main__':
		main()
