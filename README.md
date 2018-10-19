Thin Deployer
=============

[![Build Status](https://travis-ci.org/Wolnosciowiec/thin-deployer.svg?branch=master)](https://travis-ci.org/Wolnosciowiec/thin-deployer)

Securely runs your deployment commands triggered by a HTTP call.

Example case:
- POST an information to the /deploy/my-service
- Do the git pull && ./deploy.sh

PIP: https://pypi.org/project/Thin-Deployer/
Travis: https://travis-ci.org/Wolnosciowiec/thin-deployer
Docker: https://hub.docker.com/r/wolnosciowiec/thin-deployer/

Free software
-------------

Created for an anarchist portal, with aim to propagate the freedom and grass-roots social movements where the human and it's needs is on first place, not the capital and profit.

- https://wolnosciowiec.net
- http://iwa-ait.org
- http://zsp.net.pl

Configuration
-------------

Default configuration path is ~/.deployer.yml, but can be specified with a switch `--configuration={{ file path }}`

Example:
```

# service definition (and service name there)
phpdenyhosts:
    # token used to authorize via "token" GET parameter, or "X-Auth-Token" header
    token: some-token-goes-here-use-only-at-least-64-characters-long-tokens

    # optional: support for notifying Slack and other messengers
    # with wolnosciowiec-notification-client
    use_notification: true
    notification_group: "logs"

    # working directory to be in to execute every command
    pwd: /var/www/app

    # could be empty, if not empty then the deploy will execute
    # only if the INCOMING REQUEST BODY will match this regexp
    # useful for example to deploy only from a proper branch
    request_regexp: "\"branch\": \"([production|stage]+)\""

    # commands to execute in order
    commands:
        - git pull
        - composer install --no-dev

# (...) there could be more service definitions
```

Installing via PIP
------------------

One of the ways, a traditional one is to install as a Python package on the host machine.

```bash
pip install Thin-Deployer
thin-deployer --configuration=/etc/thin-deployer/.deployer.yml
```

Installing via Docker
---------------------

Modern and more secure way is to use a docker image to run the thin-deployer inside of an isolated container.

```bash
sudo docker run -p 8012:8012 -v ./deployer.yml:/root/.deployer.yml --rm --name thin-deployer wolnosciowiec/thin-deployer
```

Running dev environment
-----------------------

```
make install_dependencies

# simplest form with all default params
make run

# or advanced with possibility to add commandline switches
python3 ./bin/deployer.py
```

##### Logging to file

Use `--log-file-prefix={{ path_to_log_file }}` switch to save logs to file.

#### Changing port number and bind address

- `--port={{ port_number }}` switch will change server listen port
- `--listen={{ ip_addres }}` makes server listen to given address, defaults to 0.0.0.0

Example request to trigger the deployment
-----------------------------------------

```
POST /deploy/phpdenyhosts HTTP/1.1
Host: localhost:8012
X-Auth-Token: some-token-goes-here-use-only-at-least-64-characters-long-tokens

```

Example response
----------------

```
{
  "output": "Command \"ls -la /nonexisting\" failed, output: \"b''\""
}
```

Headers:
- X-Runs-As: UNIX username of a user on which privileges the server is working on

Dependencies
------------

- Python 3
- python-yaml
- Tornado Framework
- py-healthcheck
- [Wolnościowiec Notification server set up somewhere](https://github.com/Wolnosciowiec/wolnosciowiec-notification) (optionally - only for notifications)
- [Wolnościowiec Notification Shell Client](https://github.com/Wolnosciowiec/wolnosciowiec-notification-shell-client) (optionally - only for notifications)

Health checking
---------------

Service provides a simple monitoring endpoint at GET /technical/healthcheck

Authorization is done in two ways.
Its up to you to use a preferred one in a request to the endpoint.

- A header `X-Auth-Token` with a token as a value
- Basic authorization data, login can be any, as a password please type the token

Examples of headers:
- Authorization: YWFhOnRlc3Q=
- X-Auth-Token: test

#### Configuration

Health check endpoint is configurable via environment variables.

- `HC_TOKEN={{ token }}` health check access token
- `HC_MIN_TOKEN_LENGTH={{ min_length }}` minimum length of a token in every service
- `HC_MAX_DISK_USAGE={{ max_disk_usage_percentage }}` defaults to 90 (it's 90%), when disk usage is higher or equals to this value then an error will be reported


Integrations
------------

Integrates well with [Wolnościowiec Notification](https://github.com/Wolnosciowiec/wolnosciowiec-notification) using a [shell client](https://github.com/Wolnosciowiec/wolnosciowiec-notification-shell-client)

Good practices of securing the service
--------------------------------------

1. Its good to use long tokens
2. Hide the service behind a load balancer with a request rate per second limited (to avoid brute force attacks)
3. Optionally add a basic auth (this may impact usage of the service by external client applications)
4. Use SSL behind load balancer when service is called from the internet
