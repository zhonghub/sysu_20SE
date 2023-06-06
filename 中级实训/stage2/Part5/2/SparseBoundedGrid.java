
/**
 * Consider using a HashMap or TreeMap to implement the SparseBoundedGrid. 
 * How could you use the UnboundedGrid class to accomplish this task? 
 * Which methods of UnboundedGrid could be used without change? 
 * Fill in the following chart to compare the expected Big-Oh efficiencies 
 * for each implementation of the SparseBoundedGrid.
 */

import info.gridworld.grid.*;

import java.util.*;

public class SparseBoundedGrid<E> extends AbstractGrid<E> {

    /*
     * 使用HashMap进行哈希映射：位置Location->对象E
     */
    private Map<Location, E> occupantMap;

    private int rows;
    private int cols;
    /*
     * 自定义的异常抛出信息
     */
    private final String locNullWarning = "loc == null";
    private final String objNullWarning = "obj == null";
    private final String negativeNumWarning = "cols/rows must be greater than 0";

    /*
     * 构造器
     */
    public SparseBoundedGrid(int rows, int cols) {
        if (cols <= 0 || rows <= 0)
            throw new IllegalArgumentException(negativeNumWarning);
        this.cols = cols;
        this.rows = rows;
        occupantMap = new HashMap<Location, E>();
    }

    public int getNumRows() {
        return rows;
    }

    public int getNumCols() {
        return cols;
    }

    public boolean isValid(Location loc) {
        return 0 <= loc.getRow() && loc.getRow() < getNumRows() && 0 <= loc.getCol() && loc.getCol() < getNumCols();
    }

    /*
     * 取出HashMap中的keySet(Location),将其转化为ArrayList
     */
    public ArrayList<Location> getOccupiedLocations() {
        ArrayList<Location> locs = new ArrayList<Location>();
        for (Location loc : occupantMap.keySet()) {
            locs.add(loc);
        }
        return locs;
    }

    /*
     * 使用HashMap中的get操作
     */
    public E get(Location loc) {
        if (loc == null)
            throw new NullPointerException(locNullWarning);
        return occupantMap.get(loc);
    }

    /*
     * 使用HashMap中的put操作
     */
    public E put(Location loc, E obj) {
        if (loc == null){
            throw new NullPointerException(locNullWarning);
        }
        if (obj == null){
            throw new NullPointerException(objNullWarning);
        }
        return occupantMap.put(loc, obj);
    }

    /*
     * 使用HashMap中的remove操作
     */
    public E remove(Location loc) {
        if (loc == null)
            throw new NullPointerException(locNullWarning);
        return occupantMap.remove(loc);
    }

}
