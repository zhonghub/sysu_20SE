# 作业3

① 请用三种方法以上方法，实现物体的抛物线运动。

（如，修改Transform属性，使用向量Vector3的方法）



**以水平初速度为v0=1的平抛运动为例：**

### 方法一 直接修改Transform属性

直接使用抛物线公式x=v0\*t,  y= -0.5 \* g\* t^2 在该时刻的坐标，修改Transform属性以实现抛物线运动

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Parabola1 : MonoBehaviour
{
    public float v0, g = 9.8f;
    public float t = 0;// 时间
    // Start is called before the first frame update
    void Start()
    {
        v0 = 1;
        this.transform.position = new Vector3(0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        t += Time.deltaTime;
        //直接使用抛物线公式x=v0*t,y=-0.5*g*t^2 在该时刻的取值修改Transform属性以实现抛物线运动
        this.transform.position = new Vector3(v0*t, -0.5f *g*t*t, 0); 
    }
}

```



### 方法二  使用向量Vector3的方法

将运动分解为x方向和y方向：
x方向：v0的匀速直线运动
y方向：初速度vy，加速g的匀加速直线运动,则平均速度为(vy + g * Time.deltaTime * 0.5f)

位移 = 平均速度*时间，利用了Vector3中的Vector3.right和Vector3.down这两个变量，在这两个方向上都加上对应的位移。

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Parabola2 : MonoBehaviour
{
    public float v0, vy, g = 9.8f;
    // Start is called before the first frame update
    void Start()
    {
        v0 = 1;
        vy = 0;
        this.transform.position = new Vector3(0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        float dt = Time.deltaTime;
        // 以平抛运动为例，将运动分解为x方向和y方向：
        // x方向v0的匀速直线运动
        transform.position += Vector3.right * dt * v0;
        // y方向,初速度vy，加速g的匀加速直线运动,则平均速度为(vy + g * Time.dt * 0.5f)
        transform.position += Vector3.down * dt * (vy + g * dt * 0.5f);
        vy += g * dt;// 经过dt的末速度
    }
}

```



### 方法三 使用Translate函数来改变坐标

通过计算得到一个变换矩阵mv( {dx,dy,0} )，然后调用Translate来进行变换：

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Parabola3 : MonoBehaviour
{
    public float v0, vy, g = 9.8f;
    // Start is called before the first frame update
    void Start()
    {
        v0 = 1;
        vy = 0;
        this.transform.position = new Vector3(0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        float dt = Time.deltaTime;
        float dx = v0 * dt;
        float dy = -dt * (vy + g * dt * 0.5f);
        Vector3 mv = new Vector3(dx, dy, 0);
        this.transform.Translate(mv);
        vy += g * Time.deltaTime;
    }
}

```

