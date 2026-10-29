# Flask Apache

![Flask behind Apache](docs/images/banner.png)

[![Apache 2.0 License](https://img.shields.io/badge/License-Apache_2.0-blue)](LICENSE) [![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![CI](https://github.com/wallaceespindola/flask-apache/actions/workflows/ci.yml/badge.svg)](https://github.com/wallaceespindola/flask-apache/actions/workflows/ci.yml)

The idea: run a Flask app behind Apache httpd, the way many teams still host Python on an existing Apache box. This repo is the small, current version of that setup: a Flask 3 app factory with three JSON endpoints, an Apache 2.4 virtual host for mod_wsgi, and a Docker Compose stack that runs it end to end.

## Two ways to put Flask behind Apache

- **mod_wsgi** runs the app inside Apache worker processes. One moving part less at runtime, but mod_wsgi must be compiled against the same Python as your venv. With Python 3.14 that usually means building it yourself, so it is the bare-metal path here (`flask_apache.conf` and `flask_apache.wsgi`).
- **gunicorn behind mod_proxy** keeps Python in its own process and lets Apache forward requests to it. Any stock `httpd` image works, so this is what Docker Compose uses.

Both serve the same app and the same endpoints.

## Endpoints

| Path      | Returns                                         |
| --------- | ----------------------------------------------- |
| `/`       | greeting message                                |
| `/health` | `{"status": "UP"}`                              |
| `/info`   | service name, version, start time, server stack |

Every response is JSON and includes a UTC `timestamp`.

## Quickstart

### Local

```bash
make venv
make dev          # http://localhost:3100/health
make test
```

### Docker (Apache httpd in front of gunicorn)

```bash
cp .env.example .env    # set SECRET_KEY
make docker             # http://localhost:3100/health
make docker-down
```

### Bare-metal Apache with mod_wsgi (Debian or Ubuntu)

```bash
sudo mkdir -p /var/www/flask_apache && sudo chown $USER /var/www/flask_apache
git clone https://github.com/wallaceespindola/flask-apache /var/www/flask_apache
cd /var/www/flask_apache && uv sync --no-dev

sudo apt install apache2 apache2-dev
# mod_wsgi must match the venv Python, so build it from the venv:
uv pip install mod_wsgi
uv run mod_wsgi-express module-config | sudo tee /etc/apache2/mods-available/wsgi.load
sudo a2enmod wsgi

echo "Listen 3100" | sudo tee -a /etc/apache2/ports.conf
sudo cp flask_apache.conf /etc/apache2/sites-available/
sudo a2ensite flask_apache && sudo systemctl reload apache2
```

Edit `ServerName` in `flask_apache.conf` first. Set `SECRET_KEY` with `SetEnv` or in the daemon process environment, never in the `.wsgi` file.

## Configuration

| Variable     | Purpose                                      | Default  |
| ------------ | -------------------------------------------- | -------- |
| `SECRET_KEY` | Flask session signing key                    | empty    |
| `HTTP_PORT`  | Host port Apache publishes in Docker Compose | `3100`   |

## Development

`make format`, `make lint`, `make typecheck` and `make test` run black and isort, ruff, mypy in strict mode, and pytest with an 80% coverage floor. CI runs the same checks.

## Support

If you find this project helpful, please consider:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20my%20work-FFDD00?style=flat&labelColor=101010&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/wallace.espindola) [![Star on GitHub](https://img.shields.io/badge/Star%20on%20GitHub-flask--apache-181717?style=flat&logo=github)](https://github.com/wallaceespindola/flask-apache)

[![GitHub stars](https://img.shields.io/github/stars/wallaceespindola/flask-apache?style=social)](https://github.com/wallaceespindola/flask-apache/stargazers) [![GitHub forks](https://img.shields.io/github/forks/wallaceespindola/flask-apache?style=social)](https://github.com/wallaceespindola/flask-apache/network/members) [![GitHub watchers](https://img.shields.io/github/watchers/wallaceespindola/flask-apache?style=social)](https://github.com/wallaceespindola/flask-apache/watchers) [![GitHub issues](https://img.shields.io/github/issues/wallaceespindola/flask-apache)](https://github.com/wallaceespindola/flask-apache/issues) [![GitHub last commit](https://img.shields.io/github/last-commit/wallaceespindola/flask-apache)](https://github.com/wallaceespindola/flask-apache/commits/main)

Star the repo on GitHub if it helps your Flask and Apache work. It motivates me a lot!

## Author

Wallace Espindola, Solution Architect

- Email: <wallace.espindola@gmail.com>
- LinkedIn: <https://www.linkedin.com/in/wallaceespindola/>
- GitHub: <https://github.com/wallaceespindola/>
- Twitter/X: [@wsespindola](https://x.com/wsespindola)
- Substack: [Code & Coffee by Wallace Espindola](https://wallaceespindola.substack.com)
- Medium: <https://medium.com/@wallaceespindola>
- Dev.to: <https://dev.to/wallaceespindola>
- DZone: <https://dzone.com/users/1254611/wallacese.html>
- Speaker Deck: <https://speakerdeck.com/wallacese>
- Speaker profile: <https://sessionize.com/wallace-espindola/>
- Company: [www.wtechitsolutions.com](http://www.wtechitsolutions.com)
- Buy Me a Coffee: <https://www.buymeacoffee.com/wallace.espindola>

## License

- This project is released under the Apache 2.0 License.
- See the [LICENSE](LICENSE) file for details.
- Copyright © 2026 [Wallace Espindola](https://github.com/wallaceespindola/).
