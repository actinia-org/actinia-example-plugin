# Exception for hadoling-docker-linter:
# DL3007: using latest is prone to errors if the image will ever update. Pin the version explicitly to a release tag
# hadolint ignore=DL3007
FROM mundialis/actinia:latest AS actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG=/etc/default/actinia-example-plugin-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH=/etc/default/actinia-example-plugin-test

# install things only for tests
RUN apk add --no-cache redis==7.2.7-r0 && \
    pip3 install --no-cache-dir iniconfig==2.0.0 colorlog==6.8.2 pwgen==0.8.2.post0 pytest==8.3.5 pytest-cov==6.0.0

# COPY docker/actinia-example-plugin-test/start.sh /src/start.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

# # add data for tests
# RUN wget --quiet https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_micro.zip && \
#   unzip nc_spm_08_micro.zip && \
#   rm -f nc_spm_08_micro.zip && \
#   mv nc_spm_08_micro /actinia_core/grassdb/nc_spm_08
# RUN grass -e -c 'EPSG:4326' /actinia_core/grassdb/latlong_wgs84

# copy needed files and configs for test
COPY docker/actinia-example-plugin-test/actinia-example-plugin-test.cfg /etc/default/actinia
COPY docker/actinia-example-plugin-test/actinia-example-plugin-test.cfg /etc/default/actinia-example-plugin-test
COPY . /src/actinia-example-plugin/

WORKDIR /src/actinia-example-plugin/
RUN pip3 install --no-cache-dir -e .

RUN chmod a+x tests_with_redis.sh && make install

# RUN make test
