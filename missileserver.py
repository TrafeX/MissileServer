import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util


UDP_PORT = 7777

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICES = []

def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    global DEVICES

    DEVICES = usb.core.find(find_all=True, idVendor=0x2123, idProduct=0x1010)

    for dev in DEVICES:
        # On Linux we need to detach usb HID first
        if "Linux" == platform.system():
            try:
                dev.detach_kernel_driver(0)
            except Exception, e:
                pass # already unregistered

        dev.set_configuration()

def send_cmd(cmd, device):
    try:
        if device == "all":
            for dev in DEVICES:
                dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
        else:
            DEVICES[device].ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    except Exception, e:
        print "ERROR: Device doesn't exists: %s" % device

def led(cmd, device):
    try:
        if device == "all":
            for dev in DEVICES:
                dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
        else:
            DEVICES[device].ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    except Exception, e:
        print "ERROR: Device doesn't exists: %s" % device

def send_move(cmd, duration_ms, device):
    send_cmd(cmd, device)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP, device)

def run_command(command, value, device):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value, device)
    elif command == "left":
        send_move(LEFT, value, device)
    elif command == "up":
        send_move(UP, value, device)
    elif command == "down":
        send_move(DOWN, value, device)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000, device)
        send_move(LEFT, 8000, device)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00, device)
        else:
            led(0x01, device)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE, device)
            time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command


def main(args):

    setup_usb()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    print "Running UDP server on port {}".format(UDP_PORT)

    while True:
        data, addr = sock.recvfrom(8192)
        print "Received data %s " % data
        jsondata = json.loads(data)
        command = jsondata["command"].lower()
        value = int(jsondata["value"].lower())
        device = int(jsondata["device"].lower())
        print "Action: {}, Value: {}, Device: {}".format(command, value, device)
        run_command(command, value, device)

if __name__ == '__main__':
    main(sys.argv)

