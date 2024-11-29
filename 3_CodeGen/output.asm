.data
딕셔너리_연산기: .space 400  # Reserve space for dictionary '연산기'

.text
.globl main

# Function 더하기
더하기:
# Allocating space for variable x
sw x, 0($sp)
lw $v0, 0($sp)  # Load x
sll $t0, $v0, 2  # Multiply key by 4 (word size)
la $t1, 딕셔너리_연산기  # Load base address of dictionary
add $t2, $t0, $t1  # Compute address for key in dictionary
lw $v0, 0($sp)  # Load x
move $t1, $v0  # Save left operand
# Allocating space for variable y
sw y, -4($sp)
lw $v0, -4($sp)  # Load y
add $v0, $t1, $v0
sw $v0, 0($t2)  # Store value in dictionary
jr $ra  # Return from function

# Function 지수
지수:
jr $ra  # Return from function
move $a0, $v0  # Move value to $a0 for printing
li $v0, 1  # Print integer syscall
syscall