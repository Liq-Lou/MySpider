# MySpider
</br>

### 项目介绍
**运行环境均为python3.71**
</br>
**第三方库requests, lxml经常用, 不再提**
1. **天气查询**:
- 功能: 查询实时天气, 今日天气, 7天天气预报
- 注: 自用方便, 直接回车输出"萧山"天气

</br>

<br>

2. **谷歌翻译**:
- 功能: 中英文互译

</br>

<br>

3. **scrapy爬取Moe的图片**:
- 功能: 爬取http://moe.005.tv/ 萌化图片下的萌图(http://moe.005.tv/moeimg/tb/)
- 需要安装的包: scrapy, pillow
- 注: 网站没反爬措施, 15分钟爬了近1.2万张图片还没爬完, 避免给服务器压力没再继续

</br>

<br>

4. **网易云音乐下载**:
- 功能: 歌曲下载, 歌单下所有歌曲下载
- 不足: 需要手动上网复制歌曲/歌单的id, 有点麻烦; 想做输入歌名自动搜索的, 鉴于能力有限, params,encSecKey参数未能解密, 3.71下crypto库问题也多, 网易云搜索页面只能以后在看了

</br>
