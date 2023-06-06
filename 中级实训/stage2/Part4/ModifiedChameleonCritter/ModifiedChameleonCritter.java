import info.gridworld.actor.Actor;
import info.gridworld.actor.Critter;
import info.gridworld.grid.Location;

import java.util.ArrayList;
import java.awt.Color;

/**
 * A <code>ModifiedChameleonCritter</code> takes on the color of neighboring actors as
 * it moves through the grid. <br />
 * The implementation of this class is testable on the AP CS A and AB exams.
 */
public class ModifiedChameleonCritter extends Critter
{
    // 变暗的系数, 把系数调小使效果更明显 
    private final double DARKENING_FACTOR = 0.8d;
    /**
     * Randomly selects a neighbor and changes this critter's color to be the
     * same as that neighbor's. If there are no neighbors, no action is taken.
     * if the list of actors to process is empty, the color of the ChameleonCritter will darken (like a flower).
     */
    public void processActors(ArrayList<Actor> actors)
    {
        int n = actors.size();
        if (n == 0){
            darken();
            return;
        }
        int r = (int) (Math.random() * n);
        Actor other = actors.get(r);
        setColor(other.getColor());
    }

    /**
     * Turns towards the new location as it moves.
     */
    public void makeMove(Location loc)
    {
        setDirection(getLocation().getDirectionToward(loc));
        super.makeMove(loc);
    }

    /**
     * 参考Flower中的act方法，写出一个颜色变暗的方法
     * the ChameleonCritter darken (like a flower).
     */
    public void darken(){
        Color c = getColor();
        int red = (int) (c.getRed() * DARKENING_FACTOR);
        int green = (int) (c.getGreen() * DARKENING_FACTOR);
        int blue = (int) (c.getBlue() * DARKENING_FACTOR);
        setColor(new Color(red, green, blue));
    }
}
