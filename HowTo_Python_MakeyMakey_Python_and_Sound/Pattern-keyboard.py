#Inspiration for this comes from http://blog.dalethatcher.com/2012/07/makey-makey-raspberry-pi-soundboard.html
#list of hardware: http://www.thomann.de/be/akg_ghap1_usb.htm?sid=7f71cb300e282650b4a39d5b197ecb1a Raspberry Pi, MakeyMakey, & http://wiki.linuxaudio.org/wiki/raspberrypi -> change to "options snd-usb-audio index=0" in /etc/modprobe.d/alsa-base.conf. 

import pygame #sound & opengl
import time   #time of the system
import curses #graphical interface for terminal, and capture kvm
from datetime import datetime
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
#Setting up your sound in general
pygame.init()

switchAfter = 1;

voicesounds = {
	'a': {'sound':pygame.mixer.Sound('voice_01.wav'),'fadeout':False,'count':True}, #plays the sound till the end, when you press the letter a
	'd': {'sound':pygame.mixer.Sound('voice_10.wav'),'fadeout':1700} #plays the sound when d is pressed & fades out the sound after 1700 milliseconds if       		#another button has been pressed
}

stuffsounds = {
	'a': {'sound':pygame.mixer.Sound('stuff_01.wav'),'fadeout':False,'count':True},
	'd': {'sound':pygame.mixer.Sound('stuff_10.wav'),'fadeout':1700}
}


soundsets = [voicesounds, stuffsounds]

sounds = soundsets.pop(0)
soundsets.append(sounds)
 
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
screen.keypad(1)


screen.clear()
text = '''
	Pattern-keyboard for e-textile summercamp

	- Press the letter q to quit this Python script

	--->Attribution list of Freesound:
	- Coughing Young Man (me).wav by RutgerMuller 
	-- http://www.freesound.org/people/RutgerMuller/sounds/51136/ 
	-- License: Creative Commons 0 
	- woman humming by PSsoundproject 
	-- http://www.freesound.org/people/PSsoundproject/sounds/183565/ 
	-- License: Creative Commons 0 
	- Soda_Pressure_Spill_01.wav by MaxDemianAGL 
	-- http://www.freesound.org/people/MaxDemianAGL/sounds/130031/ 
	--  License: Attribution 
	- Consuming Cigarette 2.wav by Nakhas 
	-- http://www.freesound.org/people/Nakhas/sounds/132630/ 
	-- License: Attribution Noncommercial  
	
	--->Free Art License
	Claire Williams & Wendy Van Wynsberghe
'''

count = 0
playing = None

# Endless loop to keep application running
while True:
	screen.addstr(1, 0, text)

	# Which key was pressed?
	key = chr(screen.getch())

	screen.clear()
	
	# We have a soundfile for this key
	if key in sounds:
		# show pressed key on the terminal
		screen.addstr(0,0,key)
		# a previous sound is running
		if playing <> None:
			# if the sound is still playing we don't play it again
			if 'lastplay' in sounds[key] and sounds[key]['lastplay'] <> False:
				dt = datetime.now() - sounds[key]['lastplay']
				l = sounds[key]['sound'].get_length() * 1000
				
				if dt.microseconds / 1000 > 500:
					delta = (dt.seconds - 1) * 1000 + dt.microseconds / 1000
				else:
					delta = dt.seconds * 1000 + dt.microseconds / 1000

				if delta < l:
					continue

			# if the fadeout property of the playing sound isn't false
			# we fade the playing sound out in the given time
			elif sounds[playing]['fadeout'] <> False:
					sounds[playing]['sound'].fadeout(sounds[playing]['fadeout'])
					sounds[playing]['lastplay'] = False
		
		# if it's an indicator sound, we count it
		if 'count' in sounds[key]:
			# if count is bigger than the switch
			# change the active sound-set
			if count >= switchAfter:
				sounds = soundsets.pop(0)
				soundsets.append(sounds)
				count = 0

			count +=1
		
		# record when we started the sound
		sounds[key]['lastplay'] = datetime.now();
		# play                       
		sounds[key]['sound'].play()
		# set new sound as playing
		playing = key
		# sleep (1s)
	# q was pressed, quit
	elif key == 'q':
		break
	# there is no sound for the key which was pressed
	else:
		screen.clear()
		screen.addstr(0, 0, "That key doesn't do anything!")

curses.endwin()
