using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class MyException : System.Exception
{
    public MyException() { }
    public MyException(string message) : base(message) { }
}

public class DiskData : MonoBehaviour
{
    public int score;
    public float speedX;
    public float speedY;
}

public class DiskFactory : MonoBehaviour
{
    
    List<GameObject> used;
    List<GameObject> free;
    System.Random rand;

    // Start is called before the first frame update
    void Start()
    {
        used = new List<GameObject>();
        free = new List<GameObject>();
        rand = new System.Random();
    }

    public GameObject GetDisk(int round, bool isKinematic) {
        GameObject disk;
        if (free.Count != 0) {
            disk = free[0];
            free.Remove(disk);
        }
        else {
            disk = GameObject.Instantiate(Resources.Load("Prefabs/ufo", typeof(GameObject))) as GameObject;
            // 添加飞碟数据脚本
            disk.AddComponent<DiskData>();
        }
        // 关闭物理引擎的控制
        disk.GetComponent<Rigidbody>().isKinematic = true;
        //isKinematic为true，则不会受到物理系统的影响。如果为false，发生Rigidbody运动时则会受到物理系统的影响。

        //根据不同round设置DiskData的值
        //随意的旋转角度
        disk.transform.localEulerAngles = new Vector3(-rand.Next(20,40),0,0);
        DiskData diskData = disk.GetComponent<DiskData>();
        diskData.score = rand.Next(1,4);
        //由分数来决定速度、颜色、大小
        diskData.speedX = (3 + diskData.score + round) * 0.2f;
        diskData.speedY = (4 + diskData.score + round) * 0.2f;
        if (diskData.score == 3) {
            disk.transform.GetChild(0).gameObject.GetComponent<Renderer>().material.color = Color.red;
            disk.transform.localScale = new Vector3(0.35f,0.35f,0.35f);
        }
        else if (diskData.score == 2) {
            disk.transform.GetChild(0).gameObject.GetComponent<Renderer>().material.color = Color.green;
            disk.transform.localScale = new Vector3(0.42f,0.42f,0.42f);
        }
        else if (diskData.score == 1) {
            disk.transform.GetChild(0).gameObject.GetComponent<Renderer>().material.color = Color.blue;
            disk.transform.localScale = new Vector3(0.5f,0.5f,0.5f);
        }
        // 确定飞碟的起始位置和运动速度
        // 飞碟可从四个方向飞入（左上、左下、右上、右下）
        disk.transform.position = new Vector3(0, 0, 0);
        int direction = rand.Next(1,5);
        if (direction == 1) {
             // 左上
            disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth * 0.1f, Camera.main.pixelHeight * 1.1f, 10)));
            diskData.speedY *= -1;
        }
        else if (direction == 2) {
            // 左下
            disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth * 0.1f, Camera.main.pixelHeight * 0.1f, 10)));
        }
        else if (direction == 3) {
            // 右上
            disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth , Camera.main.pixelHeight * 1.1f, 10)));
            diskData.speedX *= -1;
            diskData.speedY *= -1;
        }
        else if (direction == 4) {
            // 右下
            disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth, -10f, 10)));
            diskData.speedX *= -1;
        } 
        // 如果使用物理学运动，飞碟从窗口中心移动
        if(!isKinematic){
            disk.transform.position = new Vector3(0, 0, 0);
            if(direction==1){
                disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth * 0.4f, Camera.main.pixelHeight * 0.74f, 10)));
            }else if(direction <=3){
                disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth * 0.50f, Camera.main.pixelHeight * 0.89f, 10)));
            }else{
                disk.transform.Translate(Camera.main.ScreenToWorldPoint(new Vector3(Camera.main.pixelWidth * 0.65f, Camera.main.pixelHeight * 0.83f, 10)));
            }
            
        } 
        // float dy = (float)rand.NextDouble(0,1);
        used.Add(disk);
        disk.SetActive(true);
        Debug.Log("generate disk");
        return disk;
    }

    // 通过回调函数回收飞碟，这样下次只需改变飞碟的属性就能重用
    public void FreeDisk(GameObject disk) {
        // 将飞碟隐藏
        disk.SetActive(false);
        //将位置和大小恢复到预制，这点很重要！
        disk.transform.position = new Vector3(0, 0, 0);
        disk.transform.localScale = new Vector3(1, 1, 1);
        if (!used.Contains(disk)) {
            throw new MyException("Try to remove a item from a list which doesn't contain it.");
        }
        Debug.Log("free disk");
        used.Remove(disk);
        free.Add(disk);
    }
}
