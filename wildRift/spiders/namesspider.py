import scrapy

# Returns a json with all names and imgs url.
class Namesspider(scrapy.Spider):
    name = 'names'

    start_urls = ['https://wildrift.leagueoflegends.com/en-us/champions/']

    def parse(self, res):
        for champions in res.css('li.ChampionList-module--championCardItem--RVNEa'):
            yield {
                'name': champions.css('h3::text').get(),
                'url': champions.css('a.ChampionListCard-module--championListCardWrapper--BJ2LG').attrib['href'],
                'image': champions.css('img').xpath('@src').get()
            }
