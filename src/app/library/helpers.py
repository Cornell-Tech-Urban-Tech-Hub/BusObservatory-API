import os.path
import markdown
import pythena
from starlette.responses import Response
import typing
import json

def openfile(filename):
    filepath = os.path.join("pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data

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
    dataframe, _ = athena_client.execute(query=query_String, workgroup="busobservatory")
    # n.b. JSON serializer doesn't like NaNs
    return dataframe.fillna('').to_dict(orient='records')

def response_packager(response, system_id, route, start, end):
    return {
        "query": 
                {
                    "system_id": system_id,
                    "route": route,
                    "start (gte)":start,
                    "end (lt)":end
                }, 
        "result":response
        }
