section .data
file db ".pass"
len equ $ - file

section .bss
fd resb 4
content resb 0x32

section .text
global _start

_start:

; open and read .pass file (x86)
; syscall numbers  3 read | 4 write | 5 open | 6 close

; open file
xor eax, eax
mov eax, 5
mov ebx, file ; change to .pass in hex
mov ecx, 0
int 0x80

; read file
mov ebx, eax
xor eax, eax
mov eax, 3
mov ecx, content
mov edx, 0x32
int 0x80

; write file contents to stdout
xor eax, eax
mov eax, 4
mov ebx, 1 ; stdout
mov ecx, content
mov edx, 0x32
int 0x80

; close file
xor eax, eax
mov eax, 6
mov ebx, fd
int 0x80

; exit
mov eax, 1
mov ebx, 0
int 0x80
