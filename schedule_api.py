import re, requests

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
def find_teacher_rating(teacher_name: str):
    result = {}
    url = "https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&" \
          "queryBy=teacherName&schoolName=University+of+California+Irvine&schoolID=1074%s&query=" + teacher_name
    page = requests.get(url=url, headers=headers)
    pageData = page.text
    pageDataTemp = re.findall(r'ShowRatings\.jsp\?tid=\d+', pageData)
    if len(pageDataTemp) > 0:
        finalUrl = "https://www.ratemyprofessors.com/" + pageDataTemp[0]
        page = requests.get(finalUrl).text
        result["rating"] = page[page.find("avgRating")+11:page.find("avgRating") + 14]
        result["take again"] = page[page.find("uof32n-1 kkESWs")+17:page.find("uof32n-1 kkESWs")+20]
    return result

