
import scrapy
from ..items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2 # This is part of the code that will allow us change the page automatically
    # Most of the websites add 'Page 2' when you press the next button. We copy page 2 link and modify the number to 1 tp have the first page
    start_urls = [
        'https://www.amazon.es/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1',
    ]

    def parse(self, response):
        
        items = AmazonItem()
        
        #I use Chrome Selector Gadget and the inspector to check the css paths required
        #This is the area were all the books information is contain.
        #In Amazon it does not contain only the books, but other ads and sections as well
        #books = response.css('div.p13n-desktop-grid') 
        books = response.css('.zg-grid-general-faceout')
        
        # To avoid having 3 large list of information, we decide to save in different columns the title, price and imagelink of each of the first 5 pages
        for book in books:        
            title = book.css('.a-link-normal span div::text').extract()
            #price = book.css('._p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z selectorgadget_suggested::text()').extract()
            #price = book.xpath('//html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[49]/div/div[2]/div/div[4]/a/span/span/text()').extract()
            price = book.xpath('//*[@id="gridItemRoot"]/div/div[2]/div/div[3]/a/span/span/text()').get()
            imagelink = book.css('.p13n-product-image::attr(src)').extract()
        
            # Save the info into a intermediate container
            items['title'] = title
            items['price'] = price
            items['imagelink'] = imagelink
        
            yield items
 

        # This will chage the page to extract the books from the next pages
        next_page = 'https://www.amazon.es/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg='+ str(AmazonSpider.page_number) 
        
        # We limit the extraction to 3 pages
        if AmazonSpider.page_number < 3:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse) #change the page and call the class again to scrape it.
