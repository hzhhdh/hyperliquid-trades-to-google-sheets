import json
import os

def load_config():
    base_dir = os.path.dirname(__file__)
    
    # Path to service account key file
    service_account_path = os.path.join(base_dir, "CloudKeys.json")
    
    # Load spreadsheet ID from a config JSON (optional)
    sheet_config_path = os.path.join(base_dir, "SheetID.json")
    
    with open(sheet_config_path, "r") as f:
        config = json.load(f)
    
    spreadsheet_id = config["spreadsheet_id"]
    
    return spreadsheet_id, service_account_path
