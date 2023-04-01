import yfinance as yf

tickers = yf.Tickers('asii.jk')

a = tickers.tickers.ASII.JK.info
b = tickers.tickers.AAPL.history(period="1mo")
c = tickers.tickers.GOOG.actions

print(a)