using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface ISceneController
{
    //加载场景资源
    void LoadResources();
}

public interface IUserAction                          
{
    //移动玩家
    void MovePlayer(float translationX, float translationZ, Vector3 mousePosition);
    //得到分数
    int GetScore();
    //得到目标
    int GetTarget();
    //得到游戏结束标志
    bool GetGameover();
    //是否获胜
    bool isWin();
    //重新开始并设置目标分数
    void Restart(int t);
    // 设置目标分数
    void setTarget(int t);
}

public interface ISSActionCallback
{
    void SSActionEvent(SSAction source,int intParam = 0,GameObject objectParam = null);
}

public interface IGameStatusOp
{
    void PlayerEscape();
    void PlayerGameover();
}
