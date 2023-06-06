import info.gridworld.actor.Actor;
import info.gridworld.actor.Critter;
import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;

import java.awt.Color;
import java.util.ArrayList;

/**
 * A <code>QuickCrab</code> looks at a limited set of neighbors when it eats and
 * moves.
 * <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class QuickCrab extends CrabCritter {

    public QuickCrab() {
        setColor(Color.GREEN);
    }

    /**
     * @return list of empty locations immediately to the right and to the left
     */
    public ArrayList<Location> getMoveLocations() {
        int[] dirs = { Location.LEFT, Location.RIGHT };
        ArrayList<Location> locs = getLocationsTwoSteps(dirs);
        if (locs.size() == 0) {
            return super.getMoveLocations();
        }
        return locs;
    }

    /**
     * Finds the valid and empty two steps adjacent locations of this critter
     * in different directions.
     * 
     * @param directions - an array of directions (which are relative to the
     *                   current direction)
     * @return a set of valid and empty locations that are two steps neighbors
     *         of the current location in the given directions
     */
    public ArrayList<Location> getLocationsTwoSteps(int[] directions) {
        ArrayList<Location> locs = new ArrayList<Location>();
        Grid gr = getGrid();
        Location loc = getLocation();
        for (int d : directions) {
            Location loc1 = loc.getAdjacentLocation(getDirection() + d);
            if (gr.isValid(loc1) && gr.get(loc1) == null) {
                Location loc2 = loc1.getAdjacentLocation(getDirection() + d);
                if (gr.isValid(loc2) && gr.get(loc2) == null) {
                    locs.add(loc2);
                }
            }
        }
        return locs;
    }
}
