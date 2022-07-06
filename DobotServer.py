import socket
import json
import threading
import DobotDllType as dType

port = 'COM4'


def initialDobot(api, portName):
    '''
    Connect to Dobot and setup connection parameters
    '''
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
    # Connect to Dobot
    state = dType.ConnectDobot(api, portName, 115200)[0]
    print("Connect status: ", CON_STR[state])
    if (state == dType.DobotConnect.DobotConnect_NoError):
        # Clean Commnads Queued
        dType.SetQueuedCmdClear(api)
        
        # Asysns Motion Params Setting
        dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
        dType.SetEndEffectorParamsEx(api, 61, 0, 0, 1)
        dType.dSleep(1000)

    else:
        print("Try to connect your computer to Dobot again!!")
        exit()


def main():
    # Initialize Dobot
    api = dType.load()
    initialDobot(api, port)

    # UDP-Server Configuration
    UDP_IP = "192.168.1.3"
    UDP_PORT = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    count = 0
    poseError = 0
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if data != None:
                count += 1
                msg = bytes.decode(data)
                cmdDict = json.loads(msg)
                print("Message Number: %d" % cmdDict['Number'])
                # Move to (X, Y, Z)
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 0, cmdDict["X"],  cmdDict["Y"],  cmdDict["Z"], current_pose[3], 1)
                
                # Get current pose after executing Cmd
                current_pose = dType.GetPose(api)
                # Compare current pose with the sent coordinates
                if (current_pose[0] != cmdDict['X']) | (current_pose[1] != cmdDict['Y']) | (current_pose[2] != cmdDict['Z']):
                    poseError += 1
                    sock.sendto('Error', addr)
                else:
                    sock.sendto('OK', addr)
            
        except KeyboardInterrupt:
            dType.DisconnectDobot(api)
            print("Number of pose error: %d" % poseError)
            print("Number of received message: %d " % count)
            sock.close()
            exit()

 
if __name__ == "__main__":
    main()