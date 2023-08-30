# download youtube video from playlist
import yt_dlp
import subprocess
import re

# define playlist url
playlist_url = 'https://www.youtube.com/watch?v=9jeaIELBlP0&list=PLlHdT83qa_1zKzg0so3sU7FtO-rxao_2H'

# get video url from playlist
def get_video_url(playlist_url, index):
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'playlistend': index,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        return info_dict['entries'][index-1]['url']

# get video title from url
def get_video_title(url):
    command = ['yt-dlp', '--get-title', url]
    output = subprocess.check_output(command).decode().strip()
    return output

# get available format id from url
def get_available_format_id(url):
    ydl_opts = {
        'listformats': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        # get ID, EXT list
        format_ids = [(format['format_id'], format['ext']) for format in formats]
        # exclude formats that have non-numeric values in format_id
        format_ids = [format_id[0] for format_id in format_ids if format_id[0].isnumeric()]
        # sort format_ids in descending order
        format_ids.sort(reverse=True)
        return format_ids[0] if format_ids else 'Unknown'

# get max resolution from url
def get_max_resolution(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        # get resolutions in width, height format
        resolutions = [(format['width'], format['height']) for format in formats if 'width' in format and 'height' in format]
        # exclude resolutions that have non-numeric values in width or height
        resolutions = [resolution[1] for resolution in resolutions if all(resolution)]
        # sort resolutions in descending order
        resolutions.sort(reverse=True)
        max_resolution = resolutions[0] if resolutions else 'Unknown'
        return max_resolution

# extract filename from title
def extract_filename_from_title(title):
    pattern = r"\(KBS_(.*?)회_(\d{4})\.(\d{2})\.(\d{2})\.[^)]+\)"
    match = re.search(pattern, title)
    if match:
        episode = match.group(1)
        year = match.group(2)
        month = match.group(3)
        day = match.group(4)
        resolution = get_max_resolution(url)
        return f"특파원 보고 세계는 지금.E{episode}.{year}{month}{day}.{resolution}p-YT"
    else:
        return f"특파원 보고 세계는 지금.{resolution}p-YT"

# download youtube video
# Got error: HTTP Error 403: Forbidden. Retrying fragment 1 (attempt 1 of 10)...
def download_youtube_video(url, format_id, output_path):
    command = ['yt-dlp', '-f', f'{format_id}', '-o', output_path, url]
    subprocess.call(command)

# download latest video from playlist
url = get_video_url(playlist_url, 1)
format_id=get_available_format_id(url)
title = get_video_title(url)
filename = extract_filename_from_title(title)
output_path = f"/tmp/{filename}.mp4"
download_youtube_video(url, format_id, output_path)