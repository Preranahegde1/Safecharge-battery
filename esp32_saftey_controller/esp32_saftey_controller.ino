#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// PYNQ UART2
HardwareSerial PYNQUART(2);

// Sensor Pins
const int DS18B20_PIN = 19;
const int ACS712_PIN  = 35;
const int VOLTAGE_PIN = 32;

// Fault Potentiometers
const int POT_VOLT = 33;
const int POT_CURR = 36;
const int POT_TEMP = 39;

// Outputs & Actuators
const int RELAY_PIN  = 26;
const int BUZZER_PIN = 25;
const int LED_GREEN  = 2;
const int LED_YELLOW = 4;
const int LED_RED    = 15;

// Buttons
const int BTN_START = 27;
const int BTN_RESET = 14;
const int BTN_TEST  = 13;
const int BTN_MENU  = 23;

OneWire oneWire(DS18B20_PIN);
DallasTemperature temperatureSensor(&oneWire);

const float ACS_ZERO_MV = 1749.5;
const float ACS_SENSITIVITY = 185.0;
const float ACS_DIVIDER_FACTOR = 1.5;

const float MAX_VOLTAGE = 5.5;
const float MAX_CURRENT = 7.5;
const float TEMP_WARNING = 32.0;
const float MAX_TEMPERATURE = 40.0;
const int FAULT_POT_LIMIT = 90;

bool systemRunning = false;
bool faultLatched = false;
bool manualFault = false;
bool tempSensorFault = false;

unsigned long lastSample = 0;
unsigned long lastLCD = 0;
unsigned long lastUART = 0;

float voltage = 0, current = 0, temperature = 0, power = 0;
int potV = 0, potI = 0, potT = 0;

void setup() {
  Serial.begin(115200);
  PYNQUART.begin(115200, SERIAL_8N1, 16, 17);

  analogReadResolution(12);
  analogSetPinAttenuation(ACS712_PIN, ADC_11db);
  analogSetPinAttenuation(VOLTAGE_PIN, ADC_11db);
  analogSetPinAttenuation(POT_VOLT, ADC_11db);
  analogSetPinAttenuation(POT_CURR, ADC_11db);
  analogSetPinAttenuation(POT_TEMP, ADC_11db);

  temperatureSensor.begin();
  temperatureSensor.setResolution(10);

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  pinMode(BTN_START, INPUT_PULLUP);
  pinMode(BTN_RESET, INPUT_PULLUP);
  pinMode(BTN_TEST, INPUT_PULLUP);
  pinMode(BTN_MENU, INPUT_PULLUP);

  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);

  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("SAFETY SYSTEM");
  lcd.setCursor(0, 1);
  lcd.print("INITIALIZING");
  delay(2000);
}

void readSensors() {
  temperatureSensor.requestTemperatures();
  float dsTemp = temperatureSensor.getTempCByIndex(0);
  if (dsTemp == DEVICE_DISCONNECTED_C) {
    tempSensorFault = true;
    temperature = -127.0;
  } else {
    tempSensorFault = false;
    temperature = dsTemp;
  }

  float sensorVoltage = analogReadMilliVolts(VOLTAGE_PIN) / 1000.0;
  voltage = sensorVoltage * 5.0;

  float acs_mV = analogReadMilliVolts(ACS712_PIN);
  float diff = (acs_mV - ACS_ZERO_MV) * ACS_DIVIDER_FACTOR;
  current = abs(diff / ACS_SENSITIVITY);
  power = voltage * current;

  potV = map(analogRead(POT_VOLT), 0, 4095, 0, 100);
  potI = map(analogRead(POT_CURR), 0, 4095, 0, 100);
  potT = map(analogRead(POT_TEMP), 0, 4095, 0, 100);
}

void safetyCheck() {
  bool vFault = voltage > MAX_VOLTAGE || potV >= FAULT_POT_LIMIT;
  bool iFault = current > MAX_CURRENT || potI >= FAULT_POT_LIMIT;
  bool tFault = temperature > MAX_TEMPERATURE || potT >= FAULT_POT_LIMIT;
  bool anyFault = vFault || iFault || tFault || tempSensorFault || manualFault;
  if (anyFault) faultLatched = true;
}

void updateOutputs() {
  if (faultLatched) {
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_RED, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    return;
  }

  if (!systemRunning) {
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_RED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    return;
  }

  bool warning = temperature >= TEMP_WARNING || potV >= 70 || potI >= 70 || potT >= 70;
  if (warning) {
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, HIGH);
    digitalWrite(LED_RED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    return;
  }

  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(BUZZER_PIN, LOW);
}

void updateLCD() {
  if (millis() - lastLCD < 2000) return;
  lastLCD = millis();
  lcd.clear();

  if (tempSensorFault) {
    lcd.setCursor(0, 0); lcd.print("TEMP SENSOR ERR");
    lcd.setCursor(0, 1); lcd.print("RELAY CUT OFF");
    return;
  }
  if (faultLatched) {
    lcd.setCursor(0, 0); lcd.print("!! FAULT !!");
    lcd.setCursor(0, 1); lcd.print("RELAY CUT OFF");
    return;
  }
  if (!systemRunning) {
    lcd.setCursor(0, 0); lcd.print("SYSTEM READY");
    lcd.setCursor(0, 1); lcd.print("Press START");
    return;
  }
  lcd.setCursor(0, 0);
  lcd.print("V:"); lcd.print(voltage, 2); lcd.print(" I:"); lcd.print(current, 2);
  lcd.setCursor(0, 1);
  lcd.print("T:"); lcd.print(temperature, 1); lcd.print(" P:"); lcd.print(power, 1);
}

void checkButtons() {
  if (digitalRead(BTN_START) == LOW) { systemRunning = true; delay(300); }
  if (digitalRead(BTN_RESET) == LOW) { faultLatched = false; manualFault = false; delay(300); }
  if (digitalRead(BTN_TEST) == LOW)  { manualFault = true; delay(300); }
}

void sendToPYNQ() {
  if (millis() - lastUART < 500) return;
  lastUART = millis();

  PYNQUART.print("V="); PYNQUART.print((int)(voltage * 1000.0));
  PYNQUART.print(",I="); PYNQUART.print((int)(current * 1000.0));
  PYNQUART.print(",T="); PYNQUART.print((int)(temperature * 100.0));
  PYNQUART.print(",F="); PYNQUART.print(faultLatched ? 1 : 0);
  PYNQUART.print(",S="); PYNQUART.println(tempSensorFault ? 0 : 1);
}

void loop() {
  checkButtons();
  if (millis() - lastSample >= 500) {
    lastSample = millis();
    readSensors();
    safetyCheck();
    updateOutputs();
  }
  updateLCD();
  sendToPYNQ();
}