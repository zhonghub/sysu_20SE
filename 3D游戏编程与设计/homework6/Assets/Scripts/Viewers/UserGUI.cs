using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserGUI : MonoBehaviour
{
    public int mode;
    public int score;
    public int round;
    public bool isKinematic = true; // true运动学/flase物理学
    private string gameState;
    private IUserAction action;
    public GUIStyle bigStyle, blackStyle, smallStyle;//自定义字体格式
    public Font pixelFont;
    private int menu_width = Screen.width / 5, menu_height = Screen.width / 10;//主菜单每一个按键的宽度和高度
    // Start is called before the first frame update
    void Start()
    {
        mode = 0;
        gameState = "待选择(默认运动学)";
        action = SSDirector.getInstance().currentSceneController as IUserAction;
        
        //大字体初始化
        bigStyle = new GUIStyle();
        bigStyle.normal.textColor = Color.white;
        bigStyle.normal.background = null;
        bigStyle.fontSize = 50;
        bigStyle.alignment=TextAnchor.MiddleCenter;

        //black
        blackStyle = new GUIStyle();
        blackStyle.normal.textColor = Color.black;
        blackStyle.normal.background = null;
        blackStyle.fontSize = 50;
        blackStyle.alignment=TextAnchor.MiddleCenter;

        //小字体初始化
        smallStyle = new GUIStyle();
        smallStyle.normal.textColor = Color.white;
        smallStyle.normal.background = null;
        smallStyle.fontSize = 20;
        smallStyle.alignment=TextAnchor.MiddleCenter;
        
    }

    // Update is called once per frame
    void Update()
    {

    }

    void OnGUI() {
        //GUI.skin.button.font = pixelFont;
        GUI.Label(new Rect(Screen.width / 2 - 100f,0,200,50), "游戏模式："+gameState, smallStyle);
        GUI.skin.button.fontSize = 28;
        switch(mode) {
            case 0:
                mainMenu();
                break;
            case 1:
                GameStart();
                break;
            
        }
        if(action.isGameOver()){
            GUI.Label(new Rect(Screen.width/2, 60, 50, 200), "Game Over!", bigStyle);
            if (GUI.Button(new Rect(Screen.width / 2 - 100, Screen.width / 2 - 200, 200, 50), "重新开始"))
            {
                action.Restart();
                return;
            }
        }       
    }

    void mainMenu() {
        GUI.Label(new Rect(Screen.width / 2 - menu_width * 0.5f, Screen.height * 0.1f, menu_width, menu_height), "Hit UFO", bigStyle);
        if (GUI.Button(new Rect(Screen.width / 2 - menu_width*0.7f, Screen.height * 0.35f, menu_width *0.69f, menu_height), "运动学")) {
            isKinematic = true;
            gameState = "运动学";
        }
        if (GUI.Button(new Rect(Screen.width / 2 ,  Screen.height * 0.35f, menu_width*0.69f, menu_height), "物理学")) {
            isKinematic = false;
            gameState = "物理学";
        }
        bool button = GUI.Button(new Rect(Screen.width / 2 - menu_width * 0.5f, Screen.height * 4 / 7, menu_width, menu_height), "Start");
        if (button) {
            mode = 1;
        }    
    }

    void GameStart() {
        GUI.Label(new Rect(0,0,100,50), "Score: " + score, smallStyle);
        GUI.Label(new Rect(Screen.width-120,0,100,50), "Round: " + round, smallStyle);
    }
}
