import info.gridworld.actor.ActorWorld;
import info.gridworld.actor.Rock;
import info.gridworld.actor.Critter;
import info.gridworld.grid.Location;

import java.awt.Color;

/**
 * This class runs a world that contains BlusterCritter critters. <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class BlusterCritterRunner
{
    public static void main(String[] args)
    {
        // 初始化网格
        ActorWorld world = new ActorWorld();
        // 往网格中添加Rock
        world.add(new Location(7, 8), new Critter());
        world.add(new Location(3, 3), new Critter());
        world.add(new Location(2, 4), new Critter());
        world.add(new Location(2, 5), new Critter());
        world.add(new Location(2, 8), new Rock(Color.BLUE));
        world.add(new Location(3, 8), new Rock(Color.GREEN));
        world.add(new Location(5, 5), new Rock(Color.PINK));
        world.add(new Location(1, 5), new Rock(Color.RED));
        world.add(new Location(7, 2), new Rock(Color.YELLOW));
        // 调用构造器设置courage
        world.add(new Location(4, 4), new BlusterCritter(2));
        world.show();
    }
}
