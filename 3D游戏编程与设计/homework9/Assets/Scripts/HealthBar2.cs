using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HealthBar2 : MonoBehaviour
{
    public Slider slider;
    private float hurtkey = 300f;
    private float healkey = 500f;

    void Start() {
        slider.maxValue = 4000.0F;
        slider.minValue = 0F;
        slider.value = slider.maxValue;
    }

    void Update() {
         if(Input.GetKeyDown("f")){
            Hurt(hurtkey);
        }

        if(Input.GetKeyDown("h")){
            Heal(healkey);
        }

        if(Input.GetKeyDown("r")){
            Restart();
        }

        // this.transform.LookAt(Camera.main.transform.position);

        slider.direction = Slider.Direction.LeftToRight;
        slider.transform.rotation = Camera.main.transform.rotation;

        if(slider.value <= 0.3 * slider.maxValue){
            slider.fillRect.transform.GetComponent<Image>().color = Color.red;
        }
        else if(slider.value <= 0.6 * slider.maxValue){
            slider.fillRect.transform.GetComponent<Image>().color = Color.yellow;
        }
        else{
            slider.fillRect.transform.GetComponent<Image>().color = Color.green;
        }
    }

    public void Hurt(float h) {
        slider.value -= h;
        if(slider.value <= 0){
            slider.value = 0;
        }
    }

    public void Heal(float h) {
        if(slider.value > 0){
            slider.value += h;
            if(slider.value >= slider.maxValue) {
                slider.value = slider.maxValue;
            }
        }
    }

    public void Restart(){
        slider.maxValue = 4000.0F;
        slider.value = slider.maxValue;
    }

}
