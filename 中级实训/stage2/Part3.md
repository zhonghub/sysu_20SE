# Part3

### Answer the following questions

#### Set 3

Assume the following statements when answering the following questions.

```
Location loc1 = new Location(4, 3);
Location loc2 = new Location(3, 4);
```

1. How would you access the row value for loc1?

   通过Location的类方法 getRow() 访问loc1的行的值：loc1.getRow()

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 110-113
   public int getRow()
   {
       return row;
   }
   ```

2. What is the value of b after the following statement is executed?

   ```
    boolean b = loc1.equals(loc2);
   ```

   false，因为loc1与loc2的行和列都不相等。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 211
   return getRow() == otherLoc.getRow() && getCol() == otherLoc.getCol();
   ```

   

3. What is the value of loc3 after the following statement is executed?

   ```
    Location loc3 = loc2.getAdjacentLocation(Location.SOUTH);
   ```

   (4, 4).

   由于Location loc2 = new Location(3, 4)，Location.SOUTH=180，所以：

   loc2.getAdjacentLocation(Location.SOUTH) = Location(4, 4)。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 147-148
   else if (adjustedDirection == SOUTH)
   	dr = 1;
   
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 168
   return new Location(getRow() + dr, getCol() + dc);
   ```

   

4. What is the value of dir after the following statement is executed?

   ```
    int dir = loc1.getDirectionToward(new Location(6, 5));
   ```

   dir = 135 = SOUTHEAST。

   已知loc1 = (4, 3)，设loc3 = (6,5)，tanθ = (5-3)/(6-4) = 1，θ=45

   而Location.NORTH = 0， 所以dir = 180 - θ = 135(度) = SOUTHEAST

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 180-194
   int dx = target.getCol() - getCol();
   int dy = target.getRow() - getRow();
   // y axis points opposite to mathematical orientation
   int angle = (int) Math.toDegrees(Math.atan2(-dy, dx));
   
   // mathematical angle is counterclockwise from x-axis,
   // compass angle is clockwise from y-axis
   int compassAngle = RIGHT - angle;
   // prepare for truncating division by 45 degrees
   compassAngle += HALF_RIGHT / 2;
   // wrap negative angles
   if (compassAngle < 0)
       compassAngle += FULL_CIRCLE;
   // round to nearest multiple of 45
   return (compassAngle / HALF_RIGHT) * HALF_RIGHT;
   ```

   

5. How does the getAdjacentLocation method know which adjacent location to return?

   getAdjacentLocation方法中的参数指明要查找的相邻网格的方向，getAdjacentLocation方法返回该方向上最接近当前位置的相邻位置。
   
   ```java
   // @file: GridWorldCode/framework/info/gridworld/Location.java
   // @line: 138-167
   // 根据方向获取 Delta r 和 Delat c
   
   // @file: gridworld/Location.java
   // @line: 168
   return new Location(getRow() + dr, getCol() + dc);
   ```
   
   



#### **Set 4**

**假设gr是一个Grid对象.**

1. How can you obtain a count of the objects in a grid? How can you obtain a count of the empty locations in a bounded grid?

   如何获取网格中对象的计数？

   gr.getOccupiedLocations().size()。

   方法ArrayList\<Location\> getOccupiedLocations()返回对象的位置列表，则其大小为对象计数。

   

   如何获取有界网格中空位置的计数？

   gr.getNumRows() * gr.getNumCols() - gr.getOccupiedLocations().size()

   空位置的计数 = 总位置计数 - 对象的计数，总位置计数 = 行数*列数

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Grid.java
   // @line: 35, 41, 85
   int getNumRows();
   int getNumCols();
   ArrayList<Location> getOccupiedLocations();
   ```

   

2. How can you check if location (10,10) is in a grid?

   gr.isValid(new Location(10,10))。isValid类方法会判断该位置是否在grid中

   ```java
   // @file: GridWorldCode/framework/info/gridworld/Grid.java
   // @line: 50
   boolean isValid(Location loc);
   ```

   

3. Grid contains method declarations, but no code is supplied in the methods. Why? Where can you find the implementations of these methods?

   Grid是一个接口类，所以类里的方法都是抽象方法：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/Grid.java
   // @line: 29
   public interface Grid<E>
       
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 29
   public class BoundedGrid<E> extends AbstractGrid<E>
       
   // @file: GridWorldCode/framework/info/gridworld/grid/UnboundedGrid.java
   // @line: 29
   public class UnboundedGrid<E> extends AbstractGrid<E>
   ```

   类BoundedGrid\<E> 和 UnboundedGrid\<E>实现了接口Grid\<E>，所以在类BoundedGrid\<E> 和 UnboundedGrid\<E>里能找到这些方法的实现。

   

4. All methods that return multiple objects return them in an ArrayList. Do you think it would be a better design to return the objects in an array? Explain your answer.

​		我认为以数组（array）形式返回对象比不上ArrayList。尽管array能通过[]访问里面保存的对象比较方便，而ArrayList需要通过get方法和set方法来访问保存的对象，但是有两者差别中最重要的一点是：array是固定大小的，初始化时就要给定大小，而ArrayList是可变大小的，可以随时通过add方法添加对象。而我们要返回多个对象时，可能并不能在编程时就能确定对象的个数，可能对象的个数会发生变化，在这种情况下，使用可变的ArrayList的优势就非常明显。



#### **Set 5**

1. Name three properties of every actor.

    位置location，方向direction，颜色color

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
   // @line: 32~34
       private Location location;
       private int direction;
       private Color color;
   ```

2. When an actor is constructed, what is its direction and color?

当一个actor被创建时，它的direction = Location.NORTH， color = Color.BLUE。

```java
// @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
// @line: 39~45
public Actor()
    {
        color = Color.BLUE;
        direction = Location.NORTH;
        grid = null;
        location = null;
    }
```

3. Why do you think that the Actor class was created as a class instead of an interface?

因为类Actor既不是接口，更不含任何抽象方法，类Actor里的所有方法都已经实现，单独使用类Actor也可以创建实例。

4. Can an actor put itself into a grid twice without first removing itself? Can an actor remove itself from a grid twice? Can an actor be placed into a grid, remove itself, and then put itself back? Try it out. What happens?

actor不能把自己放进格子里两次而不先把自己移开，否则会抛出异常IllegalStateException：

```java
// @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
// @line: 115~127
    public void putSelfInGrid(Grid<Actor> gr, Location loc)
    {
        if (grid != null)
            throw new IllegalStateException(
                    "This actor is already contained in a grid.");

        Actor actor = gr.get(loc);
        if (actor != null)
            actor.removeSelfFromGrid();
        gr.put(loc, this);
        grid = gr;
        location = loc;
    }
```

actor不能两次从网格中移除自己，否则会抛出异常IllegalStateException：

```java
// @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
// @line: 133~146
    public void removeSelfFromGrid()
    {
        if (grid == null)
            throw new IllegalStateException(
                    "This actor is not contained in a grid.");
        if (grid.get(location) != this)
            throw new IllegalStateException(
                    "The grid contains a different actor at location "
                            + location + ".");

        grid.remove(location);
        grid = null;
        location = null;
    }
```

一个actor能被放进一个格子里，把自己移走，然后放回去吗？试试看。发生了什么？

不会出错，可以正确运行。

actor第一次被放置在网格中：执行putSelfInGrid时gird==null,不会出错。

移除自己：执行removeSelfFromGrid时gird!=null 且grid.get(location) == this，不会出错。

然后将自己放回网格中：执行putSelfInGrid时gird==null,不会出错。

5. How can an actor turn 90 degrees to the right?

   执行setDirection(getDirection() + Location.RIGHT)  或  setDirection(getDirection() + 90); 

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
   // @line: 80~85    
   public void setDirection(int newDirection)
       {
           direction = newDirection % Location.FULL_CIRCLE;
           if (direction < 0)
               direction += Location.FULL_CIRCLE;
       }
   ```




#### **Set 6**

1. Which statement(s) in the canMove method ensures that a bug does not try to move out of its grid?

   以下代码：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 98~99
   if (!gr.isValid(next))
   	return false;
   ```

   

2. Which statement(s) in the canMove method determines that a bug will not walk into a rock?

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 100~101
      Actor neighbor = gr.get(next);
      return (neighbor == null) || (neighbor instanceof Flower);
   ```

3. Which methods of the Grid interface are invoked by the canMove method and why?

   isValid方法和get方法。调用isValid方法确保下一个位置是网格中的有效位置；调用get方法查看该位置中的actor，以确保它是空的或包含可以被bug替换的actor。

   

4. Which method of the Location class is invoked by the canMove method and why?

   getAdjacentLocation方法。该方法使用bug的当前方向作为参数，以找到bug下一个可能的位置。

   

5. Which methods inherited from the Actor class are invoked in the canMove method?

   从Actor中继承的方法：getGrid，getLocation，getDirection

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 93，96，97
           Grid<Actor> gr = getGrid();
           ...
           Location loc = getLocation();
           Location next = loc.getAdjacentLocation(getDirection());
   ```

   

6. What happens in the move method when the location immediately in front of the bug is out of the grid?

   bug将从网格中删除：removeSelfFromGrid()。

   ```    java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 78-81
           if (gr.isValid(next))
               moveTo(next);
           else
               removeSelfFromGrid();
   ```

   

7. Is the variable loc needed in the move method, or could it be avoided by calling getLocation() multiple times?

   是的，需要变量loc。变量loc存储bug移动之前的位置。它用于在bug移动到新位置后，在bug的旧位置插入一朵花。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 82-83
       Flower flower = new Flower(getColor());
       flower.putSelfInGrid(gr, loc);
   ```

   

8. Why do you think the flowers that are dropped by a bug have the same color as the bug?

   因为花的颜色和bug相同，花是使用bug的颜色进行构造的。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 82-83
       Flower flower = new Flower(getColor());
       flower.putSelfInGrid(gr, loc);
   ```

   

9. When a bug removes itself from the grid, will it place a flower into its previous location?

   分为两种情况：

   如果只调用removeSelfFromGrid方法将bug从网格中移除，不会在旧位置放一朵花。该方法继承自Actor类，不会在旧位置放一朵花。

   如果是通过move方法从网格中移，会在旧位置放置一朵花：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
   // @line: 78-83
   		if (gr.isValid(next))
               moveTo(next);
           else
               removeSelfFromGrid();
           Flower flower = new Flower(getColor());
           flower.putSelfInGrid(gr, loc);
   ```

   

10. Which statement(s) in the move method places the flower into the grid at the bug’s previous location?

    ```java
    // @file: GridWorldCode/framework/info/gridworld/actor/Bug.java
    // @line: 82-83
        Flower flower = new Flower(getColor());
        flower.putSelfInGrid(gr, loc);
    ```

    

11. If a bug needs to turn 180 degrees, how many times should it call the turn method?

    4次。每次旋转45°，旋转180°需要4次。
    
    ```java
    // @file: GridWorldCode/framework/info/gridworld/grid/Location.java
    // @line: 48
    public static final int HALF_RIGHT = 45;
    
    // @file: gridworld/actor/Bug.java
    // @line: 64
    setDirection(getDirection() + Location.HALF_RIGHT);
    ```
    
    
