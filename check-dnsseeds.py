#!/usr/bin/env python3
'''
Simple script to check the status of all Koyotecoin Core DNS seeds.
Seeds are available from https://github.com/koyotecoin/koyotecoin/blob/master/src/chainparams.cpp
'''
import subprocess

SEEDS_PER_NETWORK = {
    'mainnet': [
        "seed.kyc.genisyskernel.dev",
    ],
    'testnet': [
        "seed.test.kyc.genisyskernel.dev",
    ],
    'signet': [
        "seed.sig.test.kyc.genisyskernel.dev",
    ],
    'regnet': [
        "seed.reg.test.kyc.genisyskernel.dev",
    ],
}


def check_seed(x):
    p = subprocess.run(["host", x], capture_output=True,
                       universal_newlines=True)
    out = p.stdout

    # Parse matching lines
    addresses = []
    for line in out.splitlines():
        if "has address" in line or "has IPv6 address" in line:
            addresses.append(line)

    if addresses:
        print(f"\x1b[94mOK\x1b[0m   {x} ({len(addresses)} results)")
    else:
        print(f"\x1b[91mFAIL\x1b[0m {x}")


if __name__ == '__main__':
    for (network, seeds) in SEEDS_PER_NETWORK.items():
        print(f"\x1b[90m* \x1b[97m{network}\x1b[0m")

        for hostname in seeds:
            check_seed(hostname)

        print()
