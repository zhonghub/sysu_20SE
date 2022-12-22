using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//飞碟从界面左右两侧飞入，离开界面时运动结束
public class CCFlyAction : SSAction
{
    public float speedX;
    public float speedY;
    public static CCFlyAction GetSSAction(float x, float y) {
        CCFlyAction action = ScriptableObject.CreateInstance<CCFlyAction>();
        action.speedX = 2 * x;
        action.speedY = 2 * y;
        return action;
    }

    public override void Start() { }

    // Update is called once per frame
    public override void Update()
    {
        //飞碟已经被点击，通过回调函数回收飞碟
        if (this.transform.gameObject.activeSelf == false) {
            this.destroy = true;
            // 通过回调函数回收飞碟
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
        // 运动学运动
        transform.position += new Vector3(speedX, speedY, 0) * Time.deltaTime;
    }
}
