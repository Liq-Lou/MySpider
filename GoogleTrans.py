import requests
import execjs
import re


class Cocoa520():
    # 参数Google tk生成, 转载自https://github.com/cocoa520/Google_TK, 作者cocoa520
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def googletrans(tk, content, sl, tl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'\
                        'Chrome/72.0.3626.121 Safari/537.36'
    }
    url = 'https://translate.google.cn/translate_a/single?client=webapp&sl={}&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex' \
          '&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=2&ssel=3&tsel=0&kc=1&tk={}&q={}'.format(sl, tl, tk, content)
    response = requests.get(url, headers=headers)
    ans = re.findall('\["(.*?)",', re.findall('\[{3}.*?\]{2}', response.content.decode())[0])
    print('翻译结果:'.center(60, '-'))
    for eve_ans in ans:
        print(eve_ans)
    return ans


def main():
    while 1:
        lang = input("1:英>>中  2:中>>英:  0:退出  ")
        if lang == "1":
            sl, tl = 'en', 'zh-CN'
        elif lang == '2':
            tl, sl = 'en', 'zh-CN'
        elif lang == '0':
            break
        else:
            continue
        content = input('请输入内容>>>')
        if len(content) <=5000:
            Tk = Cocoa520()
            tk = Tk.getTk(content)
            ans = googletrans(tk, content, sl, tl)


if __name__ == '__main__':
    main()
