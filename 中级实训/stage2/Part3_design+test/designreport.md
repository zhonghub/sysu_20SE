## Designreport

### Coding Exercises

You are asked to create a class called Jumper. This actor can move forward two cells in each move. It “jumps” over rocks and flowers. It does not leave anything behind it when it jumps.

1. **Inception: clarify the details of the problem:**

   a. What will a jumper do if the location in front of it is empty, but the location two cells in front contains a flower or a rock?

   如果前面第2个单元格包含一朵花，jumper会直接跳到花上，花会从网格中移除。

   如果前面第2个单元格包含一块石头，jumper会不断转弯，直到到前方可以继续跳下去。

   b. What will a jumper do if the location two cells in front of the jumper is out of the grid?

   jumper会不断转弯，直到前方可以继续跳下去，然后跳到前方的单元格。

   ```java
   public void act() {
   		// 当不能jump的时候一直转弯turn，直到能jump
   		while(!canJump()){
   			turn();
   		}
   		jump();
   	}
   ```

   c. What will a jumper do if it is facing an edge of the grid?

   同b，jumper会不断转弯，直到前方可以继续跳下去，然后跳到前方的单元格。

   d. What will a jumper do if another actor (not a flower or a rock) is in the cell that is two cells in front of the jumper?

   同b，jumper会不断转弯，直到前方可以继续跳下去，然后跳到前方的单元格。

   e. What will a jumper do if it encounters another jumper in its path?

   同b，jumper会不断转弯，直到前方可以继续跳下去，然后跳到前方的单元格。

   f. Are there any other tests the jumper needs to make?

   应该测试前方一个单元格为Flower、Rock、Jumper的情况下，jumper能否跳到前方第二个单元格。

   在我的设计里，当且仅当以下这种情况jumper能继续跳到前方第2个单元格：

   | 前方第1个单元格 | 前方第2个单元格（在网格内） | canjump |
   | --------------- | --------------------------- | ------- |
   | 空/Rock/Flower  | 空/Flower                   | true    |

   其它情况都不能继续跳下去。

   

### 代码运行方式：

解压后，在当前目录（Part3）下，在终端运行指令：

```
javac -classpath .:lib/* Jumper/*.java && java -classpath .:lib/*:Jumper JumperRunner
```