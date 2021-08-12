Simple log receiver that simply logs errors to a mongodb database`

# why

a simple way to send your logs to a mongodb using flask as an inbetween layer to avoid installing pymongo in every image. simply post to the URL and submit:

- password: an app password specified via environment variable to avoid unauthorized log submission
- appname: the name of the app that submitted the error
- errorjson: just paste anything you want in here, i recommend as a json

# install:

see the docker-compose for an example

`docker-compose up --build`

docker-compose.yaml:

```
version: "3"
services:
  mongodb:
    image: bitnami/mongodb:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb-data:/bitnami/mongodb/data
    environment:
      MONGODB_DATABASE: errors
      MONGODB_USERNAME: test
      MONGODB_PASSWORD: test
    restart: always
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongo mongodb:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 5s

  mongodb-logger:
    image: guestros/mongodb-logger:latest
    build: .
    depends_on: 
      mongodb:
        condition: service_healthy
    environment: 
      MONGODB_HOST: mongodb
      MONGODB_DB: errors
      MONGODB_USER: test
      MONGODB_PASSWORD: test
      AUTH_PW: apppassword
    ports:
      - "5000:5000"

volumes:
  mongodb-data:
```


## test

### curl

```
curl --location --request POST 'localhost:5000' \
--header 'Content-Type: application/json' \
--data-raw '{
    "password": "apppassword",
    "appname": "testapp",
    "errorjson": {
        "code": 500,
        "errormsg": "example failure"
    }
}'
```

### python

run the `testpost.py` script