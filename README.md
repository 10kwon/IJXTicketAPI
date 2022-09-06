# IJXTicketAPI
Injeon Express, Korail Ticket API

## How to use
### Korail API
`http://[YOUR API ADDRESS]:[PORT]/k_tickets/Departure/Destination`
 * Departure (str): Your station to depart
 (e.g 서울, 오송, 광명)
 * Destination (str): Your destination
 (e.g 대전, 천안아산, 부산)

#### Response
```
[{"transfer":"직통","train":"KTX","no":"049","departure":"서울17:00","destination":"오송17:45","specialRoom":"true","normalRoom":"true","infantRoom":"false","freeRoom":"true","price":"18500","reserve":"false","railway":"ktx","time":"00:45"}]
```
##### Basic Train Info
 * Transfer (직통/환승): Whether train should be transferred or not.
 * Train (str): Type of train
 * No (int): Train's Identification Number
 * Departure (서울21:00): Train's Departure station & Departure time
 * Destination (부산23:00): Train's Destination station & Time
 * Price (int): Train's price (adult)
 * Railway (ktx, n/a, legacy): Highspeed railway, Not applicable (Saemaul, Mugungwha), Legacy (KTX running in legacy railway)
 * Time (00:00): Time of travel

##### Room
 * SpecialRoom (true/false/soldout): 특실 (Only applicable to KTX and tourism train)
 * NormalRoom (true/false/soldout): 일반실 (N/A for tourism train)
 * InfantRoom (true/false/soldout): 유아실 (Only applicable to Mugungwha and Saemaul)
 * FreeRoom (true/false/soldout): 자유석 (If true, sold in station with additional approve)

### AREX API
To Be Done