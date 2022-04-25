# actinia-example-plugin

This is an example plugin for [actinia-core](https://github.com/mundialis/actinia_core) which adds a "Hello World" endpoint to actinia-core.

You can run actinia-example-plugin as an actinia-core plugin.

## Installation
Use docker-compose for installation:
```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d
```

### Installation hints
* If you get an error like: `ERROR: for docker_redis_1  Cannot start service redis: network xxx not found` you can try the following:
```
docker-compose -f docker/docker-compose.yml down
# remove all custom networks not used by a container
docker network prune
docker-compose -f docker/docker-compose.yml up -d
```

### Requesting helloworld endpoint
You can test the plugin and request the `/helloworld` endpoint, e.g. with:
```
curl -u actinia-gdi:actinia-gdi -X GET http://localhost:8088/api/v2/helloworld | jq

curl -u actinia-gdi:actinia-gdi -H 'accept: application/json' -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v2/helloworld -d '{"name": "test"}' | jq
```

## DEV setup
For a DEV setup you can use the docker/docker-compose.yml:
```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml run --rm --service-ports --entrypoint sh actinia

# install the plugin
(cd /src/actinia-example-plugin && python3 setup.py install)
# start actinia-core with your plugin
gunicorn -b 0.0.0.0:8088 -w 1 --access-logfile=- -k gthread actinia_core.main:flask_app
```

### Hints

* If you have no `.git` folder in the plugin folder, you need to set the
`SETUPTOOLS_SCM_PRETEND_VERSION` before installing the plugin:
```
export SETUPTOOLS_SCM_PRETEND_VERSION=0.0
```
Otherwise you will get an error like this
`LookupError: setuptools-scm was unable to detect version for '/src/actinia-example-plugin'.`.

* If you make changes in code and nothing changes you can try to uninstall the plugin:
```
pip3 uninstall actinia-example-plugin.wsgi -y
rm -rf /usr/lib/python3.8/site-packages/actinia_example_plugin.wsgi-*.egg
```

### Running tests
You can run the tests in the actinia test docker:

```
docker build -f docker/actinia-example-plugin-test/Dockerfile -t actinia-example-plugin-test .
docker run -it actinia-example-plugin-test -i

cd /src/actinia-example-plugin/

# run all tests
make test

# run only unittests
make unittest
# run only integrationtests
make integrationtest

# run only tests which are marked for development with the decorator '@pytest.mark.dev'
make devtest
```

## Starting steps for own plugin
If you want to have your own plugin you can use this repo to create it by
executing the `scripts/create_own_plugin.sh`.

If you want the repo in git then you first have to create an empty git repository
and then run the script. Then follow the last instructions from the script
to upload the initial code to your git repository.

```
bash create_own_plugin.sh actinia-ex2-plugin git
```

If you only want your own plugin in a folder and not in git you can execute the
script like this:

```
bash create_own_plugin.sh actinia-ex2-plugin
```
