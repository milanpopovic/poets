import requests
#par = {'lat': '44.818611', 'lng': '20.468056', 'date':'2018-02-17'}
#r = requests.get('https://api.sunrise-sunset.org/json', params=par)
#print(r.text)
#print(dict(r.json())['results']['sunrise'])

r = requests.get('http://www.stands4.com/services/v2/poetry.php?uid=6774&tokenid=7etjoGkAV1hsT1r1&term=grass&format=xml')
print(r.text)