Thin Deployer
=============

Securely runs your deployment commands triggered by a HTTP call.

Example case:
- POST an information to the /deploy/my-service
- Do the git pull && ./deploy.sh

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
- [Wolnościowiec Notification server set up somewhere](https://github.com/Wolnosciowiec/wolnosciowiec-notification) (optionally - only for notifications)
- [Wolnościowiec Notification Shell Client](https://github.com/Wolnosciowiec/wolnosciowiec-notification-shell-client) (optionally - only for notifications)

Integrations
------------

Integrates well with [Wolnościowiec Notification](https://github.com/Wolnosciowiec/wolnosciowiec-notification) using a [shell client](https://github.com/Wolnosciowiec/wolnosciowiec-notification-shell-client)
