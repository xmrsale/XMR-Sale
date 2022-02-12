# xmrSale
### (Monero specialized fork of [SatSale](https://github.com/nickfarrow/xmrSale))
xmrSale is a simple, easily deployable, lightweight Monero payment processor that connects to your own Monero node.

**Website & Docs**: [xmrSale.org](https://xmrsale.org)

## [try.xmrsale.org](https://try.xmrsale.org)

Donation Button     ----->  |  Monero Payment Gateway
:-------------------------:|:-------------------------:
[![Donate demo](docs/demo_donate.png)](https://try.xmrSale.org/) <br />(Click for embed demo)<br /> Initiates payment -----> |  [![Store demo](docs/demo_pay2.png)](https://try.xmrSale.org/) <br />(Click for WordPress payments demo)

**Always manually check significant payments**.


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
- [Sponsor](#sponsor)

## [try.xmrsale.org](https://try.xmrsale.org)

xmrSale is a self-hosted Monero payment processor, serving two primary use cases:
1. Donation button for your website that you can easily embed/link to anywhere.
2. Monero payment gateway, including a Woocommerce plugin that easily turns ANY Wordpress site into a Monero accepting store.

xmrSale makes donation buttons simple - easy copy paste the one line HTML iframe into your site. With a simple Python backend to talk to your own Monero node, xmrSale uses RPC to generate new addresses, and monitors the payment status with your own copy of the blockchain.

# Features
* You don't need your own node, xmrSale sets up `monero-wallet-rpc` and connects to public nodes. (tor coming soon!)
* Lightweight and highly extendable, basic html and css stying. Modular Python backend, take a [look at the code](xmrsale.py).
* Natively extendable to all Monerod node features (e.g. segwit) through RPC.
* QR codes, customizable required payment confirmations and payment expiry time.
* Privacy ensured. Monero only.

# Installation (easy!)
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
python3 xmrsale.py
```
This will download monero-cli tools from `downloads.getmonero.org` which are used to manage payments.
Enter a new password for your new `xmrsale_wallet` (and `.keys`).
You must backup these and the seedphrase.

Click `N` when asked whether you want to mine in the background, then type `exit`.

Now xmrsale will run the `monero-wallet-rpc` and sync with a public node (`node.moneroworld.com`). Once you see `Refresh done, blocks received...` you are ready to run xmrsale! If you want, you can adjust the `config.py` to your liking.

### Start xmrSale
Run xmrSale with
```
gunicorn xmrsale:app
```
That's it! If running locally, this will be `127.0.0.1:8000`. If you allow traffic on that port you should now also be able to view your xmrSale at `http://YOUR_SERVER_IP:8000/`.

You will want to run gunicorn with nohup so it continues serving in the background:
```
nohup gunicorn xmrsale:app > log.txt 2>&1 &
tail -f log.txt
```

### Embed a Donation Button
Now we have xmrSale running, let's embed the donation button into a website HTML:
```html
<iframe src="http://YOUR_SERVER_IP:8000/" style="margin: 0 auto;display:block;width:420px;height:460px;border:none;overflow:hidden;" scrolling="no"></iframe>
```
Change `YOUR_SERVER_IP` to the IP address of the machine you're running xmrSale on, node or otherwise. Additionally, you could redirect a domain to that IP and use that instead.

### Using HTTPS & Domains
Embedded iframes are easy if your site only uses HTTP. But if your site uses HTTPS, then you can see your donation button at `http://YOUR_SERVER_IP:8000/` but will not be able to in an embedded iframe. See [HTTPS instructions](docs/HTTPS.md).


### Payment Gateway (Woocommerce)
## TESTED AND WORKING
Currently we have a plugin for Woocommerce in Wordpress that makes Monero webstores extremely easy, [please click here for installation instructions](docs/woocommerce.md). xmrSale acts as a custom payment gateway for Woocommerce via the php plugin found in `/gateways`. We have plans to extend to other web stores in the future. We have milestones for other ecommerce plugins, please reach out if there is one you desire.

# Contributions
The main code can be found in [xmrsale.py](xmrsale.py). The client-side logic for initiating the payment and querying the API sits in [static/xmrsale.js](static/xmrsale.js), button appearance in [templates/index.html](templates/index.html), and Woocommerce plugin in [gateways/woo_xmrsale.php](gateways/woo_xmrsale.php). Pull requests welcome.

# Disclaimer
xmrSale is in very early development. As such, we are not responsible for any loss of funds, vulnerabilities with software, or any other grievances which may arise. Always confirm large payments manually.

# Support

With your support, we are continually working to ensure that xmrSale remains up-to-date with the SatSale project, and also building xmrSale specific feature:
* Tor support
* Further webstore plugins
* **Better UI** with more variety of size and theme.
    * Add a currency toggle between XMR/USD on donation html.
* Timed-out payment recourse.
* Different price feeds with various currencies
* Tell us what you, the community, desire! I intent to many other features alongside the CCS milestones.

Recently we have added:
* Zero node mode
* docker
* 0-conf payments
* Woocommerce plugin is fixed and working!.
Also we've put a basic monero theme in for now. We kind of like the basic style, but will modernise over time.

Please support [via the Monero Community Crowdfunding System](https://repo.getmonero.org/monero-project/ccs-proposals/-/merge_requests/246). You can also support the [satSale](https://satsale.org) project as we relied on it heavily as a code base.
