#each data will have source sensorID, time, temperature and pressure
s1x=100
s1y=100
s1z=100
s1t=80
s2x=100
s2y=100
s2z=100
s2t=80
s3x=100
s3y=100
s3z=100
s3t=80
class risk:
    global sensorID_dict
    risklevel=""
    place=""
    riskname=""
    influence=""
    time=""
    description=""
    solution=""
    sensortype=0

    def __init__(self,risklevel="",place="",riskname="",influence="",description="",solution="",sensortype=0,time=""):
        self.risklevel = risklevel
        self.place=place
        self.riskname=riskname
        self.description=solution
        self.influence=influence
        self.solution=solution
        self.sensortype=sensortype
        self.time=time

    def tostring(self):
        return("Risklevel:"+self.risklevel+"\n"+"Place:"+self.place+"\n"+"Riskname:"+self.riskname+"\n"+"Description:"+self.description+"\n"+"Influence:"+self.influence+"\n"+"Solution:"+self.solution+"\n"+"Time:"+self.time)


    def __str__(self):
        return("Risklevel:"+self.risklevel+" place:"+self.place+" riskname:"+self.riskname+self.description+self.influence+self.solution)

    @staticmethod
    def get_innormaldata(fulldata=""):
        print("***********************Get_innormaldata***********************")
        global s1x,s1y,s1z,s1t,s2x,s2y,s2z,s2t,s3x,s3y,s3z,s3t
        li=[]
        for i in fulldata:
            for j in fulldata[i]:
                if j.sensorID=="1":
                    if float(j.vibrationx)>=s1x:
                        li.append([j,11])
                    if float(j.vibrationy)>=s1y:
                        li.append([j,12])
                    if float(j.vibrationz)>=s1z:
                        li.append([j,13])
                    if float(j.temperature)>=s1t:
                        li.append([j,14])
                if j.sensorID=="2":
                    if float(j.vibrationx)>=s2x:
                        li.append([j,21])
                    if float(j.vibrationy)>=s2y:
                        li.append([j,22])
                    if float(j.vibrationz)>=s2z:
                        li.append([j,23])
                    if float(j.temperature)>=s2t:
                        li.append([j,24])
                if j.sensorID=="3":
                    if float(j.vibrationx)>=s3x:
                        li.append([j,31])
                    if float(j.vibrationy)>=s3y:
                        li.append([j,32])
                    if float(j.vibrationz)>=s3z:
                        li.append([j,33])
                    if float(j.temperature)>=s3t:
                        li.append([j,34])
        return li

    @staticmethod
    def belt_wear(li=""):
        return False

    @staticmethod
    def belt_fall_off(li=""):
        return False

    @staticmethod
    def belt_too_loose(li=""):
        return False

    @staticmethod
    def belt_too_tight(li=""):
        return True

    @staticmethod
    def wheel_wear(li=""):
        return False

    @staticmethod
    def drive_shaft_wear(li=""):
        return False

    @staticmethod
    def wheel_fixed_loose(li=""):
        return False

    @staticmethod
    def wheel_moving(li=""):
        return False

    @staticmethod
    def overload(li=""):
        count = 0
        timelist=[]
        for i in li:
            if(i[1]==14):
                count+=1
                timelist.append(i[0].timestamp)

        if(count!=0):
            if(count<3):
                return (risk(
                    risklevel="blue",
                    place="1",
                    riskname="Overload",
                    influence="Won't cause serious result",
                    description="Just overload, focus on the mechine and make sure it won't too hot",
                    solution="Just overload, focus on the mechine and make sure it won't too hot",
                    time=str(timelist)))
            elif(count<5):
                return (risk(
                    risklevel="yellow",
                    place="1",
                    riskname="Overload",
                    influence="Overload for a long time may cause serious damage to the machine",
                    description="Multiple overloads indicate that the machine is overused and needs to be allocated properly",
                    solution="Reduce concentrated use to prevent overheating",
                    time=str(timelist)))
            else:
                return (risk(
                    risklevel="red",
                    place="1",
                    riskname="Motor overload",
                    influence="Frequent overloads can cause permanent damage to the motor",
                    description="Long time overload makes the motor temperature always too high, at a dangerous level",
                    solution="Suspend use and perform maintenance",
                    time=str(timelist)))

        return None
        



    @staticmethod
    def unstable_track(li=""):
        return True

    @staticmethod
    def cargo_fixed_loose(li=""):
        return False

    @staticmethod
    def risk_analyse(fulldata=""):
        returnrisk = []
        li = risk().get_innormaldata(fulldata)
        if(risk().belt_wear(li)):
            returnrisk.append(risk(
                risklevel="blue",
                place="2",
                riskname="Belt wear",
                influence="Won't cause serious result",
                description="The belt will broke, but it can still work a few days",
                solution="Change the belt later, just focus on it now",
                time=li[0].time))
        if(risk().belt_fall_off(li)):
            returnrisk.append(risk(
                risklevel="red",
                place="2",
                riskname="Belt fall off",
                influence="Machine is under danger state",
                description="The belt has been fall off, machine should be stopped immediately!",
                solution="Machine need to be stopped to fix"))
        if(risk().belt_too_loose(li)):
            returnrisk.append(risk(
                risklevel="yellow",
                place="2",
                riskname="Belt too loose",
                influence="This risk will be danger soon",
                description="Belt is too loose, and need to be fixed",
                solution="Fix it but this risk is not so hurry",
                sensortype=1))
        if(risk().belt_too_tight(li)):
            returnrisk.append(risk(
                risklevel="blue",
                place="2",
                riskname="Belt too tight",
                influence="Won't cause serious result",
                description="The belt is too tight",
                solution="Adjust the belt again, but not so hurry",
                sensortype=1))
        if(risk().wheel_wear(li)):
            returnrisk.append(risk(
                risklevel="blue",
                place="2",
                riskname="Wheel wear",
                influence="Won't cause serious result",
                description="The wheel will broke, but it can still work a few days",
                solution="Change the belt later, just focus on it now"))
        if(risk().drive_shaft_wear(li)):
            returnrisk.append(risk(
                risklevel="blue",
                place="1",
                riskname="Drive shaft wear",
                influence="Won't cause serious result",
                description="The drive shaft will broke, but it can still work a few days",
                solution="Change the drive shaft later, just focus on it now"))
        if(risk().wheel_fixed_loose(li)):
            returnrisk.append(risk(
                risklevel="yellow",
                place="1",
                riskname="Wheel fixed loose",
                influence="This risk will be danger soon",
                description="Wheel is too loose, and need to be fixed",
                solution="Fix it but this risk is not so hurry"))
        if(risk().wheel_moving(li)):
            returnrisk.append(risk(
                risklevel="red",
                place="1",
                riskname="Wheel moving",
                influence="Machine is under danger state",
                description="The wheel has been moving too much, machine should be stopped immediately!",
                solution="Machine need to be stopped to fix"))
        c = risk().overload(li)
        if(c!=None):
            returnrisk.append(c)
        if(risk().unstable_track(li)):
            returnrisk.append(risk(
                risklevel="blue",
                place="3",
                riskname="Unstable track",
                influence="Won't cause serious result",
                description="Track should be replaced",
                solution="Track should be changed, but it is not hurry"))
        if(risk().cargo_fixed_loose(li)):
            returnrisk.append(risk(
                risklevel="yellow",
                place="1",
                riskname="Cargo fixed loose",
                influence="This risk will be danger soon",
                description="Cargo fixed loose, it is danger for passengers",
                solution="Fix it but this risk is not so hurry"))
        for i in returnrisk:
            print(i.tostring())
            print("\n")
        return returnrisk
        