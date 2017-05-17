Thin Deployer
=============

Securely runs your deployment commands triggered by a HTTP call.

Example case:
- POST an information to the /deploy/my-service
- Do the git pull && ./deploy.sh

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
phpdenyhosts:
    token: some-token-goes-here-use-only-at-least-64-characters-long-tokens
    use_notification: true
    notification_group: "logs"
    pwd: /var/www/app
    commands:
        - git pull
        - composer install --no-dev
```

Running
-------

```
python ./bin/deployer.py
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
