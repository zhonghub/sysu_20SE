import info.gridworld.grid.*;
import java.util.ArrayList;

@SuppressWarnings("unchecked")
/**
 * Suppose that a program requires a very large bounded grid that contains very
 * few objects and that the program frequently calls the getOccupiedLocations
 * method (as, for example, ActorWorld). Create a class SparseBoundedGrid that
 * uses a “sparse array” implementation. Your solution need not be a generic
 * class; you may simply store occupants of type Object.The “sparse array” is an
 * array list of linked lists. Each linked list entry holds both a grid occupant
 * and a column index.Each entry in the array list is a linked list or is null
 * if that row is empty.You may choose to implement the linked list in one of
 * two ways. You can use raw list nodes.
 */

public class SparseBoundedGrid<E> extends AbstractGrid<E> {

    private SparseGridNode[] occupantArray;
    private int rows;
    private int cols;
    private final String positiveNumException = "cols/rows must be positive integer";

    /**
     * Constructs an empty bounded grid with the given dimensions
     * 
     * @param rows number of rows in SparseBoundedGrid
     * @param cols number of columns in SparseBoundedGrid
     */
    public SparseBoundedGrid(int rows, int cols) {
        if (cols <= 0 || rows <= 0)
            throw new IllegalArgumentException(positiveNumException);

        this.cols = cols;
        this.rows = rows;
        occupantArray = new SparseGridNode[rows];
    }

    public int getNumRows() {
        return rows;
    }

    public int getNumCols() {
        return cols;
    }

    public boolean isValid(Location loc) {
        return 0 <= loc.getRow() && loc.getRow() < getNumRows()
                && 0 <= loc.getCol() && loc.getCol() < getNumCols();
    }

    public ArrayList<Location> getOccupiedLocations() {
        ArrayList<Location> locations = new ArrayList<Location>();
        for (int i = 0; i < rows; i++) {
            SparseGridNode nodePtr = occupantArray[i];
            while (nodePtr != null) {
                locations.add(new Location(i, nodePtr.getCol()));
                nodePtr = nodePtr.getNext();
            }
        }
        return locations;
    }

    public E get(Location loc) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));

        SparseGridNode nodePtr = occupantArray[loc.getRow()];
        while (nodePtr != null) {
            if (nodePtr.getCol() == loc.getCol()) {
                return (E) nodePtr.getOccupant();
            }
            nodePtr = nodePtr.getNext();
        }
        return null;
    }

    public E put(Location loc, E obj) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));
        if (obj == null)
            throw new NullPointerException("obj == null");
        E oldOccupant = remove(loc);
        SparseGridNode headPtr = occupantArray[loc.getRow()];
        SparseGridNode newNode = new SparseGridNode(obj, loc.getCol());
        occupantArray[loc.getRow()] = newNode.insertFirst(headPtr);
        return oldOccupant;
    }

    /*
     * 分情况从链表中删除节点,并返回删除的节点的对象
     */
    public E remove(Location loc) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));
        SparseGridNode headPtr = occupantArray[loc.getRow()];
        if (headPtr == null) {
            return null;
        }
        if (headPtr.getCol() == loc.getCol()) {
            occupantArray[loc.getRow()] = headPtr.getNext();
            return (E) headPtr.getOccupant();
        } else {
            SparseGridNode p = headPtr;
            while (p.getNext() != null) {
                SparseGridNode p1 = p.getNext();
                if (p1.getCol() == loc.getCol()) {
                    p.setNext(p1.getNext());
                    return (E) p1.getOccupant();
                } else {
                    p = p1;
                }
            }
            return null;
        }

    }

    public String getNotValidMessage(Location loc) {
        return "Location " + loc + " is not valid";
    }

}
