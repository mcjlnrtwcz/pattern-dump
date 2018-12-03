# pattern-dump
Pattern dump tool for Elektron Digitakt

## Digitakt settings
Make sure that you've enabled "clock receive" and "prog ch receive". Moreover, check "prog chg in ch" in "channels" menu - it has to mach the one set in `pattern-dump`.

## Installation
```
make env
source .env/bin/activate
make install
```

## Development
```
make env
source .env/bin/activate
make install_dev
```
