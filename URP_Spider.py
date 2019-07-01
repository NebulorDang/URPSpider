#encoding=utf-8

from PIL import Image
import time
from selenium import webdriver
import sys

if __name__ == "__main__":

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # mac系统
    if sys.platform.find('darwin') >= 0:
        browser = webdriver.Chrome("../driver/chromedriver")
        #browser = webdriver.Chrome("../driver/chromedriver", chrome_options=option)
        print('当前系统mac')
    # linux系统
    elif sys.platform.find('linux') >= 0:
        print('当前系统linux')
        browser = ''
    # windows系统
    else:
        print('当前系统windows')
        browser = webdriver.Chrome(chrome_options=option)


    browser.get("http://zhjw.scu.edu.cn/login")
    userId = input("请输入学号")
    passWord = input("请输入密码")

    browser.save_screenshot('../captcha/ScreenShot.png')
    imageElement = browser.find_element_by_id("captchaImg")
    location = imageElement.location
    size = imageElement.size
    screenShot = Image.open('../captcha/ScreenShot.png')
    captchaImge = screenShot.crop((int(location['x']),int(location['y']),
                                  int(location['x'] + size['width']),
                                  int(location['y'] + size['height'])))
    captchaImge.show()

    _userId = browser.find_element_by_id("input_username")
    _passWord = browser.find_element_by_id("input_password")
    _captcha = browser.find_element_by_id("input_checkcode")


    captchaImgCode = input("请输入验证码")

    _userId.send_keys(userId)
    _passWord.send_keys(passWord)
    _captcha.send_keys(captchaImgCode)

    browser.find_element_by_id("loginButton").click()

    time.sleep(2)

    try:
        browser.find_element_by_xpath("//ul[@id='tasks']/li[2]").click()
    except Exception as e:
        print('账号密码或验证码输入错误，请重启程序!')
        sys.exit()

    time.sleep(2)

    totalClass = browser.find_element_by_id('totalkc')
    max = int(totalClass.get_attribute('innerText'))

    todoList = []
    for index in range(1,max+1):
        xpath = "//tbody[@id='jxpgtbody']/tr[%d]/td[5]"%(index)
        isdoneElement = browser.find_element_by_xpath(xpath)
        isdone = isdoneElement.get_attribute('innerText')
        if(isdone == '否'):
            print('否%d'%index)
            todoList.append(index)

    for index, item in enumerate(todoList):

        xpathTeacher = "//tbody[@id='jxpgtbody']/tr[%d]/td[3]"%(item)
        teacher = browser.find_element_by_xpath(xpathTeacher).get_attribute('innerText')
        xpath = "//tbody[@id='jxpgtbody']/tr[%d]/td[1]/button"%(item)
        todo = browser.find_element_by_xpath(xpath).click()

        time.sleep(2)

        scriptTexts = []
        scriptTexts.append("$(\"tbody\").children().find(\"input[value=\'10_1\']\").attr(\"checked\",\"checked\")")
        scriptTexts.append("$(\".form-control\").val(\"老师对待教学认真负责，语言生动，条理清晰，举例充分恰当，对待学生耐心答疑，能够鼓励学生踊跃发言，使课堂气氛比较积极热烈\")")
        scriptTexts.append('flag = true')
        scriptTexts.append("$(\"button[id=\'buttonSubmit\']\").click()")

        for scriptText in scriptTexts:
            browser.execute_script(scriptText)

        print('已完成对%s老师的评价'%(teacher))
        print('等待2分钟自动进行下一个')
        print('还剩%d个未完成'%(len(todoList) - (index + 1)))
        if(len(todoList) - (index + 1) == 0):
            sys.exit()
        time.sleep(122)
        print('go on...')
