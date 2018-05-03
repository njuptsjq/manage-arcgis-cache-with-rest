import requests
import re

def generateToken(GetTokenURL,username,password):
    URL = GetTokenURL
    requestData = {
        'f':'json',
        'username':username,
        'password':password,
        'client':'requestip',
        'expiration':60
    }
    resp = requests.get(URL,requestData)
    if resp.status_code==200:
        TokenObj = resp.json()
        return TokenObj
    return None

def manageCacheTile(manageCacheURL,token,serviceURL,Scales):
    URL = manageCacheURL
    requestsData = {
        'f':'json',
        'token':token,
        'service_url':serviceURL,
        'levels':Scales,
        'thread_count':3,
        'update_mode':'RECREATE_ALL_TILES',
    }
    resp = requests.post(URL,requestsData)
    if resp.status_code==200:
        JobObj = resp.json()
        return JobObj['jobId']
    return None

def paraseServiceURL(ServiceURL_HTTP):
    #services/JNPM/JNPM_Edit/FeatureServer
    UsefulURL = re.findall(r'services/(.*?)/MapServer',ServiceURL_HTTP)
    if UsefulURL is not None:
        return UsefulURL[0]+":MapServer"
    return None

def getScals(ServiceURL_HTTP):
    resp = requests.get(ServiceURL_HTTP)
    Scales = ''
    if resp.status_code==200:
        scales = re.findall(r'Scale:(.*?)</li>',resp.text)
        for each in scales:
            Scales = Scales + each + ';'
        return Scales
    return None


tokenAPI = "http://172.21.212.114:6080/arcgis/tokens/generateToken"
token = generateToken(tokenAPI,'siteadmin','AgsVge100')["token"]
ServiceURL_HTTP='http://172.21.212.114:6080/arcgis/rest/services/SampleWorldCities/MapServer'
cacheManageAPI = "http://172.21.212.114:6080/arcgis/rest/services/System/CachingTools/GPServer/Manage%20Map%20Cache%20Tiles/submitJob"
ServiceURL = paraseServiceURL(ServiceURL_HTTP)
Scales = getScals(ServiceURL_HTTP)
jobId = manageCacheTile(cacheManageAPI,token,ServiceURL,Scales)
# print(paraseServiceURL('http://172.21.212.114:6080/arcgis/rest/services/JNPM/JNPM_Edit/MapServer')    )
# http://172.21.212.114:6080/arcgis/rest/services/System/CachingTools/GPServer/Manage Map Cache Tiles/jobs/<jobid>
# print(getScals(ServiceURL))