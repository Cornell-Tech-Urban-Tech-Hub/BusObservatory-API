from enum import Enum
import collections
import pythena
from starlette.responses import Response
import typing
import json
import boto3

#######################################################################
# helpers
#######################################################################

# load system config from s3
def get_config(region, bucket, config_object_key):
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, config_object_key)
    configdata = json.load(obj.get()['Body'])
    sorted_configdata = collections.OrderedDict(sorted(configdata.items()))
    # return sorted_configdata
    filtered_configdata = {system_id: system_data for system_id, system_data in sorted_configdata.items() if system_data['publish'] == 'True'}
    return filtered_configdata

def get_system_id_enum(config):
    return Enum('SystemIDs', {k:k for (k,v) in config.items()} )
    # return Enum({k:k for (k,v) in get_config().items()} )

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

def query_job(config, system_id, route, start, end): 
    athena_client = pythena.Athena(database="busobservatory")
    # n.b. use single quotes in these queries otherwise Athena chokes
    query_String=   \
        f"""
        SELECT *
        FROM {system_id}
        WHERE
        "{config[system_id]['route_key']}" = '{route}'
        AND
        ("{config[system_id]['timestamp_key']}" >= from_iso8601_timestamp('{start}') AND "{config[system_id]['timestamp_key']}" < from_iso8601_timestamp('{end}'))
        """
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

def get_schema(system_id):
    client = boto3.client('athena', region_name = 'us-east-1')
    response = client.get_table_metadata(
        CatalogName='awsdatacatalog',
        DatabaseName='busobservatory',
        TableName=system_id
        )
    print(response)
    return response['TableMetadata']['Columns']
    
    
def get_routelist(config, system_id):
    athena_client = pythena.Athena(database="busobservatory")
    query_String=   \
        f"""
        SELECT "{config['route_key']}", COUNT(*)
        FROM {system_id}
        GROUP BY
        "{config['route_key']}"
        ORDER BY
        "{config['route_key']}"
        DESC
        """
    dataframe, _ = athena_client.execute(query=query_String, workgroup="busobservatory")
    # n.b. JSON serializer doesn't like NaNs
    routelist = dataframe.fillna('').to_dict(orient='records')
    return routelist

def get_system_history(config, system_id):
    athena_client = pythena.Athena(database="busobservatory")
    query_String=   \
        f"""            
        SELECT year ("{config['timestamp_key']}") as y, month ("{config['timestamp_key']}") as m, day ("{config['timestamp_key']}") as d, count(*) as ct
        FROM {system_id}      
        GROUP BY year ("{config['timestamp_key']}"), month ("{config['timestamp_key']}"), day ("{config['timestamp_key']}")
        ORDER BY year ("{config['timestamp_key']}") ASC, month ("{config['timestamp_key']}") ASC, day ("{config['timestamp_key']}") ASC
        """
    dataframe, _ = athena_client.execute(query=query_String, workgroup="busobservatory")
    # n.b. JSON serializer doesn't like NaNs
    history = dataframe.fillna('').to_dict(orient='records')
    return history