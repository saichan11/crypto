import argparse
import sys
import requests
from functools import lru_cache


def parse_args() -> argparse.Namespace:
    """Parse the arguments from the command line

    Returns
    -------
    args: argparse.Namespace
        parsed arguments
    """

    parser = argparse.ArgumentParser(
        description="Python script for fetching Crypto EUR prices. Developed by Tea n' Tech."
    )

    parser.add_argument(
        "identifier",
        type=str,
        help="Krypto Identifier (e.g. BTC-EUR, DFI-BTC) of which you want to get the current price in EUR",
    )

    if len(sys.argv) < 2:
        parser.print_help()
        exit(0)

    return parser.parse_args(sys.argv[1:])


@lru_cache(maxsize=1)
def getCryptoExchangeRate(identifier) -> float:
    """fetches the current exchange price on open api

    Returns
    -------
    ExchangeRate: float
        current ExchangeRate
    """

    identifier = identifier.upper()
    response = requests.get(f"https://www.bitfinex.com/trading{identifier}/ticker")
    try:
        exchangeRate = float(response.json()["lastTradeRate"])
    except:
        print("An exeption occured - coud not find your Crypto Identifier")
        return

    return exchangeRate


def print_header() -> None:
    """Print the CLI header"""
    print(
        """
    [underline] BTC Price Fetcher [/underline]
    """
    )


def main():

    print_header()

    # parse command line args
    args = parse_args()

    # Get the price
    exchangeRate = getCryptoExchangeRate(args.identifier)
    if exchangeRate is not None:
        cryptoFrom = args.identifier.split("-")[0]
        cryptoTo = args.identifier.split("-")[1]
        print(
            f"Your Crypto Darling {cryptoFrom} has currently a price of {exchangeRate:.5f} {cryptoTo}."
        )


if __name__ == "__main__":
    main()