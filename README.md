# Gesture-Based Smart Door Access Control System

## Overview

The **Gesture-Based Smart Door Access Control System** is an IoT-based security solution that enables users to unlock a door using predefined hand gesture patterns instead of traditional keys, RFID cards, or passwords.

The system uses an **ESP32 microcontroller**, an **APDS9960 gesture sensor**, and a **servo motor** to detect gesture sequences, validate them through a Flask-based backend server, and automatically control door access.

This project demonstrates the integration of **Embedded Systems**, **IoT**, **Computerized Access Control**, and **Web Technologies** into a smart security application.

---

## Features

* Contactless gesture-based authentication
* Custom gesture sequence registration
* Real-time access validation
* Automatic door opening and closing
* User management dashboard
* Access logging and monitoring
* SQLite database integration
* Wi-Fi communication between ESP32 and server
* Real-time status response (Granted / Denied)

---

## System Architecture

```text
+------------------+
|  User Gesture    |
+--------+---------+
         |
         v
+------------------+
| APDS9960 Sensor  |
+--------+---------+
         |
         v
+------------------+
|      ESP32       |
| Gesture Parsing  |
+--------+---------+
         |
 HTTP POST Request
         |
         v
+------------------+
| Flask Web Server |
+--------+---------+
         |
         v
+------------------+
| SQLite Database  |
+--------+---------+
         |
 Validation Result
         |
         v
+------------------+
| ESP32 + Servo    |
| Door Control     |
+------------------+
```

---

## Hardware Components

| Component               | Description           |
| ----------------------- | --------------------- |
| ESP32 Dev Board         | Main controller       |
| APDS9960 Gesture Sensor | Detects hand gestures |
| Servo Motor (SG90/MG90) | Door lock mechanism   |
| Jumper Wires            | Connections           |
| Breadboard              | Prototyping           |
| Wi-Fi Network           | Communication         |

---

## Software Stack

### Embedded Side

* Arduino IDE
* ESP32 Board Package
* Adafruit APDS9960 Library
* ESP32Servo Library
* WiFi Library
* HTTPClient Library

### Backend Side

* Python 3.x
* Flask
* SQLite3
* HTML
* CSS
* JavaScript

---

## Supported Gestures

The APDS9960 sensor detects four primary directions:

| Sensor Gesture | Registered As |
| -------------- | ------------- |
| UP             | DOWN          |
| DOWN           | UP            |
| LEFT           | RIGHT         |
| RIGHT          | LEFT          |

Example authentication pattern:

```text
UP-RIGHT-DOWN-LEFT
```

Users must perform the exact registered sequence to gain access.

---

## Project Workflow

### Step 1: Gesture Detection

The APDS9960 sensor captures directional hand movements.

### Step 2: Sequence Formation

ESP32 continuously builds a gesture sequence.

Example:

```text
UP-RIGHT-DOWN
```

### Step 3: Server Communication

ESP32 sends the sequence to the Flask server:

```json
{
  "gesture": "UP-RIGHT-DOWN"
}
```

### Step 4: Authentication

The Flask backend checks the gesture pattern against registered users stored in SQLite.

### Step 5: Response

Server returns:

```json
{
  "status": "GRANTED",
  "user": "John"
}
```

or

```json
{
  "status": "DENIED",
  "user": "Unknown"
}
```

### Step 6: Door Automation

If access is granted:

1. Servo rotates to 90°
2. Door unlocks
3. Waits 5 seconds
4. Servo returns to 0°
5. Door locks

---

## Database Structure

### Users Table

```sql
CREATE TABLE users(
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    gesture TEXT
);
```

### Logs Table

```sql
CREATE TABLE logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    entered_gesture TEXT,
    status TEXT,
    timestamp TEXT
);
```

---

## Installation Guide

### 1. Clone Repository

```bash
git clone https://github.com/patel-thedebugger/MiniProject_IoT.git

cd MiniProject_IoT
```

### 2. Install Python Dependencies

```bash
pip install flask
```

### 3. Run Flask Server

```bash
python app.py
```

Server starts at:

```text
http://localhost:5000
```

### 4. Configure ESP32

Update Wi-Fi credentials:

```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
```

Update server IP:

```cpp
const char* serverName =
"http://YOUR_PC_IP:5000/api/gesture";
```

### 5. Upload Arduino Code

* Open Arduino IDE
* Select ESP32 Board
* Upload sketch
* Open Serial Monitor

---

## API Documentation

### Verify Gesture

**Endpoint**

```http
POST /api/gesture
```

### Request

```json
{
  "gesture": "UP-RIGHT-DOWN"
}
```

### Success Response

```json
{
  "status": "GRANTED",
  "user": "John Doe"
}
```

### Failure Response

```json
{
  "status": "DENIED",
  "user": "Unknown"
}
```

---

## Dashboard Features

### User Management

* View registered users
* Add new users
* Edit existing users
* Manage gesture patterns

### Access Monitoring

* Real-time access logs
* Authentication status
* User tracking
* Timestamp records

---

## Security Advantages

* Contactless authentication
* Difficult to replicate gesture patterns
* No physical key required
* Audit logs for every access attempt
* Centralized user management

---

## Future Enhancements

* Face Recognition Integration
* Fingerprint Authentication
* MQTT Communication
* Cloud Database Support
* Mobile Application
* Email/SMS Alerts
* Multi-factor Authentication
* Remote Door Monitoring

---

## Project Outcomes

This project successfully demonstrates:

* IoT Device Communication
* Embedded Systems Programming
* Real-Time Authentication
* Smart Access Control
* Database Management
* Web Application Development
* Hardware-Software Integration

---

## Authors

**Rushi Patel**

IoT & Embedded Systems Enthusiast

GitHub: https://github.com/patel-thedebugger

---

## License

This project is developed for educational and academic purposes. Feel free to modify and extend it for learning and research.
