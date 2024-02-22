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
# links = soup.find_all("a", attrs = {'class' : 'a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold'})

def get_abebooks_listings(bookTitle):
    abeBooks = "https://www.abebooks.com/servlet/SearchResults?kn=" + bookTitle + "&sts=t&cm_sp=SearchF-_-TopNavISS-_-Results"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    response = requests.get(abeBooks, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    listings = soup.find(id="srp-results")

    titles = [title.text.replace('\n', '') for title in soup.find_all('h2', class_='title')]
    authors = [author.text.strip() if author else 'Author information not available' for author in soup.find_all('p', class_='author')]
    conditions = [condition.text if condition else 'Condition information not available' for condition in soup.find_all('span', class_='opt-subcondition')]
    prices = [price.text if price else 'Price information not available' for price in soup.find_all('p', class_='item-price')]
    #shippings = [freeShipping.text if freeShipping else 'Free Shipping information not available' for freeShipping in soup.find_all('span', class_='free-shipping item-shipping text-secondary text-500')]
    #paid_shippings = [shipping.text if shipping else 'Shipping information not available' for shipping in soup.find_all('span', class_='item-shipping text-secondary text-500')]
    
    shippings = [freeShipping.text if freeShipping else 'Free Shipping information not available' for freeShipping in soup.find_all('span', class_='free-shipping item-shipping text-secondary text-500')]
   
    # Find the maximum length among the lists
    max_length = max(len(titles), len(authors), len(conditions), len(prices))

    # Pad the lists with placeholder text to match the maximum length
    titles += ['Title information not available'] * (max_length - len(titles))
    authors += ['Author information not available'] * (max_length - len(authors))
    conditions += ['Condition information not available'] * (max_length - len(conditions))
    prices += ['Price information not available'] * (max_length - len(prices))
    shippings += ['Free Shipping not available'] * (max_length - len(shippings))

    abeBooksListings = []
    
    for i in range(len(conditions)):
        book_info = {
            'Title': titles[i],
            'Author': authors[i],
            'Condition': conditions[i],
            'Price': prices[i],
            'Free Shipping': shippings[i],
        }

        abeBooksListings.append(book_info)

    return abeBooksListings

def minAbeBooksPrice(listings):
    minPrice = float('inf')  # Initialize minPrice to positive infinity

    for idx, book in enumerate(listings, start=0):
        prices = listings[idx]['Price']
        convertPrices = float(prices.replace("US$ ", ""))
        convertPrices = "{:.2f}".format(convertPrices)

        if minPrice > float(convertPrices):
            minPrice = float(convertPrices)
            minPrice_item = listings[idx]  # Update the minimum item information

    # Display the information of the item with the minimum price
    print("\nLowest Price on AbeBooks:")
    for key, value in minPrice_item.items():
        print(f"\t{key}: {value}")


def getThriftBooksListings(bookTitle):
    thriftBooksSearch = "https://www.thriftbooks.com/browse/?b.search=" + bookTitle + "#b.s=mostPopular-desc&b.p=1&b.pp=30&b.oos&b.tile"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    response = requests.get(thriftBooksSearch, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    subheading_div = soup.find('div', class_='SearchResultTileItem-subheading')
    first_link = subheading_div.a['href'] if subheading_div and subheading_div.a else None

    thriftBooks = "https://www.thriftbooks.com" + first_link
    linkResponse = requests.get(thriftBooks, headers=HEADERS)
    soup = BeautifulSoup(linkResponse.content, 'lxml')

    titles = [title.text.replace('\n', '') for title in soup.find_all('h2', class_='AllEditionsItem-workTitle')]
    authors = [author.text.strip() if author else 'Author information not available' for author in soup.find_all('div', class_='AllEditionsItem-workAuthor')]
    conditions = [condition.text if condition else 'Condition information not available' for condition in soup.find_all('select', class_='AllEditions-selectCondition')]
    prices = [price.text if price else 'Price information not available' for price in soup.find_all('div', class_='AllEditionsItem-price')]

    max_length = max(len(titles), len(authors), len(conditions), len(prices))

    titles += ['Title information not available'] * (max_length - len(titles))
    authors += ['Author information not available'] * (max_length - len(authors))
    conditions += ['Condition information not available'] * (max_length - len(conditions))
    prices += ['Price information not available'] * (max_length - len(prices))

    thriftBookListings = []
    
    for i in range(len(conditions)):
        book_info = {
            'Title': titles[i],
            'Author': authors[i],
            'Condition': conditions[i],
            'Price': prices[i]
        }

        thriftBookListings.append(book_info)

    return thriftBookListings

def minThriftBooksPrice(listings):
    minPrice = float('inf')  # Initialize minPrice to positive infinity

    for idx, book in enumerate(listings, start=0):
        prices = listings[idx]['Price']
        if(prices == 'Price information not available'):
            continue
        convertPrices = float(prices.replace("$", ""))
        convertPrices = "{:.2f}".format(convertPrices)

        if minPrice > float(convertPrices):
            minPrice = float(convertPrices)
            minPrice_item = listings[idx]  # Update the minimum item information

    # Display the information of the item with the minimum price
    print("\nLowest Price on ThriftBooks:")
    for key, value in minPrice_item.items():
        print(f"\t{key}: {value}")

def getWoBListings(bookTitle):
    WoBSearch = "https://www.wob.com/en-us/category/all?search=" + bookTitle
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    response = requests.get(WoBSearch, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    titles = [title.text.strip() for title in soup.find_all('span', class_='title')]
    authors = [author.text.strip() if author else 'Author information not available' for author in soup.find_all('span', class_='author')]
    conditions = [condition.text.strip() if condition else 'Condition information not available' for condition in soup.find_all('div', class_='itemType')]
    prices = [price.text.strip() if price else 'Price information not available' for price in soup.find_all('div', class_='itemPrice')]


    max_length = max(len(titles), len(authors), len(conditions), len(prices))

    titles += ['Title information not available'] * (max_length - len(titles))
    authors += ['Author information not available'] * (max_length - len(authors))
    conditions += ['Condition information not available'] * (max_length - len(conditions))
    prices += ['Price information not available'] * (max_length - len(prices))

    WoBListings = []
    
    for i in range(len(conditions)):
        book_info = {
            'Title': titles[i],
            'Author': authors[i],
            'Condition': conditions[i],
            'Price': prices[i]
        }

        WoBListings.append(book_info)

    return WoBListings

def minWoBPrice(listings):
    minPrice = float('inf')  # Initialize minPrice to positive infinity

    for idx, book in enumerate(listings, start=0):
        prices = listings[idx]['Price']
        if(prices == 'Price information not available'):
            continue
        convertPrices = float(prices.replace("$", ""))
        convertPrices = "{:.2f}".format(convertPrices)

        if minPrice > float(convertPrices):
            minPrice = float(convertPrices)
            minPrice_item = listings[idx]  # Update the minimum item information

    # Display the information of the item with the minimum price
    print("\nLowest Price on WorldofBooks:")
    for key, value in minPrice_item.items():
        print(f"\t{key}: {value}")

def getPowellsListings(bookTitle):
    PowellsSearch = "https://www.powells.com/searchresults?keyword=" + bookTitle
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    response = requests.get(PowellsSearch, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    titles = [title.text.replace('\n', '') for title in soup.find_all('h2', class_='AllEditionsItem-workTitle')]
    authors = [author.text.strip() if author else 'Author information not available' for author in soup.find_all('div', class_='book-author')]
    conditions = [condition.text if condition else 'Condition information not available' for condition in soup.find_all('div', class_='book-type')]
    prices = [price.text if price else 'Price information not available' for price in soup.find_all('div', class_='book-price')]

    max_length = max(len(titles), len(authors), len(conditions), len(prices))

    titles += ['Title information not available'] * (max_length - len(titles))
    authors += ['Author information not available'] * (max_length - len(authors))
    conditions += ['Condition information not available'] * (max_length - len(conditions))
    prices += ['Price information not available'] * (max_length - len(prices))

    PowellsListings = []
    
    for i in range(len(conditions)):
        book_info = {
            'Title': titles[i],
            'Author': authors[i],
            'Condition': conditions[i],
            'Price': prices[i]
        }

        PowellsListings.append(book_info)

    return PowellsListings


if __name__ == "__main__":
    bookTitle = input("Enter the name of the book and author: ")
    bookTitle = bookTitle.replace(" ", "%20")

    AbeBooksListings = get_abebooks_listings(bookTitle)
    minAbeBooksPrice(AbeBooksListings)

    thriftBooksLists = getThriftBooksListings(bookTitle)
    minThriftBooksPrice(thriftBooksLists)

    WorldOfBookLists = getWoBListings(bookTitle)
    minWoBPrice(WorldOfBookLists)




    
