using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PhysicFlyAction : SSAction
{
    public float speedX;
    public float speedY;
    public static PhysicFlyAction GetSSAction(float x, float y) {
        PhysicFlyAction action = ScriptableObject.CreateInstance<PhysicFlyAction>();
        action.speedX = x * 2;
        action.speedX = y * 8;
        return action;
    }
    // Start is called before the first frame update
    public override void Start()
    {
        // Rigidbody,运动将受到 Unity 物理引擎的控制
        gameObject.GetComponent<Rigidbody>().isKinematic = false;
        // 速度矢量
        gameObject.GetComponent<Rigidbody>().velocity = new Vector3(speedX, speedY, 0);
        // 使用重力
        gameObject.GetComponent<Rigidbody>().useGravity = true;
        // 阻力为0
        gameObject.GetComponent<Rigidbody>().drag = 0;
    }

    // Update is called once per frame
    public override void Update()
    {
        //飞碟已经被点击，通过回调函数回收飞碟
        if (this.transform.gameObject.activeSelf == false) {
            this.destroy = true;
            this.callback.SSActionEvent(this);
            return;
        }
        // 如果飞碟超出摄像机的范围，通过回调函数回收飞碟
        Vector3 vec3 = Camera.main.WorldToScreenPoint (this.transform.position);
        if (vec3.x < -200 || vec3.x > Camera.main.pixelWidth + 200 || vec3.y < -200 || vec3.y > Camera.main.pixelHeight + 200) {
            this.destroy = true;
            this.callback.SSActionEvent(this);
            return;
        }
    }
}

