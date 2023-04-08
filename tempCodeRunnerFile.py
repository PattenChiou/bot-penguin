str1=""
r=requests.get("https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON")
content=r.json()
for i in range(0,len(content["records"])):
    if content["records"][i]["sitename"]==x or content["records"][i]["county"]==x :
        str1+=content["records"][i]["sitename"]+":"+content["records"][i]["aqi"]+"\n"+"(%s)"%content["records"][i]["publishtime"]+"\n"