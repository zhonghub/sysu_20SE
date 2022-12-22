using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface IActionManager
{
    void MoveDisk(GameObject disk);
    int GetActionCount() ;
}
