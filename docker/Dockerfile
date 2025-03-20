FROM mundialis/actinia:latest

# pwgen is needed for the tests
RUN pip3 install --no-cache-dir pwgen==0.8.2.post0

COPY docker/actinia.cfg /etc/default/actinia
COPY src /src/actinia-example-plugin/src/
COPY setup.cfg /src/actinia-example-plugin/
COPY setup.py /src/actinia-example-plugin/
COPY requirements.txt /src/actinia-example-plugin/

RUN pip3 install --no-cache-dir -r /src/actinia-example-plugin/requirements.txt && \
    pip3 uninstall actinia-example-plugin.wsgi -y
# SETUPTOOLS_SCM_PRETEND_VERSION is only needed if in the plugin folder is no
# .git folder
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0

WORKDIR /src/actinia-example-plugin
RUN pip3 install -e .

WORKDIR /src/actinia_core
