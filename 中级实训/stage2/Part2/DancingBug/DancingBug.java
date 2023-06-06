import info.gridworld.actor.Bug;

public class DancingBug extends Bug {
    private int steps;
    private int sideLength;
    private int turns;// 记录转弯次数
    private int[] turnDegree;// 记录每次转弯的角度

    /**
     * Constructs a box bug that traces a square of a given side length
     * 
     * @param length the side length
     */
    public DancingBug(int length, int[] degree) {
        steps = 0;
        sideLength = length;
        turnDegree = degree.clone();
        turns = 0;// 记录转弯次数
    }

    /**
     * Moves to the next location of the square.
     */
    public void act() {
        if (steps < sideLength && canMove()) {
            move();
            steps++;
        } else {
            if (turns < turnDegree.length) {
                // turns对应第多少次转弯
                turns(turnDegree[turns]);
                turns++;
            } else {
                // 转弯完整个数组后又从头开始
                turns(turnDegree[0]);
                turns = 1;
            }
            steps = 0;
        }
    }

    private void turns(int n) {
        // 虫子连续旋转n个45度
        for (int i = 0; i < n; ++i) {
            turn();
        }
    }
}