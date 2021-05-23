.text
main:
	li $s0, 1
	li $s5, 8
	li $s2, 1
	li $s4, 1
L0:
	la $t0, false
	bge $s0, $s5, SKIP0
	la $t0, true
SKIP0:
	la $t1, true
	beq $t1, $t0, if0
L1:
	j END
if0:
	li $t1, 1
	addu $t1, $s0, $t1
	move $s0, $t1
	move $s1, $s4
	move $s4, $s2
	addu $t0, $s1, $s2
	move $s2, $t0
	li $v0, 1
	la $a0, ($s1)
	syscall
	li $v0, 4
	la $a0, str0
	syscall
	j L0
END:
.data
	true: .byte 1
	false: .byte 0
	str0: .asciiz "\n"
