
import serial
import time

def initialize():
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1)
        
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))
            # try:	
            # 	cmd = "F"*4000 + "L"*500 + "R"*500 + "B"*4000
            # 	cmd = cmd * 1000
            # 	while True:
            # 		#cmd=input("Enter command (data,led0 or led1): ")
            # 		#cmd = "F\n"
            # 		arduino.write(cmd.encode())
                    
            # 		while arduino.inWaiting()==0: pass
            # 		if  arduino.inWaiting()>0: 
            # 			answer=str(arduino.readline())
            # 			print("---> {}".format(answer))

                            
            # except KeyboardInterrupt:
                # print("KeyboardInterrupt has been caught.")


def send_command(arduino, command: str):
    command = command * 50
    try:
        arduino.write(command.encode())
        time.sleep(0.07)	
        # for i in range(10):
        #     arduino.write(command.encode())
        #     # time.sleep(0.07)
        # for i in range(10):
        #     arduino.write(str("B" * 50).encode())
        #     time.sleep(0.07)
        # # while arduino.inWaiting()==0: pass

        # # if  arduino.inWaiting()>0: 
        #     # answer=str(arduino.readline())
        #     # print("---> {}".format(answer))       
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
