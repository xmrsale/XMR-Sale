import os

# Monero node connection settings
# This should point to your monero/lnd node,
# with the correct RPC port as set in your config.
# Connecting through local host as  i'm running xmrSale on my node
host = "127.0.0.1"
monerod_rpcport = "18081"
monerowallet_rpcport = "18090"

# From monero.conf or wherever you provide the monero arguments
# possibly in `monerod.service` and `monerowallet.service` (see docs)
monerod_username = os.getenv("MONERODRPC_USER")
monerod_password = os.getenv("MONERODRPC_PASS")
wallet_username = os.getenv("WALLETRPC_USER")
wallet_password = os.getenv("WALLETRPC_PASS")

## E.g.
# monerod_username = "monerorpc"
# monerod_password = "mypass"
# wallet_username = "walletrpc"
# wallet_password = "mypass2"

# File in which API key will be stored
api_key_path = "xmrSale_API_key"


#### Connect To Remote Node ####
# Can use SSH or TOR
# to tunnel/relay ports required to talk to the node via RPC (gRPC for lightning)

# SSH tunnel to node
# Make sure this command works `ssh HOST@IP -q -N -L 8332:localhost:8332`
# Use host = "127.0.0.1" and you will be able to see your node on 8332
tunnel_host = None # "HOST@IP"

# or tor hidden service for RPC (see docs for how to set up), need onion:
tor_monerorpc_host = None # e.g. "http://if...dwr.onion"
# and a tor proxy, default 127.0.0.1:9050 (for Tor Browser use "127.0.0.1:9150")
tor_proxy = None
################################

# Check for payment every xx seconds
pollrate = 15

# Payment expires after xx seconds
payment_timeout = 60*60

# Required confirmations for a payment
required_confirmations = 10

# Global connection attempts
connection_attempts = 3

# Generic redirect url after payment
redirect = "https://github.com/xmrsale/xmrsale"

# Payment method
pay_method = "monerod"
# Switch payment_method to lnd if you want to use lightning payments instead. And uncomment lnd_dir.
#pay_method = "lnd"
# lnd_dir is only needed if you want to copy macaroon and TLS cert locally
#lnd_dir = "~/.lnd/"
#lnd_rpcport = "10009"
#lnd_macaroon = "invoice.macaroon"
#lnd_cert = "tls.cert"

# DO NOT CHANGE THIS TO TRUE UNLESS YOU WANT ALL PAYMENTS TO AUTOMATICALLY
# BE CONSIDERED AS PAID.
free_mode = False
