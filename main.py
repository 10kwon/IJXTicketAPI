from typing import Union
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import datetime
from fastapi.responses import HTMLResponse
import json

days = ['월', '화', '수', '목', '금', '토', '일']
now = datetime.datetime.now()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def 환영_페이지():
    return """
<html><head><title>API</title>
<meta name="description" content="대충 제한없는 api">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">

</head>
<body>


<aside class="bg-gray-800">
  <div class="p-8 md:p-12 lg:px-16 lg:py-24 bg-slate-900/50">
    <div class="max-w-lg text-center sm:text-left">
      <h2 class="text-2xl font-extrabold text-white sm:text-3xl md:text-5xl mb-2">
        어서 오세요!
      </h2>

      <p class="max-w-md text-white md:mt-6 md:text-lg md:leading-relaxed md:block">
        API는 처음이시라고요? API 사용법을 배우셔서 알잘딱하게 써먹어 보세요! 제한은 '당분간' 없습니다.
      </p>

      <div class="mt-4 sm:mt-8">
        <a class="inline-flex items-center px-8 py-3 text-white transition bg-gray-900 rounded-full shadow-lg focus:outline-none focus:ring focus:ring-yellow-400 hover:bg-gray-800" href="redoc/">
          <span class="text-sm font-medium"> Docs </span>

          <svg class="w-5 h-5 ml-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
          </svg>
        </a>
      </div>
    </div>
  </div>
</aside>

</body></html>
    """

@app.get("/k_tickets/{depart}/{destination}")
def 한국철도공사_승차권_가져오기(depart: str, destination: str, q: Union[str, None] = None):
    payload = {'selGoTrain': '05',
'txtPsgFlg_1': '1',
'txtPsgFlg_2': '0',
'txtPsgFlg_8': '0',
'txtPsgFlg_3': '0',
'txtPsgFlg_4': '0',
'txtPsgFlg_5': '0',
'txtSeatAttCd_3': '000',
'txtSeatAttCd_2': '000',
'txtSeatAttCd_4': '015',
'selGoTrainRa': '05',
'radJobId': '1',
'txtGoStart': depart,
'txtGoEnd': destination,
'selGoYear': str(now.year),
'selGoMonth': str(now.month),
'selGoDay': str(now.day),
'selGoHour': str(now.hour),
'txtGoHour': str(now.strftime("%H%M%S")),
'txtGoYoil': days[now.weekday()],
'selGoSeat1': '015',
'txtPsgCnt1': '1',
'txtPsgCnt2': '0',
'txtGoPage': '1',
'txtGoAbrdDt': str(now.strftime("%Y%m%d")),
'checkStnNm': 'Y',
'SeandYo': 'N',
'chkInitFlg': 'Y',
'txtMenuId': '11',
'ra': '1',
'strChkCpn': 'N',
'txtSrcarCnt': '0',
'txtSrcarCnt1': '0',
'hidRsvTpCd': '03',
'txtPsgTpCd1': '1',
'txtPsgTpCd2': '3',
'txtPsgTpCd3': '1', 'txtPsgTpCd5': '1', 'txtPsgTpCd7': '1', 'txtPsgTpCd8': '3', 'txtDiscKndCd1': '000', 'txtDiscKndCd2': '000', 'txtDiscKndCd3': '111', 'txtDiscKndCd5': '131', 'txtDiscKndCd7': '112', 'txtDiscKndCd8': '321', 'txtCompaCnt1': '0', 'txtCompaCnt2': '0', 'txtCompaCnt3': '0', 'txtCompaCnt4': '0', 'txtCompaCnt5': '0', 'txtCompaCnt6': '0', 'txtCompaCnt7': '0', 'txtCompaCnt8': '0'}
    response = requests.post('https://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do', data=payload, headers=headers)
    jsonRtn = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
    
        table = soup.find('table', {'class': 'tbl_h'})
    
        trs = table.find_all('tr', {'class': ['clrGrey', '']})
        pari = 1
        for i in range(0, len(trs)):
            trs = table.find_all('tr', {'class': ['clrGrey', '']})
            tds = trs[i].find_all('td')
            
            for i in range(0, len(tds)):
                if i == 0:
                # 직통/환승 여부
                    transfer = tds[i].text.strip()
                elif i == 1:
                # 열차 종류
                    if 'bg-00' in tds[i]['class']:
                        train = 'KTX'
                    elif 'bg-01' in tds[i]['class']:
                        train = '새마을호'
                    elif 'bg-02' in tds[i]['class']:
                        train = '무궁화호'
                    elif 'bg-03' in tds[i]['class']:
                        train = '통근열차'
                    elif 'bg-04' in tds[i]['class']:
                        train = '누리로'
                    elif 'bg-06' in tds[i]['class']:
                        train = '공항철도'
                    elif 'bg-07' in tds[i]['class']:
                        train = 'KTX-산천 (호남)'
                    elif 'bg-08' in tds[i]['class']:
                        train = 'KTX-경부'
                    elif 'bg-09' in tds[i]['class']:
                        train = 'ITX-청춘'
                    elif 'bg-10' in tds[i]['class']:
                        train = 'KTX-이음'
                    elif 'bg-17' in tds[i]['class']:
                        train = 'SRT'
                    else:
                        train = '기타'
                    trno = ''.join([i for i in tds[i].text if i.isdigit()])
                    no = trno
    
                elif i == 2:
                # 출발지 & 시각
                    departure = tds[i].text.strip()
                elif i == 3:
                # 도착지 & 시각
                    destination = tds[i].text.strip()
                elif i == 4:
                # 특실 여부
                    trs = tds[i].find_all('a')
                    if len(trs) > 0:
                        specialRoom = 'true'
                    else:
                        if "-" in tds[i].text:
                            specialRoom = 'false'
                        else:
                            specialRoom = 'soldout'
                elif i == 5:
                # 일반실 여부
                    trs = tds[i].find_all('a')
                    if len(trs) > 0:
                        normalRoom = 'true'
                    else:
                        if "-" in tds[i].text:
                            normalRoom = 'false'
                        else:
                            normalRoom = 'soldout'
                elif i == 6:
                #유아석 여부
                    trs = tds[i].find_all('a')
                    if len(trs) > 0:
                        infantRoom = 'true'
                    else:
                        if "-" in tds[i].text:
                            infantRoom = 'false'
                        else:
                            infantRoom = 'soldout'
                elif i == 7:
                #자유석 여부
                    trs = tds[i].find_all('img')
                    if len(trs) > 0:
                        if trs[0]['src'] == '/docs/2007/img/common/btn_seet_rsv2.gif':
                            freeRoom = 'true'
                        else:
                            freeRoom = 'soldout'
                    else:
                        freeRoom = 'false'
                
                elif i == 8:
                #인터넷 특가

                    price = ''.join([i for i in tds[i].text if i.isdigit()])
                    if price.endswith('5'):
                        price = price[:-1]
                        
                elif i == 9:
                #예약대기 여부
                    trs = tds[i].find_all('img')
                    if len(trs) > 0:
                        if trs[0]['src'] == '/docs/2007/img/common/icon_wait.gif':
                            reserve = 'true'
                        else:
                            reserve = 'soldout'
                    else:
                        reserve = 'false'
                elif i == 10:
                #경유역 (기존선ktx)
                    trs = tds[i].find_all('img')
                    if len(trs) > 0:
                        railway = 'legacy'
                    else:
                        if 'bg-00' in tds[1]['class']:
                            railway = 'ktx'
                        else:
                            railway = 'n/a'
                elif i == 13:
                #소요 시간
                    time = tds[i].text.strip()
                    pari = pari+1
                    jsonRtn.append({'transfer': transfer, 'train': train, 'no': no, 'departure': departure, 'destination': destination, 'specialRoom': specialRoom, 'normalRoom': normalRoom, 'infantRoom': infantRoom, 'freeRoom': freeRoom, 'price': price, 'reserve': reserve, 'railway': railway, 'time': time})
                else:
                    pass
                
        return jsonRtn
    
    else: 
        return 'error'
    
@app.get("/a_tickets/{depart}/{destination}")
def 공항철도_승차권_가져오기(depart: str, destination: str, q: Union[str, None] = None):
    payload = {
        'language': '',
        'upMenuId': 'AR10',
        'menuId': 'AR1010',
        'medaDvsn': '01',
        'discCode': '',
        'discType': '',
        'entpr': '',
        'discSize': '',
        'dptrStnCd': depart,
        'arrvStnCd': destination,
        'dptrDate': str(now.strftime("%Y-%m-%d")),
        'dptrTime': str(now.strftime("%H%M")),
        'psnAdult': '1',
        'psnChild': '0'
    }
    response = requests.post('https://www.airportrailroad.com/rt/tktBstk.do', data=payload, headers=headers)
    jsonRtn = []
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find('ul', {'class': 'trainList'})
        trs = list.find_all('li')
        
        for i in range(0, len(trs)):
            trs = list.find_all('li')
            tds = trs[i].find_all('div')
            for i in range(0, len(tds)):
                if i == 0:
                #열차번호
                    train = '공항철도'
                    no = tds[i].text.strip()
                elif i == 1:
                    departTime = tds[i].text.strip()
                elif i == 2:
                    arriveTime = tds[i].text.strip()
                    jsonRtn.append({'train': train, 'no': no, 'departTime': departTime, 'arriveTime': arriveTime})
                else:
                    pass
        return jsonRtn
    else:
        return 'error'