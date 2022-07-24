from antares_http import antares
import sys
import random
import time

projectName = 'cobamqtt'
deviceName = 'coba'

antares.setDebug(True)
antares.setAccessKey('2eca1e61d429ec86:8cb1472de9987502')

# min = 1-89
# max = 90-560

range_set = {
    'min' : [1, 90],
    'max' : [90, 561]
}

def sensor_generator():
    rand_num = random.randint(1, 101)

    if rand_num <= 5 :
        return range_set['max']
    else :
        return range_set['min']
        
def sendData():
    for i in range(9):
        key = 'Sensor' + str(int(i+1))
        ranges = sensor_generator()
        dataToSend = {
            key : random.randint(ranges[0], ranges[1])
        }
        sentData = antares.send(dataToSend, projectName, deviceName)

while True:
    sendData()
    time.sleep(1)
    


# Get latest data
# latestData = antares.get(projectName, deviceName)

# Get all data
# allData = antares.getAll(projectName, deviceName, limit=10)

# Get only data IDs
# allDataId = antares.getAllId(projectName, deviceName, limit=50)

# Get specific data 
# specificData = antares.getSpecific(projectName, deviceName, 'cin_201898641')

# Get device ID
# deviceId = antares.getDeviceId(projectName, deviceName)

# Send by Device ID 
# sentByDevice = antares.sendById(dataToSend, 'cnt-478686259')

# Send data
# sentData = antares.send(dataToSend, projectName, deviceName)

# Get devices
# devices = antares.getDevices(projectName)

# Create device
# createdDevice = antares.createDevice(projectName, 'python-device');