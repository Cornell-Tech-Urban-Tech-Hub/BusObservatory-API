# FastAPI Lambda API Handler
# using this tutorial https://www.eliasbrange.dev/posts/deploy-fastapi-on-aws-part-1-lambda-api-gateway/

import datetime as dt
from enum import Enum
from types import SimpleNamespace
from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

from .library.helpers import *

description = """
The Bus Observatory is a public archive of real-time data on vehicle movements and status, collected from transit systems around the world. This free service is provided by the <a href="https://urban.tech.cornell.edu/">Jacobs Urban Tech Hub</a> at <a href="https://tech.cornell.edu/">Cornell Tech</a>. 🚀

## Bulk Bus Observations

You can **read items**.

"""


#root_path fix for docs/redoc endpoints
app = FastAPI(
    root_path="/",
    title="Bus Observatory API",
    description=description,
    version="1.0.0",
    # terms_of_service="http://example.com/terms/",
    contact={
         "name": "Urban Tech Hub",
         "url": "https://urban.tech.cornell.edu/",
         "email": "urbantech@cornell.edu",
         },
    license_info={
        "name": "CC BY-NC 4.0",
        "url": "http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1",
        },
    )

# for home page
# using this tutorial https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#######################################################################
# globals
#######################################################################

config = get_config()

#######################################################################
# home page
#######################################################################
@app.get("/", 
         response_class=HTMLResponse,
         include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "config": get_config()
            }
        )


#######################################################################
# system pages
#######################################################################

@app.get("/{system_id}/schema", 
         response_class=HTMLResponse,
         include_in_schema=False)
# this creates an enumeration on the fly that maps symbolic names to the unique system_ids
async def schema(request: Request, 
                 system_id: get_system_id_enum()
                 ): 
    return templates.TemplateResponse(
        "schema.html", {
            "request": request,
            "system_id": system_id.value,
            "config": get_config(), # needed for the navbar
            "feed_info": get_config()[system_id.value], # just this one system
            "schema": get_schema(
                system_id.value
                ), # and the schema fetched from Athena,
            # "routelist": get_routelist(
            #     get_config()[system_id.value],
            #     system_id.value
            #     ),
            "history": get_system_history(
                get_config()[system_id.value],
                system_id.value
                ) # and the system history from an athena query# and the routelist from an athena query,
            }
        )

#######################################################################
# by path arguments (one route-hour)
#######################################################################

@app.get("/buses/bulk/{system_id}/{route}/{year}/{month}/{day}/{hour}", 
         response_class=PrettyJSONResponse)
async def fetch_bulk_position_data(
    system_id: get_system_id_enum(), 
    route: str, 
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
    
    # otherwise run query and return results
    return response_packager(query_job(get_config(), system_id.value, route, start, end),
                             system_id.value, 
                             route, 
                             start,
                             end)

'''
# #######################################################################
# # by query arguments (currently no limit on period)
# #######################################################################
#FIXME: responses will violate Lambda memory limit (raise to 512 in template.yaml)
#FIXME: responses will violate Lambda response size limit (figure out how to pass back an S3 location per https://jun711.github.io/aws/handling-aws-api-gateway-and-lambda-413-error/)
#TODO: abstract out query args into the query path, so we can use across data sources, e.g. (e.g. 'rt' for nj, GTFSRT "vehicle.trip.route_id","vehicle.timestamp" )
#TODO: validation for start, end
#TODO: limit size of request by trimming period to 1 hour?

@app.get("/buses/query/",
         response_class=PrettyJSONResponse)
async def fetch_position_data_by_query(
    system_id: str, 
    route: str, 
    start: str, 
    end:str 
    ):

    return response_packager(query_job(system_id, route, start, end),
                            system_id, 
                            route, 
                            start,
                            end 
                            )
'''

handler = Mangum(app)