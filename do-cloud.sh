sam build --use-container &&
sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory \
    --s3-prefix _deployed_code/BusObservatoryAPI \
    --capabilities CAPABILITY_IAM