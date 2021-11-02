# xmrSale over tor
Currently you can use Tor in two ways
1) Connect xmrSale to your Monero node over a tor hidden service (if you're connecting to a remote node, may be preferable to SSH tunneling).
2) Host xmrSale as a Tor onion site

## Monero Node RPC Hidden Service
On your Monero node install tor and in `/etc/tor/torrc`:
```
HiddenServiceDir /var/lib/tor/node_rpc/
HiddenServicePort NODE_RPC_PORT 127.0.0.1:NODE_RPC_PORT
HiddenServiceDir /var/lib/tor/wallet_rpc/
HiddenServicePort WALLET_RPC_PORT 127.0.0.1:WALLET_RPC_PORT
```
with the appropriate NODE_RPC_PORT () and WALLET_RPC_PORT ()
then
```
sudo systemctl restart tor
cat /var/lib/tor/node_rpc/hostname
```
to get the onion URL for your tor hidden service. Add this in `config.py` like `tor_bitcoinrpc_host = "http://u7...bid.onion"`

On your xmrSale machine, install tor and in `/etc/tor/torrc` (thanks @x_y:matrix.org):
```
SocksPort 127.0.0.1:9050 IsolateClientProtocol IsolateDestPort IsolateDestAddr ExtendedErrors IPv6Traffic PreferIPv6 KeepAliveIsolateSOCKSAuth
SocksPolicy accept 127.0.0.1
SocksPolicy reject *
```
Now start the tor proxy on your xmrSale machine with `sudo tor` and xmrSale is now configured to connect to your node at localhost over tor.


## xmrSale Tor .Onion
It's possible to run xmrSale on an onion site. However, currently this will only work in some Tor browsers, and likely not in the official Tor Browser unless you fully enable javascript which is a bad idea. This is something we would like to change in the future.

On your xmrSale machine, install tor and in `/etc/tor/torrc`:
```
HiddenServiceDir /var/lib/tor/xmrsale/
HiddenServiceVersion 3
HiddenServicePort 80 127.0.0.1:8000
```
then
```
sudo systemctl restart tor
cat /var/lib/tor/xmrsale/hostname
```
to get your onion URL. Go visit!
