using UnityEngine;

public class CameraSwitcher : MonoBehaviour
{
    public Transform[] targets;   // players
    public Vector3 offset = new Vector3(0, 6, -6);
    public float followSpeed = 5f;

    int currentIndex = 0;

    void LateUpdate()
    {
        if (targets == null || targets.Length == 0) return;

        Transform target = targets[currentIndex];
        Vector3 desiredPos = target.position + offset;

        transform.position = Vector3.Lerp(
            transform.position,
            desiredPos,
            Time.deltaTime * followSpeed
        );

        transform.LookAt(target.position);
    }

    public void SwitchTarget()
    {
        if (targets == null || targets.Length == 0) return;
        currentIndex = (currentIndex + 1) % targets.Length;
    }
}

