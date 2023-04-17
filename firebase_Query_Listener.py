import pyrebase
from datetime import date
import time
from datetime import datetime
import random
import threading
import time
import os

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

def submitPlateNumber():
    my_strings = ["RPC7777", "x", "ABC1234", "AAD1781", "y","RPC7777", "c", "ABC1234", "AAD1781", "u","RPC7777", "v", "ABC1234", "CCD1781", "i"]
    while True:  
        PN = random.choice(my_strings)
        print(PN)
        try:
            # now = datetime.now()
            # dateToday = str(date.today())
            # timeToday = now.strftime("%H:%M:%S")
            # isApprehended = db.child("Vehicle_with_criminal_offense").child(PN).child("apprehended").get()
            # crimeScanned = db.child("Vehicle_with_criminal_offense").child(PN).child("criminalOffense").get()
            # Scanned
            data = {"PlateNumber":PN}
            db.child("ScannedQuery").set(data)

            # # ScannedPlateNmber
            # dataPlateNumber = {"PlateNumber":PN, "Apprehended": isApprehended.val(),"CriminalOffense": crimeScanned.val()}
            # db.child("ScannedPlateNumberQuery").set(dataPlateNumber)

            print('plate number submitted to db')
        except Exception as e:
            
            print("Plate Number dont't exist "+ str(e))
        print()
        print('submitPlateNumber')
        print('Latest data:', PN)
        print()
        time.sleep(1)

def checkExist():
    while True:
        filename = "scanned_platenumbers.txt"
        first_line = ""
        # Open the file for reading and writing
        with open(filename, "r+") as file:
            # Read the first line of the file
            first_line = file.readline().strip()
            # Read the remaining lines of the file
            remaining_lines = file.readlines()
            # Overwrite the file with the remaining lines
            file.seek(0)
            file.writelines(remaining_lines)
            file.truncate()
            # Close the file
            file.close()
        plateNum = first_line
        
        try:
            exist = db.child("Vehicle_with_criminal_offense").child(plateNum).child("plateNumber").get()
            print(exist.val())
            if exist.val() != None:
                isApprehended = db.child("Vehicle_with_criminal_offense").child(plateNum).child("apprehended").get()
                print("isApprehended "+isApprehended.val())
                if isApprehended.val() != 'yes':
                    # Create Data
                    nowD = datetime.now()
                    dateToday = str(date.today())
                    timeToday = nowD.strftime("%H:%M:%S")
                    crimeScanned = db.child("Vehicle_with_criminal_offense").child(plateNum).child("criminalOffense").get()
                    data = {"PlateNumber":plateNum, "Location": "Lapasan Zone 4", "Date": dateToday, "Time": timeToday, "Notification": "on", "Apprehended": "no", "CriminalOffense": crimeScanned.val()}
                    db.child("Scanned").child((dateToday+" "+timeToday)).set(data)
                    crime = db.child("Vehicle_with_criminal_offense").child(plateNum).child("criminalOffense").get()
                    dataPlateNumber = {"PlateNumber":plateNum, "Apprehended": "no","CriminalOffense": crime.val()}
                    db.child("ScannedPlateNumber").child(plateNum).set(dataPlateNumber)

                    #For Notification
                    db.child("ScannedNotification").set(data)
                    db.child("ScannedPlateNumberNotification").set(dataPlateNumber)
            else:
                print("Plate Number dont't exist")
        except Exception as e:
            
            print("Plate Number dont't exist "+ str(e))
        print()
        print('checkDatabase')
        print('Latest data:', plateNum)
        print()
        time.sleep(1)


def saveForQuery():
    filename = "scanned_platenumbers.txt"
    prevPN = ''
    # Create the file if it doesn't exist
    if not os.path.isfile(filename):
        open(filename, "w").close()

    while True:
        #Read the latest scanned on the database
        plateNum = db.child("ScannedQuery").child("PlateNumber").get()
        if plateNum.val() != prevPN:
            # Open the file in append mode
            with open(filename, "a") as file:
                # Get the text to append from the user
                plateNum = plateNum.val()
                # Append the text to the end of the file
                file.write(plateNum+ "\n")
                # Close the file
                file.close()
            print('checkdatabase')
            prevPN = plateNum
            time.sleep(1)
       
# Keep track of the latest data
latest_data = None

# Continuously get the latest data added to the database
while True:
    task1 = threading.Thread(target=submitPlateNumber)
    task2 = threading.Thread(target=saveForQuery)
    task3 = threading.Thread(target=checkExist)

    task1.start()
    task2.start()
    task3.start()

    task1.join()
    task2.join()
    task3.join()