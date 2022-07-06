import csv
import socket
import time
import json

# Read Coordiates
def readCoordinates():
    coodinates = []
    print('Reading file!')
    with open('Coordinates.csv', 'r') as file:
        number = 0
        content = csv.reader(file)
        print(content)
        for row in content:
            cmdDict = {'Number': 0, 'X': 0, 'Y': 0, 'Z': 0}
            number += 1
            cmdDict['Number'] = number
            cmdDict['X'] = float(row[0])
            cmdDict['Y'] = float(row[1])
            cmdDict['Z'] = float(row[2])
            coodinates.append(cmdDict)
        print(number)
    return coodinates


def sendCmd(sock: socket, data, serverAddr, timeout: int):
    sock.sendto(str(data).encode('UTF-8'), serverAddr)
    sendTime = time.time()
    # Wait for ACK
    while time.time() - sendTime < timeout:
        ack, addr = sock.recvfrom(200)
        if ack == 'OK':
            print("ACK - OK")
            break
        elif ack == 'Error':
            print("ACK - ERROR, resend again!")
            sock.sendto(str(data).encode('UTF-8'), serverAddr)


def main():
    # UDP-Client Configuration
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8080
    serverAddr = (UDP_IP, UDP_PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    coordinates = readCoordinates()
    number = 0
    for coordinate in coordinates:
        try:
            number += 1
            #sock.sendto(json.dumps(coordinate).encode('UTF-8'), (UDP_IP, UDP_PORT))
            print("Sending....... %d " % number)
            sendCmd(sock, coordinate, serverAddr, 1)
            time.sleep(0.5)

        except KeyboardInterrupt:
            sock.close()
            print("Number of sent messages: %d " % number)
            exit()
            
    print("Number of sent messages: %d " % number)


if __name__ == "__main__":
    main()