from bs4 import BeautifulSoup

def eventim_scan(req):
  soup = BeautifulSoup(req.content, 'html.parser')
  disponible_sectors = soup.find_all(match_disponible_sector)
  notifications = []
  for tag in disponible_sectors:
    (sector, types) = extract_data_from(tag)
    notifications.append(format_notification_message(req.url, sector, types))
  return notifications

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

def format_notification_message(url, sector, types):
  message = "Found a disponible ticket for {}.\n\n{}".format(url, sector) 
  for type in types:
    message += '\n - {}'.format(type)
  return message