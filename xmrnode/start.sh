#!/bin/bash
while true; do
    ls -l ".bitmonero/wallet/"
    if [[ -f ".bitmonero/wallet/wallet" ]]; then
        echo "Found wallet, booting monero-wallet-rpc..."
        monero-wallet-rpc --rpc-bind-ip=0.0.0.0 --rpc-bind-port=18090 --daemon-host monerod --daemon-port 18089 --wallet-file .bitmonero/wallet/wallet --password '' --non-interactive
    else
        echo ".bitmonero/wallet not found.. Not starting Monero wallet rpc. Make sure you pass wallet file to docker.."
    fi
    sleep 10
    echo "Restarting monero-wallet-rpc"
done
