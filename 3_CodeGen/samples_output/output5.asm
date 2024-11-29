
# Function 피보나치
피보나치:
lw $v0, n
move $t1, $v0
li $v0, 1
beq $v0, $zero, false_0
j end_1
false_0:
end_1:
jr $ra  # Return from function

# Function 주요_함수
주요_함수:
li $v0, 10
sw $v0, 결과
li $v0, 5.5
sw $v0, 한국어_123_변수
sw $v0, 테스트_변수
sw $v0, 널_테스트
lw $v0, 테스트_변수
move $t1, $v0
move $t1, $v0
lw $v0, 한국어_123
move $t1, $v0
lw $v0, 결과
beq $v0, $zero, false_2
li $v0, 1  # Print integer syscall
syscall
j end_3
false_2:
li $v0, 1  # Print integer syscall
syscall
end_3:
li $v0, 0
sw $v0, 카운터
start_4:
lw $v0, 카운터
move $t1, $v0
beq $v0, $zero, end_5
li $v0, 1  # Print integer syscall
syscall
lw $v0, 카운터
move $t1, $v0
li $v0, 1
add $v0, $t1, $v0
sw $v0, 카운터
j start_4
end_5:
lw $v0, 결과
move $t1, $v0
lw $v0, 한국어_123
mul $v0, $t1, $v0
move $t1, $v0
li $v0, 3
move $t1, $v0
li $v0, 2
add $v0, $t1, $v0
move $t1, $v0
li $v0, 1
sub $v0, $t1, $v0
sw $v0, 수학_결과
move $t1, $v0
lw $v0, 수학_결과
li $v0, 1  # Print integer syscall
syscall
sw $v0, 문자열_테스트
lw $v0, 문자열_테스트
li $v0, 1  # Print integer syscall
syscall
jr $ra  # Return from function
sw $v0, 문자열_테스트