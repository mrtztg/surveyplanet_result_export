import re

from pandas import DataFrame
from json import JSONDecodeError
from time import time, sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from args_parser import ArgsParser


def print_if_verbose(val):
    if args.output_verbose:
        print(val)


args = ArgsParser()

chrome_options = Options()
driver_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
chrome_options.add_argument(f'user-agent={driver_user_agent}')
if not args.display_browser:
    chrome_options.add_argument('--headless')
try:
    driver = Chrome(ChromeDriverManager().install(), options=chrome_options)
except JSONDecodeError:
    try:
        driver = Chrome("./chromedriver", options=chrome_options)
    except Exception:
        driver = Chrome("chromedriver.exe", options=chrome_options)
WAITING_TIMEOUT = 120
participants_result = {}

try:
    print('opening website...')
    driver.get(args.question_participants_url)
    login_btn = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-button'))
    )
    driver.find_element_by_css_selector('#email').send_keys(args.acc_username)
    driver.find_element_by_css_selector('#password').send_keys(args.acc_password)
    login_btn.click()
    sleep(5)
    driver.get(args.question_participants_url)
    eye_button_of_first_el_css = ('#content .participant-list .participant-item'
                                  ' .content-list-options a.participant-details-button')
    first_item_view = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, eye_button_of_first_el_css))
    )
    first_item_view.click()
    last_participant_url: str = ""
    print('getting results...')
    while True:
        answer_item_el_css = ".participant-details-list li.participant-details-item"
        WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, answer_item_el_css))
        )
        start_time = time()


        def check_for_new_participant() -> True:
            global last_participant_url
            while time() < start_time + 30:
                if last_participant_url != driver.current_url:
                    return True
                sleep(1)
            return False


        if not check_for_new_participant():
            break
        last_participant_url = driver.current_url

        pagination_el_css = 'span.sub-header-pagination-label'
        participant_pagination = WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, pagination_el_css))
        ).text.strip()

        answers_items = driver.find_elements_by_css_selector(answer_item_el_css)
        answers_map = {}
        for answer_item in answers_items:
            question_number = answer_item.find_element_by_css_selector(
                '.content-list-item-index').text.strip()
            answer_result = answer_item.find_elements_by_css_selector(
                '.content-list-item-values li.content-list-item-value')
            answer_result = "\n".join([x.text for x in answer_result])
            answers_map[question_number] = answer_result

        side_details_el_css = '#side-bar-header-details li span'
        WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, side_details_el_css))
        )
        side_details = driver.find_elements_by_css_selector(side_details_el_css)

        side_details_map = {x.text.split(":")[0]: x.text.split(":")[1].strip() for x in
                            side_details if x.text and len(x.text.split(":")) == 2}
        answers_map.update(side_details_map)

        participants_result[participant_pagination] = answers_map
        back_btn_el_css = 'a.sub-header-pagination-prev-button'
        print(f'Got {participant_pagination}')
        driver.find_element_by_css_selector(back_btn_el_css).click()
finally:
    driver.close()
    # pass

df = DataFrame.from_dict(participants_result).transpose().fillna("")
out_file_name = 'participants.csv'
df.to_csv(out_file_name)
print(f'printed all data to {out_file_name}')
