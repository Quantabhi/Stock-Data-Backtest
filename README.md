<h1 align="center">Stock Data Analysis with TA</h1>
<p align="center"><img src="https://media.giphy.com/media/QvFcfanDdhRHXHeYLX/giphy.gif" width="400px" height="180px"></p>
<table style="width: 100%;">
    <tr>
        <td style="width: 50%; text-align: left;">
            <img width="500" src="https://github.com/Quantabhi/Stock-Data-Backtest/assets/117148458/263e3fb3-3a2e-41c2-888a-fa421dec5f5c" alt="Image 1">
        </td>
        <td style="width: 50%; text-align: right;">
            <img width="500" src="https://github.com/Quantabhi/Stock-Data-Backtest/assets/117148458/5b38ed2a-79c3-45d2-8cd0-1ddad3dd26af" alt="Image 2">
        </td>
      <td style="width: 50%; text-align: right;">
            <img width="500" src="https://github.com/Quantabhi/Stock-Data-Backtest/assets/117148458/fb26c964-16d5-4448-b3cb-63743320e9e2" alt="Image 3">
        </td>
      <td style="width: 50%; text-align: right;">
            <img width="500" src="https://github.com/Quantabhi/Stock-Data-Backtest/assets/117148458/fb26c964-16d5-4448-b3cb-63743320e9e2" alt="Image 4">
        </td>
    </tr>
</table>
<h1 align="center"> Getting Started </h1>
Streamlit web application provides an interactive interface for analyzing stock data using various technical analysis indicators like Moving Averages (MA), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD)
<h2>Library Use</h2>
    <ul>
        <li><code>pip streamlit</code></li>
        <li><code>pip pandas</code></li>
        <li><code>pip install matplotlib</code></li>
        <li><code>pip yfinance</code></li>
    </ul>
 <h2> Cumulative Profit/Loss from 50-day and 200-day MA Crossover</h2>
The script iterates through each row of stock data, detecting buy and sell signals based on the crossover of two moving averages (MA). When the shorter-term MA crosses above the longer-term MA, it triggers a buy signal, and when it crosses below, it triggers a sell signal. The script calculates the profit/loss (PNL) for each trade and accumulates the PNL over time. It also handles the case where no signal is detected, ensuring the PNL remains unchanged in such instances.
 <h2> Cumulative Profit/Loss from Relative Strength Index (RSI) buy rsi is 20 and sell rsi is 80</h2>
 This section of the code calculates the Relative Strength Index (RSI) for the stock data and generates buy and sell signals based on RSI thresholds. It then computes the cumulative profit/loss (PNL) for trades executed according to these signals. This enables the analysis of trading strategies utilizing RSI indicators within the specified time frame.
<h2> Cumulative Profit/Loss from Moving Average Convergence Divergence(MACD)</h2>
This section of the code defines a function to calculate the Moving Average Convergence Divergence (MACD) indicator for the stock data. It then generates buy and sell signals based on MACD crossovers and computes the cumulative profit/loss (PNL) for trades executed according to these signals. This facilitates the analysis of trading strategies utilizing MACD indicators within the specified time frame.
 
