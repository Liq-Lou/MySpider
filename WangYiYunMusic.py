import requests
from lxml import etree
import re
from Crypto.Cipher import AES
import execjs
import base64
import codecs
import random
import os

class WangYiYun():
    def __init__(self):
        self.headers = {
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
        }
        '''self.g = '0CoJUm6Qyw8W8jud'  # buU9L(["爱心", "女孩", "惊恐", "大笑"])的值
        self.b = "010001"  # buU9L(["流泪", "强"])的值
        # buU9L(Rg4k.md)的值
        self.c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.i = execjs.compile(r"""
                    function a(a) {
                        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
                        for (d = 0; a > d; d += 1)
                            e = Math.random() * b.length,
                            e = Math.floor(e),
                            c += b.charAt(e);
                        return c
                    }
                """).call('a', 16)  # 随机生成长度为16的字符串
        self.iv = "0102030405060708"  # 偏移量

    def to_16(self, key):
        while len(key) % 16 != 0:
            key += '\0'
        return str.encode(key)

    def AES_encrypt(self, text, key, iv):
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        encryptor = AES.new(self.to_16(key), AES.MODE_CBC, self.to_16(iv))
        encrypt_aes = encryptor.encrypt(str.encode(pad2(text)))
        encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypt_text

    def RSA_encrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_params(self, id):
        encText=str({'ids': "[" + str(id) + "]", 'br': 128000, 'csrf_token': ""})
        return self.AES_encrypt(self.AES_encrypt(encText,self.g, self.iv), self.i, self.iv)

    def get_encSecKey(self):
        return self.RSA_encrypt(self.i, self.b, self.c)

    def searhch_song(self, sname):
        url = 'https://music.163.com/weapi/search/suggest/web?csrf_token='
        data = {'params': self.get_params(sname),
                'encSecKey': self.get_encSecKey()}
        response = requests.post(url, headers=self.headers, data=data)
    '''
    def parse_song_id(self, song_id, song_name=random.random()):
        url = 'http://music.163.com/song/media/outer/url?id=' + song_id
        song_name = re.sub('\\\\|/|:|\*|\?|"|<|>|\|', ' ', song_name)  # windows文件命名规则
        if not os.path.exists('music'):
            os.mkdir('music')
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print('正在下载', song_name)
            with open('./music/' + song_name + '.mp4', 'wb') as f:
                f.write(response.content)
        except:
            pass

    def parse_song_list(self, song_list):
        url = 'https://music.163.com/playlist?id=' + song_list
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            html = etree.HTML(response.content.decode())
            song_id_list = html.xpath('//ul[@class="f-hide"]/li/a/@href')
            song_name_list = html.xpath('//ul[@class="f-hide"]/li/a/text()')
            for song_id, song_name in zip(song_id_list, song_name_list):
                self.parse_song_id(song_id[9:], song_name)
        except:
            pass

if __name__ =='__main__':
    wyy = WangYiYun()
    choose = input('1: 下载单曲  2: 下载歌单所有歌曲 任意键: 退出')
    if choose == '1':
        song_id = input('输入歌曲id')
        song_name = input('保存的文件名')
        wyy.parse_song_id(song_id, song_name)
    elif choose =='2':
        song_list = input('输入歌单id')
        print('将下载此歌单下所有歌曲, 不能免费听的除外')
        wyy.parse_song_list(song_list)
