sam build --use-container &&
sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory-api \
    --capabilities CAPABILITY_IAM