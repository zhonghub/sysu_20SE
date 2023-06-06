# Part4

### Answer the following questions

#### Set 7

The source code for the Critter class is in the critters directory

1. What methods are implemented in Critter?

   act, getActors, processActors, getMoveLocations, selectMoveLocation, makeMove

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 38
   public void act();
   
   // @line: 56
   public ArrayList<Actor> getActors();
   
   // @line: 71
   public void processActors(ArrayList<Actor> actors);
   
   // @line: 88
   public ArrayList<Location> getMoveLocations();
   
   // @line: 104
   public Location selectMoveLocation(ArrayList<Location> locs);
   
   // @line: 125
   public void makeMove(Location loc);
   ```

   

2. What are the five basic actions common to all critters when they act?

   getActors, processActors, getMoveLocations, selectMoveLocation, makeMove

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 38-47
   	public void act()
       {
           if (getGrid() == null)
               return;
           ArrayList<Actor> actors = getActors();
           processActors(actors);
           ArrayList<Location> moveLocs = getMoveLocations();
           Location loc = selectMoveLocation(moveLocs);
           makeMove(loc);
       }
   ```

   

3. Should subclasses of Critter override the getActors method? Explain.

   是的，如果critter子类想要选择不同于critter类选择的actor，就需要重写方法getActors。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 50-53
   /*
    * Gets the actors for processing. Implemented to return the actors that
    * occupy neighboring grid locations. Override this method in subclasses to
    * look elsewhere for actors to process.<br />
   */
   ```

   

   

4. Describe the way that a critter could process actors.

   Critter可以处理 Actors，例如移除它们，改变它们的颜色，位置，方向，或选中一部分Actors做上述操作。

   ```java
   // @file: gridworld/actor/Critter.java
   // @line: 62-65
   
   /*
    * Processes the elements of <code>actors</code>. New actors may be added
    * to empty locations. Implemented to "eat" (i.e. remove) selected actors
    * that are not rocks or critters. Override this method in subclasses to
    * process actors in a different way. <br />
    */
   ```
   
   
   
5. What three methods must be invoked to make a critter move? Explain each of these methods.

   这3个必须方法为：getMoveLocations，selectMoveLocation，makeMove。

   getMoveLocations获取critter可以移动到的位置；

   selectMoveLocation从中选出critter接下来移动到的位置；

   makeMove再将critter移动到新位置。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 44-46
           ArrayList<Location> moveLocs = getMoveLocations();
           Location loc = selectMoveLocation(moveLocs);
           makeMove(loc);
   ```

   

   

6. Why is there no Critter constructor?

   因为子类Critter可以调用父类Actor中的默认构造器。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 31
   public class Critter extends Actor
   ```




#### Set 8 

The source code for the ChameleonCritter class is in the critters directory

**文件目录：GridWorldCode/projects/critters**

1. Why does act cause a ChameleonCritter to act differently from a Critter even though ChameleonCritter does not override act?

   因为父类Critter的act方法中调用了processActors和makeMove方法，子类ChameleonCritter对这两个方法进行了重写，导致子类ChameleonCritter的act方法会调用重写的这两个方法，从而和父类Critter的act方法不同。

   父类 Critter的act方法中调用了processActors和makeMove方法：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 43
           processActors(actors);
   // @line: 46
           makeMove(loc);
   ```

   子类ChameleonCritter重写了方法processActors和makeMove：

   ```java
   // @file: GridWorldCode/projects/critters/ChameleonCritter.java
   // @line: 36
   public void processActors(ArrayList<Actor> actors)
   // line: 50
   public void makeMove(Location loc)
   ```

2. Why does the makeMove method of ChameleonCritter call super.makeMove?

   ChameleonCritter重写makeMove只在移动前改变方向，移动则是通过super.makeMove调用父类的makeMove方法，这样不仅使代码更为简洁（相比于拷贝代码），而且使子类的行为更加趋向于父类，使面向对象设计的继承性更为突出。

   ```java
   // @file: GridWorldCode/projects/critters/ChameleonCritter.java
   // @line: 50-54
       public void makeMove(Location loc)
       {
           setDirection(getLocation().getDirectionToward(loc));
           super.makeMove(loc);
       }
   ```

3. How would you make the ChameleonCritter drop flowers in its old location when it moves?

   重写makeMove方法，记录移动前的位置，如果移动前后位置发生变化，则在原位置掉下一朵花；否则不掉。

   ```java
       public void makeMove(Location loc)
       {
       	Location loc0 = getLocation();
           setDirection(getLocation().getDirectionToward(loc));
           super.makeMove(loc);
           if(!loc0.equals(loc)) // 位置变化时才会掉下一朵花
    		{ 
    			Flower flower = new Flower(getColor()); 
    			flower.putSelfInGrid(getGrid(), loc0); 
    		} 
       }
   ```

4. Why doesn’t ChameleonCritter override the getActors method?

   因为 ChameleonCritter 处理的Actor列表与其父类Criter相同，所以它不需要重写方法getActors。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 56-59
       public ArrayList<Actor> getActors()
       {
           return getGrid().getNeighbors(getLocation());
       }
   ```

5. Which class contains the getLocation method?

   在最顶上的父类Actor里包含方法getLocation：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
   // @line: 102-105
       public Location getLocation()
       {
           return location;
       }
   ```

6. How can a Critter access its own grid?

   Critter可以调用从父类里继承的getGrid方法获取自己的grid：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Actor.java
   // @line: 92-95
   	public Grid<Actor> getGrid()
       {
           return grid;
       }
   ```

   

#### Set 9

The source code for the CrabCritter class is reproduced at the end of this part of GridWorld.

1. Why doesn’t CrabCritter override the processActors method?

   因为CrabCritter想要保持和父类Critter一样的处理Actors的操作：将选中的Actors从网格中移除，就不需要对该方法进行重写。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 71-78
   	public void processActors(ArrayList<Actor> actors)
       {
           for (Actor a : actors)
           {
               if (!(a instanceof Rock) && !(a instanceof Critter))
                   a.removeSelfFromGrid();
           }
       }
   ```

2. Describe the process a CrabCritter uses to find and eat other actors. Does it always eat all neighboring actors? Explain.

   CrabCritter通过在act方法中执行getActors方法和processActors方法吃掉其它Actors：

   getActors方法选则要被吃掉的Actors，processActors方法将选中的Actors从网格上移除。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 42-43	
   	ArrayList<Actor> actors = getActors();
   	processActors(actors);
   ```

    CrabCritter不会吃掉相邻的所有Actors，只会吃掉在它{ Location.AHEAD, Location.HALF_LEFT, Location.HALF_RIGHT }这三个方向相邻的Actors：

   ```java
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 44-57
   	public ArrayList<Actor> getActors()
       {
           ArrayList<Actor> actors = new ArrayList<Actor>();
           int[] dirs =
               { Location.AHEAD, Location.HALF_LEFT, Location.HALF_RIGHT };
           for (Location loc : getLocationsInDirections(dirs))
           {
               Actor a = getGrid().get(loc);
               if (a != null)
                   actors.add(a);
           }
   
           return actors;
       }
   ```

   

3. Why is the getLocationsInDirections method used in CrabCritter?

   CrabCritter通过方法 getLocationsInDirections获取其在{ Location.AHEAD, Location.HALF_LEFT, Location.HALF_RIGHT}这3个方向上相邻的有效位置（在网格内），继而通过位置获取其单元格上的Actor。

   ```java
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 47-49
           int[] dirs =
               { Location.AHEAD, Location.HALF_LEFT, Location.HALF_RIGHT };
           for (Location loc : getLocationsInDirections(dirs))
           
   ```

   此外，CrabCritter还通过方法 getLocationsInDirections获取其在{ Location.LEFT, Location.RIGHT }这2个方向上相邻的有效位置，作为供选择的下一步移动的位置：

   ```java
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 65-67
           int[] dirs =
               { Location.LEFT, Location.RIGHT };
           for (Location loc : getLocationsInDirections(dirs))
   ```

   

4. If a CrabCritter has location (3, 4) and faces south, what are the possible locations for actors that are returned by a call to the getActors method?

   (4, 4)、(4, 5)、(4, 3)，分别为正前、左前、右前方的位置：

   ```java
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 47-48
           int[] dirs =
               { Location.AHEAD, Location.HALF_LEFT, Location.HALF_RIGHT };
   ```

   

5. What are the similarities and differences between the movements of a CrabCritter and a Critter?

   **相同：**

   移动时不会转向：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 130
   moveTo(loc);
   
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 90
   super.makeMove(loc);
   ```

   都是随机从可移动位置列表中挑选（CrabCritter没有重写 Critter的selectMoveLocation方法）：

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 104-111
       public Location selectMoveLocation(ArrayList<Location> locs)
       {
           int n = locs.size();
           if (n == 0)
               return getLocation();
           int r = (int) (Math.random() * n);
           return locs.get(r);
       }
   ```

   **不同：**

   CrabCritter只会向左或向右移动。Critter可能的移动位置是其八个相邻位置中的任何一个。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 88-91
       public ArrayList<Location> getMoveLocations()
       {
           return getGrid().getEmptyAdjacentLocations(getLocation());
       }
   
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 62-72
       public ArrayList<Location> getMoveLocations()
       {
           ArrayList<Location> locs = new ArrayList<Location>();
           int[] dirs =
               { Location.LEFT, Location.RIGHT };
           for (Location loc : getLocationsInDirections(dirs))
               if (getGrid().get(loc) == null)
                   locs.add(loc);
   
           return locs;
       }
   ```

   当CrabCritter无法移动时，它会随机向右或向左转弯。当Critter不能移动时，它就不会转动。

   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 130
               moveTo(loc);
   
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 79-88
   	if (loc.equals(getLocation()))
           {
               double r = Math.random();
               int angle;
               if (r < 0.5)
                   angle = Location.LEFT;
               else
                   angle = Location.RIGHT;
               setDirection(getDirection() + angle);
           }
   ```

   

6. How does a CrabCritter determine when it turns instead of moving?

   当目标移动位置等当前位置时，Crab选择用转向而不是移动。

   ```java
   // @file: GridWorldCode/projects/critters/CrabCritter.java
   // @line: 79-88
   	if (loc.equals(getLocation()))
           {
               double r = Math.random();
               int angle;
               if (r < 0.5)
                   angle = Location.LEFT;
               else
                   angle = Location.RIGHT;
               setDirection(getDirection() + angle);
           }
   ```

   

7. Why don’t the CrabCritter objects eat each other?

   因为CrabCritter 吃掉其它对象使用的是继承于父类Critter的processActors方法
   
   ```java
   // @file: GridWorldCode/framework/info/gridworld/actor/Critter.java
   // @line: 75-76
   if (!(a instanceof Rock) && !(a instanceof Critter))
       a.removeSelfFromGrid();
   ```
   
   
