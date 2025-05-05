#!/usr/bin/python3
import serial
import select
from serial.tools import list_ports

def main():
    device = attach_device()
    mode = input("(R)ead, (W)rite, or (B)oth?")
    mode = mode.lower()[0]
    match mode:
        case 'r':
            cycle_read(device)
        case 'w':
            cycle_write(device)
        case 'b':
            cycle_read_write(attach_device())

def attach_device():
    """
    Attaches the first serial device found by the computer.
    """
    port_list = list_ports.comports()
    port_names = []
    for port in port_list:
        port_names += port
    device = serial.Serial(port_names[0], 9600, timeout=0)
    return device

def cycle_read(device):
    """
    Regularly reads serial device output and prints to terminal display.
    """
    while True:
        print("Press CTRL+C to quit")
        timeout = 10
        read, _, _ = select.select([device], [], [], timeout)
        device_output = device.read(0x100)

        print("Out: " + device_output.decode())

def cycle_read_write(device):
    """
    Takes a command and writes it to the serial device. Prints out the result from said device.
    """
    command = ""
    timeout = 5

    while (command.lower() != 'quit'):
        # Taken from here - https://stackoverflow.com/questions/26047544/python-serial-port-listener
        # Still need to read up on serial.Serial.read
        # https://pyserial.readthedocs.io/en/latest/pyserial_api.html?highlight=serial%20read#serial.Serial.read

        command = input('Command? ("quit" to quit) ')
        if command == 'quit':
            break
        device.write(command.encode())
        read, _, _ = select.select([device], [], [], timeout)
        device_output = device.read(0x100)

        print(device_output)

def cycle_write(device):
    """
    Takes a command and writes it to the serial device. It does not produce the response.
    Continues this until quit command it received.
    """
    command = ""

    while (command.lower != 'quit'):
        command = input('Command? ("quit" to quit)')
        if command== 'quit':
            break
        device.write(command.encode())

if __name__ == '__main__':
    main()
