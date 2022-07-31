# BusObservatory-API

### To test:
```
aws sso login
sam build --use-container && 
sam local start-api --debug
```

#### URLS
local
- Home [http://127.0.0.1:3000/](http://127.0.0.1:3000/)
- SIRI [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf)
- GTFS [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf)

deployed 
- SIRI [https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf](https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf)
- GTFSRT [https://api.buswatcher.org/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf](https://api.buswatcher.org/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf)


### To deploy/update:

```
sam build --use-container &&
sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory-api \
    --capabilities CAPABILITY_IAM
```

### Notes

1. Adding permissions to SAM role 
