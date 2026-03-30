'''
Loop through file paths:
1) If it is pip, then simply parse the left hand dependency name
2) If it is npm, then use the python built-in json library
    - Index into dependenceis and devdepdencies and get the key
3) Make a request to the api to verify the logic
'''

from constants import DEPENDENCY_FILES
import re
import json
import requests

# A hashset of tuples: dependency name + version
dependencies = {}

'''
For pip
'''
def parse_pip_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if re.match(r'[a-zA-Z]', line):
                arr = line.split("==")
                dependency_name = arr[0]
                dependency_version = arr[1].strip()
                dependencies[dependency_name]=dependency_version
                # print(dependencies)

def parse_json_file(file_path):
    with open(file_path, 'r') as f:
        content = json.load(f)
        dep = content.get("dependencies") 
        dev_dependencies = content.get("devDependencies", {}) # Empty dict if there is no devDependencies in json

        for name, version in dep.items():
            dependencies[name] = version.lstrip("^&>=~")
        for name, version in dev_dependencies.items():
            if name.startswith("@"): continue
            dependencies[name] = version.lstrip("^&>=~")

for entry_name, entry_list in DEPENDENCY_FILES.items():
    if entry_name=="npm":
        for path in entry_list:
            parse_json_file(path)
    elif entry_name=="pip":
        for path in entry_list:
            parse_pip_file(path)

eol_packages = {}
packages_cannot_find = {}
healthy_packages = {}

# print(dependencies)

for name, ver in dependencies.items():
    res = requests.get(f"https://endoflife.date/api/v1/products/{name}")
    if res.status_code==404:
        packages_cannot_find[name] = ver
    elif res.status_code==200:
       data = res.json() 
       for release in data['result']['releases']:
            if release["name"] == ver.split(".")[0]:
                print(ver.split(".")[0])
                if release["isEol"]==False:
                    healthy_packages[name]=ver
                elif release["isEol"]==True:
                    eol_packages[name]=ver

print(healthy_packages)
print(packages_cannot_find)
print(eol_packages)

               