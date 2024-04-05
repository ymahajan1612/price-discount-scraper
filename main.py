from common import *


def addProduct():
    product_information = {}
    url = input("Enter product url: ")
    price = fetchProductDetails(url)

    exists = checkProductAlreadyExists(url)
    if exists:
        print("This product is already in the list")
        return

    # Adding product to the CSV file
    file = open('products.csv','a+', newline='')
    writer = csv.writer(file)
    writer.writerow([url, price.strip(),datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
    file.close()

def checkProductAlreadyExists(product_url):
    file = open('products.csv', 'r+', newline='')
    for product in file.readlines():
        url = product.split(",")[0]
        if url == product_url:
            file.close()
            return True
    file.close()
    return False


addProduct()

