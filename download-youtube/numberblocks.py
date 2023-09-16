import yt_dlp

ydl_opts = {
    'format': 'best[ext=mp4]',
    'playlist-start': 1,
    'playlist-end': None,
    'outtmpl': f'/tmp/numberblocks/season5/%(title)s.%(ext)s',
}

playlist_url = 'https://www.youtube.com/watch?v=-KFdq63cVVo&list=PL9swKX1PviEpLQxq7gp_cqnumCt5_FjS7'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])