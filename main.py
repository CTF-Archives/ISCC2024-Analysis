import datetime
from pathlib import Path
import json
import shutil
import os
import core


with open("./docs/data/status.json", "r") as f:
    time = json.load(f)["updateTime"]

current_directory = os.getcwd()

destination_path = os.path.join(current_directory, "archives", str(datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d_%H-%M-%S")))
Path(destination_path).mkdir(parents=True, exist_ok=True)

source_folder = os.path.join(current_directory, "docs", "data")

for root, directories, files in os.walk(source_folder):
    for file in files:
        source_file = os.path.join(root, file)
        destination_file = os.path.join(destination_path, file)
        shutil.move(source_file, destination_file)

core.updateQuestion()

core.generateUserList()
