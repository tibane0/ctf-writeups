from pwn import *

context.log_level = 'debug'
p = process("./lab1C")
#p.recvuntil(b'Password:  ')
p.sendline(b'5274')
p.interactive()