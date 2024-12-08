.data
리스트_아이디: .space 400

.text
.globl main
li $a0, 4
sw $v0, 0($sp)
start_0:
lw $v0, 0($sp)
move $t1, $v0
li $a0, 5
slt $v0, $t1, $v0
beq $v0, $zero, end_1
lw $v0, 0($sp)
move $t1, $v0
li $a0, 1
add $v0, $t1, $v0
sw $v0, 0($sp)
la $t0, 아이디
addi $t1, $zero, 0
loop:
lw $t2, 0($t0)
beq $t2, $zero, end_loop
addi $t0, $t0, 4
j loop
end_loop:
sw $v0, 0($t0)
j start_0
end_1:
la $t0, 아이디
addi $t1, $zero, 0
pop_loop:
lw $t2, 0($t0)
beq $t2, $zero, pop_end
addi $t1, $t0, 0
addi $t0, $t0, 4
j pop_loop
pop_end:
lw $v0, 0($t1)
sw $zero, 0($t1)
sw $v0, -4($sp)