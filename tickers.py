import csv
import pickle

# Read tickers from CSV
tickers = []
with open('tickers.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ticker = row[0].split(',')[0].strip('"')
        tickers.append(ticker)

# Remove common words from the list
excludedTickers = ['AI', 'IQ']
for ticker in excludedTickers:
    tickers.remove(ticker)

# Save tickers to a pickle file
with open('tickers.pkl', 'wb') as f:
    pickle.dump(tickers, f)