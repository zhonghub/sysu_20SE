import info.gridworld.actor.Bug;

public class ZBug extends Bug {
    private int steps;
    private int sideLength;
    private int turns;// 记录转弯次数

    /**
     * Constructs a box bug that traces a square of a given side length
     * 
     * @param length the side length
     */
    public ZBug(int length) {
        steps = 0;
        sideLength = length;
        turns = 0;// 记录转弯次数
        // 首先将虫子转到正东方向
        turns(2);
    }

    /**
     * Moves to the next location of the square.
     */
    public void act() {
        if (sideLength == 0) {
            // 结束了,虫子不会再移动
            return;
        } else if (steps < sideLength && canMove()) {
            move();
            steps++;
        } else {
            if (turns == 0) {
                // 第一次转弯
                turns(3);
                turns++;
            } else if (turns == 1) {
                // 第二次转弯
                turns(5);
                turns++;
            } else if (turns == 2) {
                // 结束，虫子停止
                sideLength = 0;
                return;
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