import requests
import joblib
import numpy as np
import time

# ===============================
# CONFIGURATION
# ===============================

NODEMCU_IP = "http://192.168.137.19/status"

THINGSPEAK_KEY = "3J6LJDI7PCAU2IVL"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ===============================
# LOAD MODEL
# ===============================

model = joblib.load("knn_landslide_model.pkl")
encoder = joblib.load("label_encoder.pkl")

print("Model Loaded Successfully")

# ===============================
# LOOP
# ===============================

while True:

    try:

        # -------------------------
        # GET DATA FROM NODEMCU
        # -------------------------
        response = requests.get(NODEMCU_IP)
        data = response.json()

        temperature = data["temperature"]
        humidity = data["humidity"]
        moisture = data["moisture"]
        vibration = data["vibration"]
        gyro = data["gyro"]

        print("\nSensor Values")
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Moisture:", moisture)
        print("Vibration:", vibration)
        print("Gyro:", gyro)

        # -------------------------
        # ML PREDICTION
        # -------------------------

        X = np.array([[temperature, humidity, moisture, vibration, gyro]])

        prediction = model.predict(X)
        result = encoder.inverse_transform(prediction)[0]

        # -------------------------
        # RULE BASED OVERRIDE
        # -------------------------

        if gyro > 2 and vibration == 1:
            result = "severe_landslide"

        elif gyro < 0.90 or vibration == 1:
            result = "moderate_landslide"

        print("Final Prediction:", result)

        # -------------------------
        # SEND DATA TO THINGSPEAK
        # -------------------------

        payload = {
            "api_key": THINGSPEAK_KEY,
            "field1": temperature,
            "field2": humidity,
            "field3": moisture,
            "field4": vibration,
            "field5": gyro
        }

        r = requests.get(THINGSPEAK_URL, params=payload)

        if r.status_code == 200:
            print("Data sent to ThingSpeak")
        else:
            print("ThingSpeak error")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)