import socket # This line imports a module called socket, which provides access to network communication capabilities.

import RPi.GPIO as GPIO \# This line imports a module named RPi.GPIO, which provides functions to control GPIO pins on a Raspberry Pi.

import time \# This line imports a module called time, which provides various time-related functions.

import smbus \# This line imports a module named smbus, which allows communication with devices using the I2C protocol.

\# Constants

HOST = '192.168.111.241' \# This line defines a constant named HOST and assigns it the IP address of the host (server).

PORT = 8080 \# This line defines a constant named PORT and assigns it the port number used for communication.

MOTOR\_SPEED = 0.01 \# This line defines a constant named MOTOR\_SPEED and assigns it the speed at which motors will move.

STEP\_MULTIPLIER = 1 \# This line defines a constant named STEP\_MULTIPLIER which determines the number of steps motors will take.

HW290\_ADDRESS = 0x68 \# This line defines a constant named HW290\_ADDRESS and assigns it the address of a hardware device.

    52

 \# GPIO pin definitionsstepper\_pins = \{ \# This line defines a dictionary named stepper\_pins, which maps motor names to their corresponding GPIO pins.

'motor1': \{'step': 17, 'dir': 18, 'en': 22\},

'motor2': \{'step': 23, 'dir': 24, 'en': 25\},

'motor3': \{'step': 8, 'dir': 7, 'en': 10\},

'motor4': \{'step': 11, 'dir': 9, 'en': 12\}

\}

\# Initialize GPIO

GPIO.setmode(GPIO.BCM) \# This line sets the GPIO mode to use the BCM numbering scheme.

for motor, pins in stepper\_pins.items(): \# This loop sets up the GPIO pins for each motor.

for pin in pins.values():

GPIO.setup(pin, GPIO.OUT) \# This line sets the GPIO pins as output pins.

\# Initialize SMBus

bus = smbus.SMBus(1) \# This line initialises the SMBus with bus number 1.

\# Initial positions (adjust as needed)

initial\_positions = \{ \# This line defines a dictionary named initial\_positions, which stores the initial positions of each motor.

'motor1': 0.0,

'motor2': 0.0,

'motor3': 0.0,

'motor4': 0.0

\}

53

def main(): \# This function is the main entry point of the program.

with socket.socket(socket.AF\_INET, socket.SOCK\_STREAM) as s: \# This line creates a socket object for communication.

s.bind((HOST, PORT)) \# This line binds the socket to the host and port specified.

s.listen() \# This line puts the socket into listening mode.

print("Waiting for connection...") \# This line prints a message to indicate that the program is waiting for a connection.

conn, addr = s.accept() \# This line accepts a connection request from a client.

with conn: \# This line opens a connection with the client.

print(f"Connected to \{addr\}") \# This line prints a message to indicate that a connection has been established.

try:

while True: \# This loop runs continuously until a KeyboardInterrupt occurs.

data = conn.recv(1024).decode().strip() \# This line receives data from the client and decodes it.

if not data: \# This line checks if the received data is empty.

break \# This line breaks out of the loop if no data is received.

print("Received data:", data) \# This line prints the received data.

sensor\_data = [value.strip() for value in data.split(',')] \# This line splits the received data into a list of sensor readings.

  54

process\_gesture(sensor\_data) \# This line processes the sensor data.

except KeyboardInterrupt: \# This block of code executes if a KeyboardInterrupt occurs.

 print("\textbackslash{}nKeyboard interrupt detected. Exiting...") \# this line prints a message indicating that a KeyboardInterrupt has been detected.

 finally:

GPIO.cleanup() \# This line cleans up the GPIO pins.

 defprocess\_gesture(sensor\_data): \# This function processes the sensor data.

try:

if len(sensor\_data) >= 3: \# This line checks if there are at least 3 sensor readings.

gesture\_data\_x, gesture\_data\_y, gesture\_data\_z = map(float, sensor\_data) \# This line converts sensor readings to floating point numbers.

\# This block of code checks for specific gesture patterns based on sensor data.

if 35 <= gesture\_data\_x<= 60 and 20 <= gesture\_data\_y<= 35 and -70 <= gesture\_data\_z<= 70:

print("Initial position")

return\_to\_initial\_positions()

  55

elif 70 <= gesture\_data\_x<= 100 and 60 <= gesture\_data\_y<= 80 and 0 <= gesture\_data\_z<= 80:

moveMotor(stepper\_pins['motor1'], int(5 * STEP\_MULTIPLIER), MOTOR\_SPEED)

print("Move up")

elif 45 <= gesture\_data\_x<= 65 and 0 <= gesture\_data\_y<= 40 and -60 <= gesture\_data\_z<= 60:

moveMotor(stepper\_pins['motor2'], int(5 * STEP\_MULTIPLIER), MOTOR\_SPEED)

print("Move left")

elif 15 <= gesture\_data\_x<= 30 and -20 <= gesture\_data\_y<= 20 and -40 <= gesture\_data\_z<= 60:

moveMotor(stepper\_pins['motor3'], int(5 * STEP\_MULTIPLIER), MOTOR\_SPEED)

print("Move down")

 elif 30 <= gesture\_data\_x<= 60 and 0 <= gesture\_data\_y<= 35 and -40 <= gesture\_data\_z<= 70:

moveMotor(stepper\_pins['motor4'], int(5 * STEP\_MULTIPLIER), MOTOR\_SPEED)

print("Move right")

except ValueError:

print("Error: Invalid sensor data format") \# This line prints an error message if the sensor data format is invalid.

defmoveMotor(pins, steps, speed): \# This function moves a motor by a specified number of steps at a given speed.

 56

for \_ in range(abs(steps)): \# This loop iterates over the specified number of steps.

GPIO.output(pins['dir'], GPIO.HIGH if steps > 0 else GPIO.LOW) \# This line sets the direction of movement of the motor.

GPIO.output(pins['en'], GPIO.LOW) \# This line enables the motor.

GPIO.output(pins['step'], GPIO.HIGH) \# This line generates a step signal to move the motor.

time.sleep(speed) \# This line pauses execution for the specified duration.

GPIO.output(pins['step'], GPIO.LOW) \# This line stops the step signal.

time.sleep(speed) \# This line pauses execution for the specified duration.

GPIO.output(pins['en'], GPIO.HIGH) \# This line disables the motor

def readHandPositionData(): \# This function reads hand position data from a hardware device.

data = bus.read\_i2c\_block\_data(HW290\_ADDRESS, 0x3B, 6) \# This line reads data from the hardware device.

hand\_position\_x = data[0] << 8 | data[1] \# This line calculates the X position of the hand.

hand\_position\_y = data[2] << 8 | data[3] \# This line calculates the Y position of the hand.

hand\_position\_z = data[4] << 8 | data[5] \# This line calculates the Z position of the hand.

hand\_position\_x = hand\_position\_x if hand\_position\_x< 32768 else hand\_position\_x - 65536 \# This line adjusts the X position if necessary.

hand\_position\_y = hand\_position\_y if hand\_position\_y< 32768 else hand\_position\_y - 65536 \# This line adjusts the Y position if necessary.

hand\_position\_z = hand\_position\_z if hand\_position\_z< 32768 else hand\_position\_z - 65536 \# This line adjusts the Z position if necessary.

57

return hand\_position\_x, hand\_position\_y, hand\_position\_z \# This line returns the hand position data.

 def return\_to\_initial\_positions(): \# This function returns motors to their initial positions.

for motor, target\_position in initial\_positions.items(): \# This loop iterates over each motor and its target position.

current\_position = readHandPositionData()[int(motor[-1]) - 1] \# This line reads the current position of the motor.

steps = int((target\_position - current\_position) * STEP\_MULTIPLIER) \# This line calculates the number of steps needed to return to the initial position.

moveMotor(stepper\_pins[motor], steps, MOTOR\_SPEED) \# This line moves the motor to the initial position.

if \__name\__ == "\__main\__": \# This line checks if the script is being run as the main program.

main() \# This line calls the main function to start the program execution.

