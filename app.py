from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip
from tqdm import tqdm
import os
import time

app = Flask(__name__)

def download_mp3(video_url, output_path):
    youtube_video = YouTube(video_url)
    video_title = youtube_video.title

    audio_stream = youtube_video.streams.get_highest_audio_quality()

    print(f"Downloading MP3: {video_title}")
    download_start_time = time.time()

    with tqdm(total=audio_stream.filesize, unit='B', unit_scale=True, desc=f'Downloading MP3: {video_title}') as pbar:
        audio_clip = AudioFileClip(audio_stream.download(output_path=output_path, filename=f'{video_title}.mp4'))
        pbar.update(audio_stream.filesize)

    audio_clip.write_audiofile(f'{output_path}/{video_title}.mp3', codec='mp3')

    os.remove(f'{output_path}/{video_title}.mp4')

    download_end_time = time.time()
    print(f"Download complete. Time taken: {download_end_time - download_start_time} seconds")

    return f'{output_path}/{video_title}.mp3'

def download_mp4(video_url, output_path):
    youtube_video = YouTube(video_url)
    video_title = youtube_video.title

    video_stream = youtube_video.streams.get_highest_resolution()

    print(f"Downloading MP4: {video_title}")
    download_start_time = time.time()

    with tqdm(total=video_stream.filesize, unit='B', unit_scale=True, desc=f'Downloading MP4: {video_title}') as pbar:
        video_stream.download(output_path=output_path, filename=f'{video_title}.mp4')
        pbar.update(video_stream.filesize)

    download_end_time = time.time()
    print(f"Download complete. Time taken: {download_end_time - download_start_time} seconds")

    return f'{output_path}/{video_title}.mp4'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    start_time = time.time()  # Record the start time

    video_url = request.form['video_url']
    download_format = request.form['format']

    try:
        output_path = 'newDownloads'

        if download_format == 'mp3':
            file_path = download_mp3(video_url, output_path)
            return send_file(file_path, as_attachment=True)

        elif download_format == 'mp4':
            file_path = download_mp4(video_url, output_path)
            return send_file(file_path, as_attachment=True)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
#python app.py