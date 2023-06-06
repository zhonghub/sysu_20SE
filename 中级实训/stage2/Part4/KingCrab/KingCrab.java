import info.gridworld.actor.Actor;
import info.gridworld.actor.Critter;
import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;

import java.awt.Color;
import java.util.ArrayList;

/**
 * A <code>KingCrab</code> looks at a limited set of neighbors when it eats and
 * moves.
 * <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class KingCrab extends CrabCritter {

    public KingCrab() {
        setColor(Color.RED);
    }

    public void processActors(ArrayList<Actor> actors) {
        for (Actor a : actors) {
            if (a instanceof CrabCritter) {
                continue;
            }
            Location loc0 = a.getLocation();
            ArrayList<Location> locs = getGrid().getEmptyAdjacentLocations(loc0);
            for (Location loc : locs) {
                if (isFurtherLocation(loc)) {
                    a.moveTo(loc);
                    break;
                }
            }
            if (a.getLocation().equals(loc0)) {
                a.removeSelfFromGrid();
            }
        }
    }

    private boolean isFurtherLocation(Location loc1) {
        int x1 = loc1.getRow();
        int y1 = loc1.getCol();
        int xk = getLocation().getRow();
        int yk = getLocation().getCol();
        int d1 = (x1 - xk) * (x1 - xk) + (y1 - yk) * (y1 - yk);
        if (d1 > 2) {
            return true;
        }
        return false;
    }

}
