def classify_trades(size, start_position, closed_pnl,side_code):
    if side_code == "B":
        if size > 0 and start_position == 0 and closed_pnl == 0:
            return "Open Long"
        elif size > 0 and start_position > 0 and closed_pnl == 0:
            return "Add Long"
        elif -size == start_position and -start_position == size and closed_pnl != 0:
            return "Close Short"
        elif size > 0 and start_position < 0 and closed_pnl !=0:
            return "Take Profit Short"
        else:
            return "Unknown Long Trade"

    elif side_code == "A":
        if size > 0 and start_position == 0 and closed_pnl == 0:
            return "Open Short"
        elif size > 0 and start_position < 0 and closed_pnl == 0:
            return "Add Short"
        elif size == start_position and start_position == size and closed_pnl != 0:
            return "Close Long"
        elif size > 0 and start_position > 0 and closed_pnl != 0:
            return "Take Profit Long"
        else:
            return "Unknown Short Trade"