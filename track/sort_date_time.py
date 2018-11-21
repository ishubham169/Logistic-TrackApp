from collections import defaultdict;
import requests;
import urllib.parse;
from collections import OrderedDict
from ast import literal_eval
def sort_it(json_data):
    my=[]
    j=1
    for i in json_data:
        o=[]
        o.append(i['ScanDetail']['ScanDateTime'])
        o.append(j)
        j+=1
        my.append(o)
    my.sort()
    return(my)
def return_scans(json_data):
    json_data=json_data["ShipmentData"][0]["Shipment"]["Scans"]
    j=1
    d=dict()
    for i in json_data:
        d[j]=i
        j+=1
    p=sort_it(json_data)
    ans=[]
    for i in p:
        ans.append(d[i[1]])
    return(ans)
def map_status(scans):
    status_code=[]
    f=dict()
    for i in scans:
        status=i['ScanDetail']['StatusCode']
        if((status in f)== False):
            status_code.append(status)
            f[status]=1
    status_map=['A','B','C','D','E']
    what_status=dict()
    j=0
    for i in range(0,len(status_code)):
        what_status[status_code[i]]=status_map[j]
        j+=1
        if(j==len(status_map)):
            j=0
    return(what_status)
def solve(track_id_list,comp):
    ans=OrderedDict()
    track_id_list=track_id_list.split(',')
    for track_id in track_id_list:
        api='https://track.delhivery.com/api/status/packages/json/?';
        url=api+urllib.parse.urlencode({'waybill':track_id});
        json_data=requests.get(url).json()
        scans=return_scans(json_data)
        history=[]
        what_status=map_status(scans)
        map1=defaultdict(list)
        for i in scans:
            map1[what_status[i['ScanDetail']['StatusCode']]].append(i)
        status_list=[]
        d=dict()
        for i in scans:
            status=what_status[i['ScanDetail']['StatusCode']]
            if( (status in d) == False):
                status_list.append(status)
                
                d[status]=1
        his=[]
        for i in status_list:
            d=OrderedDict()
            d["STATUS"]=i
            d["LAST_COMPANY_STATUS"]=map1[i][-1]['ScanDetail']['StatusCode']
            d["LAST_CITY"]=map1[i][-1]['ScanDetail']['CityLocation']
            d["LAST_INSTRUCTION"]=map1[i][-1]['ScanDetail']['Instructions']
            d["LAST_MESSAGE"]=map1[i][-1]['ScanDetail']['Scan']
            h1=[]
            for j in map1[i]:
                d1=OrderedDict()
                d1["COMPANY_STATUS"]=j['ScanDetail']['StatusCode']
                d1["MESSAGE"]=j['ScanDetail']['Scan']
                d1["INSTRUCTION"]=j['ScanDetail']['Instructions']
                d1["DATE-TIME"]=j['ScanDetail']['ScanDateTime']
                d1["CITY-LOCATION"]=j['ScanDetail']['CityLocation']
                h1.append(d1)
            d["INFO"]=h1
            his.append(d)
        track=OrderedDict()
        ans1=OrderedDict()
        p=scans[-1]['ScanDetail']['StatusCode']
        ans1['STATUS']=what_status[p]
        ans1['COMPANY_STATUS']=scans[-1]['ScanDetail']['StatusCode']
        ans1['COMPANY']=comp
        ans1['TIME']=scans[-1]['ScanDetail']['ScanDateTime']
        ans1['STATE']=scans[-1]['ScanDetail']['CityLocation']
        ans1['HISTORY']=his
        ans[track_id]=ans1
    return(ans) 