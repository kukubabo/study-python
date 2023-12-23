import requests, yaml, re, os
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_response_to_file(url, file_path):
    try:
        response = requests.get(url)

        # 요청이 성공적으로 완료된 경우
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Response saved to {file_path} successfully.")
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")

def make_yaml(show_data, target_path):
    with open(target_path, 'w', encoding="utf-8") as outfile:
        yaml.dump(show_data, outfile, sort_keys=False, allow_unicode=True)

def get_thumb(param):
    if param.endswith('ch_id=9'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/710e7a39f7910d4d828047e1222e2dce.png'
    elif param.endswith('ch_id=10'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/55509fff870629e4db8865ed79988c56.png'
    elif param.endswith('ch_id=15'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/dfc390d3df155cbaf02be7da5c9a92af.png'
    elif param.endswith('ch_id=11'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/0011057bb69a02e3b3827ab82b57b849.png'
    elif param.endswith('ch_id=1'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/452e738814aba6b8dbe3688929368a6d.png'
    elif param.endswith('ch_id=2'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/3daa55ea25c6274dea97f35e170de79d.png'
    elif param.endswith('ch_id=3'):
        return 'https://cdn.spotvnow.co.kr/src/upload/image/20211215/0bc2fb062edbd8f2a05b64e291b148b8.png'
    else:
        return '첨부파일을 디스코드에 올려서 해당 링크를 넣습니다'
        
def get_yaml_from_m3u(file_path):

    extra_data = []
    with open(file_path, "r", encoding='utf-8') as m3u_file:
        lines = m3u_file.readlines()

        for line in lines:
            if line.strip().startswith("#EXTINF:-1"):
                start_index = line.find("tvg-name=")
                if start_index != -1:
                    end_index = line.find('"', start_index + 10)
                    title = line[start_index + 10 : end_index].strip()
                    param = lines[lines.index(line)+1].strip()
                    content = {
                        'mode': "m3u8",
                        'type': "featurette",
                        'param': param,
                        'title': title,
                        'thumb': get_thumb(param),
                    }
                extra_data.append(content)
    show_data = {
        'primary' : True,
        'code' : 'spotv',
        'title' : "[SPOTV]",
        'posters': "https://cdn.spotvnow.co.kr/src/upload/image/20211215/710e7a39f7910d4d828047e1222e2dce.png",
        'summary': f"SPOTV 채널\n{current_time}",
        'extras' : extra_data
        }
    make_yaml(show_data, '/mnt/Live/SPOTV/show.yaml')

def refresh_section_metadata(plex_url, plex_token, section_id):
    headers = {"X-Plex-Token": plex_token}
    url = f"{plex_url}/library/sections/{section_id}/refresh?force=1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while refreshing metadata: {e}")

spotv_path = '/mnt/spotv.m3u' ###spotv.m3u 저장할 로컬 경로 ex) /mnt/spotv.m3u, 실제 yaml 저장경로는 72번째줄 확인
cppl_path = '/mnt/Live/cppl/show.yaml'
naver_path = '/mnt/Live/naver/show.yaml'
save_response_to_file('your sjva3 url/klive_plus/api/m3u', spotv_path)
get_yaml_from_m3u(spotv_path)
save_response_to_file('your ff url/ff_cpp/api/yaml', cppl_path)
save_response_to_file('your ff url/ff_nsports/api/yaml', naver_path)
refresh_section_metadata("your plex url", "your plex token", 'your plex section id')