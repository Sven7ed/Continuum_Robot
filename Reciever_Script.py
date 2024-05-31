import socket # This line imports a module called socket, which provides access to network communication capabilities.

import RPi.GPIO as GPIO # This line imports a module named RPi.GPIO, which provides functions to control GPIO pins on a Raspberry Pi.

import time # This line imports a module called time, which provides various time-related functions.

import smbus # This line imports a module named smbus, which allows communication with devices using the I2C protocol.

\# Constants

HOST = '192.168.111.241' # This line defines a constant named HOST and assigns it the IP address of the host (server).

PORT = 8080 # This line defines a constant named PORT and assigns it the port number used for communication.

MOTOR\_SPEED = 0.01 # This line defines a constant named MOTOR\_SPEED and assigns it the speed at which motors will move.

STEP\_MULTIPLIER = 1 # This line defines a constant named STEP\_MULTIPLIER which determines the number of steps motors will take.

HW290\_ADDRESS = 0x68 # This line defines a constant named HW290\_ADDRESS and assigns it the address of a hardware device.

    
 \# GPIO pin definitionsstepper\_pins = \{ \# This line defines a dictionary named stepper\_pins, which maps motor names to their corresponding GPIO pins.

'motor1': {'step': 17, 'dir': 18, 'en': 22\},

'motor2': {'step': 23, 'dir': 24, 'en': 25\},

'motor3': {'step': 8, 'dir': 7, 'en': 10\},

'motor4': {'step': 11, 'dir': 9, 'en': 12\}

}

# Initialize GPIO

GPIO.setmode(GPIO.BCM) # This line sets the GPIO mode to use the BCM numbering scheme.

for motor, pins in stepper_pins.items(): \# This loop sets up the GPIO pins for each motor.

for pin in pins.values():

GPIO.setup(pin, GPIO.OUT) # This line sets the GPIO pins as output pins.

# Initialize SMBus

bus = smbus.SMBus(1) # This line initialises the SMBus with bus number 1.

# Initial positions (adjust as needed)

initial\_positions = { # This line defines a dictionary named initial\_positions, which stores the initial positions of each motor.

'motor1': 0.0,

'motor2': 0.0,

'motor3': 0.0,

'motor4': 0.0

}

53

def main(): # This function is the main entry point of the program.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # This line creates a socket object for communication.

s.bind((HOST, PORT)) # This line binds the socket to the host and port specified.

s.listen() # This line puts the socket into listening mode.

print("Waiting for connection...") # This line prints a message to indicate that the program is waiting for a connection.

conn, addr = s.accept() # This line accepts a connection request from a client.

with conn: # This line opens a connection with the client.

print(f"Connected to {addr}") # This line prints a message to indicate that a connection has been established.

try:

while True: # This loop runs continuously until a KeyboardInterrupt occurs.

data = conn.recv(1024).decode().strip() # This line receives data from the client and decodes it.

if not data: # This line checks if the received data is empty.

break # This line breaks out of the loop if no data is received.

print("Received data:", data) # This line prints the received data.

sensor_data = [value.strip() for value in data.split(',')] \# This line splits the received data into a list of sensor readings.

  54

process_gesture(sensor\_data) # This line processes the sensor data.

except KeyboardInterrupt: # This block of code executes if a KeyboardInterrupt occurs.

 print("textbackslash{}nKeyboard interrupt detected. Exiting...") # this line prints a message indicating that a KeyboardInterrupt has been detected.

 finally:

GPIO.cleanup() # This line cleans up the GPIO pins.

 defprocess_gesture(sensor_data): # This function processes the sensor data.

try:

if len(sensor_data) >= 3: # This line checks if there are at least 3 sensor readings.

gesture_data_x, gesture_data_y, gesture_data_z = map(float, sensor_data) # This line converts sensor readings to floating point numbers.

# This block of code checks for specific gesture patterns based on sensor data.

if 35 <= gesture_data_x<= 60 and 20 <= gesture_data_y<= 35 and -70 <= gesture_data_z<= 70:

print("Initial position")

return_to_initial_positions()

  55

elif 70 <= gesture_data_x<= 100 and 60 <= gesture_data_y<= 80 and 0 <= gesture_data_z<= 80:

moveMotor(stepper_pins['motor1'], int(5 * STEP_MULTIPLIER), MOTOR_SPEED)

print("Move up")

elif 45 <= gesture_data_x<= 65 and 0 <= gesture_data_y<= 40 and -60 <= gesture_data_z<= 60:

moveMotor(stepper_pins['motor2'], int(5 * STEP_MULTIPLIER), MOTOR\_SPEED)

print("Move left")

elif 15 <= gesture_data_x<= 30 and -20 <= gesture_data_y<= 20 and -40 <= gesture_data_z<= 60:

moveMotor(stepper_pins['motor3'], int(5 * STEP_MULTIPLIER), MOTOR\_SPEED)

print("Move down")

 elif 30 <= gesture_data_x<= 60 and 0 <= gesture_data_y<= 35 and -40 <= gesture_data_z<= 70:

moveMotor(stepper_pins['motor4'], int(5 * STEP_MULTIPLIER), MOTOR_SPEED)

print("Move right")

except ValueError:

print("Error: Invalid sensor data format") # This line prints an error message if the sensor data format is invalid.

defmoveMotor(pins, steps, speed): # This function moves a motor by a specified number of steps at a given speed.

 56

for _ in range(abs(steps)): # This loop iterates over the specified number of steps.

GPIO.output(pins['dir'], GPIO.HIGH if steps > 0 else GPIO.LOW) # This line sets the direction of movement of the motor.

GPIO.output(pins['en'], GPIO.LOW) # This line enables the motor.

GPIO.output(pins['step'], GPIO.HIGH) # This line generates a step signal to move the motor.

time.sleep(speed) # This line pauses execution for the specified duration.

GPIO.output(pins['step'], GPIO.LOW) # This line stops the step signal.

time.sleep(speed) # This line pauses execution for the specified duration.

GPIO.output(pins['en'], GPIO.HIGH) # This line disables the motor

def readHandPositionData(): # This function reads hand position data from a hardware device.

data = bus.read_i2c_block_data(HW290_ADDRESS, 0x3B, 6) # This line reads data from the hardware device.

hand_position_x = data[0] << 8 | data[1] # This line calculates the X position of the hand.

hand_position_y = data[2] << 8 | data[3] # This line calculates the Y position of the hand.

hand_position_z = data[4] << 8 | data[5] # This line calculates the Z position of the hand.

hand_position\_x = hand_position_x if hand_position_x< 32768 else hand_position_x - 65536 # This line adjusts the X position if necessary.

hand_position_y = hand_position_y if hand_position_y< 32768 else hand_position_y - 65536 # This line adjusts the Y position if necessary.

hand_position_z = hand_position_z if hand_position_z< 32768 else hand_position_z - 65536 # This line adjusts the Z position if necessary.

57

return hand_position_x, hand_position_y, hand_position_z # This line returns the hand position data.

 def return_to_initial_positions(): # This function returns motors to their initial positions.

for motor, target_position in initial_positions.items(): # This loop iterates over each motor and its target position.

current\_position = readHandPositionData()[int(motor[-1]) - 1] # This line reads the current position of the motor.

steps = int((target_position - current_position) * STEP_MULTIPLIER) # This line calculates the number of steps needed to return to the initial position.

moveMotor(stepper_pins[motor], steps, MOTOR_SPEED) # This line moves the motor to the initial position.

if __name__ == "__main__": # This line checks if the script is being run as the main program.

main() # This line calls the main function to start the program execution.

