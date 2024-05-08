import json

def generateUserList():
    userList = {}

    with open("./docs/data/challenge.json", "r", encoding="utf8") as f:
        data_challenge = json.load(f)

    with open("./docs/data/arena.json", "r", encoding="utf8") as f:
        data_arena = json.load(f)

    # 重建可索引的所有用户
    # 基于练武进行用户列表重建
    for category in list(data_challenge.keys()):
        for challenge in list(data_challenge[category].keys()):
            for solve_record in data_challenge[category][challenge]["solves"]:
                if solve_record["id"] in userList.keys():
                    pass
                else:
                    userList[solve_record["id"]] = {"name": solve_record["name"], "score": 0, "friends": {}}
    # 基于擂台进行用户列表重建
    for category in list(data_arena.keys()):
        for challenge in list(data_arena[category].keys()):
            for solve_record in data_arena[category][challenge]["solves"]:
                if solve_record["id"] in userList.keys():
                    pass
                else:
                    userList[solve_record["id"]] = {"name": solve_record["name"], "score": 0, "friends": {}}

    # 重建所有用户的分数信息
    # 基于练武进行用户分数重建
    for category in list(data_challenge.keys()):
        for challenge in list(data_challenge[category].keys()):
            for solve_record in data_challenge[category][challenge]["solves"]:
                solve_index = data_challenge[category][challenge]["solves"].index(solve_record)
                userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"]
                # if solve_index < 10:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"]
                # elif 10 <= solve_index and solve_index < 100:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"] * 0.9
                # elif 100 <= solve_index and solve_index < 500:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"] * 0.8
                # elif 500 <= solve_index and solve_index < 1000:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"] * 0.7
                # elif 1000 <= solve_index and solve_index < 2000:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"] * 0.6
                # else:
                #     userList[solve_record["id"]]["score"] += data_challenge[category][challenge]["score"] * 0.5
    # 基于擂台进行用户分数重建
    for category in list(data_arena.keys()):
        for challenge in list(data_arena[category].keys()):
            for solve_record in data_arena[category][challenge]["solves"]:
                solve_index = data_arena[category][challenge]["solves"].index(solve_record)
                userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"]
                # if solve_index < 10:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"]
                # elif 10 <= solve_index and solve_index < 100:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"] * 0.9
                # elif 100 <= solve_index and solve_index < 500:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"] * 0.8
                # elif 500 <= solve_index and solve_index < 1000:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"] * 0.7
                # elif 1000 <= solve_index and solve_index < 2000:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"] * 0.6
                # else:
                #     userList[solve_record["id"]]["score"] += data_arena[category][challenge]["score"] * 0.5

    # 写入用户信息
    with open("./docs/data/user.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(userList, ensure_ascii=False))
