import info.gridworld.actor.Actor;
import info.gridworld.actor.Critter;
import info.gridworld.grid.Location;
import info.gridworld.grid.Grid;

import java.util.ArrayList;
import java.awt.Color;
import java.util.HashSet;

/**
 * A <code>BlusterCritter</code> takes on the color of neighboring actors as
 * it moves through the grid. <br />
 * The implementation of this class is testable on the AP CS A and AB exams.
 */
public class BlusterCritter extends Critter {
    // 变暗的系数
    private final double DARKENING_FACTOR = 0.25d;
    private int courage;

    public BlusterCritter(int c) {
        super();
        setColor(new Color(200, 0, 0));
        courage = c;
    }

    /**
     * 
     * @return a list of Critters
     *         返回一个周围24个格子里其它Critter的list
     */
    public ArrayList<Actor> getActors() {
        ArrayList<Actor> actors = new ArrayList<Actor>();
        Grid gr = getGrid();
        int x0 = getLocation().getRow();
        int y0 = getLocation().getCol();
        for (int i = -2; i <= 2; ++i) {
            for (int j = -2; j <= 2; ++j) {
                Location loc1 = new Location(x0 + i, y0 + j);
                if (gr.isValid(loc1)) {
                    Actor a = getGrid().get(loc1);
                    if (a != null && a != this) {
                        actors.add(a);
                    }
                }
            }
        }
        return actors;
    }

    /**
     * 根据周围24个格子里其它Critter的数量进行颜色变化
     */
    public void processActors(ArrayList<Actor> actors) {
        int n = 0;
        for (Actor a : actors) {
            if (a instanceof Critter) {
                n++;
            }
        }
        if (n < courage) {
            colorChange(DARKENING_FACTOR);
        } else {
            colorChange(-DARKENING_FACTOR);
        }
        return;
    }

    /**
     * 参考Flower中的act方法，写出一个颜色变化的方法
     * i>0颜色变亮；i<0颜色变暗
     */
    public void colorChange(double i) {
        Color c = getColor();
        int red = getChangedColor(c.getRed(), i);
        setColor(new Color(red, 0, 0));
    }

    /*
     * 防止颜色越界,且不能让颜色变为0，颜色变化范围10-255
     */
    public int getChangedColor(int color0, double i) {
        int color = (int) (color0 * (1 + i));
        color = ((color < 10) ? 10 : color);
        return ((color < 255) ? color : 255);
    }
}
