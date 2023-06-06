import info.gridworld.grid.*;

/**
 * SparseGridNode is the basic structure of ArrayList in SparseGridNode
 */
public class SparseGridNode {

    private Object occupant;
    private int col;
    private SparseGridNode next;

    /**
     * Constructor
     * 
     * @param occupant the actor
     * @param col      the column number in grid
     * @param next     the pointer to next occupied grid node
     */
    public SparseGridNode(Object occupant, int col) {
        this.occupant = occupant;
        this.col = col;
        this.next = null;
    }

    /*
     * 如果使用按col的顺序插入，则可以在查找时可使用进行二分查找，
     * 但插入速率变慢
     */
    public SparseGridNode insertInOrder(SparseGridNode head) {
        if(head == null){
            this.setNext(null);
            head = this;
        }
        SparseGridNode p = head;
        SparseGridNode p2;
        while (p.next != null) {
            if (this.getCol() == p.getCol()) {
                return head;
            } else if (this.getCol() > p.getCol()) {
                p = p.getNext();
            } else {
                p2 = p.getNext();
                p.setNext(this);
                this.setNext(p2);
                return head;
            }
        }
        p.setNext(this);
        this.setNext(null);
        return head;
    }

    public SparseGridNode insertFirst(SparseGridNode head){
        this.setNext(head);
        head = this;
        return head;
    }

    public Object getOccupant() {
        return occupant;
    }

    public void setOccupant(Object occupant) {
        this.occupant = occupant;
    }

    public int getCol() {
        return col;
    }

    public void setCol(int col) {
        this.col = col;
    }

    public SparseGridNode getNext() {
        return next;
    }

    public void setNext(SparseGridNode next) {
        this.next = next;
    }

}