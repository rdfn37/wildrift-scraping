import json
import scrapy
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Chrome()
# driver.get("https://wildrift.leagueoflegends.com/en-us/champions/akali/")
# print('Open')
# driver.execute_script("window.scrollTo(0, 620)")
# time.sleep(1)
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CLASS_NAME, "thumbnail-21xPX"))
#     )
#     for i in element:
#         i.click()
#         time.sleep(1)
#         print(i.get_attribute('innerHTML'))
# finally:
#     print('Close')
#     driver.quit()


def getNames():

    names = open('names.json',)

    data = json.load(names)

    allChamps = []

    for i in data:
        allChamps.append('https://wildrift.leagueoflegends.com/en-us/champions/' +
                         i['name'].lower().replace('. ', '-').replace(' ', '-').replace("'", "-"))

    return allChamps

urlList = getNames()


driver = webdriver.Chrome()
class Wildspider(scrapy.Spider):
    name = 'wild'

    # Returns a json with all names and imgs url.

    # start_urls = ['https://wildrift.leagueoflegends.com/pt-br/champions/']

    # def parse(self, res):
    #     for champions in res.css('li.championCardItem-576IH'):
    #         yield {
    #             'name': champions.css('h3::text').get(),
    #             'img': champions.css('img.championImage-2lwUs').attrib['src']
    #         }

    # start_urls = urlList
    start_urls = ['https://wildrift.leagueoflegends.com/en-us/champions/akali', 'https://wildrift.leagueoflegends.com/en-us/champions/darius']

    
    def parse(self, res):
        heroContent = res.css('div.heroContent-1_EhD')
        skills = []

        driver.get(res.request.url)
        print('Open')
        driver.execute_script("window.scrollTo(0, 620)")
        # time.sleep(1)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "thumbnail-21xPX"))
            )

            skillImgs = res.xpath('//div[@class="abilitiesDetailsWrapper-3nyLR"]//ul//li//span//img//@src').getall()
            for index, i in enumerate(element):
                i.click()
                # time.sleep(0.5)
                tes = scrapy.Selector(text=driver.page_source)

                skillName = tes.xpath('//span[@data-testid="abilities:abilityname"]//text()').get()
                skillType = tes.xpath('//span[@data-testid="abilities:abilitytype"]//text()').get()
                skillVideo = tes.xpath('//video[@data-testid="abilities:video"]//source//@src').get()
                skillImg = skillImgs[index]

                # time.sleep(0.5)

                skill = {
                    'skillName': skillName,
                    'skillType': skillType,
                    'skillVideo': skillVideo,
                    'skillImg': skillImg
                }

                skills.append(skill)
                # print(i.get_attribute('innerHTML'))
        except:
            print('Close')
            driver.quit()

        yield {
            'name': heroContent.css('h3.championName-1JnC5::text').get(),
            'subtitle': heroContent.css('p.championSubtitle-YAx7w::text').get(),
            'role': heroContent.css('span.roleName-33zEx::text').get(),
            'difficulty': heroContent.css('span.difficultyName-3NSea::text').get(),
            'heroVideo': res.css('div.heroVideo-1Jeta').css('source').attrib['src'],
            'url': res.request.url,
            'skills': skills
        }
