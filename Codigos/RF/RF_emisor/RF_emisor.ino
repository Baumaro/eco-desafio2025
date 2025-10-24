#include <SPI.h>
#include <LoRa.h>

#define LORA_SCK 13
#define LORA_MISO 12
#define LORA_MOSI 11
#define LORA_SS 10
#define LORA_RST 9
#define LORA_DIO0 2

#define UART_BAUD 9600

void setup() {
  Serial.begin(UART_BAUD); // Comunicación con Raspberry Pi Pico
  while (!Serial);

  Serial1.begin(UART_BAUD); // UART adicional si lo necesitas
  // Inicializa LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) { // Frecuencia: 915 MHz
    Serial.println("Error inicializando LoRa!");
    while (1);
  }
  Serial.println("LoRa inicializado correctamente.");
}

void loop() {
  // Verifica si hay datos disponibles por UART
  if (Serial.available() > 0) {
    String mensaje = Serial.readStringUntil('\n'); // leer hasta salto de línea
    mensaje.trim(); // eliminar espacios innecesarios

    if (mensaje.length() > 0) {
      // Transmitir mensaje por LoRa
      LoRa.beginPacket();
      LoRa.print(mensaje);
      LoRa.endPacket();

      Serial.print("Transmitido: ");
      Serial.println(mensaje);
    }
  }

  delay(10); // pequeño retardo para no saturar la UART
}
