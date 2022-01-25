from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.tradingview.com/chart/KYErt3LL'
url_contents = urllib.request.urlopen(url).read()

soup = BeautifulSoup(url_contents,'html.parser')
tab = soup.find_all('canvas')
print(tab)