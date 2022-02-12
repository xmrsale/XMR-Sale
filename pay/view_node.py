import time
import uuid
import qrcode
import json
import moneropy

import config
import database
from payments.price_feed import get_xmr_value

BLOCKEXPLORER_API = "https://..."



class xmrd:
    def __init__(self):
        if config.secret_spend_key is not None:
            self.account = self.load_wallet_from_sk(config.secret_spend_key)
        elif config.seed_phrase is not None:
            self.account = self.load_wallet_from_seed(config.seed_phrase)
        else:
            raise Exception("Incorrect config -- Neither secret_spend_key or seed_phrase specified. ")
        
        print("Next address is #{}".format(self.get_next_address_index())  


    def create_qr(self, uuid, address, value):
        qr_str = "{}?amount={}&label={}".format(address.upper(), value, uuid)
        img = qrcode.make(qr_str)
        img.save("static/qr_codes/{}.png".format(uuid))
        return


    def check_payment(self, address):
        conf_paid, unconf_paid = 0, 0
        try:
            r = requests.get(self.api + "/address/{}".format(address))
            r.raise_for_status()
            stats = r.json()
            conf_paid = stats["chain_stats"]["funded_txo_sum"] / (10 ** 8)
            unconf_paid = stats["mempool_stats"]["funded_txo_sum"] / (10 ** 8)
            time.sleep(2)
            return conf_paid, unconf_paid

        except Exception as e:
            logging.error(
                "Failed to fetch address information from mempool: {}".format(e)
            )

        return 0, 0

    def next_address(self):
        return database.get_next_address_index()

    def get_address(self, amount, label):
        
        return None