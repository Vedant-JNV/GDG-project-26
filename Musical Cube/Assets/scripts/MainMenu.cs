using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenuManager : MonoBehaviour
{
    public GameObject startPanel;
    public GameObject singlePanel;
    public GameObject multiPanel;

    public const int SINGLE_START = 1;
    public const int MULTI_START  = 11;

    void Start()
    {
        ShowStart();
    }

    public void ShowStart()
    {
        startPanel.SetActive(true);
        singlePanel.SetActive(false);
        multiPanel.SetActive(false);
    }

    public void ShowSingle()
    {
        startPanel.SetActive(false);
        singlePanel.SetActive(true);
        multiPanel.SetActive(false);
    }

    public void ShowMulti()
    {
        startPanel.SetActive(false);
        singlePanel.SetActive(false);
        multiPanel.SetActive(true);
    }

    public void LoadSingle(int level)
    {
        SceneManager.LoadScene(SINGLE_START + level - 1);
    }

    public void LoadMulti(int level)
    {
        SceneManager.LoadScene(MULTI_START + level - 1);
    }
}
