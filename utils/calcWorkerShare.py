def calculate_payout(amount: float) -> float:
    """
    Рассчитывает выплату в зависимости от суммы.

    Условия:
    - Если сумма < 20000 → 50% от суммы
    - Если сумма < 40000 → 30% от суммы
    - Иначе → 20% от суммы
    """
    if amount < 10000:
        return amount * 0.3
    elif amount < 20000:
        return amount * 0.4
    else:
        return amount * 0.5


# Примеры:

