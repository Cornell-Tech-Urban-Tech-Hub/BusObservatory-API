The Bus Observatory is a repository of big, streaming, urban transit data for non-commercial scientific and educational use.
# Available Data
## New York City Transit
We collect two feeds from the MTA Bus Time Developer API.
### **SIRI VehicleMonitoring**
>*System ID*: `nyct_mta_bus_siri`

> *Date Coverage:*
October 16, 2020 through present. This represents nearly 2 years' worth of vehicle movements on one of the world's largest urban bus systems.

>*Schema:* The [SIRI VehicleMonitoring feed](https://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring) is a complex, data-rich feed. We parse 23 fields, but also keep the full JSON responses (these can be made available on request).

```
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
```

### **GTFS-RT Positions**
> *System ID*: `nyct_mta_bus_gtfsrt`

> *Date Coverage:*
May 15, 2020 through present, once per minute.

> *Schema*
The MTA also provides vehicle positions through its [GTFS-RT feed](https://bustime.mta.info/wiki/Developers/GTFSRt). We parse all fields in this feed.

```
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
```

## NJTransit
NJTransit provides an unofficial open API operated by Clever Devices. We built on work by Chicago's civic hacking community, and fetch positions for the entire statewide bus system.
### **Clever Devices Unofficial API**
> *System ID*: `njtransit_bus`

> *Date Coverage & Frequency:*
April 5, 2021 through present, once per minute.

> *Schema*
This feed is based on an old technology and returns an XML response. We parse most of the fields in this feed, but most of them are undocumented.

```
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
```

### Where's My Bus System?

Over the next year, we plan to continue adding bus systems. Our focus will be on those supporting feed types we already are familiar with, including GTFS-RT, SIRI, and Clever Devices. Please use this form to suggest data feeds.

# Retrieving Data

## Obtaining an API Key

Lores mumps dolor sit mate, nominal id xiv. Dec ore offend it man re, est no dolor es explicate, re dicta elect ram demo critic duo. Que mundane dissents ed ea, est virus ab torrent ad, en sea momentum patriot. Erato dolor em omit tam quo no, per leg ere argument um re. Romanesque acclimates investiture.
## Endpoints

### Bulk Data Retrieval
The simplest and preferred method for data retrieval is the bulk data endpoint that provides positions for a single route for a single hour:

```
https://api.buswatcher.org/buses/bulk/{system_id}/{route}/{year}/{month}/{day}/{hour}/{apikey}
```
For example, to get all of the positions recorded from the New York City MTA Buses SIRI feed between 9pm and 10pm on July 4, 2022.

```
https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4/sfsafasfasf
```
Those who want to retrieve more route-hour bulk data sets are encouraging to develop their own programmatic approaches to requesting hour sequences or multiple routes. For instance:

```
TK Write a simple python grabber for one day.
buses = []
url=f"https://api.buswatcher.org/buses/bulk/nyct_mta_bus_siri/M1/2022/7/4/{hour}/sfsafasfasf"
for hour in range(0:23):
    buses.append(requests.get(url(hour).content))
```

### Direct Query
We are experimenting with a more powerful tool that allows queries by arbitrary arguments. Minimum required parameters are `system_id`, `route`, `start` and `end`—with the latter two timestamps in ISO8601 format. Start times are included in the query, end times are less than constrained.

For example, to get all of the positions recorded from the New York City MTA Buses SIRI feed all day on July 4, 2022:

```
https://api.buswatcher.org/buses/query/?system_id="nyct_mta_bus_siri"&route="M1"&start="2022-07-04T00:00:00"&end="2022-07-05T00:00:00"
```



### Full Documentation
For more details on endpoints, required arguments, and response formats, see the API's [Swagger]("/docs") and [Redoc]("/redoc") pages.


# License
Lores mumps dolor sit mate, nominal id xiv. Dec ore offend it man re, est no dolor es explicate, re dicta elect ram demo critic duo. Que mundane dissents ed ea, est virus ab torrent ad, en sea momentum patriot. Erato dolor em omit tam quo no, per leg ere argument um re. Romanesque acclimates investiture.

# Acknowledgements

This project uses [FastAPI](https://fastapi.tiangolo.com/), [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/), and [Bootstrap4](https://getbootstrap.com/docs/4.1/getting-started/introduction/).
