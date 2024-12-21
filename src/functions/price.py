pricing_data = {
    "base_price": 20000,
    "discounts": [
        {"min_participants": 3, "discount": 0.24},
        {"min_participants": 5, "discount": 0.44505},
    ]
}

def calculate_price(adults: int, children: int) -> int:
    price = pricing_data["base_price"]
    participants = adults + children

    for discount in pricing_data["discounts"]:
        if participants >= discount["min_participants"]:
            price = pricing_data["base_price"] *  (1 - discount["discount"])
        else:
            break

    return price * participants