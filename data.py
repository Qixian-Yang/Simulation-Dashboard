#each data will have source sensorID, time, temperature and pressure
class data:
    global sensorID_dict
    def __init__(self,timestamp,workingtime,sensorID,temperature,vibrationx,vibrationy,vibrationz):
        self.sensorID = sensorID
        self.timestamp=timestamp
        self.workingtime=workingtime
        self.temperature=temperature
        self.vibrationx=vibrationx
        self.vibrationy=vibrationy
        self.vibrationz=vibrationz
    def __str__(self):
        return("Sensor "+self.sensorID+" got: temperature "+self.temperature+" vibrationx "+self.vibrationx+" vibrationy "+self.vibrationy+" vibrationz "+self.vibrationz+" in timestamp "+self.timestamp)




