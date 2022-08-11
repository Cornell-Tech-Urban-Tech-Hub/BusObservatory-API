# BusObservatory-API

### To test:
```
    aws sso login
    sam build --use-container && sam local start-api --debug
```

### To deploy/update:

Takes about 2-3 minutes on M1 MacBook Air laptop.

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

### Deployed AWS
- home [https://api.busobservatory.org/](https://api.busobservatory.org/)
deployed 
- SIRI [https://api.busobservatory.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4](https://api.busobservatory.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4)

