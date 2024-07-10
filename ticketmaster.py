import json
from bs4 import BeautifulSoup

def ticketmaster_scan(req):
  soup = BeautifulSoup(req.content, 'html.parser')
  desired_tag = soup.findAll('script')[-1].text
  start = desired_tag.find("App.bootstrapData(")
  end = desired_tag.find("App.start();")
  data = json.loads(desired_tag[start+18:end-7])
  desired_pricing_id = 733056 # should recover from site
  desired_sector_id = 118982 # should recover from site
  try:
    available = [
      [ticket for ticket in sector['rates'] if ticket['id'] == desired_pricing_id] 
      for sector 
      in data['model']['data']['shows'][0]['sectors'] 
      if sector['id'] == desired_sector_id
    ][0][0]['available']
  except:
    return []

  if(available):
    message = "Encontrei um ingresso para um show que te interessa! 👍 {}.\n\nPISTA PREMIUM\n- Meia\n\nJá vai pensando em como me agradecer.".format(req.url)
    return [message]

  return []