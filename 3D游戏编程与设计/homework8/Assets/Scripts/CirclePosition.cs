public class CirclePosition
{
    public float radius = 0f, angle = 0f, time = 0f, startRadius = 0f;
    public CirclePosition(float radius, float angle, float time, float startRadius)
    {
        this.radius = radius;   // 半径
        this.angle = angle;     // 角度
        this.time = time;       // 时间
        this.startRadius = startRadius;
    }
}