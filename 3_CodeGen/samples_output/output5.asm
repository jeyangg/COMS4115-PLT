.data


.text
.globl main
피보나치:
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $v0, 0($sp)
move $t1, $v0
li $a0, 1
sle $v0, $t1, $v0
beq $v0, $zero, false_0
j end_1
false_0:
end_1:
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra          
주요_함수:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $a0, 10
sw $v0, -4($sp)
li $a0, 5.5
sw $v0, -8($sp)
sw $v0, -12($sp)
sw $v0, -16($sp)
lw $v0, -12($sp)
move $t1, $v0
seq $v0, $t1, $v0
move $t1, $v0
lw $v0, -20($sp)
move $t1, $v0
lw $v0, -4($sp)
slt $v0, $t1, $v0
beq $v0, $zero, false_2
move $a0, $v0
li $v0, 1
syscall
j end_3
false_2:
move $a0, $v0
li $v0, 1
syscall
end_3:
li $a0, 0
sw $v0, -24($sp)
start_4:
lw $v0, -24($sp)
move $t1, $v0
# Error encountered: Invalid number format