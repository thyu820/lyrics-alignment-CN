import whisper
from pydub import AudioSegment
import os
import webrtcvad
import collections
import contextlib
import wave
import struct
from pypinyin import lazy_pinyin
from difflib import SequenceMatcher

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield audio[offset:offset + n], timestamp, duration
        timestamp += duration
        offset += n

def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.
    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.
    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.
    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).
    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame, timestamp, duration in frames:
        is_speech = vad.is_speech(frame, sample_rate)

        if not triggered:
            ring_buffer.append((frame, timestamp, duration))
            num_voiced = len([f for f, _, _ in ring_buffer if vad.is_speech(f, sample_rate)])
            # 降低觸發閾值
            if num_voiced > 0.7 * ring_buffer.maxlen:
                triggered = True
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, t, d in ring_buffer:
                    voiced_frames.append((f, t, d))
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append((frame, timestamp, duration))
            ring_buffer.append((frame, timestamp, duration))
            num_unvoiced = len([f for f, _, _ in ring_buffer if not vad.is_speech(f, sample_rate)])
            # 降低解除觸發閾值
            if num_unvoiced > 0.7 * ring_buffer.maxlen:
                triggered = False
                yield [f for f, _, _ in voiced_frames], voiced_frames[0][1], voiced_frames[-1][1] + voiced_frames[-1][2]
                ring_buffer.clear()
                voiced_frames = []
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield [f for f, _, _ in voiced_frames], voiced_frames[0][1], voiced_frames[-1][1] + voiced_frames[-1][2]

def convert_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    temp_path = "temp.wav"
    audio.export(temp_path, format="wav")
    return temp_path

def process_audio(audio_path):
    # 轉換音頻
    temp_path = convert_audio(audio_path)
    
    # 使用 VAD 進行語音活動檢測
    vad = webrtcvad.Vad(1)  # 降低 VAD 的攻擊性，使其更容易檢測到語音
    audio, sample_rate = read_wave(temp_path)
    frames = frame_generator(20, audio, sample_rate)  # 減少幀持續時間
    segments = vad_collector(sample_rate, 20, 200, vad, frames)  # 減少填充持續時間

    # 載入 Whisper 模型
    model = whisper.load_model("medium")  # 使用更大的模型以提高準確性
    
    results = []
    for i, segment in enumerate(segments):
        segment_audio, start_time, end_time = segment
        segment_path = f"segment_{i}.wav"
        with wave.open(segment_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(segment_audio))
        
        # 使用 Whisper 進行語音識別，指定中文
        result = model.transcribe(segment_path, language="zh")
        
        # 添加結果
        results.append({
            "start": start_time,
            "end": end_time,
            "text": result["text"].strip()
        })
        
        # 刪除臨時文件
        os.remove(segment_path)
    
    # 刪除主要的臨時文件
    os.remove(temp_path)
    
    return results

def load_lyrics(lyrics_path):
    with open(lyrics_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def pinyin_similarity(text1, text2):
    pinyin1 = ''.join(lazy_pinyin(text1))
    pinyin2 = ''.join(lazy_pinyin(text2))
    return SequenceMatcher(None, pinyin1, pinyin2).ratio()

def align_lyrics(asr_results, lyrics):
    aligned_lyrics = []
    used_indices = set()

    for lyric in lyrics:
        best_match = None
        best_score = 0
        best_index = -1

        for i, result in enumerate(asr_results):
            if i in used_indices:
                continue
            score = pinyin_similarity(lyric, result['text'])
            if score > best_score:
                best_score = score
                best_match = result
                best_index = i

        if best_match and best_score > 0.3:  # 可以調整閾值
            aligned_lyrics.append({
                "start": best_match['start'],
                "end": best_match['end'],
                "text": lyric
            })
            used_indices.add(best_index)

    # 排序對齊後的歌詞
    aligned_lyrics.sort(key=lambda x: x['start'])

    return aligned_lyrics

def generate_lrc(aligned_lyrics, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for lyric in aligned_lyrics:
            minutes, seconds = divmod(lyric['start'], 60)
            f.write(f"[{int(minutes):02d}:{seconds:05.2f}]{lyric['text']}\n")

def main(audio_path, lyrics_path, output_path):
    # 處理音頻
    asr_results = process_audio(audio_path)
    
    # 載入歌詞
    lyrics = load_lyrics(lyrics_path)
    
    # 對齊歌詞
    aligned_lyrics = align_lyrics(asr_results, lyrics)
    
    # 生成 LRC 文件
    generate_lrc(aligned_lyrics, output_path)
    
    print(f"LRC 文件已生成：{output_path}")

if __name__ == "__main__":
    audio_path = "music/test_audio.wav"
    lyrics_path = "./lyrics/test_audio.txt"
    output_path = "output.lrc"
    main(audio_path, lyrics_path, output_path)