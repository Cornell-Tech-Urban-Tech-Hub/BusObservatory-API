# BusObservatory-API


### To test:
```
aws sso login
sam local start-api --debug
```


Rebuild, every time code changes with, because we have C dependencies:

```
sam build --use-container
```
#### URLS
local
- SIRI [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf)
- GTFS [http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf](http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf)

deployed 
- SIRI [https://u8lmx5wj3g.execute-api.us-east-1.amazonaws.com/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf](https://u8lmx5wj3g.execute-api.us-east-1.amazonaws.com/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf)
- GTFSRT [https://u8lmx5wj3g.execute-api.us-east-1.amazonaws.com/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf](https://u8lmx5wj3g.execute-api.us-east-1.amazonaws.com/buses/bypath/nyct_mta_bus_gtfsrt/M1/2022/7/4/4/sfsafasfasf)




### To deploy/update:

```
sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory-api \
    --capabilities CAPABILITY_IAM
```