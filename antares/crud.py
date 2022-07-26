from antares_http import antares

projectName = 'cobamqtt'
deviceName = 'coba2'

antares.setDebug(True)
antares.setAccessKey('2eca1e61d429ec86:8cb1472de9987502')


def send_to_antares(dataToSend):
    antares.send(dataToSend, projectName, deviceName)
