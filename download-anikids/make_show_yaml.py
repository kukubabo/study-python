import requests
import yaml
from bs4 import BeautifulSoup

def find_season():
    # 시즌 선택 메뉴를 통해서 전체 시즌 내용을 확인 한다.
    _ss1 = soup.select_one('div.rea_sellbox')
    _ss2 = _ss1.select('ul > li > a')
    _result = list()
    for _s in _ss2:
        _data = {
            'title': _s.text,  # 시즌명
            'id': _s['data-id']  # 시즌id
        }
        print(_data)
        _result.append(_data)

    return _result

def str_cleanup(_line):
    # 문자열의 공백과 개행문자 등 제거
    _line = _line.replace("\n", "")
    _line = _line.replace("\r", "")
    _line = _line.replace("\t", "")
    _line = _line.strip()
    return _line

def get_basic_inform():
    # 방송 타이들 확인
    _a = soup.select_one('div.rea_title')
    _br_title = _a.select_one('a').previousSibling

    # 내용 요약 확인
    _summary = soup.select_one('div.rt_disk > p').text
    _summary = str_cleanup(_summary)

    _br_info = {
        'title': str(_br_title),
        'summary': _summary
    }

    return _br_info

def get_ep_data(_id):
    # 입력한 id값을 기준으로. 해당되는 에피소드 리스트들을 읽음
    _aaa = soup.select_one(f"div[data-id='{_id}']")
    _ep_html = _aaa.select('div.suh_subwrap > div')

    _ep_list = list()

    for _i, _b in enumerate(_ep_html, start=1):
        _bb = _b.select_one('a > img')
        _len_bb = len(_bb['class'])

        # 썸네일의 경우 현재 화면상의 리스트에 표시된 항목은 속성값이 'src', 화면에 없는 항목의 속성값은 'data-src'이다.
        if _len_bb == 2:
            _thumb = _bb['src']
        elif _len_bb == 1:
            _thumb = _bb['data-src']

        _data = {
            'index': _i,  # 에피소드 인덱스. 파싱값이 아닌 인식된 리스트의 순서에 따른다.
            'title': str_cleanup(_b.select_one('dl > dt').text),  # 제목
            'originally_available_at': _b.select_one('dl > dd.vod_date').text,  # 방송일
            'summary': str_cleanup(_b.select_one('dl > dd.vod_disk').text),  # 요약
            'thumbs': [{'url': _thumb}]  # 썸네일
        }

        _ep_list.append(_data)

    return _ep_list

def make_tot_ep(_ss_data):
    # 입력된 시즌 에피소드들을 합쳐준다.
    _tot_ep = list()
    for _i, _ss in enumerate(reversed(_ss_data), start=1):
        _tot_ep.append(
            {'index': _i, 'posters': [{'url': ''}], 'episodes': get_ep_data(_ss['id'])}
        )
    return _tot_ep

def make_show_yaml():
    _data1 = {
        'primary': True,
        'code': 'ebs_' + show_id,
        'title': show_info['title'],
        'title_sort': show_info['title'],
        'originally_available_at': "",
        'summary': show_info['summary'],
        'posters': [{'url': "", 'art': ""}],
        'seasons': tot_ep
    }
    _out_name = f"show_{show_info['title']}_{show_id}.yaml"
    with open(_out_name, 'w', encoding="utf-8") as outfile:
        yaml.dump(_data1, outfile, sort_keys=False, allow_unicode=True)
    print(_out_name)

if __name__ == '__main__':
    # 방송 show id 값을 입력함. id는 방송 홈페이지의 다시 보기 메뉴로 들어 가면 확인 가능
    show_id = "40033171"

    #vodurl = f"https://anikids.ebs.co.kr/anikids/program/show/{show_id}"
    vodurl = f"https://anikids.ebs.co.kr/anikids/program/show/10210610"     # 한글용사 아이야

    html = requests.get(vodurl).text
    soup = BeautifulSoup(html, 'html.parser')  # bs4 사용

    # 시즌 리스트 확인. 시즌명, 시즌id를 반환한다.
    season_list = find_season()

    # 방송 기본 정보를 확인. 방송명, 요약내용을 반환한다.
    show_info = get_basic_inform()

    # 전체 시즌의 에피소드 리스트 반환
    tot_ep = make_tot_ep(season_list)

    # yaml파일 작성
    make_show_yaml()