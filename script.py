from database import DatabaseManager
from nepse import Nepse

def getCurrentStocksDetail():    
    nepse = Nepse()
    nepse.setTLSVerification(False)
    today_price = nepse.getLiveMarket()
    return today_price

def searchCompany(data, symbol):
    for stock in data["content"]:
        if stock["symbol"]  == symbol:
            return stock
    return None

def getStockPrice(data, symbol):
    stock_details = searchCompany(data, symbol)
    price = stock_details['lastTradedPrice']
    return price

def sendNotification(user_id, message):
    print(message)

def run():
    today_price = getCurrentStocksDetail()
    db = DatabaseManager()
    users = db.getAllUsers()
    if users:
        for user in users:
            price_tracks = db.getUserActivePriceTracker(user['id'])
            for pt in price_tracks:
                stock_price = getStockPrice(today_price, pt['symbol'])
                if pt['min_target_price'] >= stock_price:
                    message = f"{user['username']} {pt['symbol']} has reached minimum threshold price which is {pt['min_target_price']} and stock price is {stock_price}"
                    sendNotification(user['id'], message)
                elif pt['max_target_price'] <= stock_price:
                    message = f"{user['username']} {pt['symbol']} has reached maximum threshold price which is {pt['max_target_price']} and stock price is {stock_price}"
                    sendNotification(user['id'], message)

if __name__ == "__main__":
    run()