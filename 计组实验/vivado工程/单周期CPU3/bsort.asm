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

loop:    
   j loop

#v(����) in $a0, k(����) in $a1
sort:   ...
      jr $ra                 # return to calling routine


swap: ...
      jr $ra            # return to calling routine

