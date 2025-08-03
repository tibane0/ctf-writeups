from pwn import *

pattern = cyclic(200)

doubles = []
for i in range(0, len(pattern), 8):
    chunk = pattern[i:i+8]

    if len(chunk) < 8:
        chunk = chunk.ljust(8, b'\x00')

    value = struct.unpack('d', chunk)[0]
    doubles.append(value)

print(" ".join(str(d) for d in doubles[:7]))