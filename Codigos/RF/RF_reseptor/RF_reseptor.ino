#include <SPI.h>
#include <LoRa.h>

#define LORA_NSS 10 
#define LORA_RST 2
#define LORA_DIO0 9
#define BAUDRATE 9600

void setup() {
    Serial.begin(BAUDRATE);
    while (!Serial);

    LoRa.setPins(LORA_NSS, LORA_RST, LORA_DIO0); 
    if (!LoRa.begin(915E6)) {
        Serial.println("Error inicializando LoRa!");
        while (1);
    }
    Serial.println("Receptor LoRa listo");
}

void loop() {
    int packetSize = LoRa.parsePacket();
    if (packetSize > 0) {
        String mensaje = "";
        while (LoRa.available()) {
            char c = (char)LoRa.read();
            mensaje += c;
        }
        mensaje.trim(); // quitar espacios o saltos extra
        Serial.println(mensaje); // enviamos JSON completo a la PC
    }
}
