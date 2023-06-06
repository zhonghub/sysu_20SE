import info.gridworld.actor.ActorWorld;
import info.gridworld.actor.Flower;
import info.gridworld.actor.Rock;
import info.gridworld.grid.Location;

/**
 * This class runs a world that contains a Jumper, two Rock and two Flower,
 * added at random locations. Click on empty locations to add additional actors.
 * Click on populated locations to invoke methods on their occupants. <br />
 * To build your own worlds, define your own actors and a runner class. See the
 * JumperRunner (in the Jumper folder) for an example. <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class JumperRunner {
	public static void main(String[] args) {
		// 初始化网格
		ActorWorld world = new ActorWorld();
		// 实例化Jumper
		Jumper jumper = new Jumper();
		// 将jumper添加到网格
		world.add(new Location(3, 4), jumper);
		// 设置方向
		jumper.setDirection(Location.EAST);
		// 添加Flower
		// 可以越过Flower,且能占据Flower所在的网格
		world.add(new Location(9, 4), new Flower());
		world.add(new Location(9, 5), new Flower());
		// 添加Rock
		// 只能越过Rock，不能占据Rock所在网格
		world.add(new Location(3, 6), new Rock());
		world.add(new Location(4, 5), new Rock());
		world.show();
	}
}
