from binance.client import Client
import os
import logging
from dotenv import load_dotenv

# Load your API keys
load_dotenv()

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class BasicBot:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce='GTC',
                    quantity=quantity,
                    price=price
                )
            print("✅ Order placed successfully!")
            print(order)
            logging.info(f"Order placed: {order}")
        except Exception as e:
            print("❌ Failed to place order:", str(e))
            logging.error(f"Error placing order: {str(e)}")

if __name__ == "__main__":
    bot = BasicBot()
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (BUY or SELL): ").upper()
    order_type = input("Enter order type (MARKET or LIMIT): ").upper()
    quantity = float(input("Enter quantity: "))
    price = None
    if order_type == "LIMIT":
        price = input("Enter price: ")

    bot.place_order(symbol, side, order_type, quantity, price)
