import requests
from bs4 import BeautifulSoup
import datetime

days = ['월', '화', '수', '목', '금', '토', '일']
now = datetime.datetime.now()

depart = '서울'
destination = '영등포'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}

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


if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table', {'class': 'tbl_h'})

    trs = table.find_all('tr', {'class': ['clrGrey', '']})

    for i in range(0, len(trs)):
        trs = table.find_all('tr', {'class': ['clrGrey', '']})
        tds = trs[i].find_all('td')
        for i in range(0, len(tds)):
            if i == 0:
            # 직통/환승 여부
                print(tds[i].text.strip())
            elif i == 1:
            # 열차 종류
                if 'bg-00' in tds[i]['class']:
                    print('KTX')
                elif 'bg-01' in tds[i]['class']:
                    print('새마을호')
                elif 'bg-02' in tds[i]['class']:
                    print('무궁화호')
                elif 'bg-03' in tds[i]['class']:
                    print('통근열차')
                elif 'bg-04' in tds[i]['class']:
                    print('누리로')
                elif 'bg-06' in tds[i]['class']:
                    print('공항철도')
                elif 'bg-07' in tds[i]['class']:
                    print('KTX-산천 (호남)')
                elif 'bg-08' in tds[i]['class']:
                    print('KTX-경부')
                elif 'bg-09' in tds[i]['class']:
                    print('ITX-청춘')
                elif 'bg-10' in tds[i]['class']:
                    print('KTX-이음')
                elif 'bg-17' in tds[i]['class']:
                    print('SRT')
                else:
                    print('기타')
                trno = ''.join([i for i in tds[i].text if i.isdigit()])
                print(trno)

            elif i == 2:
            # 출발지 & 시각
                print(tds[i].text.strip())
            elif i == 3:
            # 도착지 & 시각
                print(tds[i].text.strip())
            elif i == 4:
            # 특실 여부
                trs = tds[i].find_all('a')
                if len(trs) > 0:
                    print('특실 있음')
                else:
                    if "-" in tds[i].text:
                        print('특실 존재하지 않음')
                    else:
                        print('특실 매진')
            elif i == 5:
            # 일반실 여부
                trs = tds[i].find_all('a')
                if len(trs) > 0:
                    print('일반실 있음')
                else:
                    if "-" in tds[i].text:
                        print('일반실 존재하지 않음')
                    else:
                        print('일반실 매진')
            elif i == 6:
            #유아석 여부
                trs = tds[i].find_all('a')
                if len(trs) > 0:
                    print('유아석 있음')
                else:
                    if "-" in tds[i].text:
                        print('유아석 존재하지 않음')
                    else:
                        print('유아석 매진')
            elif i == 7:
            #자유석 여부
                trs = tds[i].find_all('img')
                if len(trs) > 0:
                    if trs[0]['src'] == '/docs/2007/img/common/btn_seet_rsv2.gif':
                        print('역발매중')
                    else:
                        print('자유석 매진')
                else:
                    print('자유석 없음')
            
            elif i == 8:
            #인터넷 특가
                price = ''.join([i for i in tds[i].text if i.isdigit()])
                print('₩' + price)
            elif i == 9:
            #예약대기 여부
                trs = tds[i].find_all('img')
                if len(trs) > 0:
                    if trs[0]['src'] == '/docs/2007/img/common/icon_wait.gif':
                        print('예약대기 가능')
                    else:
                        print('예약대기 매진')
                else:
                    print('예약대기 신청 불가')
            elif i == 10:
            #경유역 (기존선ktx)
                trs = tds[i].find_all('img')
                if len(trs) > 0:
                    print('기존선 경유열차')
                else:
                    if 'bg-00' in tds[1]['class']:
                        print('고속선열차 (및 일반열차 전용역)')
                    else:
                        print('일반열차')
            elif i == 13:
            #소요 시간
                print(tds[i].text.strip())
                print('---')
            else:
                pass

else: 
    print(response.status_code)
