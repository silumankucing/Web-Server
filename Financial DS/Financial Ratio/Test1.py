import yfinance as yf

tickers = yf.Tickers('msft aapl goog asii.jk')

a = tickers.tickers.MSFT.info
b = tickers.tickers.AAPL.history(period="1mo")
c = tickers.tickers.GOOG.actions
d = tickers.tickers.ASII.actions

print(d)