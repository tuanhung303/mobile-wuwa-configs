"""Decrypt WuWa Client.log files (3.x builds) to <file>.txt.

Usage: python3 decrypt_log.py Client.log [more.log ...]

Format (from Arglax's wuwa_ld.py, MIT, https://github.com/Arglax/Mobile-WuWa-Config):
3-byte header 00 54 50 ("TP"), then each byte XOR 0xA5 if odd, XOR 0xEF if even.
"""
import sys

lut = bytes((e ^ 0xA5) if (e & 1) else (e ^ 0xEF) for e in range(256))
for p in sys.argv[1:]:
    d = open(p, 'rb').read()
    if d[:3] != b'\x00TP':
        print('skip (not encrypted)', p)
        continue
    open(p + '.txt', 'wb').write(d[3:].translate(lut))
    print('ok', p + '.txt')
