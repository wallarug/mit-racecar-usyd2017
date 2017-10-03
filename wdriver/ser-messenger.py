#!/usr/bin/python3

import serial

# update to person you are sending to:
ser = serial.Serial('COM5', 9600, timeout=3)

while True:
    data = ser.read()
    print(data)
    din = input("Please enter a message: ")
    ser.write(din.encode())

ser.close()
