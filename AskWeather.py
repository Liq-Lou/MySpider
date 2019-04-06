import requests
from lxml import etree
import re
import time
import traceback

def getCityId(_city):
    url = 'http://mobile.weather.com.cn/js/citylist.xml'
    try:
        response = requests.get(url,  timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:
        traceback.print_exc()
    while True:
        r = re.compile('<d\sd1="\d{9}"\sd2="%s"\sd3="\w*?"\sd4=".*?"/>' % _city, re.M)
        city_msg = re.findall(r, response.text)
        if len(city_msg) > 0:
            break
        else:
            r = re.compile('<d\sd1="\d{9}"\sd2=".{1,10}"\sd3="%s"\sd4=".*?"/>' % _city, re.M)
            city_msg = re.findall(r, response.text)
            if len(city_msg) > 0:
                break
            else:
                print('你的输入有误,请重试')
                _city = input('输入城市>>>>')
    if len(city_msg) < 2:
        city_id = city_msg[0].split('"')[1]
        city_name = city_msg[0].split('"')[3]
    else:
        n = 0
        for i in city_msg:
            print(n, i.split('"')[7])
            n += 1
        ans =input('你输入的地址不唯一, 请选择省份')
        try:
            city_id = city_msg[int(ans)].split('"')[1]
            city_name = city_msg[int(ans)].split('"')[3]
        except:
            traceback.print_exc()
    return city_id, city_name


def oneweek(city_id, city_name, headers):
    url = 'http://www.weather.com.cn/weather/{}.shtml' .format(city_id)
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.content.decode())
    max_temp = html.xpath("//p[@class='tem']/span/text()")
    min_temp = html.xpath("//p[@class='tem']/i/text()")
    date = html.xpath("//div[@id='7d']/ul[@class='t clearfix']/li/h1/text()")
    weather = html.xpath("//div[@id='7d']/ul[@class='t clearfix']/li/p[@class='wea']/text()")
    wind_level = html.xpath("//div[@id='7d']/ul[@class='t clearfix']/li/p[@class='win']/i/text()")
    print("{}未来7天天气:".format(city_name).center(60, '-'))
    for i, j, k, l, m in zip(date, max_temp, min_temp, weather, wind_level):
        print(i, j, k, '\t', l.ljust(7, '　'), m)


def oneday(city_id, city_name, headers):
    t = int(round(time.time(), 3) * 1000)
    url = 'http://d1.weather.com.cn/sk_2d/101210101.html?_='.format(city_id) + str(t)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:
        traceback.print_exc()

    da = re.findall('"date":"(.*?)"', response.text)[0]
    temp =re.findall('"temp":"(.*?)"', response.text)[0]
    weather = re.findall('"weather":"(.*?)"', response.text)[0]
    wd = re.findall('"WD":"(.*?)"', response.text)[0]
    ws = re.findall('"WS":"(.*?)"', response.text)[0]
    sd = re.findall('"SD":"(.*?)"', response.text)[0]
    print("{}实时天气:".format(city_name).center(60, '-'))
    print(da, weather + '\t当前温度:' + temp+'℃\t风向:'+wd, ws+'\t当前湿度:'+sd)
    nexthours(city_id, city_name, headers)

def nexthours(city_id, city_name, headers):
    url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(city_id)
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.content.decode())
    day = time.localtime(time.time()).tm_mday
    r1 = re.compile('{"1d".*"?7d"', re.S)
    s1 = re.findall(r1, response.text) # 筛选文本段
    r2 = re.compile('%s日\d{2}时,.*?级' % day, re.M)
    s2 = re.findall(r2, str(s1))   # 今天各时间段天气
    print('{}天气预报'.format(city_name).center(60, '-'))
    for i in s2:
        m1, m2, m3, m4, m5, m6 = i.split(',')
        print(m1, m3, m4, m5, m6)


def main():
    headers = {
        'Referer': 'http://www.weather.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    _city = input('输入城市>>>>')
    if len(_city) == 0:  # 默认输出萧山天气
        city_id, city_name = 101210102, '萧山'
    else:
        city_id, city_name = getCityId(_city)
    while True:
        choose = input('0: 今日天气 1: 7日天气 任意键:退出>>>>')
        if choose == '0':
            oneday(city_id, city_name, headers)
            print(''.center(60, '-'))
        elif choose == '1':
            oneweek(city_id, city_name, headers)
            print(''.center(60, '-'))
        else:
            break


if __name__ == '__main__':
    main()

