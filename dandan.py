import sys
import uvicorn
from typing import Optional
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import arrow

app = FastAPI()
dmhy_base_uri = "https://share.dmhy.org"
dmhy_type_and_subgroup_uri = f"{dmhy_base_uri}/topics/advanced-search?team_id=0&sort_id=0&orderby="
dmhy_list_uri = f"{dmhy_base_uri}/topics/list/page/1?keyword={{0}}&sort_id={{1}}&team_id={{2}}&order=date-desc"
unknown_subgroup_id = -1
unknown_subgroup_name = "未知字幕组"

def parse_list_tr(tr):
    td0 = tr.select("td")[0]
    td1 = tr.select("td")[1]
    td2 = tr.select("td")[2]
    td3 = tr.select("td")[3]
    td4 = tr.select("td")[4]
    c1 = len(td2.select("a"))
    td1_a0 = td1.select("a")[0]
    td2_a0 = td2.select("a")[0]
    td2_a_last = td2.select("a")[-1]
    td3_a0 = td3.select("a")[0]

    return {
        "Title": td2_a_last.text.strip(),
        "TypeId": int(td1_a0["href"].replace("/topics/list/sort_id/", "")),
        "TypeName": td1_a0.text.strip(),
        "SubgroupId": unknown_subgroup_id if c1 != 2 else int(td2_a0["href"].replace("/topics/list/team_id/", "")),
        "SubgroupName": unknown_subgroup_name if c1 != 2 else td2_a0.text.strip(),
        "Magnet": td3_a0["href"],
        "PageUrl": dmhy_base_uri + td2_a_last["href"],
        "FileSize": td4.text.strip(),
        "PublishDate": arrow.get(td0.select("span")[0].text.strip()).format("YYYY-MM-DD HH:mm:ss")
    }


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/subgroup")
def subgroup():
    res = requests.get(dmhy_type_and_subgroup_uri)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    options = soup.select("select#AdvSearchTeam option")
    subgroups = [{"Id": int(o["value"]), "Name": o.text} for o in options]
    subgroups.append({"Id": unknown_subgroup_id, "Name": unknown_subgroup_name})
    return {"Subgroups": subgroups}


@app.get("/type")
def type():
    res = requests.get(dmhy_type_and_subgroup_uri)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    options = soup.select("select#AdvSearchSort option")
    return {"Types": [{"Id": int(o["value"]), "Name": o.text} for o in options]}


@app.get("/list")
def list(keyword: str, subgroup: Optional[int] = 0, type: Optional[int] = 0, r: Optional[str] = None):
    res = requests.get(dmhy_list_uri.format(keyword, type, subgroup))
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.select("table#topic_list tbody tr")
    has_more = True if soup.select("div.nav_title > a:contains('下一頁')") else False

    return {"HasMore": has_more, "Resources": [parse_list_tr(tr) for tr in trs]}


if __name__ == "__main__":
    for arg in sys.argv:
        if arg.startswith("host="):
            run_host = arg.replace("host=", "")
            continue
        if arg.startswith("port="):
            run_port = int(arg.replace("port=", ""))
            continue

    uvicorn.run(app, host=run_host, port=run_port, debug=False)