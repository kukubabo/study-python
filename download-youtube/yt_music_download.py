import yt_dlp

def get_playlist_info(url):
    ydl_opts = {
        'dump_single_json': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info

def download_playlist(url, output_path):
    info = get_playlist_info(url)

    for idx, entry in enumerate(info['entries'], start=1):

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '5',
            }],
            'outtmpl': f'{output_path}/{idx:02d}. %(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([entry['url']])

# 플레이리스트 URL과 다운로드할 경로를 입력하세요.
playlist_url = 'https://music.youtube.com/playlist?list=OLAK5uy_mH3EbWl55yvmwplL1yhyd2uZ9Idb0rij8'
download_path = '/tmp/music'

download_playlist(playlist_url, download_path)