# Hyperliquid Trades to Google Sheets 📊

This project fetches your recent trades from the [Hyperliquid](https://hyperliquid.xyz/) testnet and uploads them to a Google Sheet, with trade statistics automatically calculated.

## 🚀 Features
- Connects to Hyperliquid API (Testnet)
- Filters fills by coin (e.g. ETH)
- Classifies trades (e.g. Open Long, Close Short, etc.)
- Uploads trades to Google Sheets
- Creates a summary "Stats" worksheet

## 🧰 Tech Stack
- Python
- Hyperliquid API
- Google Sheets API (`gspread`)

## 🛠️ Setup Instructions
1. **Clone this repo**:
   ```bash
   git clone https://github.com/hzhhdh/hyperliquid-trades-to-google-sheets.git
   cd hyperliquid-trades-to-google-sheets
2. **Install dependencies**:
   pip install -r requirements.txt
3. **Set up your config**:
Copy Docs/config.json, SheetID.json, and CloudKeys.json and fill in your own values.

4. **Run the script:**
python main.py

📈 Output Example
Your Google Sheet will have:
- A "Trading Data" worksheet with recent fills
- A "Stats" worksheet showing:
- Total PnL
- Total fees
