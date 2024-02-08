import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Title
st.write(
    f"""
    <div style="display: flex; justify-content: center;">
        <h1>Stock Data Analysis with TA</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# User input for stock ticker symbol
ticker_symbol = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL)If you want to access Indian stock market data, use stock symbols like ITC.NS")

# User input for time frame
time_frame = st.selectbox("Select Time Frame", ["120d","1y", "2y", "3y", "4", "5y", "7y" ,"10y", "15y" , "Max"])

# Fetching stock data
if ticker_symbol:
    try:
        stock_data = yf.download(ticker_symbol, period=time_frame)
        stock_data['50MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['200MA'] = stock_data['Close'].rolling(window=200).mean()

        # Calculate cumulative PNL for MA signals
        buy_price_ma = 0
        cumulative_pnl_ma = 0
        cumulative_pnls_ma = []

        for index, row in stock_data.iterrows():
            if row['50MA'] > row['200MA'] and buy_price_ma == 0:  # Buy signal
                buy_price_ma = row['Close']
            elif row['50MA'] < row['200MA'] and buy_price_ma != 0:  # Sell signal
                sell_price_ma = row['Close']
                cumulative_pnl_ma += (sell_price_ma - buy_price_ma)
                cumulative_pnls_ma.append(cumulative_pnl_ma)
                buy_price_ma = 0
            else:
                cumulative_pnls_ma.append(cumulative_pnl_ma)

        # Calculate RSI
        def calculate_rsi(data, window=14):
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        # Calculate RSI
        stock_data['RSI'] = calculate_rsi(stock_data)

        # Generate RSI buy and sell signals
        stock_data['Buy_Signal_RSI'] = (stock_data['RSI'] < 20) & (stock_data['RSI'].shift(1) >= 20)
        stock_data['Sell_Signal_RSI'] = (stock_data['RSI'] > 80) & (stock_data['RSI'].shift(1) <= 80)

        # Calculate cumulative PNL for RSI signals
        initial_cash_rsi = 10000  # Initial investment amount
        cash_rsi = initial_cash_rsi
        stock_rsi = 0
        pnl_rsi = []

        for i in range(len(stock_data)):
            if stock_data['Buy_Signal_RSI'].iloc[i]:
                stock_rsi += cash_rsi / stock_data['Close'].iloc[i]
                cash_rsi = 0
            elif stock_data['Sell_Signal_RSI'].iloc[i]:
                cash_rsi += stock_rsi * stock_data['Close'].iloc[i]
                stock_rsi = 0
            pnl_rsi.append(cash_rsi + stock_rsi * stock_data['Close'].iloc[i])

        # Function to calculate MACD
        def calculate_macd(data, short_window=20, long_window=50):
            short_ema = data['Close'].ewm(span=short_window, min_periods=1, adjust=False).mean()
            long_ema = data['Close'].ewm(span=long_window, min_periods=1, adjust=False).mean()
            macd = short_ema - long_ema
            signal = macd.ewm(span=9, min_periods=1, adjust=False).mean()
            return macd, signal

        # Calculate MACD
        stock_data['MACD'], stock_data['Signal'] = calculate_macd(stock_data)

        # Generate MACD buy and sell signals
        stock_data['Buy_Signal_MACD'] = (stock_data['MACD'] > stock_data['Signal']) & (stock_data['MACD'].shift(1) <= stock_data['Signal'].shift(1))
        stock_data['Sell_Signal_MACD'] = (stock_data['MACD'] < stock_data['Signal']) & (stock_data['MACD'].shift(1) >= stock_data['Signal'].shift(1))

        # Calculate cumulative PNL for MACD signals
        initial_cash_macd = 10000  # Initial investment amount
        cash_macd = initial_cash_macd
        stock_macd = 0
        pnl_macd = []

        for i in range(len(stock_data)):
            if stock_data['Buy_Signal_MACD'].iloc[i]:
                stock_macd += cash_macd / stock_data['Close'].iloc[i]
                cash_macd = 0
            elif stock_data['Sell_Signal_MACD'].iloc[i]:
                cash_macd += stock_macd * stock_data['Close'].iloc[i]
                stock_macd = 0
            pnl_macd.append(cash_macd + stock_macd * stock_data['Close'].iloc[i])

        # Plotting closing price
        st.subheader(f'{ticker_symbol} Closing Price')
        fig_close, ax_close = plt.subplots(figsize=(10, 6))
        ax_close.plot(stock_data['Close'], label='Closing Price', color='black')
        ax_close.set_xlabel('Date')
        ax_close.set_ylabel('Price')
        ax_close.set_title(f'{ticker_symbol} Closing Price')
        ax_close.legend()
        st.pyplot(fig_close)

        # Plotting cumulative PNL for MA signals
        st.subheader(f'{ticker_symbol} Cumulative Profit/Loss (MA)')
        fig_ma, ax_ma = plt.subplots(figsize=(10, 6))
        ax_ma.plot(cumulative_pnls_ma, label='Cumulative PNL (MA)', color='blue')
        ax_ma.set_xlabel('Trade')
        ax_ma.set_ylabel('Cumulative Profit/Loss (MA)')
        ax_ma.set_title(f'{ticker_symbol} Cumulative Profit/Loss from 50-day and 200-day MA Crossover')
        ax_ma.legend()
        st.pyplot(fig_ma)

        # Plotting cumulative PNL for RSI signals
        st.subheader(f'{ticker_symbol} Cumulative Profit/Loss (RSI)')
        fig_rsi, ax_rsi = plt.subplots(figsize=(10, 6))
        ax_rsi.plot(pd.to_datetime(stock_data.index), pnl_rsi, label='Cumulative PNL (RSI)', color='red')
        ax_rsi.set_xlabel('Date')
        ax_rsi.set_ylabel('Cumulative Profit/Loss (RSI)')
        ax_rsi.set_title(f'{ticker_symbol} Cumulative Profit/Loss from Relative Strength Index (RSI) buy rsi is 20 and sell rsi is 80')
        ax_rsi.legend()
        st.pyplot(fig_rsi)

        # Plotting cumulative PNL for MACD signals
        st.subheader(f'{ticker_symbol} Cumulative Profit/Loss (MACD)')
        fig_macd, ax_macd = plt.subplots(figsize=(10, 6))
        ax_macd.plot(pd.to_datetime(stock_data.index), pnl_macd, label='Cumulative PNL (MACD)', color='green')
        ax_macd.set_xlabel('Date')
        ax_macd.set_ylabel('Cumulative Profit/Loss (MACD)')
        ax_macd.set_title(f'{ticker_symbol} Cumulative Profit/Loss from Moving Average Convergence Divergence (MACD)')
        ax_macd.legend()
        st.pyplot(fig_macd)

    except Exception as e:
        st.error(f"Error: {e}")
