FROM mundialis/actinia-core:4.1.0

# pwgen is needed for the tests
RUN pip3 install pwgen

COPY docker/actinia.cfg /etc/default/actinia
COPY src /src/actinia-example-plugin/src/
COPY setup.cfg /src/actinia-example-plugin/
COPY setup.py /src/actinia-example-plugin/
COPY requirements.txt /src/actinia-example-plugin/

RUN pip3 install -r /src/actinia-example-plugin/requirements.txt
RUN pip3 uninstall actinia-example-plugin.wsgi -y
# SETUPTOOLS_SCM_PRETEND_VERSION is only needed if in the plugin folder is no
# .git folder
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0
RUN (cd /src/actinia-example-plugin && python3 setup.py install)
