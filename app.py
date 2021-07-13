
import os

import schedule

# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import disease
import irrigation
import dataHandler

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

# Define a flask app
app = Flask(__name__)

#FRONTEND ROUTES
@app.route('/', methods=['GET'])
def index():
    # Main page
    return "HELLO ML"

@app.route('/diseasedoctor', methods=['GET'])
def DiseaseDoctor():
    # Main page
    return render_template('index.html')

@app.route('/SensorData', methods=["GET", "POST"])
def SensorData():
    params = request.json
    params = params[0]

    dataHandler.updateSensorValues(params)

    print(params)
    return render_template('SensorData.html')


#BACKEND ROUTES
@app.route('/diagnose', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        result = disease.diagnose(file_path)
        return result
    return None


@app.route("/calc", methods=["GET", "POST"])
def predict():
    params = request.json
    
    if params == None:
        answer = "No Data Recieved"
        return str(answer), 201

    elif params != None:
        parList = dataHandler.irrigateHandler(params)
        answer = irrigation.irrigate(parList)
        return str(answer), 201


@app.route('/manualIrrigation', methods=["GET", "POST"])
def manualIrrigation():
    params = request.json
    answer = irrigation.manualIrrigation(params)
    return answer
    
@app.route('/smartIrrigation', methods=["GET", "POST"])
def smartIrrigation():
    params = request.json
    answer = irrigation.smartIrrigation(params)
    return answer


@app.route('/scheduleIrrigationDuration', methods=["GET", "POST"])
def scheduleIrrigationDuration():
    # schedule.every(10).seconds.do(job)
    params = request.json
    answer = irrigation.scheduleIrrigationDuration(params)
    return answer

@app.route('/scheduleIrrigationMoisture', methods=["GET", "POST"])
def scheduleIrrigationMoisture():
    params = request.json
    answer = irrigation.scheduleIrrigationMoisture(params)
    return answer

if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 4449), app)
    # http_server.serve_forever()
    # app.run()
    app.run(debug=True, host="0.0.0.0", port=4449)


