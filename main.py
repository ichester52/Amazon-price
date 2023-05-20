from bs4 import BeautifulSoup
import cloudscraper
import smtplib
import os
import pprint


my_email = os.environ.get('MY_EMAIL')
my_password = os.environ.get('MY_PASSWORD')

target_price = 200

PRODUCT_URL = "https://www.amazon.com/SHW-Vista-L-Shape-Monitor-Stand/dp/B09156SFG2/ref=sr_1_31?crid=2I3HAOLTCV796&keywords=work%2Bdesk&qid=1677292232&sprefix=work%2Bdesk%2Caps%2C153&sr=8-31&th=1"

header = {
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie": "PHPSESSID=8ef970866b7cc77bc12e665517128714; _ga=GA1.2.932798517.1677290883; _gid=GA1.2.1430561532.1677290883"
}

scraper = cloudscraper.create_scraper()

amazon_page = scraper.get(PRODUCT_URL)

soup = BeautifulSoup(amazon_page.text, "html.parser")

price_int = soup.find(class_="a-price-whole").getText()

price_float = soup.find(class_="a-price-fraction").get_text()

price = float(f"{price_int}{price_float}")

try:
    title = soup.find_all(id="productTitle")[0]
    product_title = title.get_text().strip(" ")

except:
    product_title = "desk"

product_title = title.get_text().strip(" ")
print(product_title)


print(price)

if price < target_price:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: Low Price!!!\n\n your {product_title} is available for only ${price}\n visit {PRODUCT_URL}"

        )
