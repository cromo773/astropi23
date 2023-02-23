"""

This is the Astro Pi Mission Space Lab project by Team-Rex, Stiftsschule Einsiedeln

"""

from gpiozero import CPUTemperature
from pathlib import Path
from time import sleep
from picamera import PiCamera
from sense_hat import SenseHat
from logzero import logger, logfile
from orbit import ISS
from datetime import datetime, timedelta
import csv

# creates a new csv file and adds the header row
def create_csv_file(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity","CPU Temperature")
        writer.writerow(header)

# adds a row of data to the file
def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def capture(camera, image):
    camera.capture(image)

base_folder = Path(__file__).parent.resolve()
data_file = base_folder / "data.csv"

# setting up the sense hat
sense = SenseHat()

# this is the logfile's name
logfile(base_folder/"events.log")

# Setting up the camera
cam = PiCamera()
cam.resolution = (1296, 972)

# Initialise the CSV file
data_file = base_folder/"data.csv"
create_csv_file(data_file)


cpu = CPUTemperature()
#print(cpu.temperature)

# Initialise the photo counter
counter = 1

# Record the start and current time
start_time = datetime.now()
now_time = datetime.now()

# Run a loop for 178 minutes, almost 3 hours
while (now_time < start_time + timedelta(minutes=178)):
    try:
        humidity = round(sense.humidity, 4)
        temperature = round(sense.temperature, 4)
        cpu_temp = round(cpu.temperature, 4)

        # Get coordinates of location on Earth below the ISS
        location = ISS.coordinates()

        # Save the data to the file
        data = (
            counter,
            datetime.now(),
            location.latitude.degrees,
            location.longitude.degrees,
            temperature,
            humidity,
            cpu_temp
        )
        add_csv_data(data_file, data)

        # Capture image
        image_file = f"{base_folder}/photo_{counter:03d}.jpg"
        capture(cam, image_file)

        # Log event
        logger.info(f"iteration {counter}")
        counter += 1

        # waiting time about one minute until it starts again
        sleep(58)
        # Updating the current time
        now_time = datetime.now()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')