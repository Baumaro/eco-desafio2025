#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#define TFT_CS   10
#define TFT_DC    9
#define TFT_RST   8

#define HALL_PIN 3
#define WHEEL_RADIUS 0.25

  // Radio de la rueda en metros (ej. 15 cm)
#define NUM_MAGNETS 2

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);

volatile unsigned long lastPulse = 0;
volatile unsigned long pulseInterval = 0;
float velocity = 0.0;

void hallInterrupt() {
  unsigned long now = micros();
  pulseInterval = now - lastPulse;
  lastPulse = now;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);

  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), hallInterrupt, FALLING);

  tft.begin();
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextSize(3);
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(30, 100);
  tft.println("Esperando...");
}

void loop() {
  static unsigned long lastUpdate = 0;
  unsigned long currentTime = millis();

  if (pulseInterval > 0) {
    float time_s = pulseInterval / 1000000.0;
    velocity = (2 * 3.1416 * WHEEL_RADIUS / (time_s * NUM_MAGNETS)) * 3.6;
  } else {
    // Si pasa mucho tiempo sin pulsos, la velocidad baja a cero
    if (millis() - lastPulse / 1000 > 2000) velocity = 0;
  }

  // Actualizar pantalla cada 300 ms
  if (currentTime - lastUpdate > 300) {
    lastUpdate = currentTime;

    tft.fillRect(0, 80, 240, 60, ILI9341_BLACK);
    tft.setTextColor(ILI9341_CYAN);
    tft.setTextSize(5);
    tft.setCursor(40, 100);
    tft.print(velocity, 1);
    tft.print(" km/h");

    Serial.print("Velocidad: ");
    Serial.println(velocity);
  }
}
