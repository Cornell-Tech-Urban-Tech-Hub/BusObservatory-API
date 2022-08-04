# FastAPI Lambda API Handler
# using this tutorial https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-1-lambda-api-gateway/

import datetime as dt

from fastapi import FastAPI, Request, Path, Depends, Response, status
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mangum import Mangum

from .library.helpers import *
from .library.auth import *

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

#root_path fix for docs/redoc endpoints
app = FastAPI(title="BusObservatoryAPI",root_path="/")

# for home page
# using this tutorial https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#######################################################################
# home page
#######################################################################
@app.get("/", 
         response_class=HTMLResponse,
         include_in_schema=False)
async def home(request: Request):
    markdown = openfile("index.md") 
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "markdown": markdown
            }
        )
    
    
#######################################################################
# system pages
#######################################################################
@app.get("/nyct", 
         response_class=HTMLResponse,
         include_in_schema=False)
async def home(request: Request):
    markdown = openfile("nyct.md")
    return templates.TemplateResponse(
        "feeds/nyct.html", {
            "request": request,
            "markdown": markdown
            }
        )
    
@app.get("/njtransit", 
         response_class=HTMLResponse,
         include_in_schema=False)
async def home(request: Request):
    markdown = openfile("njtransit.md")
    return templates.TemplateResponse(
        "feeds/njtransit.html", {
            "request": request,
            "markdown": markdown
            }
        )

#######################################################################
# by path arguments (one route-hour)
#######################################################################

@app.get("/buses/bulk/{system_id}/{route}/{year}/{month}/{day}/{hour}", 
         response_class=PrettyJSONResponse)
async def fetch_bulk_position_data(
    system_id: str, 
    route: str, 
    year:int = Path(title="Year of service", ge=2011, le=2050), 
    month:int = Path(title="Month of service", ge=1, le=12), 
    day:int = Path(title="Day of service", ge=1, le=31),
    hour:int = Path(title="Hour of service", ge=0, le=23),
    token: str = Depends(token_auth_scheme)
    ):
    
    #convert year/month/day/hour into a start and end ISO 8601 timestamp for bottom and top of hour 
    start = dt.datetime(year,month,day,hour,0,0).isoformat()
    if hour == 23:
        # advance to midnight
        end = dt.datetime(year,month,day+1,0,0,0).isoformat()
    elif hour < 23:
        end = dt.datetime(year,month,day,(hour+1),0,0).isoformat()
    
    # verify auth0 and return 400 BAD REQUEST if failed
    result = VerifyToken(token.credentials).verify()
    response = Response()
    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return response

    # otherwise run query and return results
    return response_packager(query_job(system_id, route, start, end),
                             system_id, 
                             route, 
                             start,
                             end)

# #######################################################################
# # by query arguments (currently no limit on period)
# #######################################################################
#FIXME: responses will violate Lambda memory limit (raise to 512 in template.yaml)
#FIXME: responses will violate Lambda response size limit (figure out how to pass back an S3 location per https://jun711.github.io/aws/handling-aws-api-gateway-and-lambda-413-error/)
#TODO: abstract out query args into the query path, so we can use across data sources, e.g. (e.g. 'rt' for nj, GTFSRT "vehicle.trip.route_id","vehicle.timestamp" )
#TODO: validation for start, end
#TODO: limit size of request by trimming period to 1 hour?

# @app.get("/buses/query/",
#          response_class=PrettyJSONResponse)
# async def fetch_position_data_by_query(
#     system_id: str, 
#     route: str, 
#     start: str, 
#     end:str 
#     ):

#     return response_packager(query_job(system_id, route, start, end),
#                             system_id, 
#                             route, 
#                             start,
#                             end, 
#                             apikey)


handler = Mangum(app)