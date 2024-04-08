from common import *



def checkPriceChange():
    """
    first loop through each product in the csv
    compare current time and last_updated value
    if the difference is >= 24 hrs then pull data for that product
    check if the product is still in stock then add to a dict {product_name: (null, null)}
    compare the price value in the csv for that product vs the fetched value
    if the fetched price < original price then add to a dict : {product_name: (new price, % decrease)}

    4 scenarios:
        1: product is no longer in stock
        2: product was previously not in stock is now available
        3: Product is on a discount
        4: Product price has not changed
    """
    product_prices = {}
    products = pd.read_csv("products.csv")
    products.drop(products.filter(regex="Unname"),axis=1, inplace=True)
    for line, product in products.iterrows():
        url = product['Link']
        price = float(product['Price'])
        last_updated = product['Last_updated']
        time_difference = (datetime.now() - datetime.strptime(last_updated.strip(),"%Y-%m-%d %H:%M:%S")).days
        if time_difference >= 1:
                response = getResponse(url)
                product_name = getProductName(response)
                still_available = getProductAvailability(response)
                if not still_available: # Scenario 1
                    product_prices[product_name] = (None,None)
                    product['Price'] = 0
                    product['Last_updated'] = datetime.now()
                else:
                    new_price = getProductPrice(response)
                    if price == 0.0: # Scenario 2
                        product_prices[product_name] = (new_price, None)
                        product['Price'] = new_price
                        product['Last_updated'] = datetime.now()

                    price_change = new_price - price
                    if price_change < 0: # Scenario 3 and 4
                        change = ((new_price - price)/price) * 100
                        product_prices[product_name] = {new_price, change}
                        product['Price'] = new_price
                        product['Last_updated'] = datetime.now()
                products.loc[line] = product
    products.to_csv('products.csv',mode='w',index=False)

    return product_prices



print(checkPriceChange())