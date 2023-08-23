#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Zenzay's RPi Input/Output Library.

    Morse-Code-LED Example - Using a Binary Wave to pulse LED using Morse Code

    Created by Jens Hansen 2019.

"""

import sys
import pigpio

sys.path.append("../") # Appending sys-path with parent folder, so we can find the zpiolib module
from zpiolib.gpio.binary_wave import Binary_Wave
from zpiolib.gpio.consts import TICKS_PER_SEC

#    Dit: 1 unit
#    Dah: 3 units
#    Intra-character space (the gap between dits and dahs within a character): 1 unit
#    Inter-character space (the gap between the characters of a word): 3 units
#    Word space (the gap between two words): 7 units
# seconds per dit = 60 / (total dits * word_per_minut)

LED_PIN = 20

MORSE_DIT = 1
MORSE_DAH = 3
MORSE_KEY_GAP = 1
MORSE_CHAR_GAP = 3
MORSE_WORD_GAP = 7

MORSE_CODE = {'A':'13', 'B':'3111', 'C':'3131', 'D':'311', 'E':'1', 'F':'1131', 'G':'331', 'H':'1111', 'I':'11',
              'J':'1333', 'K':'313', 'L':'1311', 'M':'33', 'N':'31', 'O':'333', 'P':'1331', 'Q':'3313', 'R':'131',
              'S':'111', 'T':'3', 'U':'113', 'V':'1113', 'W':'133', 'X':'3113', 'Y':'3133', 'Z':'3311',
              '1':'13333', '2':'11333', '3':'11133', '4':'11113', '5':'11111', '6':'31111', '7':'33111', '8':'33311', '9':'33331', '0':'33333',
              ',':'331133', '.':'131313', '?':'113311', '/':'31131', '-':'311113', '(':'31331', ')':'313313'}

def morse_pulse_encode(message):
    keys = []
    message = message.upper()
    for letter in message:
        if letter == ' ':
            add_pause = MORSE_WORD_GAP - MORSE_CHAR_GAP #units
        else:
            code = MORSE_CODE[letter]
            for digit in code:
                keys.append(int(digit))
                keys.append(MORSE_KEY_GAP)
            add_pause = MORSE_CHAR_GAP - MORSE_KEY_GAP #units
        #change last off and add pause
        keys[-1] = keys[-1] + (add_pause)
    return keys

def morse_pulse_decode(pulse):
    build = ""
    message = ""
    i = 0
    l = len(pulse)-1
    while (i < l):
        digit = pulse[i]
        pause = pulse[i+1]
        build += str(digit)
        if pause != MORSE_KEY_GAP:
            for key, value in MORSE_CODE.items():
                if value == build:
                    message += key
                    break
            build = ""
            if (pause == MORSE_WORD_GAP):
                message += " "

            build = ""
        i += 2
    return message

if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
        print("Unable to connect to pigpio daemon!")
        exit(0)

    led = Binary_Wave(pi, LED_PIN)
    try:
        while True:
            message = input("Type message (default=SOS): ")
            if len(message) == 0:
                message = "SOS"
            message += " "	#add a space for delay between repeats
            word_per_minut = 16
            pulse = morse_pulse_encode(message)
            total_dits = 0
            for p in pulse:
                total_dits += int(p)
            usecs_per_dit = int((60 / (total_dits * word_per_minut)) * TICKS_PER_SEC)

            print(f"Message = {morse_pulse_decode(pulse)}")
            print(f"Total dits = {total_dits}")
            print(f"uSecs per dit = {usecs_per_dit}")
            print(f"Pulse = {pulse}")
            led.set_pulse(pulse, usecs_per_dit)
            led.start_wave()

            print ("Enter to stop. Ctrl-C to Quit")
            input()
            led.stop_wave()
    except KeyboardInterrupt:
        print(" - Bye!")
    finally:
        led.stop_wave()
        pi.stop()
