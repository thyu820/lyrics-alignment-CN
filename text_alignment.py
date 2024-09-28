from alignment import dtw_alignment
from audio_processing import process_audio

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{seconds:05.2f}"

def output_lrc(aligned_lyrics, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("[ti:知足]\n[ar:五月天]\n[al:知足]\n\n")
        for lyric in aligned_lyrics:
            f.write(f"[{format_time(lyric['start'])}]{lyric['text']}\n")

def process_lyrics_file(lyrics_file):
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def align_lyrics(asr_segments, lyrics):
    alignment = dtw_alignment(asr_segments, lyrics)
    aligned_lyrics = []
    
    for asr_idx, lyric_idx in alignment:
        aligned_lyrics.append({
            "start": asr_segments[asr_idx]['start'],
            "end": asr_segments[asr_idx]['end'],
            "text": lyrics[lyric_idx]
        })
    
    return aligned_lyrics

def main(audio_file, lyrics_file, output_file):
    # 讀取歌詞
    lyrics = process_lyrics_file(lyrics_file)
    
    # 處理音頻和對齊歌詞
    asr_segments = process_audio(audio_file)  # 這裡只傳入 audio_file
    aligned_lyrics = align_lyrics(asr_segments, lyrics)
    
    # 輸出 LRC 文件
    output_lrc(aligned_lyrics, output_file)
    
    print(f"LRC 文件已生成：{output_file}")

if __name__ == "__main__":
    audio_file = "music/test_audio.wav"
    lyrics_file = "lyrics/test_audio.txt"
    output_file = "test_audio.lrc"
    
    main(audio_file, lyrics_file, output_file)