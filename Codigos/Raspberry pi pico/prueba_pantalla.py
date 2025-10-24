from machine import Pin, SPI
from ili9341 import ILI9341, color565
import time

# Pines iguales a tu sistema
RST = 5
DC = 4
CS = 9
SCK = 10
MOSI = 11

# Inicializa SPI1
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(SCK), mosi=Pin(MOSI))

# Inicializa la pantalla con rotación 1 (horizontal)
tft = ILI9341(spi, cs=Pin(CS), dc=Pin(DC), rst=Pin(RST),
              w=320, h=240, r=1)

# Limpia pantalla
tft.fill_rectangle(0, 0, tft.width, tft.height, color565(0, 0, 0))

# Texto de inicio
tft.set_color(color565(255, 255, 255), color565(0, 0, 0))
tft.set_pos(20, 40)
tft.write("Test ILI9341 - Raspberry Pi Pico\n")
tft.write("------------------------------\n")
print("pepep")
time.sleep(1)

# Mostrar colores de prueba
colores = [
    ("ROJO", (255, 0, 0)),
    ("VERDE", (0, 255, 0)),
    ("AZUL", (0, 0, 255)),
    ("BLANCO", (255, 255, 255)),
    ("AMARILLO", (255, 255, 0)),
]

for nombre, rgb in colores:
    color = color565(*rgb)
    tft.fill_rectangle(0, 0, tft.width, tft.height, color)
    tft.set_color(color565(0, 0, 0), color)
    tft.set_pos(60, 110)
    tft.write(f"COLOR: {nombre}\n")
    time.sleep(1)

# Pantalla final

tft.fill_rectangle(0, 0, tft.width, tft.height, color565(255, 255, 255))
tft.set_color(color565(0, 0, 0), color565(255, 255, 255))
tft.set_pos(50, 100)
tft.write("Pantalla conectada correctamente!\n")
tft.write("Driver ILI9341 funcionando\n")
