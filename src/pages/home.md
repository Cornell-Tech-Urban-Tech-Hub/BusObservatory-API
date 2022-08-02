## Available Data

Lores mumps dolor sit mate, nominal id xiv. Dec ore offend it man re, est no dolor es explicate, re dicta elect ram demo critic duo. Que mundane dissents ed ea, est virus ab torrent ad, en sea momentum patriot. Erato dolor em omit tam quo no, per leg ere argument um re. Romanesque acclimates investiture.

###**New York City Transit (SIRI)**

*System ID*: `nyct_mta_bus_siri`

*Date Coverage:*
October 16, 2020 through present. This represents nearly 2 years' worth of vehicle movements on one of the world's largest urban bus systems.

*Schema:* The [SIRI VehicleMonitoring feed](https://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring) is a complex, data-rich feed. We parse 23 fields, but also keep the full JSON responses (these can be made available on request).

    timestamp           	timestamp       	                    
    route_long          	string              	                    
    direction           	string              	                    
    trip_id             	string              	                    
    gtfs_shape_id       	string              	                    
    route_short         	string              	                    
    agency              	string              	                    
    origin_id           	string              	                    
    destination_name    	string              	                    
    next_stop_id        	string              	                    
    next_stop_eta       	string              	                    
    next_stop_d_along_route	double              	                    
    next_stop_d         	double              	                    
    lat                 	double              	                    
    lon                 	double              	                    
    bearing             	double              	                    
    progress_rate       	string              	                    
    vehicle_id          	string              	                    
    gtfs_block_id       	string              	                    
    passenger_count     	double              	                    
    progress_status     	string              	                    
    route               	string              	                    
    service_date        	string    

###**New York City Transit (GTFS-RT)**

*System ID*: `nyct_mta_bus_gtfsrt`

*Date Coverage:*
May 15, 2020 through present, once per minute.

*Schema*: The MTA also provides vehicle positions through its [GTFS-RT feed](https://bustime.mta.info/wiki/Developers/GTFSRt). We parse all fields in this feed.

    id                  	    string              	                    
    vehicle.trip.trip_id	    string              	                    
    vehicle.trip.start_date	    string              	                    
    vehicle.trip.route_id	    string              	                    
    vehicle.trip.direction_id	int                 	                    
    vehicle.position.latitude	double              	                    
    vehicle.position.longitude	double              	                    
    vehicle.position.bearing	double              	                    
    vehicle.timestamp   	    timestamp           	                    
    vehicle.stop_id     	    string              	                    
    vehicle.vehicle.id  	    string 

###**New Jersey Transit**

NJTransit provides an unofficial open API operated by Clever Devices. We built on work by Chicago's civic hacking community, and fetch positions for the entire statewide bus system.

*System ID*: `njtransit_bus`

*Date Coverage & Frequency:*
April 5, 2021 through present, once per minute.

*Schema*: This feed is based on an old technology and returns an XML response. We parse most of the fields in this feed, but most of them are undocumented.

    id                  	string              	                    
    consist             	string              	                    
    cars                	string              	                    
    rtpifeedname        	string              	                    
    m                   	string              	                    
    rt                  	string              	                    
    rtrtpifeedname      	string              	                    
    rtdd                	string              	                    
    c                   	string              	                    
    d                   	string              	                    
    dd                  	string              	                    
    dn                  	string              	                    
    lat                 	double              	                    
    lon                 	double              	                    
    pid                 	string              	                    
    pd                  	string              	                    
    pdrtpifeedname      	string              	                    
    run                 	string              	                    
    fs                  	string              	                    
    op                  	string              	                    
    bid                 	string              	                    
    wid1                	string              	                    
    wid2                	string              	                    
    timestamp           	timestamp    


### Where's My Bus System?

Over the next year, we plan to continue adding bus systems. Our focus will be on those supporting feed types we already are familiar with, including GTFS-RT, SIRI, and Clever Devices. Please use this form to suggest data feeds.

## Retrieving Data

Lores mumps dolor sit mate, nominal id xiv. Dec ore offend it man re, est no dolor es explicate, re dicta elect ram demo critic duo. Que mundane dissents ed ea, est virus ab torrent ad, en sea momentum patriot. Erato dolor em omit tam quo no, per leg ere argument um re. Romanesque acclimates investiture.
### Obtaining an API Key

Lores mumps dolor sit mate, nominal id xiv. Dec ore offend it man re, est no dolor es explicate, re dicta elect ram demo critic duo. Que mundane dissents ed ea, est virus ab torrent ad, en sea momentum patriot. Erato dolor em omit tam quo no, per leg ere argument um re. Romanesque acclimates investiture.
### Bulk Data Endpoint
The simplest and preferred method for data retrieval is the bulk data endpoint that provides positions for a single route for a single hour:

    https://api.buswatcher.org/buses/bulk/{system_id}/{route}/{year}/{month}/{day}/{hour}/{apikey}

For example, to get all of the positions recorded from the New York City MTA Buses SIRI feed between 9pm and 10pm on July 4, 2022.

    https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf

Those who want to retrieve more route-hour bulk data sets are encouraging to develop their own programmatic approaches to requesting hour sequences or multiple routes. For instance:

### Retrieving More Than One Route-Hour
Here's a function that will take a system id, a route, and a start and end time in ISO8501 format, and your apikey and fetch all the data into a single dataframe.

    import pandas as pd
    import requests
    from datetime import datetime

    def get_buses(system_id, route, start, end, apikey):

        df = pd.DataFrame()

        times = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq='1H').to_pydatetime().tolist()
        
        for t in times:
            print(t)
            url=f"https://api.buswatcher.org/buses/bulk/{system_id}/{route}/{t.year}/{t.month}/{t.day}/{t.hour}/{apikey}"
            print(url)
            r = requests.get(url).json()
            print(r['query'])
            newdata = pd.DataFrame.from_dict(r['result'])
            df = pd.concat([df, newdata], ignore_index=True, sort=False)        
        return df

### Custom Query Endpoint (future)
We are experimenting with a more powerful tool that allows queries by arbitrary arguments.

### Full Documentation
For more details on endpoints, required arguments, and response formats, see the API's [Swagger]("/docs") and [Redoc]("/redoc") pages.
