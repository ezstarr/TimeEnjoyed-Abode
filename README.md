# TIMEENJOYED-ABODE
DJANGO BLOG SITE THAT ALLOWS FOR MULTIPLE USERS USING TWITCH ALL-AUTH

## Setup

The first thing to do is clone teh repository:

```bash
$ git clone https://github.com/ezstarr/TimeEnjoyed-Abode.git
$ cd TimeEnjoyed-Abode
```
Create a virtual environment to install dependencies in and activate it:

```bash
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:
```bash
(env)$ pip install -r requirements.txt
```
Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once pip has finished downloading the dependencies:
```bash
(env)$ cd TimeEnjoyed-Abode
(env)$ python manage.py runserver
```
`And navigate to http://127.0.0.1:8000`


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
