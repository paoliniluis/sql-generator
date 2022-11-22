# ###################
# # STAGE 1: create-file
# ##################

FROM python:3.11-alpine3.16 as generator

ARG target
ARG config=requirements.yaml
ARG n_of_rows=1000

WORKDIR /home/app

ADD main.py requirements.txt source/requirements.yaml ./
RUN pip install -r requirements.txt && python3 main.py config=$config target=$target n_of_rows=$n_of_rows

# ###################
# # STAGE 2: export-stage
# ###################

FROM scratch as export-stage

COPY --from=generator /home/app/finalSQL.sql.gz /