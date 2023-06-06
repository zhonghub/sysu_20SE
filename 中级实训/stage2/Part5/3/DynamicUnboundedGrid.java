
/**
 * Consider an implementation of an unbounded grid 
 * in which all valid locations have non-negative row and column values. 
 * The constructor allocates a 16 x 16 array. 
 * When a call is made to the put method with a row or column index 
 * that is outside the current array bounds, 
 * double both array bounds until they are large enough, 
 * construct a new square array with those bounds, 
 * and place the existing occupants into the new array. 
 * Implement the methods specified by the Grid interface using this data structure. 
 * What is the Big-Oh efficiency of the get method? 
 * What is the efficiency of the put method 
 * when the row and column index values are within the current array bounds? 
 * What is the efficiency when the array needs to be resized?
 */

import info.gridworld.grid.*;

import java.util.*;

@SuppressWarnings("unchecked")

public class DynamicUnboundedGrid<E> extends AbstractGrid<E> {

    private Object[][] occupantArray;
    private final String positiveNumException = "cols/rows must be positive integer";
    // SIZE为默认rows/cols
    private final int SIZE = 16;
    private int rows;
    private int cols;

    /**
     * 默认构造器
     * 创建一个16*16大小的动态数组
     */
    public DynamicUnboundedGrid() {
        cols = SIZE;
        rows = SIZE;
        occupantArray = new Object[rows][cols];
    }

    /**
     * Constructs an empty unbounded grid with the initial col and row
     * 
     * @param rows number of rows in SparseBoundedGrid
     * @param cols number of columns in SparseBoundedGrid
     */
    public DynamicUnboundedGrid(int rows, int cols) {
        if (cols <= 0 || rows <= 0)
            throw new IllegalArgumentException(positiveNumException);
        this.cols = cols;
        this.rows = rows;
        occupantArray = new Object[rows][cols];
    }

    public int getNumRows() {
        return rows;
    }

    public int getNumCols() {
        return cols;
    }

    public boolean isValid(Location loc) {
        return 0 <= loc.getRow() && 0 <= loc.getCol();
    }

    /*
     * 和普通数组处理方法相同
     * 遍历网格并将网格中所有非空位置取出
     */
    public ArrayList<Location> getOccupiedLocations() {
        ArrayList<Location> locs = new ArrayList<Location>();
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                Location loc = new Location(r, c);
                if (get(loc) != null) {
                    locs.add(loc);
                }
            }
        }
        return locs;
    }

    /*
     * get方法处理逻辑和普通的数组处理相同
     */
    public E get(Location loc) {
        if (!isValid(loc)) {
            throw new IllegalArgumentException(getNotValidMessage(loc));
        }
        if (loc.getRow() >= rows || loc.getCol() >= cols) {
            return null;
        } else {
            return (E) occupantArray[loc.getRow()][loc.getCol()];
        }
    }

    /*
     * put方法处理逻辑:
     * 在没有超过当前网格界限时和普通的数组处理相同；
     * 否则需要先拓展网格，再将其加入到网格中
     */
    public E put(Location loc, E obj) {

        if (obj == null) {
            throw new NullPointerException("obj == null");
        }
        if (!isValid(loc)) {
            throw new IllegalArgumentException(getNotValidMessage(loc));
        }
        while (loc.getRow() >= rows || loc.getCol() >= cols) {
            doubleExpand();
        }
        E oldOccupant = get(loc);
        occupantArray[loc.getRow()][loc.getCol()] = obj;
        return oldOccupant;
    }

    /*
     * remove方法处理逻辑和普通数组相同
     */
    public E remove(Location loc) {

        if (!isValid(loc)) {
            throw new IllegalArgumentException(getNotValidMessage(loc));
        }
        if (loc.getRow() >= rows || loc.getCol() >= cols) {
            return null;
        } else {
            E oldOccupant = get(loc);
            occupantArray[loc.getRow()][loc.getCol()] = null;
            return oldOccupant;
        }
    }

    /**
     * 拓展网格数组
     * 方式：网格大小倍增，再将原网格拷贝到新网格
     * col * 2 and row * 2
     */
    private void doubleExpand() {
        Object[][] newArray = new Object[rows * 2][cols * 2];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                newArray[r][c] = occupantArray[r][c];
            }
        }
        occupantArray = newArray;
        cols *= 2;
        rows *= 2;
    }

    /*
     * 异常抛出信息：Location非法
     */
    public String getNotValidMessage(Location loc) {
        return "Location " + loc + " is not valid";
    }
}
