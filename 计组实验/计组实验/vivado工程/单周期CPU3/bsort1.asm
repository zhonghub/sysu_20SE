.data
nums: .word 0x16,0x6,0x9,0x20,0x39,0x5,0x8,0x18
 .space 200
 sptop:

.text
.globl main

main:
# ��$s0,$s1,$s2�ڱ����ֳ�ʱ�и�ֵ
  addi $s0,$s0,0
  addi $s1,$s1,0
  addi $s2,$s2,0

  la $sp,sptop 

  la $a0,nums
  li $a1,8
  jal sort

#ȡ�������������ڷ���ʱ��ʾ�����
  la $s0,nums
  lw $s1,0($s0)
  lw $s1,4($s0)
  lw $s1,8($s0)
  lw $s1,12($s0)
  lw $s1,16($s0)
  lw $s1,20($s0)
  lw $s1,24($s0)
  lw $s1,28($s0)
  #�������,��������
   #li      $v0,    10          # ����ϵͳ
  #syscall

#v(����) in $a0, k(����) in $a1
sort: 
     sw $ra,0($sp)
     addi $t8,$0,1 #8��������ѭ��7��
loop1:#����ѭ��
      addi $a1,$a1,-1
      addi $t9,$a1,0
      addi $t3,$a0,0
      j loop2
next1:
      bne $a1,$t8,loop1
      lw $ra,0($sp)
      jr $ra                 # return to calling routine

loop2:#����ѭ��
      addi $t9,$t9,-1
      lw $t1,0($t3)
      lw $t2,4($t3)
      slt $t4,$t1,$t2 #t1>t2ʱt4==0,������������
      bne $t4,$0,next2
      jal swap
next2:
      addi $t3,$t3,4  #j++
      beq $t9,$0,next1
      j loop2 #��������ѭ��
      
swap: #t1>t2ʱ������������
      addi $t0,$t1,0
      addi $t1,$t2,0
      addi $t2,$t0,0
      sw $t1,0($t3)
      sw $t2,4($t3)
      jr $ra          # return to calling routine

