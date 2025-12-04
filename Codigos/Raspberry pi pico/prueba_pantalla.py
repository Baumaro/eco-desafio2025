from machine import Pin, SPI
import time
import ili9341

# -------------------------
# Pines según tu PCB
# -------------------------
PIN_SCK  = 8   # SPI1 SCK
PIN_MOSI = 7   # SPI1 TX
PIN_CS   = 5   # Chip Select
PIN_DC   = 3   # D/C
PIN_RST  = 4   # Reset

# -------------------------
# Inicializa SPI1
# -------------------------
spi = SPI(
    1,  # SPI1
    baudrate=40000000,
    polarity=0,
    phase=0,
    sck=Pin(PIN_SCK),
    mosi=Pin(PIN_MOSI),
    miso=None
)

# -------------------------
# Inicializa ILI9341
# -------------------------
tft = ili9341.ILI9341(
    spi,
    cs=Pin(PIN_CS),
    dc=Pin(PIN_DC),
    rst=Pin(PIN_RST),
    w=240,
    h=320,
    rotation=0
)

# -------------------------
# TEST RÁPIDO
# -------------------------
tft.fill(ili9341.color565(0, 0, 255))    # Pantalla azul
time.sleep(1)

tft.fill(ili9341.color565(0, 0, 0))      # Pantalla negra

tft.fill_rect(30, 40, 180, 150, ili9341.color565(255, 0, 0))  # Rectángulo rojo

tft.text("PICO 2W OK!", 60, 120, ili9341.color565(255, 255, 255))
