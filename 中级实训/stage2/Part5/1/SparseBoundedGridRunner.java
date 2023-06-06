import info.gridworld.grid.*;
import info.gridworld.actor.*;

public class SparseBoundedGridRunner {
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        world.addGridClass("SparseBoundedGrid");
        world.add(new Location(2, 2), new Bug());
        world.add(new Location(4, 2), new Critter());
        world.add(new Flower());
        world.add(new Rock());
        world.add(new Rock());
        world.show();
    }
}
