# https://pythonhosted.org/pyserial/

import serial
import keyboard

portName = 'COM6'
baudRate = 9600

ser = serial.Serial(portName, baudRate, timeout=1)  # open serial port
print('Port ' + ser.name + ' opened, ' + str(baudRate) + ' baud')  # check which port was really used


while True:
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('\nQuitting!')
            break  # finishing the loop
        else:
            pass
    except:
        break  # if user pressed a key other than the given key the loop will break

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('t'):  # if key 't' is pressed
            ser.write(b'hello')  # write a string
        else:
            pass
    except:
        break  # if user pressed a key other than the given key the loop will break



    # Serial read section
    msg = ser.readline()
    print("Message from arduino: ")
    print(msg)


ser.close()  # close port
