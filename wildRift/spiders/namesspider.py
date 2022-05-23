import scrapy

# Returns a json with all names and imgs url.
class Namesspider(scrapy.Spider):
    name = 'names'

    start_urls = ['https://wildrift.leagueoflegends.com/en-us/champions/']

    def parse(self, res):
        for champions in res.css('li.championCardItem-576IH'):
            yield {
                'name': champions.css('h3::text').get(),
                'img': champions.css('img.championImage-2lwUs').attrib['src'],
                'url': champions.css('a.championListCardWrapper-3Kf-3').attrib['href']
            }
