from machine import Pin, SPI
import time

# ----------------------------
#  COLOR 565
# ----------------------------
def color565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


# ----------------------------
#  FUENTE 8x8
# ----------------------------
FONT = [
    b"\x00\x00\x00\x00\x00\x00\x00\x00",  # 32   
    b"\x18\x18\x18\x18\x18\x00\x18\x00",  # 33 !
    b"\x6c\x6c\x6c\x00\x00\x00\x00\x00",  # 34 "
    b"\x6c\x6c\xfe\x6c\xfe\x6c\x6c\x00",  # 35 #
    b"\x18\x7c\xc0\x7c\x06\xfc\x18\x00",  # 36 $
    b"\x00\xc6\xcc\x18\x30\x66\xc6\x00",  # 37 %
    b"\x38\x6c\x38\x76\xdc\xcc\x76\x00",  # 38 &
    b"\x30\x30\x60\x00\x00\x00\x00\x00",  # 39 '
    b"\x0c\x18\x30\x30\x30\x18\x0c\x00",  # 40 (
    b"\x30\x18\x0c\x0c\x0c\x18\x30\x00",  # 41 )
    b"\x00\x66\x3c\xff\x3c\x66\x00\x00",  # 42 *
    b"\x00\x18\x18\x7e\x18\x18\x00\x00",  # 43 +
    b"\x00\x00\x00\x00\x30\x30\x60\x00",  # 44 ,
    b"\x00\x00\x00\x7e\x00\x00\x00\x00",  # 45 -
    b"\x00\x00\x00\x00\x00\x18\x18\x00",  # 46 .
    b"\x06\x0c\x18\x30\x60\xc0\x80\x00",  # 47 /
    b"\x7c\xc6\xce\xd6\xe6\xc6\x7c\x00",  # 48 0
    b"\x18\x38\x18\x18\x18\x18\x7e\x00",  # 49 1
    b"\x7c\xc6\x06\x1c\x70\xc0\xfe\x00",  # 50 2
    b"\x7c\xc6\x06\x3c\x06\xc6\x7c\x00",  # 51 3
    b"\x1c\x3c\x6c\xcc\xfe\x0c\x1e\x00",  # 52 4
    b"\xfe\xc0\xfc\x06\x06\xc6\x7c\x00",  # 53 5
    b"\x3c\x60\xc0\xfc\xc6\xc6\x7c\x00",  # 54 6
    b"\xfe\xc6\x0c\x18\x30\x30\x30\x00",  # 55 7
    b"\x7c\xc6\xc6\x7c\xc6\xc6\x7c\x00",  # 56 8
    b"\x7c\xc6\xc6\x7e\x06\x0c\x78\x00",  # 57 9
    b"\x00\x18\x18\x00\x00\x18\x18\x00",  # 58 :
    b"\x00\x18\x18\x00\x00\x18\x18\x30",  # 59 ;
    b"\x0e\x1c\x38\x70\x38\x1c\x0e\x00",  # 60 <
    b"\x00\x00\x7e\x00\x00\x7e\x00\x00",  # 61 =
    b"\x70\x38\x1c\x0e\x1c\x38\x70\x00",  # 62 >
    b"\x7c\xc6\x0e\x1c\x18\x00\x18\x00",  # 63 ?
    b"\x7c\xc6\xde\xde\xde\xc0\x78\x00",  # 64 @
    b"\x38\x6c\xc6\xc6\xfe\xc6\xc6\x00",  # 65 A
    b"\xfc\xc6\xc6\xfc\xc6\xc6\xfc\x00",  # 66 B
    b"\x7c\xc6\xc0\xc0\xc0\xc6\x7c\x00",  # 67 C
    b"\xf8\xcc\xc6\xc6\xc6\xcc\xf8\x00",  # 68 D
    b"\xfe\xc0\xc0\xf8\xc0\xc0\xfe\x00",  # 69 E
    b"\xfe\xc0\xc0\xf8\xc0\xc0\xc0\x00",  # 70 F
    b"\x7c\xc6\xc0\xde\xc6\xc6\x7e\x00",  # 71 G
    b"\xc6\xc6\xc6\xfe\xc6\xc6\xc6\x00",  # 72 H
    b"\x7e\x18\x18\x18\x18\x18\x7e\x00",  # 73 I
    b"\x1e\x06\x06\x06\x06\xc6\x7c\x00",  # 74 J
    b"\xc6\xcc\xd8\xf0\xd8\xcc\xc6\x00",  # 75 K
    b"\xc0\xc0\xc0\xc0\xc0\xc0\xfe\x00",  # 76 L
    b"\xc6\xee\xfe\xd6\xc6\xc6\xc6\x00",  # 77 M
    b"\xc6\xe6\xf6\xde\xce\xc6\xc6\x00",  # 78 N
    b"\x7c\xc6\xc6\xc6\xc6\xc6\x7c\x00",  # 79 O
    b"\xfc\xc6\xc6\xfc\xc0\xc0\xc0\x00",  # 80 P
    b"\x7c\xc6\xc6\xc6\xd6\xcc\x76\x00",  # 81 Q
    b"\xfc\xc6\xc6\xfc\xd8\xcc\xc6\x00",  # 82 R
    b"\x7e\xc0\xc0\x7c\x06\x06\xfc\x00",  # 83 S
    b"\xff\x18\x18\x18\x18\x18\x18\x00",  # 84 T
    b"\xc6\xc6\xc6\xc6\xc6\xc6\x7c\x00",  # 85 U
    b"\xc6\xc6\xc6\xc6\xc6\x6c\x38\x00",  # 86 V
    b"\xc6\xc6\xc6\xd6\xd6\xfe\x6c\x00",  # 87 W
    b"\xc6\xc6\x6c\x38\x6c\xc6\xc6\x00",  # 88 X
    b"\xc6\xc6\x6c\x38\x18\x18\x18\x00",  # 89 Y
    b"\xfe\x06\x0c\x18\x30\x60\xfe\x00",  # 90 Z
    b"\x3c\x30\x30\x30\x30\x30\x3c\x00",  # 91 [
    b"\xc0\x60\x30\x18\x0c\x06\x02\x00",  # 92 \
    b"\x3c\x0c\x0c\x0c\x0c\x0c\x3c\x00",  # 93 ]
    b"\x10\x38\x6c\xc6\x00\x00\x00\x00",  # 94 ^
    b"\x00\x00\x00\x00\x00\x00\x00\xff",  # 95 _
    b"\x18\x18\x0c\x00\x00\x00\x00\x00",  # 96 `
    b"\x00\x00\x7c\x06\x7e\xc6\x7e\x00",  # 97 a
    b"\xc0\xc0\xfc\xc6\xc6\xc6\xfc\x00",  # 98 b
    b"\x00\x00\x7c\xc6\xc0\xc6\x7c\x00",  # 99 c
    b"\x06\x06\x7e\xc6\xc6\xc6\x7e\x00",  # 100 d
    b"\x00\x00\x7c\xc6\xfe\xc0\x7c\x00",  # 101 e
    b"\x1c\x30\x30\xfc\x30\x30\x30\x00",  # 102 f
    b"\x00\x00\x7e\xc6\xc6\x7e\x06\x7c",  # 103 g
    b"\xc0\xc0\xfc\xc6\xc6\xc6\xc6\x00",  # 104 h
    b"\x18\x00\x38\x18\x18\x18\x3c\x00",  # 105 i
    b"\x06\x00\x0e\x06\x06\x06\x06\x7c",  # 106 j
    b"\xc0\xc0\xcc\xd8\xf0\xd8\xcc\x00",  # 107 k
    b"\x38\x18\x18\x18\x18\x18\x3c\x00",  # 108 l
    b"\x00\x00\xec\xfe\xd6\xd6\xd6\x00",  # 109 m
    b"\x00\x00\xdc\xe6\xc6\xc6\xc6\x00",  # 110 n
    b"\x00\x00\x7c\xc6\xc6\xc6\x7c\x00",  # 111 o
    b"\x00\x00\xfc\xc6\xc6\xfc\xc0\xc0",  # 112 p
    b"\x00\x00\x7e\xc6\xc6\x7e\x06\x06",  # 113 q
    b"\00\x00\xdc\xf6\xf0\xc0\xc0\x00",  # 114 r
    b"\x00\x00\x7e\xc0\x7c\x06\xfc\x00",  # 115 s
    b"\x30\x30\xfc\x30\x30\x30\x1c\x00",  # 116 t
    b"\x00\x00\xc6\xc6\xc6\xc6\x7e\x00",  # 117 u
    b"\x00\x00\xc6\xc6\xc6\x6c\x38\x00",  # 118 v
    b"\x00\x00\xc6\xd6\xd6\xfe\x6c\x00",  # 119 w
    b"\x00\x00\xc6\x6c\x38\x6c\xc6\x00",  # 120 x
    b"\x00\x00\xc6\xc6\xc6\x7e\x06\x7c",  # 121 y
    b"\x00\x00\xfe\x0c\x18\x30\xfe\x00",  # 122 z
    b"\x0e\x18\x18\x70\x18\x18\x0e\x00",  # 123 {
    b"\x18\x18\x18\x00\x18\x18\x18\x00",  # 124 |
    b"\x70\x18\x18\x0e\x18\x18\x70\x00",  # 125 }
    b"\x6e\x3b\x00\x00\x00\x00\x00\x00",  # 126 ~
    b"\x7c\xc6\xc6\xfe\xc6\xc6\xc6\x00",  # 127 (DEL placeholder)
]


# extend font for ASCII
for i in range(0x30, 0x7F):
    FONT.append(bytearray([0x00] * 8))  # placeholder for full ASCII (simple)

# ----------------------------
#  DRIVER ILI9341
# ----------------------------
class ILI9341:
    def __init__(self, spi, cs, dc, rst, width=240, height=320, rotation=0):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height
        self._rotation = rotation

        self.cs.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=1)

        self.reset()
        self.init_display()

    # -------------------------
    #  RESET
    # -------------------------
    def reset(self):
        self.rst(0)
        time.sleep_ms(50)
        self.rst(1)
        time.sleep_ms(50)

    # -------------------------
    #  LOW-LEVEL WRITE
    # -------------------------
    def write_cmd(self, cmd):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(bytearray([data]))
        self.cs(1)

    def write_data_buffer(self, buf):
        self.cs(0)
        self.dc(1)
        self.spi.write(buf)
        self.cs(1)

    # -------------------------
    #  INIT
    # -------------------------
    def init_display(self):
        self.write_cmd(0x01)  # SW reset
        time.sleep_ms(120)

        self.write_cmd(0x28)

        self.write_cmd(0x3A)
        self.write_data(0x55)  # 16 bit

        self.set_rotation(self._rotation)

        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x29)

    # -------------------------
    #  WINDOW
    # -------------------------
    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A)
        self.write_data(x0 >> 8)
        self.write_data(x0 & 0xFF)
        self.write_data(x1 >> 8)
        self.write_data(x1 & 0xFF)

        self.write_cmd(0x2B)
        self.write_data(y0 >> 8)
        self.write_data(y0 & 0xFF)
        self.write_data(y1 >> 8)
        self.write_data(y1 & 0xFF)

        self.write_cmd(0x2C)

    # -------------------------
    #  PIXEL
    # -------------------------
    def pixel(self, x, y, color):
        self.set_window(x, y, x+1, y+1)
        self.write_data(color >> 8)
        self.write_data(color & 0xFF)

    # -------------------------
    #  FILL
    # -------------------------
    def fill(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)
        hi = color >> 8
        lo = color & 0xFF
        buf = bytearray(self.width * 2)
        for i in range(self.width):
            buf[2*i] = hi
            buf[2*i+1] = lo
        for _ in range(self.height):
            self.write_data_buffer(buf)

    # -------------------------
    #  RECTÁNGULOS
    # -------------------------
    def fill_rect(self, x, y, w, h, color):
        self.set_window(x, y, x + w - 1, y + h - 1)
        hi = color >> 8
        lo = color & 0xFF
        line = bytearray(w * 2)
        for i in range(w):
            line[2*i] = hi
            line[2*i+1] = lo
        for _ in range(h):
            self.write_data_buffer(line)

    def rect(self, x, y, w, h, color):
        self.fill_rect(x, y, w, 1, color)
        self.fill_rect(x, y+h-1, w, 1, color)
        self.fill_rect(x, y, 1, h, color)
        self.fill_rect(x+w-1, y, 1, h, color)

    # -------------------------
    #  LÍNEAS
    # -------------------------
    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = err << 1
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # -------------------------
    #  TEXTO
    # -------------------------
    def char(self, x, y, ch, color):
        if ord(ch) < 32 or ord(ch) > 126:
            return
        glyph = FONT[ord(ch) - 32]
        for row in range(8):
            bits = glyph[row]
            for col in range(8):
                if bits & (1 << (7 - col)):
                    self.pixel(x + col, y + row, color)

    def text(self, string, x, y, color):
        for ch in string:
            self.char(x, y, ch, color)
            x += 8
    
    def set_rotation(self, rotation):
        rot = rotation % 4

        if rot == 0:
            madctl = 0x48   # MX, BGR
            self.width = 240
            self.height = 320

        elif rot == 1:
            madctl = 0x28   # MV | BGR
            self.width = 320
            self.height = 240

        elif rot == 2:
            madctl = 0x88   # MY | BGR
            self.width = 240
            self.height = 320

        elif rot == 3:
            madctl = 0xE8   # MX | MY | MV | BGR
            self.width = 320
            self.height = 240

        self.write_cmd(0x36)
        self.write_data(madctl)