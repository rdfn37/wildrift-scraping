import json
import scrapy
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getNames():

    names = open('names.json',)

    data = json.load(names)

    allChamps = []

    for i in data:
        allChamps.append('https://wildrift.leagueoflegends.com' + i['url'])

    return allChamps


urlList = getNames()
# urlList = [getNames()[11], getNames()[22]]

driver = webdriver.Chrome()

# Returns more detailed information on Wild Rift champions.
class Wildspider(scrapy.Spider):
    name = 'wild'

    start_urls = ['https://wildrift.leagueoflegends.com/en-us/champions/ahri']

    def parse(self, res):

        for link in urlList:
            driver.get(link)
            currentChamp = scrapy.Selector(text=driver.page_source)

            print('Open')
            driver.execute_script("window.scrollTo(0, 650)")

            heroContent = currentChamp.css('div.ChampionDetailHero-module--heroContent--qV1Vv')
            skills = []
            skins = []

            try:
                element = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[@class="ChampionAbilities-module--abilitiesWrapper--Y7oJG"]//div//ul//li//span'))
                )

                skillImgs = currentChamp.xpath(
                    '//div[@class="ChampionAbilities-module--abilitiesDetailsWrapper--pzoo6"]//ul//li//span//img//@src').getall()
                for index, i in enumerate(element):
                    i.click()
                    currentSkill = scrapy.Selector(text=driver.page_source)

                    skillName = currentSkill.xpath(
                        '//span[@data-testid="abilities:abilityname"]//text()').get()
                    skillType = currentSkill.xpath(
                        '//span[@data-testid="abilities:abilitytype"]//text()').get()
                    skillVideo = currentSkill.xpath(
                        '//video[@data-testid="abilities:video"]//source//@src').get()
                    skillImg = skillImgs[index]

                    if skillType == "4":
                        skillType = "ULTIMATE"

                    skill = {
                        'skillName': skillName,
                        'skillType': skillType,
                        'skillVideo': skillVideo,
                        'skillImg': skillImg
                    }

                    skills.append(skill)

                driver.execute_script("window.scrollTo(0, 1850)")

                skinIcons = currentChamp.css(
                    'li.SkinsSection-module--thumbnail--CGbJK').xpath('.//span//img//@src').getall()

                iconClick = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[@class="SkinsSection-module--skinsListWrapper--lJstv"]//ul//li//span'))
                )

                for skinIconIndex, skinIcon in enumerate(iconClick):
                    skinIcon.click()

                    currentSkin = scrapy.Selector(text=driver.page_source)

                    skinImage = currentSkin.xpath(
                        '//img[@data-testid="skins:skin-image"]//@src').get()

                    skinName = currentSkin.xpath(
                        '//span[@class="SkinsSection-module--skinName--G8Yg9"]//text()').get()

                    skin = {
                        'skinImage': skinImage,
                        'skinIcon': skinIcons[skinIconIndex],
                        'skinName': skinName
                    }

                    skins.append(skin)

            except:
                print('Close')
                driver.quit()

            yield {
                'name': heroContent.css('h3.ChampionDetailHero-module--championName--eyJEV::text').get(),
                'subtitle': heroContent.css('p.ChampionDetailHero-module--championSubtitle--3twYV::text').get(),
                'role': heroContent.css('span.ChampionDetailHero-module--roleName--If7UP::text').get(),
                'difficulty': heroContent.css('span.ChampionDetailHero-module--difficultyName--ZpgVc::text').get(),
                # 'heroVideo': currentChamp.css('div.heroVideo-1Jeta').css('source').attrib['src'],
                'skills': skills,
                'skins': skins
            }

        print("Scraping completed")
        driver.quit()
