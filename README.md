# Landslide-Prediction
🌍 Landslide Prediction System (GeoGuard)
📌 Overview

The Landslide Prediction System is an AI-powered solution designed to monitor environmental conditions and predict potential landslides in real time. This project integrates IoT sensors, machine learning, and web-based visualization to provide early warnings and improve disaster preparedness.

🚀 Features
📡 Real-time data collection using IoT (ESP8266)
🤖 Machine Learning-based landslide prediction (KNN model)
📊 Data preprocessing using scaling and encoding
🌐 Simple web interface for monitoring
⚡ Early warning capability for high-risk conditions

🛠️ Tech Stack
💻 Software
Python
Scikit-learn
Pandas & NumPy
Flask (optional for backend)

🔌 Hardware
ESP8266 (NodeMCU)
Sensors (e.g., soil moisture, rainfall, vibration)

🌐 Frontend
HTML

⚙️ How It Works
Data Collection
Sensors collect environmental data such as soil moisture, rainfall, and ground vibrations.
Data Processing
The collected data is preprocessed using:
Standard Scaler
Label Encoder
Model Prediction
A trained K-Nearest Neighbors (KNN) model predicts whether a landslide is likely.
Alert System
If risk is high, the system can trigger alerts (extendable to SMS/notifications).

🙌 Acknowledgment

This project was developed as part of academic research to explore real-time disaster prediction using AI and IoT.
