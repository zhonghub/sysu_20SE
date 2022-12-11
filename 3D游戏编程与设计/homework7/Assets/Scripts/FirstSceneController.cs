using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class FirstSceneController : MonoBehaviour, IUserAction, ISceneController
{
    public PropFactory patrol_factory;                               //巡逻者工厂
    public PatrolActionManager action_manager;                       //运动管理器
    public int wall_sign = -1;                                       //当前玩家所处哪个格子
    public GameObject player;                                        //玩家
    public Camera main_camera;                                       //主相机
    public float player_speed = 5;                                  //玩家移动速度
    public float rotate_speed = 135f;                                //玩家旋转速度
    private List<GameObject> patrols;                                //场景中巡逻者列表
    public int target = 50;                                          //目标得分
    public int score = 0;                                          //当前得分
    private bool game_over = false;                                  //游戏结束

    void Update()
    {
        if(player_speed <= 6){
            player_speed += 0.0005f;
        }
        for (int i = 0; i < patrols.Count; i++)
        {
            patrols[i].gameObject.GetComponent<PatrolData>().wall_sign = wall_sign;
        }
        // 达到目标分数
        if(isWin())
        {
            Gameover();
        }
    }
    
    void Start()
    {
        SSDirector director = SSDirector.GetInstance();
        director.CurrentScenceController = this;
        patrol_factory = Singleton<PropFactory>.Instance;
        action_manager = gameObject.AddComponent<PatrolActionManager>() as PatrolActionManager;
        LoadResources();
        main_camera.GetComponent<CameraFlow>().follow = player;
        score = 0;
    }

    public void LoadResources()
    {
        Instantiate(Resources.Load<GameObject>("Prefabs/Plane"));
        player = Instantiate(Resources.Load("Prefabs/Player"), new Vector3(0, 9, 0), Quaternion.identity) as GameObject;
        patrols = patrol_factory.CreatPatrols();
        //所有侦察兵移动
        for (int i = 0; i < patrols.Count; i++)
        {
            action_manager.GoPatrol(patrols[i]);
        }
    }

    //玩家移动
    public void MovePlayer(float translationX, float translationZ, Vector3 mousePosition)
    {
        if(!game_over)
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            //Debug.Log(ray);
            RaycastHit hitInfo;
            if(Physics.Raycast(ray, out hitInfo)){
                Vector3 target = hitInfo.point;
                //Debug.Log(target);
                target.y = player.transform.position.y;
                player.transform.LookAt(target);
            }

            if (translationX != 0 || translationZ != 0)
            {
                
                player.GetComponent<Animator>().SetBool("run", true);
            }
            else
            {
                player.GetComponent<Animator>().SetBool("run", false);
            }
            //移动和旋转
            player.transform.Translate(translationX * player_speed * Time.deltaTime, 0, translationZ * player_speed * Time.deltaTime); 
        }
    }

    public int GetScore()
    {
        return score;
    }

    public int GetTarget()
    {
        return target;
    }

    public void setTarget(int t){
        target = t;
    }

    public bool GetGameover()
    {
        return game_over;
    }

    public bool isWin(){
        return score >= target;
    }

    public void Restart(int t)
    {
        SceneManager.LoadScene("Scenes/mySence");
        target = t;
    }

    void OnEnable()
    {
        GameEventManager.ScoreChange += AddScore;
        GameEventManager.GameoverChange += Gameover;
    }
    void OnDisable()
    {
        GameEventManager.ScoreChange -= AddScore;
        GameEventManager.GameoverChange -= Gameover;
    }

    void AddScore()
    {
        score++;
    }
    void Gameover()
    {
        game_over = true;
        patrol_factory.StopPatrol();
        action_manager.DestroyAllAction();
    }
}
