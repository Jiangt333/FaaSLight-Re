import json
version_json = '\n{\n "date": "2023-04-22T13:47:13-0400",\n "dirty": false,\n "error": null,\n "full-revisionid": "14bb214bca49b167abc375fa873466a811e62102",\n "version": "1.24.3"\n}\n'

def get_versions():
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_version.py=get_versions=20')
    return json.loads(version_json)

