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
            driver.execute_script("window.scrollTo(0, 620)")

            heroContent = currentChamp.css('div.heroContent-1_EhD')
            skills = []
            skins = []

            try:
                element = WebDriverWait(driver, 100).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "thumbnail-21xPX"))
                )

                skillImgs = currentChamp.xpath(
                    '//div[@class="abilitiesDetailsWrapper-3nyLR"]//ul//li//span//img//@src').getall()
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

                driver.execute_script("window.scrollTo(0, 1800)")

                skinIcons = currentChamp.css(
                    'li.thumbnail-3NKId').xpath('.//span//img//@src').getall()

                iconClick = WebDriverWait(driver, 100).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "thumbnail-3NKId"))
                )

                for skinIconIndex, skinIcon in enumerate(iconClick):
                    skinIcon.click()

                    currentSkin = scrapy.Selector(text=driver.page_source)

                    skinImage = currentSkin.xpath(
                        '//img[@data-testid="skins:skin-image"]//@src').get()

                    skinName = currentSkin.xpath(
                        '//span[@class="skinName-5H0GE"]//text()').get()

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
                'name': heroContent.css('h3.championName-1JnC5::text').get(),
                'subtitle': heroContent.css('p.championSubtitle-YAx7w::text').get(),
                'role': heroContent.css('span.roleName-33zEx::text').get(),
                'difficulty': heroContent.css('span.difficultyName-3NSea::text').get(),
                'heroVideo': currentChamp.css('div.heroVideo-1Jeta').css('source').attrib['src'],
                'skills': skills,
                'skins': skins
            }

        print("Scraping completed")
        driver.quit()
