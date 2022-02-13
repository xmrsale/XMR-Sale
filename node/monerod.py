import time
import uuid
import qrcode
import json

import config
from payments.price_feed import get_xmr_value

if config.tor_monerorpc_host is not None:
    from gateways.tor import session


def call_tor_monero_rpc(method, params):
    url = "{}:{}".format(config.tor_monerorpc_host, config.rpcport)
    payload = json.dumps({"method": method, "params": params})
    headers = {"content-type": "application/json", "cache-control": "no-cache"}
    response = session.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=(config.username, config.password),
    )
    return json.loads(response.text)


class xmrd:
    def __init__(self, rpc_secret):
        from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

        # monerowallet_connection_str = "http://{}:{}@{}:{}/json_rpc".format(
        #     config.wallet_username, config.wallet_password, config.host, config.monerowallet_rpcport,# config.wallet
        # )

        monerowallet_connection_str = "http://monerorpc:{}@{}:{}/json_rpc".format(
            rpc_secret,
            config.host,
            config.monerowallet_rpcport,  # config.wallet
        )

        # for i in range(config.connection_attempts):
        for i in range(5):
            if config.tor_monerorpc_host is None:
                self.tor = False
            else:
                self.tor = True
                print(
                    "Attempting to contact monerod rpc tor hidden service: {}:{}".format(
                        config.tor_monerorpc_host, 0  # config.rpcport
                    )
                )

            try:
                # Normal Connection
                if config.tor_monerorpc_host is None:
                    print(
                        "Attempting to connect to mondero wallet rpc daemon {}.".format(
                            monerowallet_connection_str
                        )
                    )
                    self.monerowallet_rpc = AuthServiceProxy(
                        monerowallet_connection_str
                    )
                    balance = self.monerowallet_rpc.get_balance()
                    print(balance)
                    print("Successfully contacted monero wallet.")
                else:
                    info = call_tor_bitcoin_rpc("getblockchaininfo", None)
                    print(info)

                break

            except Exception as e:
                print(e)
                time.sleep(config.pollrate)
                print("Attempting again... {}/{}...".format(i + 1, 5))
        else:
            raise Exception(
                "Could not connect to monerod. \
                Check your RPC / port tunneling settings and try again."
            )

    def create_qr(self, uuid, address, value):
        qr_str = "{}?amount={}&label={}".format(address.upper(), value, uuid)

        img = qrcode.make(qr_str)
        img.save("static/qr_codes/{}.png".format(uuid))
        return

    def check_payment(self, address):
        try:
            if not self.tor:
                transactions = self.monerowallet_rpc.get_payments(
                    {"payment_id": address}
                )
            else:
                transactions = call_tor_bitcoin_rpc("listtransactions", None)["result"]

        except Exception as e:
            print(e)
            print(
                "Can't connect to wallet-rpc, pausing for a few seconds in case of high load."
            )
            time.sleep(5)
            return 0, 0

        if "payments" not in transactions.keys():
            return 0, 0
        else:
            transactions = transactions["payments"]

        conf_paid = 0
        unconf_paid = 0
        current_block_height = self.monerowallet_rpc.get_height()["height"]
        for tx in transactions:
            print(tx)
            if (
                current_block_height - tx["block_height"]
                >= config.required_confirmations
            ):
                conf_paid += tx["amount"] / 10 ** 12
            else:
                unconf_paid += tx["amount"] / 10 ** 12

        return conf_paid, unconf_paid

    def get_address(self, amount, label):
        for i in range(config.connection_attempts):
            try:
                if not self.tor:
                    address_data = self.monerowallet_rpc.make_integrated_address(label)
                    print(address_data)
                    address, payment_id = (
                        address_data["integrated_address"],
                        address_data["payment_id"],
                    )
                    return address, payment_id
                else:
                    address = call_tor_bitcoin_rpc("getnewaddress", [label])["result"]

                return address, None

            except Exception as e:
                print(e)
                print(
                    "Attempting again... {}/{}...".format(
                        i + 1, config.connection_attempts
                    )
                )
            if config.connection_attempts - i == 1:
                print("Reconnecting...")
                self.__init__()
        return None
