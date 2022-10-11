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
  #多的两句,结束程序
   #li      $v0,    10          # 返回系统
  #syscall

#v(数组) in $a0, k(个数) in $a1
sort: 
     sw $ra,0($sp)
     addi $t8,$0,1 #8个数外重循环7次
loop1:#外重循环
      addi $a1,$a1,-1
      addi $t9,$a1,0
      addi $t3,$a0,0
      j loop2
next1:
      bne $a1,$t8,loop1
      lw $ra,0($sp)
      jr $ra                 # return to calling routine

loop2:#内重循环
      addi $t9,$t9,-1
      lw $t1,0($t3)
      lw $t2,4($t3)
      slt $t4,$t1,$t2 #t1>t2时t4==0,交换相邻两数
      bne $t4,$0,next2
      jal swap
next2:
      addi $t3,$t3,4  #j++
      beq $t9,$0,next1
      j loop2 #返回外重循环
      
swap: #t1>t2时交换相邻两数
      addi $t0,$t1,0
      addi $t1,$t2,0
      addi $t2,$t0,0
      sw $t1,0($t3)
      sw $t2,4($t3)
      jr $ra          # return to calling routine

