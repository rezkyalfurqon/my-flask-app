import random

range_set = {
    1: [2,88],
    2: [2,88],
    3: [0, 0],
    4: [0, 0],
    5: [0, 0],
    6: [0, 0],
    7: [0, 0],
    8: [89, 99],
    9: [0, 0],
}

        
def get_data_dummy(realSensor = 0):
    dataToSend = {}
    for i in range(9):
        key = 'Sensor' + str(int(i + 1))
        ranges = range_set[i + 1]
        dataToSend[key] = random.randint(ranges[0], ranges[1])

    dataToSend['Sensor10'] = float(realSensor)

    return dataToSend 


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