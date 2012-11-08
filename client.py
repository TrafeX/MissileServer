#!/usr/bin/env python
#
#    USB Missile Launcher client
#
#    Copyright (c) 2012, Tim de Pater <code AT trafex DOT nl>
#    <https://github.com/TrafeX/MissileServer>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
try:
   # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 7777
DEVICE = 1

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def run_command(cmd, value):
    global sock
    msg = '{"command":"%s","value":"%s","device":"%s"}' % (cmd, value, DEVICE)
    print "Sending message {}".format(msg)
    sock.sendto(msg, (UDP_IP, UDP_PORT))

def key(event):
    global DEVICE
    if event.keysym == 'Escape':
        root.destroy()
    print( 'Key %r' % event.keysym )
    if event.keysym  == 'Up':
        run_command('up', 50)
    if event.keysym == 'Down':
        run_command('down', 50)
    if event.keysym == 'Left':
        run_command('left', 100)
    if event.keysym == 'Right':
        run_command('right', 100)
    if event.keysym == 'space':
        run_command('fire', 1)
    if event.keysym == 'l':
        run_command('led', 1)
    if event.keysym == 'o':
        run_command('led', 0)
    if event.keysym == 'z':
        run_command('zero', 0)
    if event.keysym == '1':
        DEVICE = 0
    if event.keysym == '2':
        DEVICE = 1


root = tk.Tk()
print( "Press a key (Escape key to exit):" )
root.bind_all('<Key>', key)
# don't show the tk window
#root.withdraw()
root.mainloop()
