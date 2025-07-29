#!/bin/python3
from pwn import *

elf = context.binary = ELF("./split")
context.log_level = 'debug'

pattern = cyclic(200)

p = process()
p.recvuntil('> ')
p.sendline(pattern)

p.wait()

core = p.corefile
rbp = core.rbp
log.success(f"RBP at crash: {hex(rbp)}")
log.success(f"Offset to RIP: {cyclic_find(rbp) + 8}")



