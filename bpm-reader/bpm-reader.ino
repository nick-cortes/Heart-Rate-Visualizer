#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

// Moving average of IR values
#define WINDOW_SIZE 200
long readings[WINDOW_SIZE];
int readingIndex = 0;
long irTotal = 0;

byte ledBrightness = 0x7F; // Increase LED current: 0x1F → 0x7F or 0xFF
byte sampleAverage = 4;    // Lowering average can improve responsiveness
byte ledMode = 2;          // Red + IR mode (you can try 1 = Red only too)
int sampleRate = 400;      // Boost from 100 → 400 (more resolution)
int pulseWidth = 411;      // Longer pulse → deeper penetration
int adcRange = 16384;      // Wider ADC range allows stronger signal

// Moving average of BPM values
const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
int bpmSum = 0;


long lastBeat = 0; //Time at which the last beat occurred
int waitTime = 400;

void setup() {
  Serial.begin(115200);
  // Serial.println("Initializing...");

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found. Please check wiring/power. ");
    while (1);
  }
  // Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
}

void loop() {
  long irValue = particleSensor.getIR();

  irTotal -= readings[readingIndex];
  readings[readingIndex] = irValue;
  irTotal += irValue;
  readingIndex = (readingIndex + 1) % WINDOW_SIZE;
  long irAvg = irTotal / WINDOW_SIZE;

  long detrended = irValue - irAvg;
  Serial.println(detrended);
  if (detrended > 200 && (millis() - lastBeat > waitTime)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    // Serial.print(irValue);
    // Serial.print(",");
    // Serial.println("beat detected");

    float beatsPerMinute = 60.0 / (delta / 1000.0);
    bpmSum -= rates[rateSpot];
    rates[rateSpot] = beatsPerMinute;
    bpmSum += beatsPerMinute;
    rateSpot = (rateSpot + 1) % RATE_SIZE;

    float bpmAvg = bpmSum / RATE_SIZE;
    // Serial.println(bpmAvg);
  }

}