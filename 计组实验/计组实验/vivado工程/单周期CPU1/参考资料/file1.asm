.data
nums: .word 11,6,9,18,79,90,25,95

.text
.globl main
main:  
  addi $t0,$zero,4     #   ��mars������ʱ�á�la  $t0,nums + 4"����
  lw $s1,0($t0)
  lw $s2,4($t0)
  add $s3,$zero,$zero
loop:
  addi $s1,$s1,1  
  beq $s1,$s2,exit
  add $s3,$s3,$s1 
  j loop
exit:
  sub $s3,$s3,$s2
  sw $s3,8($t0)
ll:
  lw $s3,8($t0)
  j ll

