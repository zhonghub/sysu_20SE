using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TicTacToe : MonoBehaviour
{
    // counter记录棋盘上的棋子数（总步数）
    private int counter = 0;
    // turn记录当前玩家：1: X; -1: O.
    private int turn = 1;
    // turnResult记录上一回合的结果：2: 游戏继续; 0: 棋盘下满且无获胜者; 1: X获胜; -1: O获胜.
    private int turnResult = 2;
    // state记录棋盘状态
    private int [,]state = new int[3,3];
    // 棋盘布局如下：state[i,j]
    // (00,01,02) 
    // (10,11,12)
    // (20,21,22)

    // 重置棋盘及游戏状态
    private void reset(){
        turnResult = 2;
        counter = 0;
        turn = 1;
        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                state[i,j] = 0;
    }

    // 根据当前下的棋子state[i,j],判断并返回对局结果turnResult:
    // return 2: 游戏继续;
    // return 0: 棋盘下满且无获胜者;
    // return now: 当前的选手获胜;
    private int checkWinner(int i, int j){
        int now = state[i,j];
        // 判断(i,j)是否为在角线左上至右下
        if(i == j)
            if(state[(i+1)%3,(j+1)%3] == now && state[(i+2)%3,(j+2)%3] == now)
                return now;
        // 判断(i,j)是否在对角线左下至右上
        if(i+j == 2)
            if(state[(i+1)%3,(j+2)%3] == now && state[(i+2)%3,(j+1)%3] == now)
                return now;
        // 判断(i,j)所处的行和列
        if((state[i,(j+1)%3] == now && state[i,(j+2)%3] == now)||
            (state[(i+1)%3,j] == now && state[(i+2)%3,j] == now))
            return now;
        // 棋盘下满且无获胜者
        if(counter >= 9)
            return 0;
        // 游戏继续
        else
            return 2;
    }


    // Start is called before the first frame update
    void Start()
    {
        // 重置游戏
        reset();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnGUI()
    {   
        // 定义一个矩形区域作为背景：起点(0,0),宽1000，高500
        GUI.Box(new Rect(0,0,1000,500), "井字棋");
        // 当改按钮被按下时，开始新的对局，重置游戏
        if(GUI.Button(new Rect(550,130,200,50), "New game"))
		{
			reset();
		}

        // 根据上一回合结果turnResult输出相关信息：
		if (turnResult == 1) {
			GUI.Label (new Rect (330, 60, 150, 60), "玩家 X 获胜");
		} 
		else if (turnResult == -1) {
			GUI.Label (new Rect (330, 60, 150, 60), "玩家 O 获胜");
		} 
		else if (turnResult == 0) {
			GUI.Label (new Rect (270, 60, 150, 60), "棋盘下满且无获胜者");
		} 
        // 否则turnResult == 2，游戏继续
		else {
			if (turn == 1) {
				GUI.Label (new Rect (270, 60, 200, 60), "游戏继续! It's X's turn");
			}
			else if (turn == -1) {
				GUI.Label (new Rect (270, 60, 200, 60), "游戏继续! It's O's turn");
			}
		}

        // 用Button画出9个按钮作为棋盘
		for(int i = 0; i < 3; i++)
		{
			for(int j = 0; j < 3; j++)
			{   
				if (state[i, j] == 1)
                    // 表示被玩家X下了的位置
                    GUI.Button(new Rect(i * 100 + 200, j * 100 + 100, 100, 100), "X");
				else if (state[i, j] == -1)
                    // 表示被玩家O下了的位置
                    GUI.Button(new Rect(i * 100 + 200, j * 100 + 100, 100, 100), "O");
				else if(GUI.Button(new Rect(i * 100 + 200, j * 100 + 100, 100, 100), "")){
                    // 当空按钮被按下且游戏对局未结束时，代表当前回合的玩家在该位置下了，即令state[i, j] = turn
                    if(turnResult == 2)
					{   
                        // 该位置被当前玩家turn下了
						state[i, j] = turn;
                        // 步数+1
                        counter++;
                        // 获取这一步的游戏结果
                        turnResult = checkWinner(i,j);
                        // 转换游戏玩家
                        turn = -turn;
					}
                }
			}
		}
    }
}