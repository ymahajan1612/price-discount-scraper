from common import *


def addProduct():
    product_information = {}
    createProductCSV()
    url = input("Enter product url: ")
    response = getResponse(url)
    exists = checkProductAlreadyExists(url)
    if exists:
        print("This product is already in the list")
        return

    if not getProductAvailability(response):
        print("This product is out of stock. You'll be notified when it's back")
        price = 0
    else:
        price = getProductPrice(response)
    # Adding product to the CSV file
    file = open('products.csv','a+',newline='')
    writer = csv.writer(file)
    writer.writerow([url, price ,str(datetime.now()).split(".")[0]])
    file.close()

def checkProductAlreadyExists(product_url):
    file = open('products.csv', 'r+')
    for product in file.readlines():
        url = product.split(",")[0]
        if url == product_url:
            file.close()
            return True
    file.close()
    return False


def createProductCSV():
    path = './products.csv'
    file_exists = os.path.exists(path)
    if not file_exists:
        with open('products.csv',"w") as file:
            writer = csv.writer(file,lineterminator='\n')
            writer.writerow(['Link','Price','Last_updated'])
            file.close()


addProduct()
