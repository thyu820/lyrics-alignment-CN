from alignment import dtw_alignment

def test_dtw_alignment():
    asr_segments = [
        {"text": "怎麼去擁有", "start": 0.0, "end": 2.0},
        {"text": "一道彩虹", "start": 2.0, "end": 4.0},
        {"text": "怎麼去擁抱", "start": 4.0, "end": 6.0},
        {"text": "一夏天的風", "start": 6.0, "end": 8.0}
    ]
    lyrics = [
        "怎麼去擁有 一道彩虹",
        "怎麼去擁抱 一夏天的風",
        "天上的星星 笑地上的人"
    ]
    alignment = dtw_alignment(asr_segments, lyrics)
    print("DTW 對齊結果：")
    for asr_idx, lyric_idx in alignment:
        print(f"ASR 索引：{asr_idx}, 歌詞索引：{lyric_idx}")

if __name__ == "__main__":
    test_dtw_alignment()