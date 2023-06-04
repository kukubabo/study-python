import requests
import urllib
import os

# 비디오 URL을 입력합니다.
video_url = "blob:https://player.vimeo.com/898d4af7-1006-456f-8354-890766d53734"

# 비디오 파일의 이름을 지정합니다.
video_file_name = "video.mp4"

with urllib.request.urlopen(video_url) as response:
    video_file = response.read()

with open("video.mp4", "wb") as f:
    f.write(video_file)

# 비디오를 다운로드합니다.
response = requests.get(video_url)
with open(video_file_name, "wb") as f:
    f.write(response.content)

# 비디오가 다운로드되었는지 확인합니다.
if os.path.exists(video_file_name):
    print("Video downloaded successfully!")
else:
    print("Error downloading video.")