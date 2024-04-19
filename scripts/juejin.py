from typing import List
import requests
from loguru import logger
from common import get_config
from fake_useragent import UserAgent
from notify import wxpusher

"""
掘金 网页版签到
https://juejin.cn/user/center/signin?from=sign_in_menu_bar
"""

check_url = "https://api.juejin.cn/growth_api/v1/check_in"

configs = get_config()
juejin_config = configs["juejin"]


def _init_payload() -> List:
    request_params_list = []
    for cookie in juejin_config:
        headers = {
            "content-type": "application/json",
            "cookie": cookie["cookie"],
            "origin": "https://juejin.cn",
            "referer": "https://juejin.cn/",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": UserAgent().random,
            "x-secsdk-csrf-token": cookie["x-secsdk-csrf-token"],
        }
        payload = {
            "aid": cookie["aid"],
            "uuid": cookie["uuid"],
            "spider": 0,
            "msToken": cookie["msToken"],
            "a_bogus": cookie["a_bogus"],
        }
        request_params_list.append({"headers": headers, "payload": payload})
    return request_params_list


def main():
    request_params_list = _init_payload()
    for request_params in request_params_list:
        response = requests.post(
            check_url, headers=request_params["headers"], json=request_params["payload"]
        )
        if response.status_code == 200:
            if response.json()["err_msg"] == "success":
                logger.info("签到成功")
                content = "掘金-签到成功"
                summary = "掘金-签到提醒"
                wxpusher(content, summary, configs["uid"])
            else:
                logger.error(response.json())
                content = f"掘金-签到失败: {response.json()}"
                summary = "掘金-签到提醒"
                wxpusher(content, summary, configs["uid"])
        else:
            logger.error(f"请求失败: {response.text}")
