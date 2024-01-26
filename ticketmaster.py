import json
from bs4 import BeautifulSoup

def ticketmaster_scan(req):
  soup = BeautifulSoup(req.content, 'html.parser')
  desired_tag = soup.findAll('script')[-1].text
  start = desired_tag.find("App.bootstrapData(")
  end = desired_tag.find("App.start();")
  data = json.loads(desired_tag[start+18:end-7])
  available = [
    [ticket for ticket in sector['rates'] if ticket['id'] == 280873] 
    for sector 
    in data['model']['data']['shows'][0]['sectors'] 
    if sector['id'] == 56165
  ][0][0]['available']

  if(available):
    message = "Encontrei um ingresso para um show que te interessa! 👍 {}.\n\nPISTA PREMIUM\n- Meia\n\nJá vai pensando em como me agradecer.".format(req.url)
    return [message]

  return []