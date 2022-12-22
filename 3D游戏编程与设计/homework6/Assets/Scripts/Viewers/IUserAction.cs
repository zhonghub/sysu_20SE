using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface IUserAction {
    
    void GetHit();
    bool isGameOver();
    void Restart();
}
