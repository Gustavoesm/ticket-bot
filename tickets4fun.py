from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

def t4f_scan(url):
  html = extract_js_rendered_html(url)
  soup = BeautifulSoup(html, 'html.parser')
  tag = soup.find('div', 'q-list no-border q-list-separator q-list-multiline')
  dates = []
  for event_day in tag.contents: # type: ignore
    if type(event_day) is Tag and is_available(event_day):
      dates.append(extract_show_date(event_day))

  return [generate_notification_message(dates, url)]

def is_available(tag):
  if tag.find('div', 'tickets-available'):
    return True
  return False

def extract_show_date(tag):
  weekday = tag.find('span', 'event-weekday')
  day = tag.find('span', 'event-day')
  return (day.text.strip(), weekday.text.strip())

def generate_notification_message(dates, url):
  message = "Encontrei ingressos para um show desejado {}.\n\nDatas:\n".format(url)
  for date in dates:
    message += " - {}, {}\n".format(date[0], date[1])
  return message

def extract_js_rendered_html(url):
  options = webdriver.FirefoxOptions()
  options.add_argument("--headless")
  options.set_preference('intl.accept_languages', 'pt-BR')
  options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
  browser = webdriver.Firefox(options=options)
  browser.get(url)
  WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'event-date')))
  html = browser.page_source
  browser.quit()
  return html