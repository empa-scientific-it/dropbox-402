FROM openbis/debian-openbis:20.10.6
RUN mkdir -p /home/openbis/openbis_state/core-plugins/empa/1/dss/drop-boxes
COPY src/collection-handler /home/openbis/openbis_state/core-plugins/empa/1/dss/drop-boxes/collection-handler
RUN mkdir -p /home/openbis/openbis_state/dss_store/incoming-collection
