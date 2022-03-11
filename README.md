# xmrSale
### Monero specialized fork of [SatSale](https://github.com/nickfarrow/xmrSale)
xmrSale is a simple, easily deployable, lightweight Monero payment processor that connects to your own Monero node.

**Website & Docs**: [xmrSale.org](https://xmrsale.org)

## [try.xmrsale.org](https://try.xmrsale.org)

Donation Button     ----->  |  Monero Payment Gateway
:-------------------------:|:-------------------------:
[![Donate demo](docs/demo_donate.png)](https://try.xmrSale.org/) <br />(Click for embed demo)<br /> Initiates payment -----> |  [![Store demo](docs/demo_pay2.png)](https://try.xmrSale.org/) <br />(Click for WordPress payments demo)

**Always manually check significant payments**.
<!-- 

- [Purpose](#purpose)
- [Features](#features)
- [Installation (short!)](#installation--short--)
    + [Install](#install)
    + [Connect to your Monero Node](#connect-to-your-monero-node)
    + [Run xmrsale](#run-xmrsale)
    + [Embed a Donation Button](#embed-a-donation-button)
    + [Using HTTPS & Domains](#using-https---domains)
    + [Security](#security)
    + [Payment Gateway (Woocommerce)](#payment-gateway--woocommerce-)
- [Contributions welcomed](#contributions-welcomed)
- [Coming soon](#coming-soon)
- [Disclaimer](#disclaimer)
- [Sponsor](#sponsor) -->

## [try.xmrsale.org](https://try.xmrsale.org)

xmrSale is a self-hosted Monero payment processor, serving two primary use cases:
1. Donation button for your website that you can easily embed/link to anywhere.
2. Monero payment gateway, including a Woocommerce plugin that easily turns ANY Wordpress site into a Monero accepting store.

xmrSale makes donation buttons simple - easy copy paste the one line HTML iframe into your site. With a simple Python backend to talk to your own Monero node, xmrSale uses RPC to generate new addresses, and monitors the payment status with your own copy of the blockchain.

# Features
* You don't need your own node, xmrSale sets up `monero-wallet-rpc` and connects to public nodes (can be over tor!)
* Lightweight and highly extendable, basic html and css stying. Modular Python backend, take a [look at the code](xmrsale.py).
* Natively extendable to all Monerod node features (e.g. segwit) through RPC.
* QR codes, customizable required payment confirmations and payment expiry time.
* Privacy ensured. Monero only.

# Installation
If you want to run on your own node or docker, please checkout this [original branch](https://github.com/xmrsale/xmrSale/tree/original).

First, clone and install dependencies
```
git clone https://github.com/xmrsale/xmrSale
cd xmrSale/
pip3 install -r requirements.txt
```
## xmrSale Setup
Run
```
python3 xmrsale.py --setup
```
This will download monero-cli tools from `downloads.getmonero.org` which are used to manage payments.
Enter a new password for your new `xmrsale_wallet` (and `.keys`).
You **must backup your passphrase and seedphrase**.

Click `N` when asked whether you want to mine in the background, then type `exit`.

Now xmrsale will run the `monero-wallet-rpc` and sync with a public node (`node.moneroworld.com`). Once you see `Refresh done, blocks received...` you are ready to run xmrsale! If you want, you can adjust the `config.py` to your liking. You can always sync with `python3 xmrsale.py --sync`.

### Start xmrSale
Run xmrSale with
```
gunicorn xmrsale:app --timeout 120
```
That's it! If running locally, this will be `127.0.0.1:8000`. If you allow traffic on that port you should now also be able to view your xmrSale at `http://YOUR_IP:8000/`. If you're running on a VPS you may need to `ufw allow 8000` or make an [nginx config](https://github.com/xmrsale/xmrSale/blob/master/docs/HTTPS.md).

You will want to run gunicorn with nohup so it continues serving in the background:
```
nohup gunicorn xmrsale:app --timeout 120 > log.txt 2>&1 &
tail -f log.txt
```

### Embed a Donation Button
Now we have xmrSale running, let's embed the donation button into a website HTML:
```html
<iframe src="http://YOUR_SERVER_IP:8000/" style="margin: 0 auto;display:block;width:420px;height:460px;border:none;overflow:hidden;" scrolling="no"></iframe>
```

### Debugging
* Make sure you are synced `python3 xmrsale.py --sync`
* Check `rpc.log` for node connection errors.
* Processes already running / wallet in use -> Kill any monero-rpc running in the background and restart. `ps ax | grep monero`, `ps ax | grep gunicorn` then `kill`.
* You can clean environment with `python3 xmrsale.py --clean`

Change `YOUR_SERVER_IP` to the IP address of the machine you're running xmrSale on, node or otherwise. Additionally, you could redirect a domain to that IP and use that instead.

### Using HTTPS & Domains
Embedded iframes are easy if your site only uses HTTP. But if your site uses HTTPS, then you can see your donation button at `http://YOUR_SERVER_IP:8000/` but will not be able to in an embedded iframe. See [HTTPS instructions](docs/HTTPS.md).


### Payment Gateway (Woocommerce)
Currently we have a plugin for Woocommerce in Wordpress that makes Monero webstores extremely easy, [please click here for installation instructions](docs/woocommerce.md). xmrSale acts as a custom payment gateway for Woocommerce via the php plugin found in `/gateways`. We have plans to extend to other web stores in the future. We have milestones for other ecommerce plugins, please reach out if there is one you desire.

### Tor
First ensure that you have installed `torsocks` (`sudo apt install tor`) and have `tor` running in the background. You can now enable `tor=True` in the config to connect to remote public nodes over tor.

### Additional Usage
```
xmrsale - Self Hosted Monero Payment Gateway [-h] [-s] [-c] [-t] [--sync]

optional arguments:
  -h, --help        show this help message and exit
  -s, --setup       Initialise xmrsale for the first time
  -c, --clean       Clean up xmrsale directory
  -t, --test-start  Test run xmrsale
  --sync            Run wallet-rpc alone in foreground to sync wallet
```

# Contributions
The main code can be found in [xmrsale.py](xmrsale.py). The client-side logic for initiating the payment and querying the API sits in [static/xmrsale.js](static/xmrsale.js), button appearance in [templates/index.html](templates/index.html), and Woocommerce plugin in [gateways/woo_xmrsale.php](gateways/woo_xmrsale.php). Pull requests welcome.

# Disclaimer
xmrSale is in very early development. As such, we are not responsible for any loss of funds, vulnerabilities with software, or any other grievances which may arise. Always confirm large payments manually.

# Support

With your support, we are continually working to ensure that xmrSale remains up-to-date with the SatSale project, and also building xmrSale specific feature:
* Further webstore plugins
* Timed-out payment recourse.
* Different price feeds with various currencies

Recently we have added:
* Lightweight remote node version with easy install
* Tor connection to node
* Zero node mode
* docker
* 0-conf payments
* Woocommerce plugin is fixed and working!.
Also we've put a basic monero theme in for now. We kind of like the basic style, but will modernise over time.

Please support [via the Monero Community Crowdfunding System](https://repo.getmonero.org/monero-project/ccs-proposals/-/merge_requests/246). You can also support the [satSale](https://satsale.org) project as we relied on it heavily as a code base.
