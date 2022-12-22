using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Threading;

public class RoundController : MonoBehaviour, ISceneController, IUserAction
{
    int round = 0;
    int max_round = 5;
    int ufo_num;
    float timer = 0.5f;
    int score;
    GameObject disk;
    DiskFactory factory;
    public IActionManager actionManager;
    public UserGUI userGUI;
    // Start is called before the first frame update
    void Start()
    {
        SSDirector director = SSDirector.getInstance();
        director.currentSceneController = this;
        gameObject.AddComponent<UserGUI>();
        gameObject.AddComponent<DiskFactory>();
        gameObject.AddComponent<CCActionManager>();
        gameObject.AddComponent<PhysicActionManager>();
        actionManager = gameObject.GetComponent<CCActionManager>() as IActionManager;
        factory = Singleton<DiskFactory>.Instance;
        userGUI =  gameObject.GetComponent<UserGUI>();
    }

    // Update is called once per frame
    void Update()
    {
        if (userGUI.mode == 0) return;
        if (userGUI.isKinematic == false) {
            // 物理学
            actionManager = gameObject.GetComponent<PhysicActionManager>() as IActionManager;
            ufo_num = 6;
        }
        else {
            // 运动学
            actionManager = gameObject.GetComponent<CCActionManager>() as IActionManager;
            ufo_num = 10;
        }
        GetHit();
        if (round >= max_round) {
            return;
        }
        timer -= Time.deltaTime;
        if (timer <= 0 && actionManager.GetActionCount() == 0) {
            //从工厂中得到ufo_num个飞碟，为其加上动作
            for (int i = 0; i < ufo_num; ++i) {
                disk = factory.GetDisk(round, userGUI.isKinematic);
                actionManager.MoveDisk(disk);
            }
            round += 1;
            if (round <= max_round) {
                userGUI.round = round;
            }
            timer = 4.0f;
        }
        
    }

    public bool isGameOver(){
        return (round >= max_round && actionManager.GetActionCount() == 0);
    }

    public void Restart(){
        SceneManager.LoadScene("Scenes/hitUFO");
    }

    // 判断飞碟是否被鼠标点击，如果被点击则将该飞碟隐藏
    public void GetHit() {
        if (Input.GetButtonDown("Fire1")) {
			Camera ca = Camera.main;
			Ray ray = ca.ScreenPointToRay(Input.mousePosition);
			RaycastHit hit;
			if (Physics.Raycast(ray, out hit)) {
                Record(hit.transform.gameObject);
                hit.transform.gameObject.SetActive(false);
			}
		}
    }

    public void Record(GameObject disk) {
        score += disk.GetComponent<DiskData>().score;
        userGUI.score = score;
    }
}
