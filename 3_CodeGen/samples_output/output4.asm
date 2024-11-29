start_0:
move $t1, $v0
li $v0, 10
beq $v0, $zero, end_1
sw $v0, 원소
j start_0
end_1:
sw $v0, 아이디_원소_0
sw $v0, 3원소