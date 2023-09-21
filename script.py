#!/usr/bin/env python3

import sys, time, asyncio, requests, json, telegram
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

global config
config = json.load(open('config.json'))
chrome_ua_headers = {'User-Agent':str(UserAgent().chrome)}

def main():
  counter=1
  while(True):
    print("Performing status check for desired URL's. {}st attempt".format(counter))
    for url in config['urls']:
      if check_availability(url):
        time.sleep(30)
    time.sleep(5)
    counter += 1

def check_availability(url) -> bool:
  req = requests.get(url, headers=chrome_ua_headers)
  if req.status_code != 200:
    print("Failed request.\n", req.status_code)
  soup = BeautifulSoup(req.content, 'html.parser')
  disponible_ticket_types = soup.find_all(match_disponible_ticket)
  for tag in disponible_ticket_types:
    asyncio.run(send_telegram_notification(url, tag))
  return len(disponible_ticket_types) > 0

def match_disponible_ticket(tag) -> bool:
  if tag.has_attr('class') and 'ticket-type-item' in tag['class']:
    if tag.find('div', string="Indisponível no momento"):
      return False
    else:
      return True
  return False

async def send_telegram_notification(url, ticket_tag):
  bot = telegram.Bot(token=config['botToken'])
  # sector = ticket_tag.find_parent("form").find('div', 'pc-list-category').contents[1].string
  # type = ticket_tag.find('div', 'ticket-type-title').string
  await bot.send_message(config['channelId'], "Found a disponible ticket for {}.".format(url))
  return

if __name__ == '__main__':
  sys.exit(main())