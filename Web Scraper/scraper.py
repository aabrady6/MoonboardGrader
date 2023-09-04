#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author - Aaron Brady
# Contains the methods required for to scrape the problem holds and grades 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from requests_html import HTMLSession


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# General Browser / Login Methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Browser:
    browser, service = None, None

    ## Intialize the webdriver Firefox
    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Firefox(service=self.service)

    ## Open firefox instance
    def open_page(self, url:str):
        self.browser.get(url)

    ## Close firefox instance
    def close_browser(self):
        self.browser.close()

    ## Add text to input field
    def add_input(self, by: By, value: str, text:str):
        field = self.browser.find_element(by = by, value = value)
        field.send_keys(text)
        time.sleep(1)

    ## Simulate mouse click
    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by = by, value = value)
        button.click()
        time.sleep(1)

    ## Complete login process. Clicks login dropdown, inputs credentials, clicks login button
    def login(self, username: str, password: str):
        self.click_button(by = By.ID, value = 'loginDropdown')
        self.add_input(by = By.ID, value = 'Login_Username', text = username)
        self.add_input(by = By.ID, value = 'Login_Password', text = password)
        self.click_button(by = By.ID, value = 'navlogin')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MoonBoard Dashboard / Benchmark Table Methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ## Select the board to be scraped. Options are Masters 2019, Masters 2017 or Moonboard 2016. 
    def board_selection(self, board: str):
        if (board == 'Masters 2019'):
                board = '17';
        elif (board == 'Masters 2017'):
                board = '15';
        else:
                board = '1'
        choice = Select(self.browser.find_element(by = By.ID, value = 'Holdsetup'))
        choice.select_by_value(board)

    ## Returns the current benchmark table page the browser is on
    def get_current_page(self):
        tag_names = self.browser.find_elements(by = By.CLASS_NAME, value = 'k-state-selected')
        current = int(tag_names[1].text)
        return(current)
                  
    ## Navigates to next page of benchmark problems
    def nav_next_page(self, all_pages):
        all_pages = False
        current = str(self.get_current_page())
        li_list = self.browser.find_elements(by = By.XPATH, value = '//*[@id="grdBenchmarks"]/div[4]/div/ul/li')
        i = 0
        while (i < 7):
             if (current == li_list[i].text):
                next_li = str(i + 2)
                next_xpath = '//*[@id="grdBenchmarks"]/div[4]/div/ul/li[' + next_li + ']/a'
                try:
                    self.click_button(by = By.XPATH, value = next_xpath)
                    break
                except:
                    all_pages = True
                    break
             else:
                  i = i + 1
        return all_pages

    ## Scrape the benchark problem URLs from a single page and write to dataframe. 
    def scrape_table_urls(self, urls):
        #problems = []
        i = 1
        while True:
            try:
                xpath_value = '//*[@id="grdBenchmarks"]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a'
                table_url_values = self.browser.find_element(by = By.XPATH, value = xpath_value).get_attribute('href')
                urls.append(table_url_values)
                #print(table_url_values)
                i = i + 1
            except:
                break
    
    ## Driver function to scrape URLs
    def get_problems(self, urls):
        all_pages = False
        while True:
             if all_pages == False:
                self.scrape_table_urls(urls)
                all_pages = self.nav_next_page(all_pages)
                time.sleep(1)
             else:
                break


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Problem Page Methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Problems:
    def __init__(self, urls):
        self.urls = urls

    # Scrape through the URLs and create 4 txt files containing each problems grades, legal holds, the start locations and the finish location
    def scrape_holds(self):
        try:
            os.mkdir("Raw Data")
        except:
            pass
        g = open("./Raw Data/grades.txt", "w")
        h = open("./Raw Data/holds.txt", "w")
        sh = open("./Raw Data/start holds.txt", "w")
        eh = open("./Raw Data/end holds.txt", "w")
        i = 0
        for url in self.urls:
            s = HTMLSession()
            page = s.get(url)
            page_contents = page.html.xpath('/html/body/div/script/text()')
            self.parse_info(page_contents, g, h, sh, eh)
            s.close()
            i = i + 1
            print(i, "/", len(self.urls), " problems completed")
        g.close()
        h.close()
        sh.close()
        eh.close()
        
    # Parse out the information and build txt files
    def parse_info(self, page_contents, g, h, sh, eh):
        grade_key_start = '"Grade":"'
        grade_key_end = '","UserGrade":'
        holds_key_start = '"Moves":['
        holds_key_end = ']'
        grade = page_contents[0][page_contents[0].find(grade_key_start)+len(grade_key_start):page_contents[0].find(grade_key_end)]
        g.write(grade)
        holds_raw = page_contents[0][page_contents[0].find(holds_key_start)+len(holds_key_start):page_contents[0].find(holds_key_end)]
        holds_raw_list = holds_raw.split('}')
        for hold in holds_raw_list:
            hold_location = hold[hold.find('"Description":"')+len('"Description":"'):hold.find('","IsStart')]
            h.write(hold_location + " ")
            start = hold[hold.find('"IsStart":')+len('"IsStart":'):hold.find(',"IsEnd')]
            if start == 'true':
                sh.write(hold_location + " ")
            finish = hold[hold.find('"IsEnd":')+len('"IsEnd":'):]
            if finish == 'true':
                eh.write(hold_location + " ")
        g.write("\n")
        h.write("\n")
        sh.write("\n")
        eh.write("\n")

