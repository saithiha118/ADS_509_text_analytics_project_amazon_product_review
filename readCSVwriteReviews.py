
from requests_html import HTMLSession

class ProductReviews:
  def __init__(self, asin):
    self.review_pages = [
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_4?ie=UTF8&reviewerType=all_reviews&pageNumber=4',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_6?ie=UTF8&reviewerType=all_reviews&pageNumber=6',
    'https://www.amazon.com/product-reviews/ASIN/ref=cm_cr_arp_d_paging_btm_next_7?ie=UTF8&reviewerType=all_reviews&pageNumber=7'
    ]
    self.asin = None
    self.search_urls = []
    for review_page in self.review_pages:
      review_page = review_page.replace('ASIN', asin)
      self.search_urls.append(review_page)
    self.proxies = {
      'http': 'http://66.29.154.103',
      'http': 'http://10.10.1.10:3128',
      'https': 'http://11.22.33.255:10',
      'https': 'http://165.22.211.212:3128',
      'https': 'http://151.106.17.124:1080',
      'https': 'http://66.70.178.214:9300',
      'https': 'http://104.131.109.98:3128',
      'https': 'http://151.106.18.123:1080',
    }
    self.session = HTMLSession()
    self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
      
  def parse(self, reviews):
    output = []
    for review in reviews:
      review_body = review.find('span[data-hook="review-body"] span', first=True)
      if review_body:
        review_body = review_body.text.strip().replace('\n', ' ')
        output.append(review_body)
      else: 
        return False
    return output
  
  def readPage(self, pageURL):
    r = self.session.get(pageURL)
    r.html.render(timeout = 40)
    if r.status_code == 200:
      print("Status Code: " + str(r.status_code))
      reviews = r.html.find('div[data-hook=review]')
      if reviews:
        return reviews
      else:
        print("No reviews from readPage()")
        return False
    else:
      return False
    
  def getPageURLs(self):
    return self.search_urls
  
# end class: ProductReviews

# main
products = ["spatula",
            "pan",
            "bowl",
            "cups",
            "silverware",
            "food storage"]

product_name = products[5]
ASIN_list = []
with open(product_name + 'ASIN' + '.csv', 'r') as f:
  import csv
  reader = csv.reader(f)
  for row in reader:
    if row:
      ASIN_list.append(row[0])

results = []

for asin in ASIN_list:
  product = ProductReviews(asin)
  pageURLs = product.getPageURLs()
  for pageURL in pageURLs:
    reviews = product.readPage(pageURL)
    if reviews:
      parsed = product.parse(reviews)
      if parsed:
        results = results + parsed
        
with open(product_name + "_reviews.csv", 'w') as review_file:
  writer = csv.writer(review_file)
  for result in results:
    writer.writerow([result])
    
