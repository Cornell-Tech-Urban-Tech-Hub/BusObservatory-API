# using this tutorial https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-1-lambda-api-gateway/

'''

To build:

Delete the docker images then,

# because we have C dependencies
sam build --user-container

To test:
sam local start-api --force-build-image --debug

To deploy:

sam deploy \
    --stack-name BusObservatoryAPI \
    --s3-bucket busobservatory-api \
    --capabilities CAPABILITY_IAM
'''
    
from fastapi import FastAPI, Path
from mangum import Mangum
import os
import datetime as dt
import pythena
 
# app = FastAPI()

#FIXME: "openapi_prefix" has been deprecated in favor of "root_path", which follows more closely the ASGI standard, is simpler, and more automatic. 
#FIXME: Check the docs at https://fastapi.tiangolo.com/advanced/sub-applications/
# fix path for auto-gen docs on Lambda
# from https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="BusObservatoryAPI", openapi_prefix=openapi_prefix)

def query_job(system_id, route, start, end): 
    athena_client = pythena.Athena(database="busobservatory")
    # use single quotes in these queries otherwise Athena chokes
    query_String=   \
        f"""
        SELECT *
        FROM {system_id}
        WHERE
        route = '{route}'
        AND
        (timestamp >= from_iso8601_timestamp('{start}') AND timestamp < from_iso8601_timestamp('{end}'))
        """  
    # print(query_String)
    dataframe, _ = athena_client.execute(query=query_String)
    #FIXME: format the return properly
    return{
        "Table Records": dataframe.to_json()
    }

########################################################################################################
# One route-hour by path arguments
# https://fastapi.tiangolo.com/tutorial/path-params/
# test locally http://127.0.0.1:3000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf
# test deployed with https://u8lmx5wj3g.execute-api.us-east-1.amazonaws.com/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf
########################################################################################################
@app.get("/buses/bypath/{system_id}/{route}/{year}/{month}/{day}/{hour}/{apikey}")
async def fetch_buses_by_path(
    system_id: str, 
    route: str, 
    apikey:str,
    year:int = Path(title="Year of service", ge=2011, le=2050), 
    month:int = Path(title="Month of service", ge=1, le=12), 
    day:int = Path(title="Day of service", ge=1, le=31),
    hour:int = Path(title="Hour of service", ge=0, le=23)
    ):
    
    #convert year/month/day/hour into a start and end ISO 8601 timestamp for bottom and top of hour 
    start = dt.datetime(year,month,day,hour,0,0).isoformat()
    if hour == 23:
        # advance to midnight
        end = dt.datetime(year,month,day+1,0,0,0).isoformat()
    elif hour < 23:
        end = dt.datetime(year,month,day,(hour+1),0,0).isoformat()
    
    #TODO: auth0 integration using 'apikey'
    # https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
    
    ## debugging output
    # return json_response of run_query(system_id, route, year, month, day, hour)

    # live db query
    return {
            "query": 
                    {
                        "system_id": system_id,
                        "year":year,
                        "month":month,
                        "day":day,
                        "hour":hour,
                        "start (derived, inclusive)":start,
                        "end (derived, not inclusive)":end,
                        "apikey": apikey
                    }, 
            "result":query_job(system_id, route, start, end)
            }

########################################################################################################
# Unlimited data by query arguments
# https://fastapi.tiangolo.com/tutorial/query-params/
# test locally with
# TODO:
########################################################################################################
@app.get("/buses/byquery/")
async def fetch_buses_by_query(
    system_id: str, 
    route: str, 
    apikey:str, #TODO: better validation
    start: str, #TODO: better validation
    end:str #TODO: better validation
    ):
       
    #TODO: auth0 integration using 'apikey'
    # https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
    
    ## debugging output
    # return {"system_id": system_id, "route": route, "start":start, "end":end, "apikey":apikey}

    # live db query
    return {
            "query": 
                    {
                        "system_id": system_id,
                        "start (inclusive)":start,
                        "end (not inclusive)":end,
                        "apikey": apikey
                    }, 
            "result":query_job(system_id, route, start, end)
            }

@app.get("/")
async def get_root():
    return {"message": "FastAPI chicken sandwich running in a Lambda function"}
 
handler = Mangum(app)