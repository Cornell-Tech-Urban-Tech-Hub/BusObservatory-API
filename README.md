# BusObservatory-API

### To test:
```
    aws sso login
    sam build --use-container 
        && sam local start-api --debug
```

### To deploy/update:

```
    sam build --use-container &&
    sam deploy \
        --stack-name BusObservatoryAPI \
        --s3-bucket busobservatory-api \
        --capabilities CAPABILITY_IAM
```

### To view logs:

```
    sam logs --stack-name BusObservatoryAPI
```

## URLS

### local test
- Home [http://127.0.0.1:3000/](http://127.0.0.1:3000/)
- SIRI [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4)
- GTFS [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4)

### Deployed AWS
- home [https://api.buswatcher.org/](https://api.buswatcher.org/)
deployed 
- SIRI [https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4](https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4)
- GTFSRT [https://api.buswatcher.org/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4](https://api.buswatcher.org/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4)



## testing authentication mechanism

### Unauthenticated
Should fail

```
curl --request GET \
  --url http://127.0.0.1:3000/buses/bulk/nyct_mta_bus_siri/M1/2022/7/7/4
```

### Authenticated
With test token from auth0 API dashboard, should return a full response of bus data.

```
curl --request GET \
  --url http://127.0.0.1:3000/buses/bulk/nyct_mta_bus_siri/M1/2022/7/7/4 \
  --header 'authorization: Bearer blahblahblah'

```