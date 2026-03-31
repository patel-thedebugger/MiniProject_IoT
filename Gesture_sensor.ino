#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_APDS9960.h>
#include <ESP32Servo.h>

// -------- WIFI --------
const char* ssid = "4G";
const char* password = "9824775520RP";

// -------- SERVER --------
const char* serverName = "http://192.168.29.166:5000/api/gesture";

// -------- SENSOR --------
Adafruit_APDS9960 apds;

// -------- GESTURE BUFFER --------
String gestureSequence = "";
unsigned long lastGestureTime = 0;
const int gestureTimeout = 5000; // 5 sec pause
int lastLength = 0;
int sameCount = 0;
const int stabilityThreshold = 40;

//-----------Servo motor -----------
Servo myServo;
int servoPin = 18;

// -------- SEND FUNCTION --------
void sendToServer(String gestureSequence) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"gesture\":\"" + gestureSequence + "\"}";

    Serial.println("\nSending: " + jsonData);

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();

      Serial.print("Response: ");
      Serial.println(response);

      if (response.indexOf("GRANTED") >= 0) {
        Serial.println("✅ ACCESS GRANTED");

        // 🔓 OPEN (90°)
        Serial.println("Servo → 90° (OPEN)");
        myServo.write(90);

        delay(5000);  // wait 5 sec

        // 🔒 CLOSE (0°)
        Serial.println("Servo → 0° (CLOSE)");
        myServo.write(0);

      } else if (response.indexOf("LOCKED") >= 0) {
        Serial.println("🔒 SYSTEM LOCKED");
      } else {
        Serial.println("❌ ACCESS DENIED");
      }

    } else {
      Serial.print("Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }
}

// -------- SETUP --------
void setup() {
  Serial.begin(115200);
  myServo.attach(servoPin);
  myServo.write(0);  // initial position
  Wire.begin(21, 22);
  delay(500);

  Serial.println("Initializing APDS9960...");

  if (!apds.begin()) {
    Serial.println("❌ APDS9960 not detected!");
    while (1);
  }

  // Enable gesture detection
  apds.enableGesture(true);

  Serial.println("Gesture sensor READY 🚀");

  // WiFi connect
  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
}

// -------- LOOP --------
void loop() {

  delay(30);

  uint8_t gesture = apds.readGesture();

  // Detect gesture
  if (gesture != 0) {
    String gestureStr = "";

    switch (gesture) {
      case APDS9960_UP: gestureStr = "DOWN"; break;
      case APDS9960_DOWN: gestureStr = "UP"; break;
      case APDS9960_LEFT: gestureStr = "RIGHT"; break;
      case APDS9960_RIGHT: gestureStr = "LEFT"; break;
      default: return;
    }

    Serial.println("Detected: " + gestureStr);

    // ---- DEBOUNCE ----
    static String lastGesture = "";
    static unsigned long lastTime = 0;

   

    lastGesture = gestureStr;
    lastTime = millis();

    // Build sequence
    if (gestureSequence.length() > 0) {
      gestureSequence += "-";
    }
    gestureSequence += gestureStr;

    Serial.println("Current Sequence: " + gestureSequence);

    lastGestureTime = millis();
  }

  // -------- STABILITY CHECK --------
  if (gestureSequence.length() > 0) {

    if (gestureSequence.length() == lastLength) {
      sameCount++;
    } else {
      sameCount = 0;
      lastLength = gestureSequence.length();
    }

    // If stable for 20 cycles → send
    if (sameCount >= stabilityThreshold &&
    millis() - lastGestureTime > 1000) {
      Serial.println("\nStable Sequence Detected: " + gestureSequence);

      sendToServer(gestureSequence);

      // Reset
      gestureSequence = "";
      sameCount = 0;
      lastLength = 0;

      return;
    }
  }

  // -------- TIMEOUT (backup) --------
  if (gestureSequence.length() > 0 &&
      millis() - lastGestureTime > gestureTimeout) {

    Serial.println("\nTimeout Sequence: " + gestureSequence);

    sendToServer(gestureSequence);

    gestureSequence = "";
    sameCount = 0;
    lastLength = 0;
  }
}
