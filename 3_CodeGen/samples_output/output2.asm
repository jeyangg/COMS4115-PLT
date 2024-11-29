lw $v0, x
move $t1, $v0
li $v0, 10
beq $v0, $zero, false_0
li $v0, 1  # Print integer syscall
syscall
j end_1
false_0:
li $v0, 1  # Print integer syscall
syscall
end_1: