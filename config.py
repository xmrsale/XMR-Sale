import os

# Monero node connection settings
host = "127.0.0.1"
monerowallet_rpcport = "18090"
cli_dir="monero-cli"
wallet_name="xmrsale_wallet"

# File in which API key will be stored
api_key_path = "xmrSale_API_key"

# Contact public monero-node over tor (`tor` must be running. Also uses torsocks - `apt install torsocks`)
tor = False

# Use SSH to tunnel into a machine and connect to port locally
# (leave None)
tunnel_host = None

# Amount $X you want to instantly accept 0-conf payments under. (or None)
zero_conf_limit = 100

# Check for payment every xx seconds
pollrate = 15

# Payment expires after xx seconds
payment_timeout = 60*60

# Required confirmations for a payment
required_confirmations = 5

# Global connection attempts
connection_attempts = 10

# Generic redirect url after payment
redirect = "https://github.com/xmrsale/xmrsale"

# Payment method
pay_method = "monerod"

# DO NOT CHANGE THIS TO TRUE UNLESS YOU WANT ALL PAYMENTS TO AUTOMATICALLY
# BE CONSIDERED AS PAID.
free_mode = False
