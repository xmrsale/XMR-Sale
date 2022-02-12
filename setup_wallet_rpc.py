import os
import requests
import tarfile
import subprocess
import getpass
import time
import sys
import select

RPC_CONF_FILE = "xmrsale_rpc.conf"
DOWNLOAD_URL = "https://downloads.getmonero.org/cli/linux64"
DEFAULT_WALLET_NAME = "xmrsale_wallet"
REMOTE_NODE_URL = "node.moneroworld.com"  # "100.14.93.124"
REMOTE_NODE_PORT = "18089"


def download_monero_cli():
    print("Downloading monero-cli from {}".format(DOWNLOAD_URL))
    r = requests.get(DOWNLOAD_URL, allow_redirects=True)
    filename = "monero-linux.tar.bz2"
    open(filename, "wb").write(r.content)
    return filename


def unpack_monero_cli(filename):
    output_dir = "monero-cli"
    tar = tarfile.open(filename, "r:bz2")
    tar.extractall(output_dir)
    tar.close()
    os.remove(filename)

    folder = os.listdir(output_dir)[0]
    print(folder)

    for f in os.listdir(output_dir + "/" + folder):
        os.rename(output_dir + "/" + folder + "/" + f, output_dir + "/" + f)

    os.rmdir(output_dir + "/" + folder)

    return output_dir


def check_download_cli(cli_dir):
    if not os.path.exists(cli_dir):
        cli_dir = unpack_monero_cli(download_monero_cli())
    else:
        return cli_dir


def cli_create_wallet(cli_dir, wallet_name, password=""):
    subprocess.run(
        [
            cli_dir + "/" + "monero-wallet-cli",
            "--generate-new-wallet",
            wallet_name,
            "--password",
            "{}".format(password),
            "--mnemonic-language",
            "English",
        ]
    )
    return


def create_password():
    print(
        "WARNING: Wallet password will be saved to your wallet_rpc config file in plaintext."
    )
    password1 = getpass.getpass("Wallet password:")
    password2 = getpass.getpass("Wallet password again:")
    if password1 != password2:
        raise Exception("Unmatching passwords")

    return password1


def check_create_wallet(cli_dir, wallet_name, rpc_password):
    if not os.path.exists(wallet_name):
        print("WARNING: Creating a new wallet: {}".format(wallet_name))
        # if wallet_name == DEFAULT_WALLET_NAME:
        print("Creating a wallet {}".format(wallet_name))
        password = create_password()

        # with open("rpc_password", "w") as f:
        #     f.write(os.urandom(32).hex())
        create_rpc_conf(wallet_name, rpc_password, password)
        cli_create_wallet(cli_dir, wallet_name, password)
        return password
    else:
        return False


def create_rpc_conf(wallet_name, rpc_password, password, port="18090"):
    conf = """
rpc-login=monerorpc:{}
rpc-bind-ip=0.0.0.0
rpc-bind-port={}
confirm-external-bind=1
non-interactive=1
daemon-address={}:{}
wallet-file={}
password={}
log-level=2
""".format(
        rpc_password, port, REMOTE_NODE_URL, REMOTE_NODE_PORT, wallet_name, password
    )

    print()
    print("Writing config:\n{}".format(conf))
    with open(RPC_CONF_FILE, "w") as f:
        print("Writing to {}".format(RPC_CONF_FILE))
        f.write(conf)

    return RPC_CONF_FILE


def run_wallet_rpc(cli_dir, config_file, log=None):
    cmd = [cli_dir + "/" + "monero-wallet-rpc", "--config-file", config_file]
    print("Starting wallet_rpc with command  {}".format(" ".join(cmd)))

    if log is not None:
        log = open(log, "a")
        p = subprocess.Popen(cmd, stdout=log, stderr=log)
    else:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p


def run_xmrsale_detached():
    cmd = [sys.executable, "-u", "xmrsale.py"]
    print("Starting xmrSale with command  {}".format(" ".join(cmd)))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p


def output(s, p_name):
    for f in [sys.stdout]:
        f.write(p_name + ": " + s.decode("utf-8"))
        f.flush()


def check_wallet_setup(cli_dir, wallet_name, rpc_password):
    check_download_cli(cli_dir)
    check_create_wallet(cli_dir, wallet_name, rpc_password)
    return


def run_rpc_process(cli_dir):
    import traceback

    try:
        rpc_pid = run_wallet_rpc(cli_dir, RPC_CONF_FILE, "log_rpc.log")
        # import xmrsale
        # xmrsale.app.run(debug=False)
    except Exception as e:
        print(traceback.format_exc())
        print("Exception running RPC: {}".format(e))
    # finally:
    #     print("Killing rpc process...")
    #     rpc_pid.kill()
    #     print("killed")

    return rpc_pid
