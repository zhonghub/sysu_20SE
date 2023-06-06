# Part1

## **Step1：Running the Demo**

1. Does the bug  always move to a new location? Explain.

   不是。只有当虫子正前方存在空的单元格或有花的单元格时，虫子才会移动到它前面的单元格。

2. In which direction does the bug move?

   虫子往前移动（如果可以往前移动的话，即满足1中的情况）。

3. What does the bug do if it does not move?

   当虫子不能移动时，它会向右旋转45度（重复这个动作直到正前方）。

4. What does a bug leave   behind when it moves?

   当虫子移动到一个新的单元格时，它会在旧的单元格里留下一朵颜色和虫子一样的花

5. What happens when the bug  is at an edge of the grid? (Consider whether the bug is facing the edge as  well as whether the bug is facing some other direction when answering this  question.)

   如果虫子正对着网格边缘，并被告知执行actor()，它将向右旋转45度。当被告知再次执行actor()时，它将再向右转45度。

   如果虫子正对着网格边缘，并被告知执行move()，它将从网格中出去（被移除了），一朵花将替换该位置的虫子。

   如果虫子斜对着网格边缘（通过前面的向右旋转45度变成的状态），执行move()，也会从网格中移出。

   如果虫子斜对着网格内部，执行move()则会沿当前斜线方法移动一格。

6. What happens when a bug has  a rock in the location immediately in front of it?

   虫子向右旋转45度。

7. Does a flower move?

   不会。

8. What behavior does a flower have?

   花的颜色随时间会变深，直到变成深灰色。

9. Does a rock move or have any other behavior?

   不会。当使用step或run时，岩石仍然会停留在其位置，并且不会出现任何其他行为。

10. Can more than one actor (bug, flower, rock) be in the same location in the grid at the same time?

​		不可以。网格中的一个单元格某个时刻只能包含一个actor (bug, flower, rock)。



## Step2：Exploring Actor State and Behavior

1. Test the setDirection method with the following inputs and complete the table,     giving the compass direction each input represents.

| **Degrees** | **Compass Direction** |
| ----------- | --------------------- |
| 0           | 正北                  |
| 45          | 东北                  |
| 90          | 正东                  |
| 135         | 东南                  |
| 180         | 正南                  |
| 225         | 西南                  |
| 270         | 正西                  |
| 315         | 西北                  |
| 360         | 正北                  |

1. Move a bug to a  different location using the moveTo method. In which directions can you     move it? How far can you move it? What happens if you try to move the bug outside the grid?

   使用moveTo方法将虫子移动到网格中的任何有效位置（原有位置的actor会被清除），且使用moveTo方法移动虫子时，虫子不会改变其原始方向。

   尝试将虫子移动到网格外部的位置，会导致IllegalArgumentException，例如：

   ​	java.lang.IllegalArgumentException: Location (234, 2) is not valid.

2. Change the color of a bug, a flower, and a rock. Which method did you use?

   setcolor方法。

3. Move a rock on top of a bug and then move the rock again. What happened to the bug?

   但岩石移动到虫子顶部时，虫子会从网格中移除，即使岩石再次移动到另一个位置，虫子也不会再出现。当一个新actor移动到另一个actor占据的格子时，旧actor将从网格中移除。