#!/usr/bin/env python3

import sys, time, asyncio, requests, json, telegram
from eventim import eventim_scan
from luiza import luiza_scan
from tickets4fun import t4f_scan
from fake_useragent import UserAgent
from urllib.parse import urlparse

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
  domain = urlparse(url).hostname
  match domain:
    case "www.eventim.com.br":
      return monitorate_eventim(req)
    case "www.ticketmaster.com.br":
      return monitorate_luiza(req)
    case "sales.ticketsforfun.com.br":
      return monitorate_t4f(req.url)
    case _:
      print("Invalid domain")
      sys.exit(-1)

def monitorate_eventim(req):
  found_tickets = False
  for pending_notification in eventim_scan(req):
    asyncio.run(send_telegram_notification(pending_notification))
    found_tickets = True
  return found_tickets

def monitorate_luiza(req):
  found_tickets = False
  for pending_notification in luiza_scan(req):
    asyncio.run(send_telegram_notification(pending_notification))
    found_tickets = True
  return found_tickets

def monitorate_t4f(url):
    found_tickets = False
    for pending_notification in t4f_scan(url):
      asyncio.run(send_telegram_notification(pending_notification))
      found_tickets = True
    return found_tickets

async def send_telegram_notification(message):
  bot = telegram.Bot(token=config['botToken'])
  await bot.send_message(config['channelId'], message)
  return

if __name__ == '__main__':
  sys.exit(main())