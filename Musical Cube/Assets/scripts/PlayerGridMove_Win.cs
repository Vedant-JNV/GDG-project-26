using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;
using System.Collections.Generic;

public class PlayerGridMove_Win : MonoBehaviour
{
    [Header("Ground")]
    public LayerMask groundLayer;

    [Header("Fall")]
    public float fallSpeed = 6f;
    public float deathY = -10f;

    [Header("Win")]
    public int blocksToWin = 10;
    public float winFlySpeed = 3f;
    public float winRotateSpeed = 360f;
    public float winHeight = 8f;

    [Header("Blocked Positions (Per Player)")]
    public List<Vector3Int> blockedGridPositions = new List<Vector3Int>();
    [Header("Blocked Move Sound")]
    public AudioClip blockedClip;
    public float blockedPitch = 0.4f;


    [Header("UI (Level Scene)")]
    public GameObject hudPanel;
    public GameObject winPanel;
    public GameObject nextButton;

    static int deletedBlocks = 0;
    static bool gameLocked = false;
    static bool isWinning = false;
    static bool notePlayedThisFrame = false;
    static int lastLoadedScene = -1;
    static bool anyPlayerFalling = false;

    bool isMoving = false;
    bool isFalling = false;

    ProceduralMoveMusic music;

    void OnEnable()
    {
        int currentScene = SceneManager.GetActiveScene().buildIndex;

        if (currentScene != lastLoadedScene)
        {
            deletedBlocks = 0;
            gameLocked = false;
            isWinning = false;
            notePlayedThisFrame = false;
            anyPlayerFalling = false;
            lastLoadedScene = currentScene;
        }
    }

    void Start()
    {
        music = GetComponent<ProceduralMoveMusic>();
        if (winPanel != null)
            winPanel.SetActive(false);
    }

    void Update()
    {
        if (gameLocked)
        {
            if (isFalling) Fall();
            if (isWinning) WinAnimation();
            return;
        }

        if (isMoving) return;

        Vector3 dir = ReadInput();
        if (dir == Vector3.zero) return;

        Vector3 target = transform.position + dir;

        if (IsBlocked(target))
        {
            PlayBlockedSound();
            return;
        }

        StartCoroutine(MoveSmooth(target));
    }

    Vector3 ReadInput()
    {
        if (Keyboard.current != null)
        {
            if (Keyboard.current.upArrowKey.wasPressedThisFrame) return Vector3.forward;
            if (Keyboard.current.downArrowKey.wasPressedThisFrame) return Vector3.back;
            if (Keyboard.current.leftArrowKey.wasPressedThisFrame) return Vector3.left;
            if (Keyboard.current.rightArrowKey.wasPressedThisFrame) return Vector3.right;
        }

        return Vector3.zero;
    }

    System.Collections.IEnumerator MoveSmooth(Vector3 target)
    {
        isMoving = true;
        GameObject currentBlock = GetGroundBlock();

        if (!notePlayedThisFrame && music != null)
        {
            music.PlayNote();
            notePlayedThisFrame = true;
        }

        Vector3 start = transform.position;
        float t = 0f;

        while (t < 1f)
        {
            t += Time.deltaTime * 8f;
            transform.position = Vector3.Lerp(start, target, t);
            yield return null;
        }

        transform.position = target;

        if (currentBlock != null)
        {
            Destroy(currentBlock);
            deletedBlocks++;
        }

        if (!HasGroundBelow())
        {
            anyPlayerFalling = true;
            gameLocked = true;
            isFalling = true;
            isMoving = false;
            yield break;
        }

        if (deletedBlocks >= blocksToWin && HasGroundBelow() && !anyPlayerFalling)
        {
            gameLocked = true;
            isWinning = true;
            isMoving = false;
            yield break;
        }

        isMoving = false;
    }

    void Fall()
    {
        transform.position += Vector3.down * fallSpeed * Time.deltaTime;

        if (transform.position.y < deathY)
        {
            ResetState();
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }
    }

    void WinAnimation()
    {
        transform.Rotate(Vector3.up * winRotateSpeed * Time.deltaTime);
        transform.position += Vector3.up * winFlySpeed * Time.deltaTime;

        if (transform.position.y > winHeight)
        {
            if (hudPanel != null)
                hudPanel.SetActive(false);

            if (winPanel != null)
                winPanel.SetActive(true);

            if (nextButton != null)
                nextButton.SetActive(!IsLastLevel());
        }
    }

    public void RestartLevel()
    {
        ResetState();
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    public void LoadNextLevel()
    {
        ResetState();
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void GoHome()
    {
        ResetState();
        SceneManager.LoadScene(0);
    }

    bool IsLastLevel()
    {
        return SceneManager.GetActiveScene().buildIndex
               >= SceneManager.sceneCountInBuildSettings - 1;
    }

    Vector3Int WorldToGrid(Vector3 pos)
    {
        return new Vector3Int(
            Mathf.RoundToInt(pos.x),
            Mathf.RoundToInt(pos.y),
            Mathf.RoundToInt(pos.z)
        );
    }

    bool IsBlocked(Vector3 targetWorldPos)
    {
        Vector3Int targetGrid = WorldToGrid(targetWorldPos);

        for (int i = 0; i < blockedGridPositions.Count; i++)
        {
            if (blockedGridPositions[i] == targetGrid)
                return true;
        }
        return false;
    }

    void PlayBlockedSound()
    {
        if (music == null || blockedClip == null) return;

        music.audioSource.pitch = blockedPitch;
        music.audioSource.PlayOneShot(blockedClip);
    }

    GameObject GetGroundBlock()
    {
        RaycastHit hit;
        Vector3 origin = transform.position + Vector3.up * 0.6f;

        if (Physics.Raycast(origin, Vector3.down, out hit, 2f, groundLayer))
            return hit.collider.gameObject;

        return null;
    }

    bool HasGroundBelow()
    {
        Vector3 origin = transform.position + Vector3.up * 0.6f;
        return Physics.Raycast(origin, Vector3.down, 2f, groundLayer);
    }

    void LateUpdate()
    {
        notePlayedThisFrame = false;
    }

    static void ResetState()
    {
        anyPlayerFalling = false;
        deletedBlocks = 0;
        gameLocked = false;
        isWinning = false;
        notePlayedThisFrame = false;
    }
}

