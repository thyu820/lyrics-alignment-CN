def load_lyrics(lyrics_path):
    try:
        with open(lyrics_path, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"錯誤：找不到歌詞文件 '{lyrics_path}'")
        return []
    except Exception as e:
        print(f"讀取歌詞文件時發生錯誤：{e}")
        return []

# 測試函數
def test_load_lyrics():
    # 測試存在的文件
    lyrics = load_lyrics("test_lyrics.txt")
    print("讀取的歌詞：", lyrics)

    # 測試不存在的文件
    lyrics = load_lyrics("non_existent.txt")
    print("讀取不存在的文件：", lyrics)

if __name__ == "__main__":
    test_load_lyrics()