import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.Location;

import java.awt.Color;

public class CircleBugRunner
{
    public static void main(String[] args)
    {
        // 初始化网格
        ActorWorld world = new ActorWorld();
        // 初始化虫子1
        CircleBug alice = new CircleBug(6);
        // 设置虫子1的颜色
        alice.setColor(Color.ORANGE);
        // 初始化虫子2
        CircleBug bob = new CircleBug(6);
        // 将虫子加入网格中的某个位置
        world.add(new Location(7, 8), alice);
        world.add(new Location(5, 5), bob);
        world.show();
    }
}