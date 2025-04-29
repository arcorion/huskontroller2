#!/usr/bin/python3
import serial
import select
from serial.tools import list_ports

def main():
    cycle_read_write(attach_device())

def attach_device():
    port_list = list_ports.comports()
    port_names = []
    for port in port_list:
        port_names += port
    device = serial.Serial(port_names[0], 9600, timeout=0)
    return device

def cycle_read_write(device):
    command = ""
    timeout = 5

    while (command.lower() != 'quit'):
        command = input('Command? ("quit to quit") ')
        device.write(command.encode())
        read, _, _ = select.select([device], [], [], timeout)
        device_output = device.read(0x100)

        print(device_output)

if __name__ == '__main__':
    main()
