from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
url = "https://www.boston.gov/departments/public-works/recycling-boston#!rc-cpage=wizard_material_list"

browser.get(url)
time.sleep(1)

html = browser.page_source
doc = BeautifulSoup(html, features="html.parser")

li = doc.find("div", {"class": "paragraphs-items paragraphs-items-field-text-blocks paragraphs-items-field-text-blocks-full paragraphs-items-full"}).findAll("li")
a = []
for index in range(len(li)):
    a.append(li[index].find("a"))

a_list = a[12:] # remove the other useless <a> tags that were roped in by findAll


material_list = []
material_dict = {}
browser.close()


for item in a_list:
    material = str(item).split(">", 1)[1].split("<")[0].strip()# just some string manipulation to remove all the tags and whitespace
    link = str(item).split("href=\"")[-1].split("\"")[0]

    temp_options = Options()
    temp_options.add_argument("--headless")
    temp_browser = webdriver.Chrome(options=temp_options)
    temp_url = link ##
    temp_browser.get(temp_url)
    time.sleep(1)
    temp_html = temp_browser.page_source
    temp_doc = BeautifulSoup(temp_html, features="html.parser")

    page_section = temp_doc.findAll("div", {"class": "card page-section"})

    if len(page_section) == 0:
        page_section.append(temp_doc.find("div", {"class": "rCpage"}))

    strong = None
    reset = True
    indexer = -1
    while reset == True: # This loop finds the right page-row-content that contains a <strong> tag
        if abs(indexer) > len(page_section[-1].findAll("div", {"class": "page-row-content"})):  # this is for the faulty pages on the website that don't list a mode of disposal
            strong = "<strong>None</strong>"
            break
        page_row_content = page_section[-1].findAll("div", {"class": "page-row-content"})[indexer]

        strong = page_row_content.strong
        if strong != None:
            reset = False

        indexer = indexer - 1


    result = str(strong).split(">")[1].split("<")[0]
    print("Material: " + material)
    print("Result: " + result)
    print("Link: " + link)
    
    result_list = []
    in_result_list = False

    for i in result_list:
        if result == i:
            in_result_list = True
            break
    if not in_result_list: result_list.append(result)
    
    material_list.append(material)
    material_dict[material] = [result, link]
    
for i in material_dict:
    print(i, material_dict[i])

with open("results.txt" ) as f:
    f.write(i, material_dict[i])
    f.close();

with open("boston-recyclable-materials.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(material_dict)
    # writer.close()

