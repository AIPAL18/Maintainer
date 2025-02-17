import subprocess
import json
from core import get_greater_version, download, remove, unzip, rename
import os

try:
    releases = subprocess.check_output(['gh', 'api', "/repos/MDL-LDV/Bar-Numerique/releases", "--method", "GET"])
except subprocess.CalledProcessError as err:
    print(err)

releases = json.loads(releases)

max_r = get_greater_version(releases) 
zip_link = max_r["zipball_url"]

path = download(zip_link, max_r["tag_name"] + ".zip")[0]

user = os.getenv("USERPROFILE")
destination = os.path.join(user, "Documents")
remove(os.path.join(destination, "Bar numérique"))

print(destination)
folder_name = unzip(path, destination)

remove(path)

temp_folder = os.path.join(destination, folder_name)
print(temp_folder)
rename(temp_folder, "Bar numérique")
