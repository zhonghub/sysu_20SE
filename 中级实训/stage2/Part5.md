# Part5

### Answer the following questions

#### **Set 10**

源文件夹：GridWorldCode/framework/info/gridworld/grid

The source code for the AbstractGrid class is in Appendix D.

1. Where is the isValid method specified? Which classes provide an implementation of this method?

   isValid 被声明在Grid接口中

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/Grid.java
   // @line: 50
   boolean isValid(Location loc);
   ```

   BoundedGrid类和UnboundedGrid类实现了该声明

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 60
   public boolean isValid(Location loc);
   
   // @file: GridWorldCode/framework/info/gridworld/grid/UnboundedGrid.java
   // @line: 53
   public boolean isValid(Location loc);
   ```

2. Which AbstractGrid methods call the isValid method? Why don’t the other methods need to call it?

   Abstract在`getValidAdjacentLocations`方法中调用了`isValid`方法

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/AbstractGrid.java
   // @line: 44
   if (isValid(neighborLoc))
   ```

   解释：`getEmptyAdjacentLocations`和`getOccupiedAdjacentLocations`虽然和`getValidAdjacentLocations`类似，但是它们不直接调用`isValid`，而是通过调用`getValidAdjacentLocations`来间接使用`isValid`，这样可以简化`getEmptyAdjacentLocations`和`getOccupiedAdjacentLocations`的代码，避免代码重复。

3. Which methods of the Grid interface are called in the getNeighbors method? Which classes provide implementations of these methods?

   接口Grid中的`get`方法和`getOccupiedAdjacentLocations`方法被`getNeighbors `方法调用。

   在`AbstractGrid`类中实现了方法`getOccupiedAdjacentLocations`；

   在`BoundedGrid`类和`UnboundedGrid`类中都分别实现了`get`方法。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/AbstractGrid.java
   // @line: 28-34
   	public ArrayList<E> getNeighbors(Location loc)
       {
           ArrayList<E> neighbors = new ArrayList<E>();
           for (Location neighborLoc : getOccupiedAdjacentLocations(loc))
               neighbors.add(get(neighborLoc));
           return neighbors;
       }
   ```

   `getOccupiedAdjacentLocations`方法的实现：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/AbstractGrid.java
   // @line: 62-71
       public ArrayList<Location> getOccupiedAdjacentLocations(Location loc)
       {
           ArrayList<Location> locs = new ArrayList<Location>();
           for (Location neighborLoc : getValidAdjacentLocations(loc))
           {
               if (get(neighborLoc) != null)
                   locs.add(neighborLoc);
           }
           return locs;
       }
   ```

   `get`方法的实现:

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 85-91
       public E get(Location loc)
       {
           if (!isValid(loc))
               throw new IllegalArgumentException("Location " + loc
                       + " is not valid");
           return (E) occupantArray[loc.getRow()][loc.getCol()]; // unavoidable warning
       }
   
   // @file: GridWorldCode/framework/info/gridworld/grid/UnboundedGrid.java
   // @line: 66-71
       public E get(Location loc)
       {
           if (loc == null)
               throw new NullPointerException("loc == null");
           return occupantMap.get(loc);
       }
   ```

4. Why must the get method, which returns an object of type E, be used in the getEmptyAdjacentLocations method when this method returns locations, not objects of type E?

   `getEmptyAdjacentLocations`方法调用`get`方法的目的是，判断这个位置是否有对象存在，如果这个位置没有对象存在，则该位置为`EmptyAdjacentLocations`，否则为`OccupiedAdjacentLocations`。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/AbstractGrid.java
   // @line: 67-68
   if (get(neighborLoc) != null)
       locs.add(neighborLoc);
   ```

   `get`方法用于获取一格位置的对象，返回结果可能是该对象或null。

5. What would be the effect of replacing the constant Location.HALF_RIGHT with Location.RIGHT in the two places where it occurs in the getValidAdjacentLocations method?

   如果把`Location.HALF_RIGHT`换成`Location.RIGHT`，`getValidAdjacentLocations`就只会考虑东南西北四个方向的相邻位置，而原本会考虑八个方向的相邻位置。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/AbstractGrid.java
   // @line: 41
   // Location.FULL_CIRCLE / Location.HALF_RIGHT = 360 / 45 = 8
   // Location.FULL_CIRCLE / Location.RIGHT = 360 / 90 = 4
   for (int i = 0; i < Location.FULL_CIRCLE / Location.HALF_RIGHT; i++){}
   ```

   ### 

#### Set 11

The source code for the BoundedGrid class is in Appendix D.

1. What ensures that a grid has at least one valid location?

   通过在行数或列数小于等于0时抛出异常，保证行数和列数都大于等于1，使Grid至少会有一个有效位置：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 41-44
   if (rows <= 0)
       throw new IllegalArgumentException("rows <= 0");
   if (cols <= 0)
       throw new IllegalArgumentException("cols <= 0");
   ```

2. How is the number of columns in the grid determined by the getNumCols method? What assumption about the grid makes this possible?

   `occupantArray[0].length`。规定行数、列数都大于0保证了occupantArray为非空的二维数组，且二维数组中每个一维数组的大小相同（occupantArray[i].length），从而可以直接取`occupantArray[0].length`为列数：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 41-44
   if (rows <= 0)
       throw new IllegalArgumentException("rows <= 0");
   if (cols <= 0)
       throw new IllegalArgumentException("cols <= 0");
   occupantArray = new Object[rows][cols];
   ```

3. What are the requirements for a Location to be valid in a BoundedGrid?

   一个Location是有效的当且仅当：0<=行数<行总数 且 0<=列数<列总数。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 62-63
   return 0 <= loc.getRow() && loc.getRow() < getNumRows()
       && 0 <= loc.getCol() && loc.getCol() < getNumCols();
   ```

   

In the next four questions, let r = number of rows, c = number of columns, and n = number of occupied locations.

1. What type is returned by the getOccupiedLocations method? What is the time complexity (Big-Oh) for this method?

   返回类型：`ArrayList<Location>`

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 66
   public ArrayList<Location> getOccupiedLocations(){}
   ```

   时间复杂度：O(r * c) ，假设每次取出并判断一个位置是否有效的复杂度为 O(1)

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 71-80
   for (int r = 0; r < getNumRows(); r++){ // row: r
       for (int c = 0; c < getNumCols(); c++){ // col: c
           // ...
       }
   }
   ```

   

2. What type is returned by the get method? What parameter is needed? What is the time complexity (Big-Oh) for this method?

   返回类型：`E`

   参数：`Location loc`，即网格中的指定的位置

   时间复杂度：O(1)

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 85
   public E get(Location loc);
   ```

3. What conditions may cause an exception to be thrown by the put method? What is the time complexity (Big-Oh) for this method?

   当参数中的位置loc非法（!isValid(loc)）或对象obj为空时抛出异常。

   时间复杂度为O(1)。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 95-99
   		if (!isValid(loc))
               throw new IllegalArgumentException("Location " + loc
                       + " is not valid");
           if (obj == null)
               throw new NullPointerException("obj == null");
   ```

   

4. What type is returned by the remove method? What happens when an attempt is made to remove an item from an empty location? What is the time complexity (Big-Oh) for this method?

   返回类型：`E`

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 114-116
   		E r = get(loc);
           occupantArray[loc.getRow()][loc.getCol()] = null;
           return r;
   ```

   移除一个空位置的对象会返回 null ，不会报错。仅当参数中的位置loc非法（!isValid(loc)）时才会抛出异常。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/BoundedGrid.java
   // @line: 109-111
   		if (!isValid(loc))
               throw new IllegalArgumentException("Location " + loc
                       + " is not valid");
   ```

   时间复杂度为O(1)

   

5. Based on the answers to questions 4, 5, 6, and 7, would you consider this an efficient implementation? Justify your answer.

   是一个比较高效的实现。唯一效率低下的方法是`getOccupiedLocations`方法，其时间复杂度为O(r * c)。其他方法（put、get和remove）都是O(1)。所以可以同时使用一个`HashMap或者Set`来存储被占据的**位置**，然后涉及到**位置的变化**时都应对`HashMap或者Set`进行相应的**插入**或**删除**操作或者**不操作**，这样`getOccupiedLocations`方法就可以直接返回从`HashMap或者Set`中得到的被占据位置的`ArrayList<Location>`。



#### Set 12

The source code for the UnboundedGrid class is in Appendix D.

1. Which method must the Location class implement so that an instance of HashMap can be used for the map? What would be required of the Location class if a TreeMap were used instead? Does Location satisfy these requirements?

   `equals`和`hashCode`方法是Location作为HashMap主键必须要实现的方法，前者用于判断两个Location是否相等，后者提供一个哈希映射的编码方式。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/Location.java
   // @line: 205, 218
   public boolean equals(Object other){}
   public int hashCode(){}
   ```

   `comparedTo`方法是Location作为TreeMap使用必须实现的方法，用于比较两个Location的大小，要构建一个TreeMap，主键必须是可以比较大小的。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/Location.java
   // @line: 234
   public int compareTo(Object other){}
   ```

   Location实现了Comparable接口，满足上述条件。

   

2. Why are the checks for null included in the get, put, and remove methods? Why are no such checks included in the corresponding methods for the BoundedGrid?

   因为对于`UnboundedGrid`任意一个位置都是合法的，有关`Location`出错的原因只能是该位置的对象为空，故需要判断；同时`UnboundedGrid`使用哈希表来实现其基本结构，哈希表的`get`、`put`、`remove`方法没有对参数为空的情况进行处理（null在哈希表的访问中也是一个合法的参数），故需要在代码中额外处理，抛出空指针异常。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/UnboundedGrid.java
   // @line: 70
   return occupantMap.get(loc);
   
   // @line: 79
   return occupantMap.put(loc, obj);
   
   // @line: 86  
   return occupantMap.remove(loc);
   ```

   

3. What is the average time complexity (Big-Oh) for the three methods: get, put, and remove? What would it be if a TreeMap were used instead of a HashMap?

   对于 `HashMap`，`get`, `put` 和`remove`的复杂度都是 O(1)。

   对于 `TreeMap`，`get`, `put` 和`remove`的复杂度都是 O(log(n))，令n为格子的总数，log(n)即为平衡树的高度。

   

4. How would the behavior of this class differ, aside from time complexity, if a TreeMap were used instead of a HashMap?

   不同之处出现在`getOccupiedLocations`的返回结果上，使用 HashMap 返回的 `ArrayList<Location>`一般是无序的，使用 TreeMap 返回的 `ArrayList<Location>`是有序的，从小到大排列。

   这是由于二叉平衡树本身的性质决定的，TreeMap在添加和删除节点的时候会进行重排序，从而遍历可以得到一个有序的`ArrayList<Location>`。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/grid/UnboundedGrid.java
   // @line: 58
   public ArrayList<Location> getOccupiedLocations(){}
   ```

5. Could a map implementation be used for a bounded grid? What advantage, if any, would the two-dimensional array implementation that is used by the BoundedGrid class have over a map implementation?

   可以使用Map来实现BoundedGrid。
   
   使用数组实现的好处：
   
   * 一是数组访问时间复杂度稳定为O(1)，而对于哈希表，如果哈希函数设计的不好，复杂度会退化为O(n)。
   * 二是空间效率，对于比较满的网格，数组实现比映射实现更能节省空间，因为后者储存的是<Location，E>二元组，数组实现不需要显示储存Location。





### Coding Exercises

#### 1 稀疏矩阵实现

对于非常大的有界网格并经常调用 getOccupiedLocations 方法的程序，此实现的时间复杂度为 O(r + n)，其中 r 是行数，n 是网格中的项目数。 此方法的 BoundedGrid 实现的时间复杂度为 O(r * c)，其中 r 是行数，c 是列数。



#### 2 HashMap实现

用HashMap同样能达到稀疏矩阵的效果，实现上类似于UnboundedGrid，只是对 Location进行了约束。

 和UnboundedGrid类的实现一致的方法有： getOccupiedLocations ， get ， put ， remove 。

以下是各种BoundGrid实现方式的复杂度对比：设r = 行数，c = 列数，n = 非空位置总数

|            Methods             | `SparseGridNode` version | `LinkedList<OccupantInCol>` version | `HashMap` version | `TreeMap` version |
| :----------------------------: | :----------------------: | :---------------------------------: | :---------------: | :---------------: |
|         `getNeighbors`         |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |
|  `getEmptyAdjacentLocations`   |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |
| `getOccupiedAdjacentLocations` |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |
|     `getOccupiedLocations`     |          O(r+n)          |               O(r+n)                |       O(n)        |       O(n)        |
|             `get`              |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |
|             `put`              |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |
|            `remove`            |           O(c)           |                O(c)                 |       O(1)        |     O(log n)      |



#### 3  DynamicUnboundedGrid 动态分配

What is the Big-Oh efficiency of the get method? What is the efficiency of the put method when the row and column index values are within the current array bounds? What is the efficiency when the array needs to be resized?

**时间复杂度分析：** r = 行数，c = 列数

get 方法： O(1)

put 方法：当不需要扩大网格时，时间复杂度为 O(1)；当需要扩大网格时，时间复杂度为O(r * c+1)

扩大网格：时间复杂度为O(r * c)
