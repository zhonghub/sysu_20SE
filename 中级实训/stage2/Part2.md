# Part2

### Answer the following questions

#### **Set 2** 

#### The source code for the BoxBug class can be found in the boxBug directory.

1. **What is the role of the instance variable sideLength?**

   sideLength作为虫子保持当前方向能够连续移动的最大步数。

   当steps小于sideLength且可以向前移动时，虫子向前移动，step++。

   ```java
   // @file: gridworld/projects/boxBug/BoxBug.java
   // @line: 45~49
   if (steps < sideLength && canMove())
   	{
   		move();
   		steps++;
   	}
   ```

   否则虫子要改变方向：连续向右转2个45°（转90°）

   ```java
   // @file: gridworld/projects/boxBug/BoxBug.java
   // @line: 50~55
   else
   	{
   		turn();
   		turn();
   		steps = 0;
   	}
   ```

   

2. **What is the role of the instance variable steps?**

   steps作为虫子保持当前方向**已经**连续移动的步数。

   在每执行一次move()（保持当前方向向前移动一步）时，都令steps++：

   ```java
   // @file: gridworld/projects/boxBug/BoxBug.java
   // @line: 45~49
   if (steps < sideLength && canMove())
           {
               move();
               steps++;
           }
   ```

   

3. **Why is the turn method called twice when steps becomes equal to sideLength?**

   因为调用1次turn方法虫子只会向右转弯45°，而要构建一个方形图案就要让虫子在转弯时(steps == sideLength 或前方是网格边界)旋转90°，所以要调用2次turn。

   

4. **Why can the move method be called in the BoxBug class when there is no move method in the BoxBug code?**

   因为Boxbug类**继承**了Bug类，而Bug类里有**公有**的move方法。

   ```java
   // @file: gridworld/projects/boxBug/BoxBug.java
   // @line: 19
   import info.gridworld.actor.Bug;
   // @line: 25
   public class BoxBug extends Bug
   ```

   

5. **After a BoxBug is constructed, will the size of its square pattern always be the same? Why or why not?**

   方形图案的大小始终相同，因为边长 sideLength是确定的，在初始化时就确定了：

   ```java
   // @file: gridworld/projects/boxBug/BoxBugRunner.java
   // @line: 33，35
   	BoxBug alice = new BoxBug(6);
       BoxBug bob = new BoxBug(6);
   ```

   

6. **Can the path a BoxBug travels ever change? Why or why not?**

   不会改变，因为起始位置、边长以及旋转方向都是确定的 。

   起始位置、边长：

   ```java
   // @file: gridworld/projects/boxBug/BoxBugRunner.java
   // @line: 33~37
   	BoxBug alice = new BoxBug(6);
       alice.setColor(Color.ORANGE);
       BoxBug bob = new BoxBug(6);
       world.add(new Location(7, 8), alice);
       world.add(new Location(5, 5), bob);
   ```

   旋转方向:向右旋转90°

   ```java
   else
   {
        turn();
        turn();
        steps = 0;
   }
   ```

   

7. **When will the value of steps be zero?**

初始化调用构造器BoxBug(int length)时，或当虫子改变方向时，steps为0。

构造器BoxBug(int length)：

```java
// @file: gridworld/projects/boxBug/BoxBug.java
// @line: 34~38
public BoxBug(int length)
    {
        steps = 0;
        sideLength = length;
    }
```

虫子改变方向：

```java
// @file: gridworld/projects/boxBug/BoxBug.java
// @line: 50~55
else
   {
       turn();
       turn();
       steps = 0;
   }
```





### Coding Exercises

1. Write a class `CircleBug` that is identical to `BoxBug`, except that in the `act` method the `turn` method is called once instead of twice. How is its behavior different from a `BoxBug`?

   红色虫子的移动轨迹是八边形，橙色虫子的移动轨迹是六边形。



5. Study the code for the `BoxBugRunner` class. Summarize the steps you would use to add another `BoxBug` actor to the grid.

    步骤：world为目标网格

   1.初始化BoxBug Actor：

   BoxBug alice = new BoxBug(6);

   2.（可选）设置BoxBug Actor的颜色（默认红色）：

   alice.setColor(Color.ORANGE);

   3.将BoxBug Actor添加到网格world上的某个位置：

   world.add(new Location(7, 8), alice);

