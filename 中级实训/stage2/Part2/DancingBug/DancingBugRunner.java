import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.Location;
import info.gridworld.grid.UnboundedGrid;
import info.gridworld.actor.Actor;

import java.awt.Color;

/**
 * This class runs a world that contains box bugs. <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class DancingBugRunner 
{
    public static void main(String[] args)
    {
        // 网格
        ActorWorld world = new ActorWorld(new UnboundedGrid<Actor>());
        // 每次旋转的角度    
        final int [] degree = {1,2,3,6,2,1};
        // 通过边长和每次旋转的角度进行初始化
        DancingBug alice = new DancingBug(4,degree);
        // 将虫子添加到网格
        world.add(new Location(15, 15), alice);
        world.show();
    }
}