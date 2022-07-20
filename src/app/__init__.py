# using this tutorial https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-1-lambda-api-gateway/

'''
To test:

sam local start-api 

To deploy:

sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory-api \
    --capabilities CAPABILITY_IAM
'''
    
from fastapi import FastAPI
from mangum import Mangum
 
app = FastAPI()
 
 
@app.get("/")
def get_root():
    return {"message": "FastAPI chicken sandwich running in a Lambda function"}
 
 
handler = Mangum(app)