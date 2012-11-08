Missile Laucher Server/Client
=============================
* Run the missileserver.py on a computer with the USB Missile Launcher(s).
* Run the client.py on every computer you want and control the Missile Launcher(s).
* Tested with the Dream Cheeky Thunder USB Missile Launcher.
* Based on the Retaliation Project: <https://github.com/codedance/Retaliation>


Server Protocol
===============
The MissileServer accepts JSON packets on UDP port 7777.
The JSON packet had the following structure:

    {"command":"[arg1]","value":"[arg2]","device":"[arg3]"}


* arg1
** up
** down
** left
** right
** fire
** led
** zero
* arg2
** in case arg1 is value; this is the amount of miliseconds to move
** in case arg1 is fire; this is the amount of missiles to fire
** in case arg1 is led; use 1 for on, 0 for off
** in case arg1 is zero; use 1 to place the missile launcher in the zero position
* arg3
** define which device to use
** use 'all' to control all devices at the same time

Client keyboard controls
========================
The client can be controlled with the keyboard using the following keys;

* Movement: up,down,left,right
* Fire: space
* Led on: l
* Led off: o
* To zero position: z
* Device: 0 or 1
* Exit: escape
