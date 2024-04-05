from common import *



def checkPriceChange():
    file = open("products.csv","r")
    """
    first loop through each product in the csv
    compare current time and last_updated value
    if the difference is >= 24 hrs then pull data for that product
    compare the price value in the csv for that product vs the fetched value
    if the fetched price < original price then add to a dict : {product_name: (new price, % decrease)}
    """
    for product in file.readlines():
        original_price =

