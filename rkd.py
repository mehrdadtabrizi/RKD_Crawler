#Function Library
#Web crawler for the Photo Archive RKD
#Written by Mehrdad Tabrizi, May 2019, Erlangen - Germany
#Contact: mehrdad.tabrizi1991@gmail.com 

import  csv
import  re
from    bs4         import BeautifulSoup
from    urllib      import request
from    collections import OrderedDict
from    selenium    import webdriver
from    selenium.webdriver.support.ui import WebDriverWait
from    selenium.webdriver.support import expected_conditions as EC
from    selenium.webdriver.common.by import By
import  rkd_Parameters as Parameters
import  time

def browser_open():
    driver = webdriver.Firefox(executable_path=Parameters.Firefox_Driver_PATH)
    return driver

def browser_open_url(browser, url):
    browser.get(url)
    return browser

def get_html_page(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup

def search_for_the_keyword(browser):
    print('Searching for the Keyword "' + Parameters.KEYWORD + '"...')
    keyword = browser.find_element_by_xpath("//*/input[@id='query']")
    keyword.send_keys(Parameters.KEYWORD)
    submit = browser.find_element_by_xpath("//*/form[@id='searchall']/button[@class='submit']")
    submit.click()
    print('Search is done!')
    time.sleep(2)

    wait = WebDriverWait(browser, 10)
    table = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*/div[@class="image-holder"]/a')))
    if table is not None:
        first_item = browser.find_element_by_xpath('//*/div[@class="image-holder"]/a')
        first_item.click()

    return browser
def find_last_page(browser):

    wait = WebDriverWait(browser, 10)
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultcount')))
    s = get_html_page(browser)
    rescount = s.find('span', {'class' : 'resultcount'}).text
    last = int((re.findall("\d+", rescount))[-1])
    return last

def get_html_page(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup

def page_loaded_successfully(browser):
    wait = WebDriverWait(browser, 15)
    table = wait.until(EC.presence_of_element_located((By.XPATH, "//*/div[@class='right results']")))
    wait2 = WebDriverWait(browser, 15)
    img = wait2.until(EC.presence_of_element_located((By.XPATH, "//*/div[@class='galleria-stage']")))
    #hidden = wait.until(EC.presence_of_element_located((By.XPATH, "//*/div[@class='fieldGroup split expandable']")))
    if (table is not None and img is not None ):
        print('Loaded Successfully!')
        return True
    else:
        return False

def extract_item_metadata(browser,current_item):
    artist = ' '
    date = ' '
    title = ' '
    material = ' '
    image_url = ' '
    genre = ' '
    repository_number = ''
    item_URL = browser.current_url
    soup = get_html_page(browser)
    file_name = ''

    if (page_loaded_successfully(browser)):
        try:


            image_box = browser.find_element_by_xpath('//*/div[@class="galleria-images"]//*/img')
            image_url = image_box.get_attribute('src')

            repository_boxes = browser.find_elements_by_xpath('//*/div[@class="galleria-info-title"]/span[@class="galleria-info-licence-attribution"]')
            for b in repository_boxes:
                if "Illustration" in b.text:
                    repository_number = b.text.replace('Illustration number ', '')
            file_name = image_url.split('/')[-1]
            if not Parameters.Images_are_already_downloaded:
                download_image(image_url,file_name)

            boxes = soup.find_all('div' , {'class' : 'fieldGroup split'})
            for box in boxes:
                labels = box.find_all('dt')
                for label in labels:
                    if "medium" in label.text:
                        dd = label.find_next_sibling('dd')
                        material = re.sub(' +', ' ', (dd.text.replace('\n', '')))
                        break
                    if "category" in label.text:
                        dd = label.find_next_sibling('dd')
                        genre = re.sub(' +', ' ', (dd.text.replace('\n', '')))
                        break
                    if "Current attribution" in label.text:
                        dd = label.find_next_sibling('dd')
                        artist = re.sub(' +', ' ', (dd.text.replace('\n', '')))
                        break

                    if "Date" in label.text:
                        dd = label.find_next_sibling('dd', recursive=False)
                        date = re.sub(' +', ' ', (dd.text.replace('\n', '')))
                        break


        except:
            pass

        try:

            hidden_boxes = soup.find_all('div', {'class': 'fieldGroup split expandable'})
            box = hidden_boxes[0]
            dts = box.find_all('dt')
            for dt in dts:
                if "English title" == dt.text:
                    dd = dt.find_next_sibling('dd')
                    title = re.sub(' +', ' ',(dd.text.replace('\n', '')))
                    break
                else:
                    if "Title" == dt.text:
                        dd = dt.find_next_sibling('dd')
                        title = re.sub(' +', ' ', (dd.text.replace('\n', '')))
                        break
        except:
            pass
    print(title)

    item_dic = {
        'Photo Archive'     : Parameters.base_url,
        'Iconography'       : Parameters.Iconography,
        'Branch'            : 'ArtHist',
        'File Name'         : file_name,
        'Title'             : title,
        'Additional Information' : ' ',
        'Artist'            : artist,
        'Earliest Date'     : date,
        'Original Location' : '',
        'Current Location'  : '',
        'Repository Number' : repository_number,
        'Genre'             : genre,
        'Material'          : material,
        'Details URL'       : item_URL,
        'Image Credits'     : image_url
    }
    keyorder = Parameters.Header
    item_dic = OrderedDict(sorted(item_dic.items(), key=lambda i: keyorder.index(i[0])))
    print('......................')

    return item_dic

def go_to_next_page(browser):
    next_button = browser.find_element_by_xpath("//*/div[@class='nextprev']/a[@class='next']")
    if next_button is not None:
        next_button.click()
        browser.implicitly_wait(30)
        return True
    return  False


def download_image(url,file_name):
    path = Parameters.Images_PATH + file_name
    request.urlretrieve(url, path)

def create_csv_file(file_path):
    keyorder = Parameters.Header
    with open(file_path, "w") as f:
        wr = csv.DictWriter(f, dialect="excel", fieldnames=keyorder)
        wr.writeheader()

def append_metadata_to_CSV(dic):
    keyorder = Parameters.Header
    with open(Parameters.CSV_File_PATH, "a", encoding="utf-8") as fp:
        wr = csv.DictWriter(fp,dialect="excel",fieldnames=keyorder)
        wr.writerow(dic)

def browser_quit(browser):
    browser.quit()
