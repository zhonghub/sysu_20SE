import info.gridworld.actor.Bug;

public class SpiralBug extends Bug
{
    private int steps;
    private int sideLength;

    /**
     * Constructs a box bug that traces a square of a given side length
     * @param length the side length
     */
    public SpiralBug(int length)
    {
        steps = 0;
        // 由于steps从0开始，所以边长=sideLength+1
        sideLength = length;
    }

    /**
     * Moves to the next location of the square.
     */
    public void act()
    {
        // 步数小于边长且可以往前移动时：往前移动一格，步数+1
        if (steps < sideLength && canMove())
        {
            move();
            steps++;
        }
        // 否则向右旋转90度，步数清0，边长+1
        else
        {
            // 向右旋转90度
            turn();
            turn();
            // 步数清0
            steps = 0;
            // 边长+1
            sideLength += 1;
        }
    }
}