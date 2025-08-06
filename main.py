import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from hyperliquid.api import API
from hyperliquid.utils.constants import TESTNET_API_URL
from Docs import Trading_Tracker_Utils
from Docs import GoogleSheets 
from Docs import classify_trades

class TradingTracker:
    def __init__(self):
        self.api = API(TESTNET_API_URL)
        self.address, self.info, self.exchange = Trading_Tracker_Utils.setup(TESTNET_API_URL, skip_ws=True)

    def get_fills(self, coin_filter="ETH"):
        fills = self.info.user_fills(self.address)
        if not fills:
            print("No fills found.")
            return []

        filtered = []
        for fill in fills:
            if fill.get("coin") == coin_filter:
                readable_time_dt = datetime.fromtimestamp(fill.get("time") / 1000)  
                readable_time_str = readable_time_dt.strftime('%Y-%m-%d %H:%M:%S')
                side_code = fill.get("side")
                start_position = float(fill.get("startPosition", 0))
                size = float(fill.get("sz", 0))
                closed_pnl = float(fill.get("closedPnl", 0))
                transformed = {
                    "Coin": fill.get("coin"),
                    "Price": fill.get("px"),
                    "Size": size,
                    "Trading Type": classify_trades.classify_trades(size, start_position, closed_pnl, side_code),
                    "Time": readable_time_str,
                    "Transaction ID": fill.get("tid"),
                    "Position": start_position,
                    "Fee":float(fill.get("fee", 0)),
                    "PNL": float(fill.get("closedPnl", 0)),
                    "TotalPNL": round(float(fill.get("closedPnl", 0)) - float(fill.get("fee", 0)),2),
                    "_timestamp": readable_time_dt
                }
                filtered.append(transformed)

        filtered.sort(key=lambda x: x["_timestamp"], reverse= False)

        for f in filtered:
            f.pop("_timestamp", None)

        return filtered

    def upload_to_google_sheets(self, fills, spreadsheet_id, worksheet_index=0, service_account_path="service_account.json"):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id)
        worksheet = sheet.get_worksheet(worksheet_index)

        header = ["Coin", "Price", "Size", "Trading Type", "Time", "Transaction ID", "Position", "Fee", "PNL", "TotalPNL"]
        existing_rows = worksheet.get_all_values()

        if not existing_rows or not existing_rows[0]:
            worksheet.insert_row(header, index=1)
            existing_rows = [header]   

        data_rows = [[
        fill.get("Coin"),
        fill.get("Price"),
        fill.get("Size"),
        fill.get("Trading Type"),
        fill.get("Time"),
        fill.get("Transaction ID"),
        fill.get("Position"),
        fill.get("Fee"),
        fill.get("PNL"),
        fill.get("TotalPNL")
    ] for fill in fills]
        
        if data_rows:
            worksheet.append_rows(data_rows, value_input_option="USER_ENTERED")
            print(f"Uploaded {len(data_rows)} rows.")
        else:
            print("No data rows to upload.")
        return sheet     

    def stats(self, sheet, fills):
        try:
            trading_data_sheet = sheet.get_worksheet(0)
            trading_data_sheet.update_title("Trading Data")
        except Exception as e:
            print("Failed to rename first worksheet:", e)

        try:
            stats_sheet = sheet.get_worksheet(1)
        except gspread.exceptions.WorksheetNotFound:
            stats_sheet = sheet.add_worksheet(title="Stats", rows="10", cols="4")

        df = pd.DataFrame(fills)
        all_pnl = df["TotalPNL"].sum()
        total_fees = df["Fee"].sum()
        long_count = df["Trading Type"].value_counts().get("Close Long", 0)
        short_count = df["Trading Type"].value_counts().get("Close Short", 0)

        stats_data = [
            ["Metric", "Value"],
            ["All PNL", float(all_pnl)],
            ["Total Fees", float(total_fees)],
            ["Number of trades for Longs", int(long_count)],
            ["Number of trades for Shorts", int(short_count)]
        ]

        stats_sheet.clear()
        stats_sheet.update(range_name="A1", values=stats_data)

        print("Trade statistics uploaded to 'Stats' worksheet.")

if __name__ == "__main__":  
    tracker = TradingTracker()
    fills = tracker.get_fills()
    spreadsheet_id, service_account_path = GoogleSheets.load_config()
    sheet = tracker.upload_to_google_sheets(fills, spreadsheet_id, service_account_path=service_account_path) # 
    tracker.stats(sheet, fills)