from machine import Pin, SPI, ADC
import time
import ili9341
import math

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
    width=320,
    height=240,
    rotation=1
)

# --- Sensores ---
pin_hall = Pin(18, Pin.IN, Pin.PULL_UP)
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
# DIBUJO EN PANTALLA
# -----------------------------
prev_angle_speed = 180
prev_power_w = -1

def init_ui():
    display.fill(0)
    
    # --- Velocímetro estático ---
    cx, cy = 160, 150
    r = 100
    # Dibujar arco (ticks)
    for i in range(0, 181, 20):
        angle = math.radians(180 - i)
        x1 = int(cx + (r - 10) * math.cos(angle))
        y1 = int(cy - (r - 10) * math.sin(angle))
        x2 = int(cx + r * math.cos(angle))
        y2 = int(cy - r * math.sin(angle))
        display.line(x1, y1, x2, y2, ili9341.color565(255, 255, 255))
        
    display.text("km/h", cx - 15, cy + 20, ili9341.color565(255, 255, 255))
    
    # --- Barra de potencia estática ---
    x, y, w, h = 10, 200, 300, 20
    display.rect(x, y, w, h, ili9341.color565(255, 255, 255))

def update_speedometer(speed, max_speed=60):
    global prev_angle_speed
    cx, cy = 160, 150
    r = 100
    
    # Calcular nuevo ángulo
    angle_speed = 180 - (speed / max_speed) * 180
    if angle_speed < 0: angle_speed = 0
    if angle_speed > 180: angle_speed = 180
    
    # Borrar aguja anterior (dibujar en negro)
    if prev_angle_speed != angle_speed:
        rad_old = math.radians(prev_angle_speed)
        ox = int(cx + (r - 15) * math.cos(rad_old))
        oy = int(cy - (r - 15) * math.sin(rad_old))
        display.line(cx, cy, ox, oy, 0)
        
        # Dibujar nueva aguja
        rad_new = math.radians(angle_speed)
        nx = int(cx + (r - 15) * math.cos(rad_new))
        ny = int(cy - (r - 15) * math.sin(rad_new))
        display.line(cx, cy, nx, ny, ili9341.color565(255, 0, 0))
        
        prev_angle_speed = angle_speed
    
    # Actualizar texto (borrar fondo primero)
    display.fill_rect(cx - 20, cy + 10, 50, 8, 0)
    display.text("{:.1f}".format(speed), cx - 15, cy + 10, ili9341.color565(255, 255, 255))

def update_power_bar(power, max_power=500):
    global prev_power_w
    
    # Si no cambió mucho, no redibujar (opcional, aquí redibujamos igual para suavidad)
    # Pero para evitar parpadeo, solo dibujamos lo necesario
    
    x, y, w, h = 10, 200, 300, 20
    
    fill_w = int((power / max_power) * w)
    if fill_w > w: fill_w = w
    if fill_w < 0: fill_w = 0
    
    # Color según nivel
    color = ili9341.color565(0, 255, 0)
    if fill_w > w * 0.8: color = ili9341.color565(255, 0, 0)
    elif fill_w > w * 0.5: color = ili9341.color565(255, 255, 0)
    
    # Dibujar barra llena
    if fill_w > 0:
        display.fill_rect(x+1, y+1, fill_w-2, h-2, color)
        
    # Borrar el resto (si disminuyó)
    if fill_w < w:
        display.fill_rect(x+1 + fill_w, y+1, w - fill_w - 2, h-2, 0)
    
    # Texto consumo
    display.fill_rect(x, y - 15, 150, 8, 0)
    display.text("CONSUMO: {:.1f} W".format(power), x, y - 15, ili9341.color565(255, 255, 255))

# -----------------------------
# LOOP PRINCIPAL NO BLOQUEANTE
# -----------------------------
ULTIMA_ACT = time.ticks_ms()
INTERVALO = 50   # 50 ms

init_ui()
print("Sistema iniciado. (Interrumpible)")

try:
    while True:
        ahora = time.ticks_ms()

        # ¿Pasaron 50ms?
        if time.ticks_diff(ahora, ULTIMA_ACT) >= INTERVALO:
            dt = time.ticks_diff(ahora, ULTIMA_ACT)
            ULTIMA_ACT = ahora

            # --- Calcular velocidad ---
            giros = pulsos
            pulsos = 0

            # Evitar división por cero
            if dt > 0:
                vueltas_s = giros * (1000 / dt)
            else:
                vueltas_s = 0
                
            vel_m_s = vueltas_s * perimetro_rueda_m
            vel_kmh = vel_m_s * 3.6
            
            # Debug
            # print(f"Pulsos: {giros}, DT: {dt}ms, Vel: {vel_kmh:.1f} km/h")

            # --- Sensores eléctricos ---
            corriente_A = leer_corriente()
            voltaje_V = leer_bateria()

            # --- Actualizar pantalla ---
            # display.fill(0)  <-- YA NO SE BORRA TODO
            
            # Potencia = V * I
            potencia_W = voltaje_V * corriente_A
            
            update_speedometer(vel_kmh)
            update_power_bar(potencia_W)

        # Muy importante: deja respirar al intérprete
        time.sleep_ms(1)

except KeyboardInterrupt:
    print("Ejecución detenida limpiamente.")
