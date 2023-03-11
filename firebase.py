import pyrebase
from datetime import date
import time
from datetime import datetime

firebaseConfig = {
  "apiKey": "AIzaSyB_4cNoh3klH4mKPSd7dhJzr5QUGoLihy8",
  "authDomain": "scanmemaster-9da58.firebaseapp.com",
  "projectId": "scanmemaster-9da58",
  "databaseURL" : "https://scanmemaster-9da58-default-rtdb.firebaseio.com/",
  "storageBucket": "scanmemaster-9da58.appspot.com",
  "messagingSenderId": "270970295536",
  "appId": "1:270970295536:web:02ecd24ee665578e6d9e35",
  "measurementId": "G-27WEKS22GB"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def submitPlateNumber(PN):
    try:
        now = datetime.now()
        dateToday = str(date.today())
        timeToday = now.strftime("%H:%M:%S")
        isApprehended = db.child("Vehicle_with_criminal_offense").child(PN).child("apprehended").get()
        crimeScanned = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()

        # Scanned
        data = {"PlateNumber":PN, "Location": "Lapasan Zone 4", "Date": dateToday, "Time": timeToday, "Notification": "on", "Apprehended": isApprehended.val(), "CriminalOffense": crimeScanned.val()}
        db.child("Scanned").child((dateToday+" "+timeToday)).set(data)

        # ScannedPlateNmber
        dataPlateNumber = {"PlateNumber":PN, "Apprehended": isApprehended.val(),"CriminalOffense": crimeScanned.val()}
        db.child("ScannedPlateNmber").child(PN).set(dataPlateNumber)
      # exist = db.child("Vehicle_with_criminal_offense").child(PN).child("plateNumber").get()
      # print(exist.val())
      # if exist.val() != None:
      #     isApprehended = db.child("Vehicle_with_criminal_offense").child(PN).child("apprehended").get()
      #     print("isApprehended "+isApprehended.val())
      #     if isApprehended.val() != 'yes':
      #       # Create Data
      #       now = datetime.now()
      #       dateToday = str(date.today())
      #       timeToday = now.strftime("%H:%M:%S")
      #       crimeScanned = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()
      #       data = {"PlateNumber":PN, "Location": "Lapasan Zone 4", "Date": dateToday, "Time": timeToday, "Notification": "on", "Apprehended": "no", "CriminalOffense": crimeScanned.val()}
      #       db.child("Scanned").child((dateToday+" "+timeToday)).set(data)
      #       crime = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()
      #       dataPlateNumber = {"PlateNumber":PN, "Apprehended": "no","CriminalOffense": crime.val()}
      #       db.child("ScannedPlateNmber").child(PN).set(dataPlateNumber)
      # else:
      #     print("Plate Number dont't exist")
        print('plate number submitted to db')
    except Exception as e:
        
        print("Plate Number dont't exist "+ str(e))

#isulod ang ang plate number sa plateNumber na variable gaw
plateNumber = "321"

submitPlateNumber(plateNumber)
  




