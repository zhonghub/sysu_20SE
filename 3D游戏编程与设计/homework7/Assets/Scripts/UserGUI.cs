using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserGUI : MonoBehaviour {

    private IUserAction action;
    private GUIStyle score_style = new GUIStyle();
    private GUIStyle text_style = new GUIStyle();
    private GUIStyle over_style = new GUIStyle();
    public  int show_time = 8;                         //展示提示的时间长度
    public static int target = 50;                            //目标得分
    public GameObject inputtext;
    void Start ()
    {
        action = SSDirector.GetInstance().CurrentScenceController as IUserAction;
        text_style.normal.textColor = new Color(1, 0, 0, 1);
        text_style.fontSize = 16;
        score_style.normal.textColor = new Color(1,0.92f,0.016f,1);
        score_style.fontSize = 16;
        over_style.fontSize = 25;
        //展示提示
        StartCoroutine(ShowTip());
    }

    void Update()
    {
        action.setTarget(target);
        //获取方向键的偏移量
        float translationX = Input.GetAxis("Horizontal");
        float translationZ = Input.GetAxis("Vertical");
        //获取鼠标位置
        Vector3 mousePosition = Input.mousePosition;
        //移动玩家
        action.MovePlayer(translationX, translationZ, mousePosition);
    }

    private void OnGUI()
    {
        GUI.Label(new Rect(10, 5, 200, 50), "分数:", text_style);
        GUI.Label(new Rect(55, 5, 200, 50), action.GetScore().ToString(), score_style);
        GUI.Label(new Rect(Screen.width - 130, 5, 50, 50), "目标", text_style);
        GUI.Label(new Rect(Screen.width - 80, 5, 50, 50), action.GetTarget().ToString(), score_style);
        if(action.GetGameover() && !action.isWin())
        {
            GUI.Label(new Rect(Screen.width / 2 - 50, Screen.width / 2 - 250, 100, 50), "游戏结束", over_style);
            setBtns();
        }
        else if(action.isWin())
        {
            GUI.Label(new Rect(Screen.width / 2 - 50, Screen.width / 2 - 250, 100, 50), "恭喜胜利！", over_style);
            setBtns();
        }
        if(show_time > 0)
        {
            GUI.Label(new Rect(Screen.width / 2 - 180 ,10, 150, 100), "按WSAD或方向键移动,使用鼠标控制方向", text_style);
            GUI.Label(new Rect(Screen.width / 2 - 180, 30, 100, 100), "成功躲避巡逻兵追捕加1分", text_style);
            GUI.Label(new Rect(Screen.width / 2 - 180, 50, 100, 100), "达到目标分数即可获胜", text_style);
        }
    }

    public IEnumerator ShowTip()
    {
        while (show_time >= 0)
        {
            yield return new WaitForSeconds(1);
            show_time--;
        }
    }

    public void setBtns(){
        GUI.Label(new Rect(Screen.width / 2 - 230, Screen.width / 2 - 70, 100, 50), "设置目标分数:", text_style);
        if (GUI.Button(new Rect(Screen.width / 2 - 50 , Screen.width / 2 - 120, 100, 40), "30")){
            target = 30;
        }
        if (GUI.Button(new Rect(Screen.width / 2 + 50, Screen.width / 2 - 120, 100, 40), "50")){
            target = 50;
        }
        if (GUI.Button(new Rect(Screen.width / 2  - 50, Screen.width / 2 - 80, 100, 40), "100")){
            target = 100;
        }
        if (GUI.Button(new Rect(Screen.width / 2 + 50, Screen.width / 2 - 80, 100, 40), "200")){
            target = 200;
        }
        if (GUI.Button(new Rect(Screen.width / 2 - 50, Screen.width / 2 - 200, 100, 50), "重新开始"))
        {
            action.Restart(target);
            return;
        }
    }
}
