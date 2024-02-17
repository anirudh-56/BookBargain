from twilio.rest import Client
import keys
import requests
import time
from bs4 import BeautifulSoup
import string
import smtplib


def pushNotif(phoneNumber, messageBody):
    keys.target_number = phoneNumber
    client = Client(keys.account_sid, keys.auth_token)

    try:
        message = client.messages.create(
            body = messageBody,
            from_ = keys.twilio_number,
            to = keys.target_number
        )

        print(message.body)
    except Exception as e:
        print(f"Error sending message: {e}")


def check_price(book_title, desired_price, phoneNumber):
    url = f"https://www.abebooks.com/servlet/SearchResults?kn={book_title}&sts=t&cm_sp=SearchF-_-topnav-_-Results&ds=20"
    
    while True:
        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.find('p', class_='item-price')

        if price_element:

            current_price = float(price_element.text.replace('US$ ', '').strip())

            min, max = desired_price.split('-')

            minimum_price = float(min)
            maximum_price = float(max)

            if minimum_price <= current_price <= maximum_price:
                message = f"Book '{book_title}' found within the desired price range at ${current_price}!"
                print("Sending notification...")
                pushNotif(phoneNumber, message)
                break
            
        time.sleep(60)  # Wait for 60 seconds before checking again


if __name__ == "__main__":
    option = input("Did you find your book at a desired price? (Y/N): ")

    if option.upper() == "N":
        book_title = input("Enter the book title (e.g., Dune Messiah): ")
        desired_price = input("Enter your desired price range (e.g., 3.00-4.00): ")
        phoneNumber = input("Enter your phone number (Format: +1, no dashes or spaces): ")

        print(f"We'll notify you if '{book_title}' is found within the price range of ${desired_price}")
        check_price(book_title, desired_price, phoneNumber)
    else:
        print("Exiting program.")
