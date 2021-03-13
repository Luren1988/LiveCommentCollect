import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CommentCollect:

    def __init__(self):
        self.COLLECT_INTERVAL = 10
        self.DRIVER_PATH = 'driver/chromedriver'
        self.TARGET_URL = ''
        self.dump_list = []
        self.driver = webdriver.Chrome(self.DRIVER_PATH)
    
    #def __del__(self):
    #    self.driver.quit()
     
    def __GetInnerHTML(self,content,target):
        result = ""
        try:
            result = content.find_element_by_id(target).get_attribute('innerHTML')
        except:
            result = ""
        return result

    def __GetText(self,content,target):
        result = ""
        try:
            result = content.find_element_by_id(target).text
        except:
            result = ""
        return result       

    def Prepare(self):
        if self.TARGET_URL:
            try:
                self.driver.get(self.TARGET_URL)
                time.sleep(5)

                iframe = self.driver.find_element_by_xpath('//*[@id="chatframe"]')
                self.driver.switch_to.frame(iframe)
            except:
                print("ドライバーが設定できませんでした。")
        else:
            print('urlがセットされていません')

    def UpdateComment(self,contents):

        if len(contents) > 0:
            for content in contents:
                try:
                    unique_id = content.get_attribute('id')
                    check_duplicate = [ d.get(unique_id) for d in self.dump_list if d.get(unique_id)]
                    if len(check_duplicate) == 0:
                        timestamp = self.__GetInnerHTML(content,'timestamp')
                        message = self.__GetText(content,'message')
                        author = self.__GetText(content,'author-name')
                        self.dump_list.append({unique_id:{"timestamp":timestamp,"author":author,"message":message}})

                        #print(timestamp + " - " +  author + " - " + message  )

                except Exception as e:
                    print(e)
            
    
    def CheckComment(self):
        while True:
            try:
                items = self.driver.find_elements_by_xpath('//*[@id="items"]')
                if len(items) > 0 :
                    contents = items[1].find_elements_by_tag_name('yt-live-chat-text-message-renderer')
                    self.UpdateComment(contents)

                    lastcomment = self.dump_list[-1]
                    for key in lastcomment.keys():
                        name = lastcomment[key]["author"]
                        talk = lastcomment[key]["message"]
                        answer = self.conversation_generate(name,talk)
                        print(answer)

                else:
                    print('no element found')

            except Exception as e:
                print(e)

            time.sleep(self.COLLECT_INTERVAL)
    
    def conversation_generate(self,name,talk):

        return f'{name}さん、こんにちは'    



    

if __name__=='__main__':
    CC = CommentCollect()
    CC.TARGET_URL = 'https://www.youtube.com/watch?v=Eq8tg0kt44Y'
    
    CC.Prepare()
    CC.CheckComment()
