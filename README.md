# Boring net

This service creates ssh tunnels and keep them running, among reboots if necesary.

## Install

Run `./install.sh` as root:
```
$ sudo ./install.sh
```

Edit `/usr/local/boringnet/config.yml` to setup your own tunnels.
See [config.yml.example](config.yml.example) as example

# Test config

You can test the config file by calling:
```
$ /usr/local/boringnet/boring.py test
```

# Start

To start while system is running:
```
$ sudo service boring start
```

# Enable (Persistance along reboots)

Activate the service to start on boot

```
$ sudo service boring activate
```

# Uninstall

To remove the service, just run `./install --uninstall`
```
$ ./install --uninstall
```
 