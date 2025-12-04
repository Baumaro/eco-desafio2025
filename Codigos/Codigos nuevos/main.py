from machine import Pin, SPI, ADC
import time
import ili9341

# -----------------------------
# CONFIGURACIÓN DE HARDWARE
# -----------------------------

# --- SPI para la pantalla
spi = SPI(
    0,
    baudrate=40000000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3)
)

display = ili9341.ILI9341(
    spi,
    cs=Pin(5, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    rst=Pin(9, Pin.OUT),
    width=240,
    height=320,
    rotation=0
)

# --- Sensores ---
pin_hall = Pin(10, Pin.IN, Pin.PULL_UP)
adc_corriente = ADC(26)
adc_bateria = ADC(27)

# -----------------------------
# VARIABLES DEL SISTEMA
# -----------------------------
diametro_rueda_m = 0.60         # 60 cm
perimetro_rueda_m = 3.1416 * diametro_rueda_m

pulsos = 0
vel_kmh = 0
corriente_A = 0
voltaje_V = 0

# -----------------------------
# INTERRUPCIÓN HALL
# -----------------------------
def hall_irq(pin):
    global pulsos
    pulsos += 1

pin_hall.irq(trigger=Pin.IRQ_RISING, handler=hall_irq)

# -----------------------------
# LECTURAS ANALÓGICAS
# -----------------------------
def leer_corriente():
    lectura = adc_corriente.read_u16()
    voltaje = lectura * (3.3 / 65535)
    corriente = (voltaje - 1.65) / 0.185
    return corriente

def leer_bateria():
    lectura = adc_bateria.read_u16()
    volt_adc = lectura * (3.3 / 65535)
    volt_bat = volt_adc * 15.45
    return volt_bat

# -----------------------------
# LOOP PRINCIPAL NO BLOQUEANTE
# -----------------------------
ULTIMA_ACT = time.ticks_ms()
INTERVALO = 50   # 50 ms

display.fill(0)
print("Sistema iniciado. (Interrumpible)")

try:
    while True:
        ahora = time.ticks_ms()

        # ¿Pasaron 50ms?
        if time.ticks_diff(ahora, ULTIMA_ACT) >= INTERVALO:
            ULTIMA_ACT = ahora

            # --- Calcular velocidad ---
            giros = pulsos
            pulsos = 0

            vueltas_s = giros * (1000 / INTERVALO)
            vel_m_s = vueltas_s * perimetro_rueda_m
            vel_kmh = vel_m_s * 3.6

            # --- Sensores eléctricos ---
            corriente_A = leer_corriente()
            voltaje_V = leer_bateria()

            # --- Actualizar pantalla ---
            display.fill(0)

            display.text("VELOCIDAD:", 10, 10, ili9341.color565(255,255,0))
            display.text("{:.1f} km/h".format(vel_kmh), 10, 30, ili9341.color565(255,255,255))

            display.text("CORRIENTE:", 10, 70, ili9341.color565(0,255,255))
            display.text("{:.2f} A".format(corriente_A), 10, 90, ili9341.color565(255,255,255))

            display.text("BATERIA:", 10, 130, ili9341.color565(255,0,255))
            display.text("{:.1f} V".format(voltaje_V), 10, 150, ili9341.color565(255,255,255))

        # Muy importante: deja respirar al intérprete
        time.sleep_ms(1)

except KeyboardInterrupt:
    print("Ejecución detenida limpiamente.")