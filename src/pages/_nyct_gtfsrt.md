
###**GTFS-RT**

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