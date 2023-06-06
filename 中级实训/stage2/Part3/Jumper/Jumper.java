import info.gridworld.actor.Actor;
import info.gridworld.actor.Rock;
import info.gridworld.actor.Flower;
import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;

import java.awt.Color;

public class Jumper extends Actor {
	/**
	 * Constructs a blue jumper.
	 */
	public Jumper() {
		setColor(Color.RED);
	}

	/**
	 * Constructs a jumper of a given color.
	 * 
	 * @param jumperColor the color for this jumper
	 */
	public Jumper(Color jumperColor) {
		setColor(jumperColor);
	}

	/**
	 * Jumps if it can jump, turn until it can jump otherwise.
	 */
	public void act() {
		// 当不能jump的时候一直转弯turn，直到能jump
		while(!canJump()){
			turn();
		}
		jump();
	}

	/**
	 * Turns the Jumper 45 degrees to the right without changing its location.
	 */
	public void turn() {
		setDirection(getDirection() + Location.HALF_RIGHT);
	}

	/**
	 * Moves the Jumper forward, putting nothing into the location it previously
	 * occupied.
	 */
	public void jump() {
		Grid<Actor> gr = getGrid();
		if (gr == null)
			return;
		Location loc = getLocation();
		Location loc1 = loc.getAdjacentLocation(getDirection());
		Location loc2 = loc1.getAdjacentLocation(getDirection());
		if (gr.isValid(loc2))
			moveTo(loc2);
		else
			removeSelfFromGrid();
	}

	/**
	 * Tests whether this Jumper can move forward into a location that is empty
	 * 
	 * @return true if this Jumper can move.
	 */
	public boolean canJump() {
		Grid<Actor> gr = getGrid();
		if (gr == null)
			return false;
		Location loc = getLocation();
		Location loc1 = loc.getAdjacentLocation(getDirection());
		Location loc2 = loc1.getAdjacentLocation(getDirection());
		if (!gr.isValid(loc2))
			return false;
		Actor neighbor1 = gr.get(loc1);
		// 只能跳过空格子、Rock、Flower
		if (!((neighbor1 == null) || (neighbor1 instanceof Flower) || (neighbor1 instanceof Rock)))
			return false;
		Actor neighbor2 = gr.get(loc2);
		// 可以跳到空格子、Flower
		return ((neighbor2 == null) || (neighbor2 instanceof Flower));
		// ok to move into empty location
		// not ok to move onto any other actor
	}
}
