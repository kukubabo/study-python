import sys
import subprocess
from datetime import datetime
import re

def get_youtube_title(url):
    command = ['yt-dlp', '--get-title', url]
    output = subprocess.check_output(command).decode().strip()
    return output

def sanitize_filename(filename):
    # 파일명으로 사용할 수 없는 문자를 제거하는 정규식 패턴
    # 윈도우즈에서 사용 불가능한 문자들을 대체하여 유효한 파일명으로 변환
    invalid_chars = r'[\/:*?"<>|]'
    sanitized_filename = re.sub(invalid_chars, '', filename)
    return sanitized_filename

def download_youtube_video(url, output_path):
    command = ['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', '--merge-output-format', 'mp4', '-o', output_path, url]
    subprocess.call(command)

if len(sys.argv) < 2:
    print("URL을 입력해주세요.")
    sys.exit(1)

url = sys.argv[1]  # 첫 번째 파라미터로부터 URL을 받아옴

output_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")  # 날짜와 시간을 포맷팅하여 파일 이름에 추가

youtube_title = get_youtube_title(url)  # YouTube 동영상의 제목을 가져옴
sanitized_title = sanitize_filename(youtube_title)  # 파일명으로 사용할 수 있는 형식으로 제목을 변환

output_filename = f"output_{output_datetime}_{sanitized_title}.mp4"  # default 출력 파일명 생성
output_path = f"/download/{output_filename}"  # 기본 경로

if len(sys.argv) > 2:
    output_path = sys.argv[2]  # 두 번째 파라미터로부터 output 경로를 받아옴

download_youtube_video(url, output_path)

 
# 네, URL에서 동영상의 제목(Title)을 가져와서 default output 파일명으로 설정하는 기능을 추가할 수 있습니다. YouTube의 동영상 제목은 일반적으로 URL의 일부로 포함되어 있습니다. 이를 활용하여 제목을 추출하고, 파일명에 사용할 수 있습니다. 아래는 해당 기능을 추가한 예제 코드입니다.
# 위의 코드에서는 get_youtube_title 함수를 사용하여 YouTube 동영상의 제목을 추출합니다. sanitize_filename 함수는 파일명으로 사용할 수 없는 문자를 제거하여 유효한 파일명으로 변환합니다. 그리고 output_filename에 날짜, 시간, 제목을 포함하여 default 출력 파일명을 생성합니다.

# 이제 코드를 실행할 때 두 번째 파라미터를 생략하면 default로 "output_날짜시간_제목.mp4" 형식의 파일이 생성됩니다. 예를 들어:
# python download_youtube.py https://www.youtube.com/watch?v=VIDEO_ID
# 위와 같이 실행하면 "output_날짜시간_제목.mp4" 파일이 생성됩니다.