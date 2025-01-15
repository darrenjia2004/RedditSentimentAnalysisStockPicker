from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import config
import asyncio

client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
acc = dict(client.get_account())
# for k,v in acc.items():
#     print(f"{k:30}{v}")

order_details = MarketOrderRequest(
    symbol = "SPY",
    qty = 1,
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY
)
order = client.submit_order(order_data = order_details)


# async def trade_status(data):
#     print(data)

# trades = TradingStream(config.API_KEY, config.SECRET_KEY, paper=True)
# trades.subscribe_trade_updates(trade_status)
# trades.run()

assets = [asset for asset in client.get_all_positions()]
positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]
print("Positions")
print(f"{'Symbol':9}{'Quantity':>4}{'Value':>15}")
print("-" * 28)
for position in positions:
    print(f"{position[0]:9}{position[1]:>4}{float (position[1]) * float(position[2]):>15.2f}")