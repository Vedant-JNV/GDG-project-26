using UnityEngine;

public class ProceduralMoveMusic : MonoBehaviour
{
    public AudioSource audioSource;
    public AudioClip baseNote;

    int[] scale = { 0,1,3,5,7,8,10 }; 

    [Header("Optional Note Sequence")]
    public TextAsset noteSequenceFile;

    int[] sequence;
    int index = 0;

    void Start()
    {
        if (audioSource == null)
            audioSource = GetComponent<AudioSource>();

        if (noteSequenceFile != null)
        {
            string[] t = noteSequenceFile.text.Split(
                new char[] { ' ', ',', '\n', '\r' },
                System.StringSplitOptions.RemoveEmptyEntries
            );

            sequence = new int[t.Length];
            for (int i = 0; i < t.Length; i++)
                int.TryParse(t[i], out sequence[i]);
        }
    }

    public void PlayNote()
    {
        if (audioSource == null || baseNote == null) return;

        int semitone;
        if (sequence != null && sequence.Length > 0)
        {
            int idx = sequence[index % sequence.Length];
            idx = Mathf.Clamp(idx, 0, scale.Length - 1);
            semitone = scale[idx];
            index++;
        }
        else
        {
            semitone = scale[Random.Range(0, scale.Length)];
        }

        float pitch = Mathf.Pow(2f, semitone / 12f);
        audioSource.pitch = pitch;
        audioSource.PlayOneShot(baseNote);
    }
}
