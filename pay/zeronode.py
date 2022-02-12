import time
import uuid
import qrcode
import json

import config
from payments.price_feed import get_xmr_value


class xmrd:
    def __init__(self):
        pass

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


class account:
    def __init__(self, address):
        self.address = address

    def get_address(self, major, minor):
        if major < 0 or major >= 2 ** 32:
            raise ValueError("major index {} is outside uint32 range".format(major))
        if minor < 0 or minor >= 2 ** 32:
            raise ValueError("minor index {} is outside uint32 range".format(minor))
        master_address = self.address()
        if major == minor == 0:
            return master_address
        master_svk = unhexlify(self.view_key())
        master_psk = unhexlify(self.address().spend_key())
        # m = Hs("SubAddr\0" || master_svk || major || minor)
        hsdata = b"".join(
            [
                b"SubAddr\0",
                master_svk,
                struct.pack("<I", major),
                struct.pack("<I", minor),
            ]
        )
        m = keccak_256(hsdata).digest()
        # D = master_psk + m * B
        D = ed25519.add_compressed(
            ed25519.decodepoint(master_psk),
            ed25519.scalarmult(ed25519.B, ed25519.decodeint(m)),
        )
        # C = master_svk * D
        C = ed25519.scalarmult(D, ed25519.decodeint(master_svk))
        netbyte = bytearray(
            [
                42
                if master_address.is_mainnet()
                else 63
                if master_address.is_testnet()
                else 36
            ]
        )
        data = netbyte + ed25519.encodepoint(D) + ed25519.encodepoint(C)
        checksum = keccak_256(data).digest()[:4]
        return address.SubAddress(base58.encode(hexlify(data + checksum)))
