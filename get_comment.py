import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#取得間隔
COLLECT_INTERVAL = 10
#driverのパス
driver_path = 'driver/chromedriver'
#取得するyoutubeのライブ
target_url = ''
#結果ストレージ [{id:{"message":message,"timestamp":timestamp,"author":author}},....]
dump_list = []

def getInnerHTML(content,target):
    result = ""
    try:
        result = content.find_element_by_id(target).get_attribute('innerHTML')
    except:
        result = ""
    return result

def getText(content,target):
    result = ""
    try:
        result = content.find_element_by_id(target).text
    except:
        result = ""
    return result       

def update_comment(contents):

    if len(contents) > 0:
        for content in contents:
            try:
                unique_id = content.get_attribute('id')
                check_duplicate = [ d.get(unique_id) for d in dump_list if d.get(unique_id)]
                if len(check_duplicate) == 0:
                    timestamp = getInnerHTML(content,'timestamp')
                    message = getText(content,'message')
                    author = getText(content,'author-name')
                    dump_list.append({unique_id:{"timestamp":timestamp,"author":author,"message":message}})

                    print(timestamp + " - " +  author + " - " + message  )

            except Exception as e:
                print(e)


#[TODO]:headless chrome 対応 
#options = Options()
#options.add_argument('--headless')


driver = webdriver.Chrome(driver_path)
driver.get(target_url)
#起動待ち時間
time.sleep(5)

iframe = driver.find_element_by_xpath('//*[@id="chatframe"]')
driver.switch_to.frame(iframe)

while True:
    try:
        items = driver.find_elements_by_xpath('//*[@id="items"]')
        contents = items[1].find_elements_by_tag_name('yt-live-chat-text-message-renderer')
        update_comment(contents)
         
    except Exception as e:
        print(e)

    time.sleep(COLLECT_INTERVAL)

driver.quit()

