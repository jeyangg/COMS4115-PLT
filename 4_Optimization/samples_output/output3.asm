.data
딕셔너리_연산기: .space 400

.text
.globl main
더하기:
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $v0, 0($sp)
sll $t0, $v0, 2
la $t1, 딕셔너리_연산기
add $t2, $t0, $t1
lw $v0, 0($sp)
move $t1, $v0
lw $v0, -4($sp)
add $v0, $t1, $v0
sw $v0, 0($t2)
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra          
# Error encountered: Unexpected function open