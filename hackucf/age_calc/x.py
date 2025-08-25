from pwn import *


shellcode = asm(shellcraft.sh())
leng = len(shellcode)

print(leng)
