import sensorValues

def irrigateHandler(params):
    paramIndex = [6, 4, 5, 2, 3]
    parList = []
    parDict = params[0]
    parListValues = list(parDict.values())

    for i in paramIndex:
        parList.append(parListValues[i])
    
    return parList

def updateSensorValues(params):
    sensorValues.DATE = params['Date']
    sensorValues.TIME = params['Time']

    sensorValues.TEMP = params['Temp']
    sensorValues.HUMIDITY = params['Humidity']

    sensorValues.SM1 = params['SM1']
    sensorValues.SM2 = params['SM2']

    sensorValues.LIGHT = params['Light']
