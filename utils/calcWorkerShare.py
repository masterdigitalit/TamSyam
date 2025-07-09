def calculate_payout(amount: float) -> float:

    if amount < 10000:
        return amount * 0.3
    elif amount < 20000:
        return amount * 0.4
    else:
        return amount * 0.5



