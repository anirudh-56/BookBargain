import requests
from bs4 import BeautifulSoup
import string
import smtplib


online_bookStores = [
    "https://www.abebooks.com/",
    "https://www.amazon.com/",
    "https://www.barnesandnoble.com/",
    "https://www.thriftbooks.com/",
]

WebsitePrices = []

bookTitle = input("Enter the name of the book and author: ")
bookTitle.replace(" ", "%20")

abeBooks = "https://www.abebooks.com/servlet/SearchResults?kn=" + bookTitle + "&sts=t&cm_sp=SearchF-_-TopNavISS-_-Results"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
response = requests.get(abeBooks, headers=HEADERS)
soup = BeautifulSoup(response.content, 'lxml')
listings = soup.find(id = "srp-results")

print("Listings length:", len(listings))

abeBooksListings = {}

titles = [title.text.replace('\n', '') for title in soup.find_all('h2', class_='title')]
authors = [author.text.strip() if author else 'Author information not available' for author in soup.find_all('p', class_='author')]
conditions = [condition.text if condition else 'Condition information not available' for condition in soup.find_all('span', class_='opt-subcondition')]
prices = [price.text if price else 'Price information not available' for price in soup.find_all('p', class_='item-price')]
costShippings = [costShipping.text if costShipping else 'Shipping information not available' for costShipping in soup.find_all('span', class_='item-shipping text-secondary text-500')]
freeShippings = [shipping.text if shipping else 'Free Shipping information not available' for shipping in soup.find_all('span', class_='free-shipping item-shipping text-secondary text-500')]

# Find the maximum length among the lists
max_length = max(len(titles), len(authors), len(conditions), len(prices))

# Pad the lists with placeholder text to match the maximum length
titles += ['Title information not available'] * (max_length - len(titles))
authors += ['Author information not available'] * (max_length - len(authors))
conditions += ['Condition information not available'] * (max_length - len(conditions))
prices += ['Price information not available'] * (max_length - len(prices))


abeBooksListings = []

for i in range(len(conditions)):
    book_info = {
        'Title': titles[i],
        'Author': authors[i],
        'Condition': conditions[i],
        'Price': prices[i],
    }

    abeBooksListings.append(book_info)

# Displaying the information for each book
for idx, book in enumerate(abeBooksListings, start=1):
    print(f"Listing {idx}:")
    for key, value in book.items():
        print(f"{key}: {value}")
    print()

# links = soup.find_all("a", attrs = {'class' : 'a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold'})




