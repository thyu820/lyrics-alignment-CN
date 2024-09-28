from audio_processing import process_audio

def test_process_audio():
    audio_path = "path/to/test_audio.wav"
    segments = process_audio(audio_path)
    print("ASR 結果：")
    for segment in segments:
        print(f"開始時間：{segment['start']:.2f}, 結束時間：{segment['end']:.2f}, 文本：{segment['text']}")

if __name__ == "__main__":
    test_process_audio()