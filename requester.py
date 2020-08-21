import requests


def __get_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}


def get_content(url):
    r = requests.get(url, headers=__get_headers())
    if r.ok:
        return r.content
    raise RequestFailed()
