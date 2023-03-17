import pyrebase
from datetime import date
import time
from datetime import datetime
import random

import time

# Initialize the Firebase app with your service account credentials
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
        exist = db.child("Vehicle_with_criminal_offense").child(PN).child("plateNumber").get()
        print(exist.val())
        if exist.val() != None:
            isApprehended = db.child("Vehicle_with_criminal_offense").child(PN).child("apprehended").get()
            print("isApprehended "+isApprehended.val())
            if isApprehended.val() != 'yes':
              # Create Data
              now = datetime.now()
              dateToday = str(date.today())
              timeToday = now.strftime("%H:%M:%S")
              crimeScanned = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()
              data = {"PlateNumber":PN, "Location": "Lapasan Zone 4", "Date": dateToday, "Time": timeToday, "Notification": "on", "Apprehended": "no", "CriminalOffense": crimeScanned.val()}
              db.child("Scanned").child((dateToday+" "+timeToday)).set(data)
              crime = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()
              dataPlateNumber = {"PlateNumber":PN, "Apprehended": "no","CriminalOffense": crime.val()}
              db.child("ScannedPlateNmber").child(PN).set(dataPlateNumber)
        else:
            print("Plate Number dont't exist")
    except Exception as e:
        
        print("Plate Number dont't exist "+ str(e))

# Keep track of the latest data
latest_data = None

# Continuously get the latest data added to the database
while True:
    
    data = db.child("ScannedQuery").order_by_key().limit_to_last(1).get()
    
    # Get the latest data
    # latest_data_key = max(data.key())
    # latest_data = data[latest_data_key]
    plateNum = data[0].val()

    print('Latest data:', plateNum['PlateNumber'])
    submitPlateNumber('4321')