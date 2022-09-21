#.data
#nums: .word 11,6,9,18,79,90,25,95
.text
.globl main
main:  
  # la  $t0,nums + 4
  addi $t0,$zero,4           # 0400  在mars下运行时用“la  $t0,nums + 4"代替 
  addi $zero,$zero,0x1a  #1a04 
  addi $zero,$zero,0x1b  #1b08 
  lw $s1,0($t0)                 # 060c
  lw $s2,4($t0)                # 0910
  add $s3,$zero,$zero    # 0014
  addi $zero,$zero,0x2a  #2a18 
loop:
  addi $s1,$s1,1            # 071c 081c 091c
  addi $zero,$zero,0x3a  #3a20 
  addi $zero,$zero,0x3b  #3b24 
  beq $s1,$s2,exit         # fe28 ff28 0028，这里插入1个气泡
  addi $zero,$zero,0x4a  #4a2c
  add $s3,$s3,$s1         # 0730  0f30
  j loop                        # 0034 0034
  addi $zero,$zero,0x5a   #//5a38
exit:
  sub $s3,$s3,$s2          # 063c
  addi $zero,$zero,0x6a #6a40 
  addi $zero,$zero,0x6b #6b44
  sw $s3,8($t0)             # 0c48
ll:
  lw $s3,8($t0)              # 064c
  j ll                             # 0050
 addi $zero,$zero,0x7a #//7a54

#0400 1a04 1b08 060c 0910 0014 2a18    
#071c 3a20 3b24 fe28 4a2c 0730 0034 //5a38
#081c 3a20 3b24 ff28 4a2c 0f30 0034 //5a38
#091c 3a20 3b24 0028 //4a2c
#063c 6a40 6b44 0c48 
#064c 0050 //7a54
#064c 0050 //7a54