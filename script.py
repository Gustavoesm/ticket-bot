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
  disponible_sectors = soup.find_all(match_disponible_sector)
  for tag in disponible_sectors:
    (sector, ticket_types) = extract_data_from(tag)
    asyncio.run(send_telegram_notification(url, sector, ticket_types))
  return len(disponible_sectors) > 0

def match_disponible_sector(tag) -> bool:
  if tag.name == 'form':
    all_types = tag.find_all('div', 'ticket-type-item')
    for type in all_types:
      if not type.find('div', 'ticket-type-unavailable-sec'):
        return True
  return False

def extract_data_from(tag):
  sector = tag.find('div', 'pc-list-category').contents[1].string
  types = []
  types_tag = tag.find_all('div', 'ticket-type-item')
  for each in types_tag:
    if not(each.find('div', 'ticket-type-unavailable-sec')):
      types.append(each.find('div', 'ticket-type-title').contents[1].string)
  return (sector, types)

async def send_telegram_notification(url, sector, types):
  bot = telegram.Bot(token=config['botToken'])
  message = "Found a disponible ticket for {}.\n\n{}".format(url, sector) 
  for type in types:
    message += '\n - {}'.format(type)
  await bot.send_message(config['channelId'], message)

  return

if __name__ == '__main__':
  sys.exit(main())