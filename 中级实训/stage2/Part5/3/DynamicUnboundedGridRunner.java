import info.gridworld.grid.*;
import info.gridworld.actor.*;

public class DynamicUnboundedGridRunner {
    /*
     * 首先初始化网格,设置为我实现的UnboundedGrid
     * 然后向网格中加入Bug，Flower，Rock等Actor
     */
    public static void main(String[] args)
    {
    	DynamicUnboundedGrid<Actor> grid = new DynamicUnboundedGrid<Actor>();
        ActorWorld world = new ActorWorld(grid);
        world.addGridClass("DynamicUnboundedGrid");
        world.add(new Location(2, 7), new Flower());
        world.add(new Location(8, 2), new Rock());
        world.add(new Location(3, 6), new Bug());
        world.add(new Location(4, 13), new Bug());
        world.add(new Location(18, 2), new Bug());
        world.show();
    }
}
