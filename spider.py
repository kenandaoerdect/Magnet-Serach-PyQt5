from lxml import etree
import requests
# import multiprocessing


class MagnetSpider(object):
    def __init__(self, url):
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        self.url = url

    def run(self):
        magnets = []
        titles = []
        pages_url = self._get_all_pages_url(self.url)
        # po = multiprocessing.Pool(2)
        for page_url in pages_url:
            one_page_files_url = self._get_one_page_all_file_url(page_url)
            for one_page_file_url in one_page_files_url:
                title, magnet = self._get_one_info(one_page_file_url)
                # title, magnet = po.apply_async(self._get_one_info, args=(one_page_file_url,)).get()
                titles.append(title)
                magnets.append(magnet)
        # po.close()
        # po.join()
        return titles, magnets

    def _get_all_pages_url(self, _url):
        '''获取所有页的链接'''
        pages_url = []
        pages_url.append(_url)
        temp_url = _url
        while True:
            if len(pages_url) >= 1:
                break
            reponse = requests.get(temp_url, headers=self.header)
            html = etree.HTML(reponse.text)
            next_page_idx = len(html.xpath('//*[@id="app"]/div[1]/div[2]/div/div[1]/div/ul/li'))
            try:
                next_page_url = html.xpath('//*[@id="app"]/div[1]/div[2]/div/div[1]/div/ul/li[%d]/a//@href'%next_page_idx)[0]
                next_page_url = r'https://findcl.com' + next_page_url
            except IndexError:
                break
            pages_url.append(next_page_url)
            temp_url = next_page_url
        # print(pages_url)
        return pages_url

    def _get_one_page_all_file_url(self, _url):
        '''获取一页的文件链接'''
        one_page_files_url = []
        reponse = requests.get(_url, headers=self.header)
        html = etree.HTML(reponse.text)
        one_page_num = len(html.xpath('//*[@id="app"]/div[1]/div[2]/div/div[1]/ul/li'))
        for i in range(one_page_num):
            one_url = html.xpath('//*[@id="app"]/div[1]/div[2]/div/div[1]/ul/li[%d]/a//@href'%(i+1))[0]
            one_url = r'https://findcl.com' + one_url
            one_page_files_url.append(one_url)
        return one_page_files_url

    def _get_one_info(self, _url):
        '''获取单个文件的标题和磁力链接'''
        reponse = requests.get(_url, headers=self.header)
        html = etree.HTML(reponse.text)
        try:
            magnet = html.xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[2]/div[2]/code/text()')[0]
        except IndexError:
            magnet = '磁力链接获取失败'
        file_type = html.xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/text()')[0]
        file_size = html.xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/text()')[0]
        file_size = (int(file_size)/(1024**3))
        try:
            file_title = html.xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/text()')[0]
        except IndexError:
            file_title = '文件名获取失败'
        title = '[{}][{}][{:.1f}GB]'.format(file_title, file_type, file_size)
        return title, magnet


if __name__ == '__main__':
    import time
    bigin_time = time.time()
    magnet_spider = MagnetSpider('https://findcl.com/list?q=ipx')
    a, b = magnet_spider.run()
    end_time = time.time()
    print(end_time-bigin_time)
    print(a)
    print(b)