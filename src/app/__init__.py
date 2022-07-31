#FastAPI Lambda API Handler
# using this tutorial https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-1-lambda-api-gateway/
    
from fastapi import FastAPI, Path, Request
from mangum import Mangum
import datetime as dt
import pythena
from starlette.responses import Response
import typing
import json



#root_path fix for docs/redoc endpoints
app = FastAPI(title="BusObservatoryAPI",root_path="/")

# for home page
# using this tutorial https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
from .library.helpers import *

#######################################################################
# helpers
#######################################################################
class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")

def query_job(system_id, route, start, end): 
    athena_client = pythena.Athena(database="busobservatory")
    # n.b. use single quotes in these queries otherwise Athena chokes
    query_String=   \
        f"""
        SELECT *
        FROM {system_id}
        WHERE
        route = '{route}'
        AND
        (timestamp >= from_iso8601_timestamp('{start}') AND timestamp < from_iso8601_timestamp('{end}'))
        """  
    print(query_String)
    dataframe, _ = athena_client.execute(query=query_String)
    # n.b. JSON serializer doesn't like NaNs
    return dataframe.fillna('').to_dict(orient='records')

def response_packager(response, system_id, route, start, end, apikey):
    return {
        "query": 
                {
                    "system_id": system_id,
                    "route": route,
                    "start (gte)":start,
                    "end (lt)":end,
                    "apikey": apikey
                }, 
        "result":response
        }


#######################################################################
# home page
#######################################################################
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
    

#######################################################################
# by path arguments (one route-hour)
#######################################################################

#TODO: auth0 integration using 'apikey' https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

@app.get("/buses/bypath/{system_id}/{route}/{year}/{month}/{day}/{hour}/{apikey}", 
         response_class=PrettyJSONResponse)
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

    return response_packager(query_job(system_id, route, start, end),
                             system_id, 
                             route, 
                             start,
                             end, 
                             apikey)


#######################################################################
# by query arguments (currently no limit on period)
#######################################################################

#TODO: abstract out query args into the query path, so we can use across data sources, e.g. (e.g. 'rt' for nj, GTFSRT "vehicle.trip.route_id","vehicle.timestamp" )
#TODO: validation for start, end
#TODO: limit size of request by trimming period to 1 hour?
#TODO: auth0 integration using 'apikey' https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

@app.get("/buses/byquery/",
         response_class=PrettyJSONResponse)
async def fetch_buses_by_query(
    system_id: str, 
    route: str, 
    apikey:str,
    start: str, 
    end:str 
    ):
    
    # # live db query
    # return {
    #         "query": 
    #                 {
    #                     "system_id": system_id,
    #                     "route": route,
    #                     "start (inclusive)":start,
    #                     "end (not inclusive)":end,
    #                     "apikey": apikey
    #                 }, 
    #         "result":query_job(system_id, route, start, end)
    #         }
    
    return response_packager(query_job(system_id, route, start, end),
                            system_id, 
                            route, 
                            start,
                            end, 
                            apikey)


handler = Mangum(app)