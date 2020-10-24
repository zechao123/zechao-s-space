# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IpAgent89IpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #代理地址
    ip_url = scrapy.Field()
    # 地理位置
    address = scrapy.Field()
    # 运营商
    perators= scrapy.Field()
    # 收录时间
    recording_time = scrapy.Field()
