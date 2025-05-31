def get_sl_target_message(entry_price):
    target = entry_price * 1.06
    sl = entry_price * 0.97
    trail_info = "Move SL to cost at 5%, then trail ₹3"
    return sl, target, trail_info
