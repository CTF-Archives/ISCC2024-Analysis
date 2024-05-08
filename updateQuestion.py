from requests import Session
import re
import json
import time
from authorization import username, password

host = "https://iscc.isclab.org.cn"


ss = Session()
ss.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

ptnProfile = re.compile(r'<h1 id="team-id">(.*?)</h1>\s+<h3 class="text-center">总积分为:(\d*?),排在(\d*?)位。</h3>')


def updateQuestionList(type, valueName):
    ret = ss.get(f"{host}/{type}")
    if ret.status_code == 200:
        ret = ret.json()
        for q in ret["game"]:
            if q["category"] not in valueName.keys():
                valueName[q["category"]] = {}
            retret = ss.get(f'{host}/{type}/{q["id"]}')
            if retret.status_code == 200:
                retret = retret.json()
                valueName[q["category"]][q["id"]] = {
                    "name": retret["name"],
                    "score": retret["value"],
                    "description": retret["description"],
                    "files": retret["files"],
                    "solves": [],
                }
                if type == "arenas":
                    valueName[q["category"]][q["id"]]["author"] = retret["author"]
                print(q["category"], q["id"], retret["value"], retret["name"], sep="\t")
            else:
                raise Exception(f"HTTP {retret.status_code}")
            pass
    else:
        raise Exception(f"HTTP {ret.status_code}")
    pass


def updateQuestionsolve(type, valueName):
    for category in valueName.keys():
        for id in valueName[category].keys():
            ret = ss.get(f"{host}/{type}/{id}/solves")
            if ret.status_code == 200:
                ret = ret.json()
                valueName[category][id]["solves"] = ret["teams"]
                if type == "are":
                    for i in valueName[category][id]["solves"]:
                        if i["name"] == valueName[category][id]["author"]:
                            valueName[category][id]["solves"].remove(i)
                            print(category, id, "成功排除擂台赛中出题人自动解题造成的误差")
                            break
                print(category, id, valueName[category][id]["solves"], sep="\t")


if __name__ == "__main__":
    challengeList = {}
    arenaList = {}

    # 检查登录情况
    assert ss.post(f"{host}/login", data={"name": username, "password": password}, allow_redirects=False).status_code == 302

    # 练武的题目信息
    updateQuestionList("chals", challengeList)
    # 练武的题目解出情况
    updateQuestionsolve("chal", challengeList)
    # 保存练武的信息
    with open("./docs/data/challenge.json", "w+", encoding="UTF-8") as f:
        f.write(json.dumps(challengeList, ensure_ascii=False))

    # 擂台的题目信息
    updateQuestionList("arenas", arenaList)
    # 擂台的题目解出情况
    updateQuestionsolve("are", arenaList)
    # 保存擂台的信息
    with open("./docs/data/arena.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(arenaList, ensure_ascii=False))

    # 写入状态信息
    with open("./docs/data/status.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps({"updateTime": time.time()}, ensure_ascii=False))
