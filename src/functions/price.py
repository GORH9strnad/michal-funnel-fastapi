pricing_data = {
    "base_price": 15200,
    "discounts": [
        {"min_participants": 4, "discount": 4101},
    ]
}

def calculate_price(adults: int, children: int) -> int:
    price = pricing_data["base_price"]
    participants = adults + children

    for discount in pricing_data["discounts"]:
        if participants >= discount["min_participants"]:
            price = pricing_data["base_price"] - discount["discount"]
        else:
            break

    return price * participants