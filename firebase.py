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

now = datetime.now()

dateToday = str(date.today())
timeToday = now.strftime("%H:%M:%S")

data = {"PlateNumber":"000-111-222", "Location": "Lapasan Zone 2", "Date": dateToday, "Time": timeToday, "Notification": "on"}
#-------------------------------------------------------------------------------
# Create Data

db.child("Scanned").child((dateToday+" "+timeToday)).set(data)