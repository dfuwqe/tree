# tree
Iot Christmas tree

Careful: Power the LEDs with power adapter. Do not power through Arduinos, the current can be high!

# How to run
python3 tree.py

# Files
tree.py - main code for calculation and communication
visualizer.py - graphical demo for the LEDs.
compress.py - compress the tree.py outputs by reduing unused outputs. This file is used since the demo machine has too limited RAM and CPU.
LED/LED.ino - Arduino code for LEDs

# Main idea of the program
Each LED has two control input, one for RGB (color) and one for state. The arudino code adjusts brightness based on the state code. Blinking is achieved by adjusting the brightness of LEDs.

the message format looks like this:

0F0F 1010 2020 ...
^    ^ 
1st  2nd
LED  LED

The control signals are sequential. Two bytes for one LED, the first byte indicates LED state and the second byte controls color. Each run,
the python program computes the colors and state for all LEDs based on our animation rule and serialize all the values and send to Arduino
via the serial line. This may be inefficient, other methods like sending signals only for those that require change my be viable. 

The parsed BGP data are stored into pandas and queried for a time unit (like 0.5 s). The results are then filtered and only the last row is chosen 
for display (one LED cannot show that much info). 

# Variables to modify
SerialPort 
numLED - number of LEDs
tableStarttime - starting time, note offset is in seconds
inputName - parsed output file
playSpeed, timeUnitBase, fps -- used to control playback speed

# Modify program
self.table holds the BGP data in pandas
self.frames -- 2d array for the control signals in one second. 1st dimension, number of frames in one second (e.g, 2fps gives size 2 in 1st dimension). 2nd dimension is 2* numLED (2 bytes to control each LED). The color is derived from AS number. But the state number is kind of hard-coded (sorry). The state number decrements at each frame so the LED will light up only for a fixed period. Other state code (196 - 202) will cause the LED to blink red-blue (bogon). Other normal updates will blink the LED by changing the state code as well.

