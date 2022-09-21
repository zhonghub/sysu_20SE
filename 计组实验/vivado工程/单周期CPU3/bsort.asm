.data
nums: .word 0x16,0x6,0x9,0x20,0x39,0x5,0x8,0x18
 .space 200
 sptop:

.text
.globl main

main:
# 令$s0,$s1,$s2在保存现场时有个值
  addi $s0,$s0,0
  addi $s1,$s1,0
  addi $s2,$s2,0

  la $sp,sptop 

  la $a0,nums
  li $a1,8
  jal sort

#取出排序结果（用于仿真时显示结果）
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

#v(数组) in $a0, k(个数) in $a1
sort:   ...
      jr $ra                 # return to calling routine


swap: ...
      jr $ra            # return to calling routine

