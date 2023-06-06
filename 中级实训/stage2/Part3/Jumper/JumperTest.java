import static org.junit.Assert.assertEquals;
import org.junit.Test;
import org.junit.Before;

import info.gridworld.grid.Location;
import info.gridworld.actor.Rock;
import info.gridworld.actor.Flower;
import info.gridworld.actor.ActorWorld;

public class JumperTest {

	private ActorWorld world;
	private Jumper jumper;
	private Jumper jumper2;
	private Rock rock;
	private Flower flower;

	public JumperTest() {
		// 有界网格:10*10
		// 初始化网格和Actor
		world = new ActorWorld();
		jumper = new Jumper();
		jumper2 = new Jumper();
		rock = new Rock();
		flower = new Flower();
		// 将Actor添加到网格
		world.add(new Location(1, 1), jumper);
		world.add(new Location(1, 2), jumper2);
		world.add(new Location(1, 3), rock);
		world.add(new Location(1, 4), flower);
	}

	// 每次测试前都将所有actor移到初始位置
	@Before
	public void before() {
		jumper.moveTo(new Location(1, 1));
		jumper2.moveTo(new Location(1, 2));
		rock.moveTo(new Location(1, 3));
		flower.moveTo(new Location(1, 4));
	}

	// 测试Jumper(2,2)是否能跳2格，答案是YES
	@Test
	public void testJumpTwoCells() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		jumper.act();
		// 判断是否成功地跳到了2格
		assertEquals(4, jumper.getLocation().getCol());
	}

	// 测试Jumper(2,2)是否能跳过一个空位置(2,3)上，答案是YES
	@Test
	public void testJumpOverEmpty() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		// 判断能否跳过(2,3)
		assertEquals(true, jumper.canJump());
	}

	// 测试Jumper(2,2)是否能跳过Rock(2,3)上,答案是YES
	@Test
	public void testCanJumpOverRock() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		rock.moveTo(new Location(2, 3));
		assertEquals(true, jumper.canJump());
	}

	// 测试Jumper(2,2)是否能跳过flower(2,3)上,答案是YES
	@Test
	public void testCanJumpOverFlower() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		flower.moveTo(new Location(2, 3));
		assertEquals(true, jumper.canJump());
	}

	// 测试Jumper(2,2)是否能跳过jumper2(2,3)上,答案是NO
	@Test
	public void testCanJumpOverJumper() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		jumper2.moveTo(new Location(2, 3));
		assertEquals(false, jumper.canJump());
	}

	// 测试Jumper(2,2)是否能跳到一个Rock(2,4)上，答案是NO
	@Test
	public void testCanJumpToRock() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		rock.moveTo(new Location(2, 4));
		assertEquals(false, jumper.canJump());
	}

	// 测试Jumper(3,4)是否能跳到一个jumper2(2,4)上，答案是NO
	@Test
	public void testCanJumpToJumper() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		jumper2.moveTo(new Location(2, 4));
		assertEquals(false, jumper.canJump());
	}

	// 测试Jumper(2,2)是否能跳到一个flower(2,4)上，答案是YES
	@Test
	public void testCanJumpToFlower() {
		jumper.moveTo(new Location(2, 2));
		jumper.setDirection(Location.EAST);
		flower.moveTo(new Location(2, 4));
		assertEquals(true, jumper.canJump());
	}

	// 测试Jumper(2,9)是否能跳到网格外(2,11)上，答案是NO
	@Test
	public void testCanJumpToNotValid() {
		jumper.moveTo(new Location(2, 9));
		jumper.setDirection(Location.EAST);
		assertEquals(false, jumper.canJump());
	}

	// 测试Jumper(3,4)是否能跳到正确的位置(5,6)，答案是YES
	@Test
	public void testCanJumpToRightPlace() {
		jumper.moveTo(new Location(3, 4));
		jumper.setDirection(Location.EAST);
		rock.moveTo(new Location(3, 6));
		// 再执行一次act,向右旋转45度,前进2格
		jumper.act();
		assertEquals(Location.SOUTHEAST, jumper.getDirection());
		assertEquals(5, jumper.getLocation().getRow());
		assertEquals(6, jumper.getLocation().getCol());
	}

}
