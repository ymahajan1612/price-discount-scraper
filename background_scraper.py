from common import *



def checkPriceChange():
    file = open("products.csv","r")
    """
    first loop through each product in the csv
    compare current time and last_updated value
    if the difference is >= 24 hrs then pull data for that product
    check if the product is still in stock then add to a dict {product_name: (null, null)}
    compare the price value in the csv for that product vs the fetched value
    if the fetched price < original price then add to a dict : {product_name: (new price, % decrease)}

    """
    product_prices = {}
    all_products = file.readlines()

    for line, row in enumerate(all_products):
        if line != 0:
            product  = row.split(",")
            url = product[0]
            price = float(product[1])
            last_updated = product[2]
            time_difference = (datetime.now() - datetime.strptime(last_updated.strip(),"%Y-%m-%d %H:%M:%S")).days
            if time_difference >= 1:
                response = getResponse(url)
                product_name = getProductName(response)
                still_available = getProductAvailability(response)
                if not still_available:
                    product_prices[product_name] = (None,None)
                else:
                    new_price = getProductPrice(response)
                    price_change = new_price - price
                    if price_change < 0:
                        change = ((new_price - price)/price) * 100
                        product_prices[product_name] = {new_price, change}
    return product_prices

checkPriceChange()