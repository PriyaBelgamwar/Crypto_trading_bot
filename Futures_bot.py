import os
from binance.client import Client
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Logging setup (simpler)
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TradingBot:
    def __init__(self):
        key = os.getenv("API_KEY")
        secret = os.getenv("API_SECRET")

        # Connect to Binance testnet
        self.client = Client(key, secret, testnet=True)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    def submit_order(self, pair, action, order_kind, amount, rate=None):
        try:
            if order_kind == "MARKET":
                details = self.client.futures_create_order(
                    symbol=pair,
                    side=action,
                    type="MARKET",
                    quantity=amount
                )
            elif order_kind == "LIMIT":
                details = self.client.futures_create_order(
                    symbol=pair,
                    side=action,
                    type="LIMIT",
                    timeInForce='GTC',
                    quantity=amount,
                    price=rate
                )
            else:
                print("⚠️ Unsupported order type.")
                return

            print("✅ Order was sent!")
            print(details)
            logging.info(f"Order sent: {details}")
        except Exception as problem:
            print("❌ Something went wrong:", problem)
            logging.error(f"Error: {str(problem)}")

if __name__ == "__main__":
    bot = TradingBot()
    
    print("=== Simple Binance Testnet Bot ===")
    coin = input("Symbol (e.g. BTCUSDT): ").upper()
    side = input("Side (BUY or SELL): ").upper()
    order_type = input("Order type (MARKET or LIMIT): ").upper()
    qty = float(input("Amount to trade: "))

    limit_price = None
    if order_type == "LIMIT":
        limit_price = input("Limit price: ")

    bot.submit_order(coin, side, order_type, qty, limit_price)
