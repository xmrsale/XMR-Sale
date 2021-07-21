import requests

import config


def get_price(currency):
    price_feed = "https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=USD"
    r = requests.get(price_feed)

    for i in range(config.connection_attempts):
        try:
            price_data = r.json()
            price = price_data["USD"]
            break

        except Exception as e:
            print(e)
            print(
                "Attempting again... {}/{}...".format(i + 1, config.connection_attempts)
            )

    else:
        raise ("Failed to reach {}.".format(price_feed))

    return price


def get_xmr_value(dollar_value, currency):
    price = get_price(currency)
    if price is not None:

        try:
            float_value = float(dollar_value) / float(price)
            if not isinstance(float_value, float):
                raise Exception("Dollar value should be a float.")
        except Exception as e:
            print(e)

        return float_value

    raise Exception("Failed to get dollar value.")
