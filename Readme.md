# 歌詞對齊項目

這個項目旨在開發一個自動化工具，用於將音頻文件中的歌曲與其對應的歌詞文本進行精確對齊。通過使用先進的語音識別技術和文本對齊算法，我們的目標是提高歌詞時間戳的準確性，從而增強音樂播放和卡拉OK等應用的用戶體驗。

## 功能特點

- 使用Whisper模型進行高精度語音識別
- 支持中文歌詞的對齊
- 使用WebRTC VAD進行語音活動檢測
- 實現了基於音素相似度的初步文本對齊算法
- 可處理WAV格式音頻文件
- 生成初步的LRC格式歌詞文件

## 系統要求

- Python 3.11 或更高版本
- 支持Windows、macOS和Linux

## 安裝說明

1. 克隆此儲存庫:
   ```
   git clone https://github.com/yourusername/lyrics-alignment-project.git
   ```

2. 安裝所需的Python庫:
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 準備您的WAV格式音頻文件和對應的歌詞文本文件。

2. 運行主程序:
   ```
   python main.py path/to/audio.wav path/to/lyrics.txt path/to/output.lrc
   ```

3. 程序將輸出初步對齊後的LRC格式歌詞文件。

## 項目結構

```
lyrics-alignment-project/
│
├── main.py             # 主程序
├── audio_processing.py # 音頻處理和歌詞對齊模塊
├── utils.py            # 工具函數
├── requirements.txt    # 項目依賴
├── music/              # 存放音樂文件的目錄
├── lyrics/             # 存放歌詞文件的目錄
└── README.md           # 項目說明文件
```

## 當前狀態

- [x] 實現基本的音頻處理和轉換
- [x] 集成Whisper模型進行語音識別
- [x] 實現WebRTC VAD進行語音活動檢測
- [x] 開發初步的基於音素相似度的文本對齊算法
- [x] 生成基本的LRC格式輸出文件

## 待辦事項

- [ ] 改進文本對齊算法的準確性和覆蓋率
- [ ] 優化處理大型音頻文件的性能
- [ ] 添加對多種音頻格式的支持
- [ ] 實現更精確的時間戳對齊
- [ ] 開發圖形用戶界面(GUI)
- [ ] 實現批量處理功能

## 已知問題

- 部分歌詞無法成功對齊和輸出
- 時間戳可能不夠精確
- 僅支持WAV格式音頻文件

## 貢獻

歡迎提出問題，提交pull請求或者提供改進建議。對於重大變更，請先開issue討論您想要改變的內容。

## 許可證

本項目採用MIT許可證 - 詳情請見 [LICENSE](LICENSE) 文件。

## 聯繫方式

如有任何問題或建議，請通過以下方式聯繫我:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

感謝您對這個項目的關注!
