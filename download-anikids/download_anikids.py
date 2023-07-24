# https://anikids.ebs.co.kr/anikids/program/show/10210610 페이지의 vod 목록 url 가져오기
import requests
from bs4 import BeautifulSoup

def get_vod_url():
    # vod 목록 url 가져오기
    # vodurl = f"https://anikids.ebs.co.kr/anikids/program/show/{show_id}"
    vodurl = f"https://anikids.ebs.co.kr/anikids/program/show/10210610"     # 한글용사 아이야
    res = requests.get(vodurl)
    print(res)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # vod 목록 url 가져오기
    _vod_list = soup.select('div.suh_subwrap > div > a')
    _vod_url = list()
    for _i in _vod_list:
        _vod_url.append(_i['href'])

    return _vod_url

if __name__ == '__main__':

    # get_vod_url 함수 호출 결과를 출력
    print(get_vod_url())