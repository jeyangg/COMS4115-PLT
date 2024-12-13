.data


.text
.globl main
li $a0, 54
sw $v0, 0($sp)
li $a0, 0
beq $v0, $zero, false_0
move $a0, $v0
li $v0, 1
syscall
j end_1
false_0:
move $a0, $v0
li $v0, 1
syscall
end_1: