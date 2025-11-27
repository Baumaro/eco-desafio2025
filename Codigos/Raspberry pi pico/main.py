try:
    import ujson as json
except Exception:
    import json
import glcdfont
from machine import Pin, ADC, UART, SPI
from ili9341 import ILI9341, color565
import time
import gc

class RaspberryPiPico():
    def __init__(self):

        self.rst = Pin(5, Pin.OUT) # Reset pin for TFT
        self.dc = Pin(4, Pin.OUT)   # data/command pin for TFT
        self.cs = Pin(9, Pin.OUT)  # Chip Select

        self.sensorCorriente = ADC(Pin(26)) #define el pin del sensor de corriente analogico 
        self.sensorVoltaje = ADC(Pin(27)) #define el pin del sensor de voltaje
        self.sensorMagnetico = ADC(Pin(28)) #define el pin del sensor magnetico
        self.tiempo = time.ticks_ms() #obtiene el tiempo actual en milisegundos
        
    def leerCorriente(self):
        valor = self.sensorCorriente.read_u16() # Lee el valor del ADC del sensor de corriente
        corriente = (valor * 20 / 65535) # Convierte el valor ADC en amperios, usando regla de tres simple 20A = 65535 valor ADC
        return corriente

    def leerVoltaje(self):
        valor = self.sensorVoltaje.read_u16() # Lee el valor del ADC del sensor de voltaje
        
        voltaje = (valor * 48 / 65535) # Convierte el valor ADC en voltios, usando regla de tres simple 48V = 65535 valor ADC
        time.sleep(1)
        return voltaje
    
    def leerMagnetico(self):
        magnetico = self.sensorMagnetico.read_u16() # Lee el valor del ADC del sensor magnetico
        print(magnetico)
        return magnetico
    
class Pantalla:
    def __init__(self, raspberry_pico):
        # Inicializa SPI (usar SPI1 por defecto, pines ajustables si necesitas)
        spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
        # guardar display
        self.display = ILI9341(spi, cs=raspberry_pico.cs, dc=raspberry_pico.dc, rst=raspberry_pico.rst, w = 340, h = 240, r = 0)
        self.font = None
        
    def imprimirDatos(self, DatosBateria, DatosCinematica):
        
        try:
            # Limpia pantalla (usa fill si erase falla)
            self.display.fill(color565(255, 255, 255))  # Fondo blanco
        except Exception:
            self.display.erase()
    

    # Últimos datos
        velocidad = distancia = 0
        voltaje = corriente = 0
        if DatosCinematica:
            ultimo = DatosCinematica[-1]
            velocidad = ultimo.get('velocidad',0)
            distancia = ultimo.get('distancia',0)
        if DatosBateria:
            ultimo_b = DatosBateria[-1]
            voltaje = ultimo_b.get('voltaje',0)
            corriente = ultimo_b.get('corriente',0)

    # Establece fuente y color
        self.display.set_font(glcdfont)
        self.display.set_color(color565(0,0,0), color565(255,255,255))  # negro sobre blanco

    # Imprime cada dato
        print("hola")
        self.display.set_pos(10, 20)
        self.display.write('VEL:{:.2f} m/s'.format(velocidad))

        self.display.set_pos(10, 60)
        self.display.write('DIST:{:.2f} m'.format(distancia))

        self.display.set_pos(10, 100)
        self.display.write('V:{:.2f} V'.format(voltaje))

        self.display.set_pos(10, 140)
        self.display.write('I:{:.2f} A'.format(corriente))



class Teletrimetria:
    def __init__(self):
        self.raspberry_pico = RaspberryPiPico()
        # Usar listas de diccionarios serializables a JSON
        self.DatosCinematica = []  # [{'tiempo','distancia','velocidad'}, ...]
        self.DatosBateria = []     # [{'corriente','voltaje','porcentaje'}, ...]
        self.pantalla = Pantalla(self.raspberry_pico)
        self.RadioFrecuencia = Modulo_RF()
        self.PerimetroRueda = 0.5 * 3.14 # donde 0.5m es el perimetro y 3.14 es pi 
    
    def calcularPorcentajeBateria(self, corriente, voltaje, PotenciaEfectivaMin):
        pass

    def convertirMagneticoDistancia(self, magnetico):
        # Ejemplo simple: si el sensor detecta cambio, suma el perímetro
        if magnetico > 12000 :
            distancia = self.PerimetroRueda
        else:
            distancia = 0
        return distancia
        
    def CalcularVelocidad(self, distancia, tiempo):
        # velocidad = delta_distancia / delta_tiempo (segundos)
        if self.DatosCinematica:
            ultimo = self.DatosCinematica[-1]
            dt_ms = tiempo - ultimo.get('tiempo', tiempo)
            dt = dt_ms / 1000.0 if dt_ms != 0 else 0
            dx = distancia - ultimo.get('distancia', distancia)
            velocidad = (dx / dt) if dt > 0 else 0
        else:
            velocidad = 0
        return velocidad

    def ActualizarDatosCinematica(self):
        magnetico = self.raspberry_pico.leerMagnetico()
        distancia = self.convertirMagneticoDistancia(magnetico)
        tiempo = time.ticks_ms()
        velocidad = self.CalcularVelocidad(distancia, tiempo)
        linea = {'tiempo': tiempo, 'distancia': distancia, 'velocidad': velocidad}
        return linea
    
    def ActualizarDatosBateria(self):
        corriente = self.raspberry_pico.leerCorriente()
        voltaje = self.raspberry_pico.leerVoltaje()
        linea = {'corriente': corriente, 'voltaje': voltaje, 'porcentaje': 0}
        return linea
        
    def agregarDatos(self, lineaDatosCinematica, LineaDatosBateria):
        self.DatosCinematica.append(lineaDatosCinematica)
        self.DatosBateria.append(LineaDatosBateria)
        
    def exportarJSON(self):
        paquete = {'cinematica': self.DatosCinematica, 'bateria': self.DatosBateria}
        try:
            return json.dumps(paquete)
        except Exception:
            return '{}'



class Modulo_RF():
    def __init__(self):
        self.Comunicacion = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    def transmitir(self, dato):
        if isinstance(dato, str):
            self.Comunicacion.write(dato.encode())
        else:
            self.Comunicacion.write(str(dato).encode())

def main():
    Sistema = Teletrimetria()
    while True:
        datos_cinematica = Sistema.ActualizarDatosCinematica()
        datos_bateria = Sistema.ActualizarDatosBateria()
        Sistema.agregarDatos(datos_cinematica, datos_bateria)
        # crea el paquete
        paquete = {
            'tiempo': datos_cinematica.get('tiempo', 0),
            'distancia': datos_cinematica.get('distancia', 0),
            'velocidad': datos_cinematica.get('velocidad', 0),
            'voltaje': datos_bateria.get('voltaje', 0),
            'corriente': datos_bateria.get('corriente', 0)
        }
        mensaje_json = json.dumps(paquete)
        Sistema.RadioFrecuencia.transmitir(mensaje_json + '\n')
        # Mostrar
        Sistema.pantalla.imprimirDatos(Sistema.DatosBateria, Sistema.DatosCinematica)
        print(paquete)
        # 🧹 Liberar memoria
        Sistema.DatosCinematica.clear()
        Sistema.DatosBateria.clear()
        gc.collect()

        
        
        


if __name__ == '__main__':
    main()




