from common import *


from email.message import EmailMessage
import ssl
import smtplib



def checkPriceChange():
    """
    first loop through each product in the csv by reading it into a pandas datafram
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
    product_links = {}
    products = pd.read_csv("products.csv")
    products.drop(products.filter(regex="Unname"),axis=1, inplace=True)
    for line, product in products.iterrows():
        url = product['Link']
        price = float(product['Price'])
        last_updated = product['Last_updated']
        time_difference = (datetime.now() - datetime.strptime(last_updated.strip(),"%Y-%m-%d %H:%M:%S")).days
        print(time_difference)
        if time_difference >= 1:
                response = getResponse(url)
                product_name = getProductName(response)
                still_available = getProductAvailability(response)
                if not still_available: # Scenario 1
                    product_prices[product_name] = (None,None)
                    product['Price'] = 0

                else:
                    new_price = getProductPrice(response)
                    if price == 0.0: # Scenario 2
                        product_prices[product_name] = (new_price, None)
                        product_links[product_name] = url
                        product['Price'] = new_price


                    price_change = new_price - price
                    if price_change < 0: # Scenario 3 and 4
                        product_links[product_name] = url
                        change = ((new_price - price)/price) * 100
                        product_prices[product_name] = {new_price, change}
                        product['Price'] = new_price
                product['Last_updated'] = str(pd.to_datetime('now').to_pydatetime()).split(".")[0]
                products.loc[line] = product
    products.to_csv('products.csv',mode='w',index=False)
    return product_prices, product_links

def emailUser(price_changes,product_links):
    sender = #enter email here
    email_password = # set up an app password and enter that here
    recipient = #enter email here

    subject = "An update on your Amazon products"

    body = ""

    for product, price_information in price_changes.items():
        new_price, percentage_change = price_information

        if new_price == None and percentage_change == None:
            body += "{} is now out of stock! \n\n".format(product)
        elif new_price and percentage_change == None:
            body += "{} is now back in stock! You can find it here: {} \n\n".format(product, product_links[product])
        else:
            body += "{} is on discount at £{} with {}% reduction! You can find it here {}\n\n".format(product,new_price,abs(round(percentage_change,2)), product_links[product])

    em = EmailMessage()
    em['From'] = sender
    em['To'] = recipient
    em['Subject'] = subject

    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, recipient, em.as_string())

path = './products.csv'
file_exists = os.path.exists(path)
if file_exists:
    price_changes, product_links = checkPriceChange()
    if price_changes != {}:
        emailUser(price_changes, product_links)