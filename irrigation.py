import csv
import json
import schedule

import datetime
import requests
import pandas as pd
import tensorflow as tf
from apscheduler.schedulers.background import BackgroundScheduler

import sensorValues

irrigationModel = tf.keras.models.load_model(
    r"Tensorflow Models\\irrigation.h5")

min_val = 135
max_val = 600


def RangeScaling(val):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    else:
        return val


# ------- LIST ASSIGNMENT -------
min_max_values = []

# ------ READING MinMaxValue Csv Created During Normalization --------
with open(r"CSVs/minMaxVals.csv", "rt") as f:
    data = csv.reader(f)
    for row in data:
        min_max_values.append(row[0])
# ------ Converting to Float --------

for i in range(2, len(min_max_values)):
    min_max_values[i] = float(min_max_values[i])


def irrigate(parList):
 # ------ Converting to Float --------
        data = []
        for i in parList:
            data.append(float(i))

        data[1] = RangeScaling(data[1])
        data[2] = RangeScaling(data[2])

        # ------ Normalizing The Input To The Network --------
        data[0] = (data[0] - (min_max_values[2])) / (
            (min_max_values[3]) - (min_max_values[2])
        )
        data[1] = (data[1] - (min_max_values[4])) / (
            (min_max_values[5]) - (min_max_values[4])
        )
        data[2] = (data[2] - (min_max_values[6])) / (
            (min_max_values[7]) - (min_max_values[6])
        )
        data[3] = (data[3] - (min_max_values[8])) / (
            (min_max_values[9]) - (min_max_values[8])
        )
        data[4] = (data[4] - (min_max_values[10])) / (
            (min_max_values[11]) - (min_max_values[10])
        )

        # ------ Creating A Dataframe Object --------
        df = pd.DataFrame(
            [data], columns=["Light", "Moisture 1",
                "Moisture 2", "Temp", "Humidity"]
        )
        properties = list(df.columns.values)
        x = df[properties]

        # ------ Passing The inputData To Tensorflow irrigationModel --------
        prediction = irrigationModel.predict(x)
        print(prediction)
        answer = round(prediction[0][0], 0)

        # ------ Returning The Answer --------
        return str(answer)


def manualIrrigation(params):
    my_json_string = json.dumps(params)
    print(params)
    return params

def smartIrrigateToday():
    irrStatus = 1
    if not sensorValues.smartIrrigationToggle:
        irrStatus = 0

    params ={'irrDry': str(sensorValues.dryValue), 'irrWet': str(sensorValues.wetValue), 'irrStatus':str(irrStatus)}
    response = requests.post(url= "http://192.168.0.113:1880/irrigatetoday",json=params)

    if not sensorValues.smartIrrigationToggle:
        sched.pause_job("myjob")

sched = BackgroundScheduler(daemon=True)
sched.add_job(smartIrrigateToday,'interval',seconds=int(sensorValues.irrFreq),id="myjob")
sched.start(paused=True)

def smartIrrigation(params):
    sensorValues.irrFreq = params['irrFreq']
    sensorValues.dryValue = params['irrDry']
    sensorValues.wetValue = params['irrWet']
    sensorValues.smartIrrigationToggle = bool(params['irrStatus'])
    
    sched.resume()
    sched.resume_job("myjob")
    print(params)
    return params

def scheduleIrrigationDuration(params):
    date=params['SirrigationDate'][:10]
    time = params['SirrigationTime'][:10]
    sensorValues.datetime = datetime.strptime(date, '%y/%m/%d')
    print(params)
    return params

def scheduleIrrigationMoisture(params):
    print(params)
    return params