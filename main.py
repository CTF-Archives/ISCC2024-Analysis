import datetime
from pathlib import Path
import json
import shutil
import os
import core


class ISCCError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.error_code = -1


with open("./docs/data/status.json", "r") as f:
    data_time = str(datetime.datetime.fromtimestamp(json.load(f)["updateTime"]).strftime("%Y-%m-%d_%H-%M-%S"))


# 尝试获取新数据，如果失败就放弃本次爬取
try:
    core.updateQuestion()
    core.generateUserList()
except:
    raise ISCCError("ISCC 网站可用性降低，自动停止本次爬取")

print("a")

current_directory = os.getcwd()

# 成功获取到数据，迁移旧数据
destination_path = os.path.join(current_directory, "archives", data_time)
Path(destination_path).mkdir(parents=True, exist_ok=True)
source_folder = os.path.join(current_directory, "docs", "data")
for root, directories, files in os.walk(source_folder):
    for file in files:
        source_file = os.path.join(root, file)
        destination_file = os.path.join(destination_path, file)
        shutil.move(source_file, destination_file)

# 转移新数据
destination_path = os.path.join(current_directory, "docs", "data")
source_folder = os.path.join(current_directory, "temp")
for root, directories, files in os.walk(source_folder):
    for file in files:
        source_file = os.path.join(root, file)
        destination_file = os.path.join(destination_path, file)
        shutil.move(source_file, destination_file)
