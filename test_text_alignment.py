from text_alignment import align_lyrics, output_lrc, process_lyrics_file
from audio_processing import process_audio

def test_align_and_output():
    audio_file = "path/to/test_audio.wav"
    lyrics_file = "path/to/test_lyrics.txt"
    output_file = "test_output.lrc"

    # 處理音頻
    asr_segments = process_audio(audio_file)

    # 讀取歌詞
    lyrics = process_lyrics_file(lyrics_file)

    # 對齊歌詞
    aligned_lyrics = align_lyrics(asr_segments, lyrics)

    # 輸出 LRC 文件
    output_lrc(aligned_lyrics, output_file)

    print(f"LRC 文件已生成：{output_file}")

if __name__ == "__main__":
    test_align_and_output()