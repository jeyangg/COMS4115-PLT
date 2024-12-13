.data


.text
.globl main
li $a0, 10
sw $v0, 0($sp)
move $a0, $v0
li $v0, 1
syscall