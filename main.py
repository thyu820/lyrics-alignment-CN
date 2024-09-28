import argparse
from audio_processing import process_audio
from text_alignment import align_lyrics, output_lrc
from utils import load_lyrics

def main(audio_path, lyrics_path, output_path):
    # 處理音頻
    asr_segments = process_audio(audio_path)
    
    # 載入歌詞
    lyrics = load_lyrics(lyrics_path)
    
    # 對齊歌詞
    aligned_lyrics = align_lyrics(asr_segments, lyrics)
    
    # 輸出 LRC 文件
    output_lrc(aligned_lyrics, output_path)
    
    print(f"LRC 文件已生成：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="歌詞對齊工具")
    parser.add_argument("audio", help="音頻文件路徑")
    parser.add_argument("lyrics", help="歌詞文件路徑")
    parser.add_argument("output", help="輸出 LRC 文件路徑")
    args = parser.parse_args()
    
    main(args.audio, args.lyrics, args.output)