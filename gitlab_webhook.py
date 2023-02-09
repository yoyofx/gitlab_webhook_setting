# encoding: utf8
import os
import sys,getopt
import json
import time, datetime
import requests
import urllib.parse
import urllib3

projectList = ["AutoAftermarket/infrastructure/git-stats"]

params= {
    "token":"",
    "webhook":""
}

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "t:w:", ["token=", "webhook="])
    except getopt.GetoptError:
        sys.exit(2)
    print('action')
    for opt, arg in opts:
        if opt in ("-t", "--token"):
            params['token'] = arg
        elif opt in ("-w", "--webhook"):
            params['webhook'] = arg
    
    if (params["webhook"] == "" or params["token"] == ""):
        print("请检查token或webhook参数！")
        sys.exit(2)

    print('action')
    urllib3.disable_warnings()

    errorFile = open('./errors.txt','w',encoding='utf-8')
    gitlabApi = "https://gitlab2.bitautotech.com/api/v4"
    for p in projectList:
        projectNameByEncode = urllib.parse.quote(p, safe="")
        print(projectNameByEncode)
        reuqestUrl = "%s/projects/%s/hooks" % (gitlabApi, projectNameByEncode)
        hasHookAndDelete(reuqestUrl)
        stateCode = postData(reuqestUrl,{
            "url": params['webhook'],
            "push_events": "false",
            "merge_requests_events": "true",
            "enable_ssl_verification":"false"
        })
        print("项目:",p,"设置webhook状态",stateCode)
        if stateCode != 200:
            errorFile.write(p + '\n')
    errorFile.close()


def postData(url,data):
    try:
        r = requests.post(url,headers=getRequestHeaders(),json=data, verify=False)
    except Exception as e:
        print(e)
        return 401
    else:
        return 200
    return 200


def hasHookAndDelete(url):
    r = requests.get(url,headers=getRequestHeaders(), verify=False)
    hooks = r.json()
    if len(hooks) > 0:
        hook_id = hooks[0]["id"]
        print("found hook, that delete is:",hook_id)
        r = requests.delete(url + "/"+ str(hook_id),headers=getRequestHeaders(), verify=False)


def getRequestHeaders():
    headers = {
        "PRIVATE-TOKEN": params['token'],
        "Content-Type": "application/json"
    }
    return headers


if __name__ == "__main__":
    main(sys.argv[1:])
