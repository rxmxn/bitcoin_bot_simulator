# pycoin

The purpose of this repo is to be able to simulate different bot strategies based on Bitcoin historics.

### Environment Requirements

- `ALPHAVANTAGE_KEY`: Key given by AlphaVantage to access to the API
- `CB_API_SECRET`: Secret provided by Coinbase Pro
- `CB_ACCESS_KEY`: Key provided by Coinbase Pro
- `CB_ACCESS_PASSPHRASE`: Pass phrase generated in Coinbase Pro
- `COINBASE_PRO_SANDBOX`: Set to 1 to use Sandbox

### Installing executable

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .

$ pycoin --help
```

### Files that need to be downloaded

Download this file with historical data and decompress inside the base directory

http://api.bitcoincharts.com/v1/csv/btcalphaUSD.csv.gz
