import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css('section[id=numerical-index]')
        tbody = section.css('tbody')
        all_peps = tbody.css('a::attr(href)')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.css(
            'li:contains("PEP Index") + li::text'
        ).get().replace('PEP ', '')
        name = response.css('h1.page-title::text').get()
        status = response.css('dt:contains("Status") + dd::text').get()
        yield PepParseItem({
            'number': int(number),
            'name': name,
            'status': status
        })
