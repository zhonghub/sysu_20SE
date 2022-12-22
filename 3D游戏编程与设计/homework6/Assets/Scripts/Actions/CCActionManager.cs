using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CCActionManager : SSActionManager, IActionCallback, IActionManager
{
    public RoundController sceneController;
    public CCFlyAction action;
    public DiskFactory factory;
    
    // Start is called before the first frame update
    protected new void Start()
    {
        sceneController = (RoundController)SSDirector.getInstance().currentSceneController;
        sceneController.actionManager = this;
        factory = Singleton<DiskFactory>.Instance;
    }

    // 回调函数回收飞碟
    public void SSActionEvent(SSAction source,
        SSActionEventType events = SSActionEventType.Completed,
        int intParam = 0,
        string strParam = null,
        Object objectParam = null) {
            factory.FreeDisk(source.transform.gameObject);
    }

    public void MoveDisk(GameObject disk) {
        // 调用运动学运动
        action = CCFlyAction.GetSSAction(disk.GetComponent<DiskData>().speedX, disk.GetComponent<DiskData>().speedY);
        RunAction(disk, action, this);

    }

}
