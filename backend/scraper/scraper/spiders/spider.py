import scrapy
from scraper.items import CursoItem

class QuotesSpider(scrapy.Spider):
    name = 'cursos'

    start_urls = [
        'https://brasil.io/dataset/cursos-prouni/cursos?page=' + str(x)
        for x in range (1,2048)
        ]

    def parse(self, response):
        for row in response.xpath('//*[@id="cursos-prouni"]//tbody/tr'):
            item = CursoItem()
            item["uf"] = row.xpath('td[1]//text()').extract_first()
            item["cidade"] = row.xpath('td[2]//text()').extract_first()
            item["universidade"] = row.xpath('td[3]//text()').extract_first()
            item['nome_campus'] = row.xpath('td[4]//text()').extract_first()
            item['curso'] = row.xpath('td[5]//text()').extract_first()
            item['grau'] = row.xpath('td[6]//text()').extract_first()
            item['turno'] = row.xpath('td[7]/text()').extract_first()
            item['mensalidade'] = row.xpath('td[8]//text()').extract_first()
            item['bolsas_integrais_cota'] = row.xpath('td[9]//text()').extract_first()
            item['bolsas_integrais_ampla'] = row.xpath('td[10]//text()').extract_first()
            item['bolsas_parciais_cota'] = row.xpath('td[11]//text()').extract_first()
            item['bolsas_parciais_ampla'] = row.xpath('td[12]//text()').extract_first()
            item['nota_integral_ampla'] = row.xpath('td[13]//text()').extract_first()
            item['nota_integral_cota'] = row.xpath('td[14]//text()').extract_first()
            item['nota_parcial_ampla'] = row.xpath('td[15]//text()').extract_first()
            item['nota_parcial_cota'] = row.xpath('td[16]//text()').extract_first()

            yield item
    