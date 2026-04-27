#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <MPU6050.h>
#include <DHT.h>

#define DHTPIN D0
#define DHTTYPE DHT11

#define MOISTURE_PIN A0
#define VIB_PIN D5

const char* ssid = "Project";
const char* password = "12345678";

ESP8266WebServer server(80);
LiquidCrystal_I2C lcd(0x27,16,2);
MPU6050 mpu;
DHT dht(DHTPIN, DHTTYPE);

float temperature;
float humidity;
int moisture;
int vibration;

float gyroValue;

String json;

void handleStatus()
{
  json = "{";
  json += "\"temperature\":" + String(temperature) + ",";
  json += "\"humidity\":" + String(humidity) + ",";
  json += "\"moisture\":" + String(moisture) + ",";
  json += "\"vibration\":" + String(vibration) + ",";
  json += "\"gyro\":" + String(gyroValue);
  json += "}";

  server.send(200,"application/json",json);
}

void setup()
{
  Serial.begin(115200);

  pinMode(VIB_PIN,INPUT);

  lcd.begin();
  lcd.backlight();

  Wire.begin(D2,D1);
  mpu.initialize();

  dht.begin();

  WiFi.begin(ssid,password);

  lcd.setCursor(0,0);
  lcd.print("Connecting WiFi");

  while(WiFi.status()!=WL_CONNECTED)
  {
    delay(500);
  }

  lcd.clear();
  lcd.print("IP:");
  lcd.setCursor(0,1);
  lcd.print(WiFi.localIP());

  server.on("/status",handleStatus);
  server.begin();
}

void loop()
{
  server.handleClient();

  // DHT
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  // Other sensors
  moisture = analogRead(MOISTURE_PIN);
  vibration = digitalRead(VIB_PIN);

  // MPU6050
  int16_t ax,ay,az;
  mpu.getAcceleration(&ax,&ay,&az);

  float x = ax/16384.0;
  float y = ay/16384.0;
  float z = az/16384.0;

  gyroValue = sqrt(x*x + y*y + z*z);

  // LCD
  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("T:");
  lcd.print(temperature);

  lcd.setCursor(8,0);
  lcd.print("M:");
  lcd.print(moisture);

  lcd.setCursor(0,1);
  lcd.print("V:");
  lcd.print(vibration);

  lcd.setCursor(6,1);
  lcd.print("G:");
  lcd.print(gyroValue,2);

  delay(2000);
}
