############################################################################################
## File name   : yt_kbs_worldreport_download.py
## Description : "특파원보고 세계는 지금" 최신 회차 다운로드
## Information :
##==========================================================================================
##  version   date             author      reason
##------------------------------------------------------------------------------------------
##  1.0       2023-06-04       kukubabo    First Revision.
############################################################################################
#import sys
import os
import subprocess
import re
import yt_dlp
import paramiko
from scp import SCPClient

# 재생목록에서 n번째 영상 url 가져오기
def get_video_url(playlist_url, n):
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'playlist_items': str(n),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        entries = info_dict.get('entries', [])
        if entries:
            nth_video_url = entries[0]['url']
            return nth_video_url
        else:
            return None

# url에서 타이틀 가져오기
def get_youtube_title(url):
    command = ['yt-dlp', '--get-title', url]
    output = subprocess.check_output(command).decode().strip()
    return output

# url에서 최대 해상도 가져오기
def get_max_resolution(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        # 해상도 목록에서 width, height 형태의 것들만 가져오기
        resolutions = [(format['width'], format['height']) for format in formats if 'width' in format and 'height' in format]
        # width, height 값에 숫자가 아닌 것이 있을 경우 제외한 뒤 height 값(resolution[1])만 가져오기
        resolutions = [resolution[1] for resolution in resolutions if all(resolution)]
        # height 목록을 내림차순으로 정렬
        resolutions.sort(reverse=True)
        max_resolution = resolutions[0] if resolutions else 'Unknown'
        return max_resolution

def extract_filename_from_title(title):
    pattern = r"\(KBS_(.*?)회_(\d{4})\.(\d{1,2})\.(\d{1,2})\.[^)]+\)" #  (KBS_328회_2023.10.14.방송 / KBS_339회_2024.1.6.방송)
    match = re.search(pattern, title)
    if match:
        episode = match.group(1)
        year = match.group(2)
        month = match.group(3)
        # 일자가 한 자리일 경우 앞에 0 붙이기
        if len(month) == 1:
            month = '0' + month
        day = match.group(4)
        # 일자가 한 자리일 경우 앞에 0 붙이기
        if len(day) == 1:
            day = '0' + day
        resolution = get_max_resolution(url)
        return f"특파원 보고 세계는 지금.E{episode}.{year}{month}{day}.{resolution}p-YT"
    else:
        return f"특파원 보고 세계는 지금-YT"

def download_youtube_video(url, output_path):
    command = ['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', '--merge-output-format', 'mp4', '-o', output_path, url]
    subprocess.call(command)

def upload_to_nas(output_path):
    print(output_path)

    # ====================================
    # NAS 접속 정보를 설정해줘야 함
    # ====================================
    hostname = os.getenv('NAS_HOST')
    port = os.getenv('NAS_PORT')
    username = os.getenv('NAS_USER')
    password = os.getenv('NAS_PASS')

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # connect ssh
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        
        with SCPClient(ssh_client.get_transport()) as scp:
            local_file = output_path
            remote_file = '/volume2/video/tv/특파원 보고 세계는 지금 [KBS1]/'

            scp.put(local_file, remote_file)

    except Exception as e:
        print(e)
    
    finally:
        # close ssh
        ssh_client.close()
    
    os.remove(output_path)

# 파라미터 체크해서 URL 정보가 없으면 URL 입력하라고 알려주기
# - 최신 버전으로 다운받는 방식으로 바꿔서 일단 주석 처리(추후에 필요하면 풀어서 다시 사용)
#if len(sys.argv) < 2:
#    print("URL을 입력해주세요.")
#    sys.exit(1)
# 첫 번째 파라미터에서 다운로드 대상 URL을 받아옴
#url = sys.argv[1]

# 특파원 보고 세계는 지금 본방송 재생목록
playlist_url = 'https://www.youtube.com/playlist?list=PLlHdT83qa_1zKzg0so3sU7FtO-rxao_2H'
# n번째 영상 url 가져오기(최근방송 받으려면 default 1 사용)
url = get_video_url(playlist_url, 1)
# url을 가지고 YouTube 동영상의 제목을 가져옴
youtube_title = get_youtube_title(url)
# 제목으로 파일명 작성
filename=extract_filename_from_title(youtube_title)

# 기본 다운로드 경로 설정
output_path = f"/tmp/{filename}.mp4"
# 다운로드 경로를 두 번째 파라미터로 받으면 경로 수정
# - 최신 버전으로 다운받는 방식으로 바꿔서 일단 주석 처리(추후에 필요하면 풀어서 다시 사용)
#if len(sys.argv) > 2:
#    output_path = sys.argv[2]

# 지정된 경로로 다운로드 실행
download_youtube_video(url, output_path)

# NAS로 업로드(scp)
upload_to_nas(output_path)