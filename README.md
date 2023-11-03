# slack-meishi
## requirements
* Python
* poetry

## preparement
```
poetry install

echo "SLACK_TOKEN=<your slack app token>" >> .env
```

## usage
```
# run
poetry run python main.py <ch name>
```

```
$ poetry run python3 main.py --help
usage: main.py [-h] [-t TEMPLATE] [-f FONT] [-o OUTPUT] ch_name

positional arguments:
  ch_name               slack channel name

options:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        path to template image of nameplate
  -f FONT, --font FONT  path to font you want
  -o OUTPUT, --output OUTPUT
                        path to output
```

## slack permission
* `channels:read`
* `users:read`
* `groups.read` ; if you want to use for private channel

## acknowledgement
* `assets/template.png` is generated from Google Slide
