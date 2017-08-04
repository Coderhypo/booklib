import requests

from stone.config import get_config_obj
from stone.common.errors import ClientError

config_obj = get_config_obj()


class __BaseClient(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers = {}

    def _set_headers(self, headers):
        self.headers.update(headers)

    def _get(self, url):
        result = self.result_or_raise(
            self.get(url=url, headers=self.headers),
            json=True,
        )
        return result

    def get_file(self, url):
        rsp = self.get(url)
        code = rsp.status_code

        if code // 100 != 2:
            raise ClientError(
                "can't get a response: status code {}".format(code))
        return rsp.content


    @staticmethod
    def result_or_raise(rsp, json=False):
        code = rsp.status_code

        if code // 100 != 2:
            raise ClientError(
                "can't get a response: status code {}".format(code))
        if json:
            return rsp.json()
        return rsp.text


class DouClient(__BaseClient):
    def __init__(self):
        super().__init__()
        headers = {}
        if config_obj.DOU_API_KEY:
            headers.update({"apikey": config_obj.DOU_API_KEY})
        self._set_headers(headers)

    @staticmethod
    def __get_book_info(payload):
        return {
            "title": payload.get('title'),
            "dou_id": payload.get("id"),
            "rating": payload.get('rating', {}).get('average'),
            "author": ", ".join(payload.get("author", [])),
            "origin_title": payload.get("origin_title") or payload.get("alt_title"),
            "translator": ", ".join(payload.get("translator", [])),
            "douban_link": payload.get("alt"),
            "publisher": payload.get("publisher"),
            "isbn10": payload.get("isbn10"),
            "isbn13": payload.get("isbn13"),
            "summary": payload.get("summary"),
            "tags": payload.get("tags", []),
            "images": payload.get("images", {})
        }

    def get_book_info_by_dou_id(self, dou_id):
        url = "https://api.douban.com/v2/book/{}".format(dou_id)
        result = self._get(url)
        return self.__get_book_info(result)

    def get_book_info_by_isnb(self, isnb):
        url = "https://api.douban.com/v2/book/isbn/{}".format(isnb)
        result = self._get(url)
        return self.__get_book_info(result)
