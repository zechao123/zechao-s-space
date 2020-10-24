import scrapy
from scrapy import Request
from urllib.parse import urljoin

class IpAgentSpider(scrapy.Spider):
    name = 'ip_agent'
    allowed_domains = ['www.89ip.cn']
    start_urls = ['https://www.89ip.cn/index_1.html']
    page_url = None


    def parse(self, response):
        ip_list=response.xpath('//table[@class="layui-table"]/tbody/tr')
        for elem in ip_list:
            ip_url=elem.xpath('normalize-space(./td[1]/text())').extract()
            port=elem.xpath('normalize-space(./td[2]/text())').extract()
            perators=elem.xpath('normalize-space(./td[3]/text())').extract()
            recording_time=elem.xpath('normalize-space(./td[4]/text())').extract()
            item = dict(
                ip_url=ip_url,
                port=port,
                perators=perators,
                recording_time=recording_time
            )
            yield item
        # 获取下一页url
        if item is not None:
            self.page_url = response.xpath('//*[@id="layui-laypage-1"]/a[8]/@href').extract()
        # page_url 是一个数组
        else:
             self.page_url=None
        for next_url in self.page_url:

            yield Request(urljoin("https://www.89ip.cn", next_url), callback=self.parse)

