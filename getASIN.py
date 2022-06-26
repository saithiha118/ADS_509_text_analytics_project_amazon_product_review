from requests_html import HTMLSession
import csv

search_words = ["spatula",
                "pan",
                "bowl",
                "cups",
                "silverware",
                "utensil",
                "food storage"]

for word in search_words:
  url = 'https://www.amazon.com/s?k=' + word
  s = HTMLSession()
  r = s.get(url)
  r.html.render(sleep=1)
  products = r.html.find('div[data-asin]')
  asins = []
  for product in products:
    asin = product.attrs['data-asin']
    if asin:
      asins.append(asin)
    
  with open(word + "ASIN.csv", 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for asin in asins:
      writer.writerow([asin])