from selenium import webdriver
import time
import datetime
import json
from selenium.webdriver.chrome.options import Options
def data_get(num,pwd):
    Date_Dict = {'0102':'第一二节','0304':'第三四节','0506':'第五六节','0708':'第七八节','0910':'第九十节','1112':'第十一十二节'}
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    try:
        browser.get("https://i.nefu.edu.cn")
        browser.find_element_by_xpath('//*[@id="un"]').send_keys(num)
        browser.find_element_by_xpath('//*[@id="pd"]').send_keys(pwd)
        browser.find_element_by_xpath('//*[@id="index_login_btn"]/input').click()
        data = []
        for x in range(2,9):
            course = browser.find_element_by_xpath('//*[@id="wid_home_course-content"]/div/div[3]/div[%d]'%x)
            m_d = course.find_element_by_xpath('//*[@id="wid_home_course-content"]/div/div[3]/div[%d]/p[1]/span[2]'%x).text  #获取月份
            week = course.find_element_by_xpath('//*[@id="wid_home_course-content"]/div/div[3]/div[%d]/p[1]/span[1]'%x).text #获取周几
            for y in course.find_elements_by_class_name('st_second_bar'):
                try:
                    course_info = y.find_element_by_class_name('ssc_describe_text').get_attribute('innerHTML') #span隐藏文本，因此通过读html获取到文本
                    id = y.get_attribute("id").split('_')[1][1:]
                    new_list = course_info.split('<br>') #将HTML中br标签去掉
                    new_list.append(Date_Dict[id])
                    new_list.append(week)
                    new_list.append(m_d)
                    data.append(new_list)
                except:
                    pass

        browser.close()
        with open('%s.txt'%num,'w') as myfile: #将爬取好的数据写入txt
            json.dump(data,myfile)
        return 0
    except Exception as e:
        return(str(e))

def comfire(num,pwd):
    now_time = datetime.datetime.now().strftime('%m.%d') #获取目前时间
    data = []
    now_data = []
    try:
        with open('%s.txt'%num,'r') as infile:  #首先读取缓存，如果没有缓存再通过爬虫爬取
            data = json.load(infile)
    except:
        data_get(num,pwd)
        with open('%s.txt'%num,'r') as infile:
            data = json.load(infile)
    for x in data:
        if(x[-1]==now_time): #匹配时间
            now_data.append(x)
    return(now_data)


    