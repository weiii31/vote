import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
vote_url = "https://poll.fm/14165530/embed"
interval = 60 #1 minutes later vote it again
votes_per_round = 5 # 每輪投票的次數

try:
    while True:  
        for _ in range(votes_per_round):
            driver.get(vote_url)

            # 選擇投票選項（: Blank the series）
            wait = WebDriverWait(driver, 10)
            vote_option = wait.until(EC.element_to_be_clickable((By.ID, "PDI_answer63080042")))
            vote_option.click()

            # click vote button
            vote_button = driver.find_element(By.ID, "pd-vote-button14165530")
            vote_button.click()

            # wait and find the element (+)
            math_question_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='captcha_14165530']/span/p")))

            # 加法處理（"X + Y = "）
            question_text = math_question_element.text.strip()  # 確保移除首尾空格
            operands = [int(s) for s in question_text.split() if s.isdigit()]
            answer = sum(operands)

            # enter ans
            answer_input = driver.find_element(By.ID, "answer_14165530")
            answer_input.send_keys(str(answer))

            # submit ans
            submit_button = driver.find_element(By.ID, "pd-vote-button14165530")
            submit_button.click()

            # return to poll button
            return_poll_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pds-return-poll")))
            return_poll_button.click()

            # 防止過快操作
            time.sleep(2)

        # 投完5次之後等1分鐘再投下一輪
        time.sleep(interval)

except KeyboardInterrupt:
    # 允許手動中斷
    print("程序被用戶中斷")

# 保持瀏覽器開啟直到手動關閉
print("請手動關閉瀏覽器。")
driver.quit()

#finally:
    # 關閉瀏覽器
    #driver.quit()
