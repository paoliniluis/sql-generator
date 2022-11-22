SQL Generator
===

# Quick start
You don't need to have Python installed, just Docker
DOCKER_BUILDKIT=1 docker build --build-arg n_of_rows=1000 --output=target/ .

## Arguments
- source: the specification of what you want to build
- target: where the file will be generated
- n_of_rows: how many rows you want to generate

## How does this work
Depending on the number of tables and types of fields you specify in the requirements.yaml, it will generate SQL syntax to create those tables and then generate fake data with [Mimesis](https://mimesis.name/) writing to disk in a compressed gzip all the data.

I tried to generate basic data types to be as compatible as possible with many engines, this currently works for Postgres, but I haven't tried to use it in another DB.

## Performance
It takes 20 seconds to generate the sample requirements file of 50K rows in a Ryzen 5800H / 32GB of RAM