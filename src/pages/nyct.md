###**SIRI**

*System ID*: `nyct_mta_bus_siri`

*Date Coverage:*
October 16, 2020 through present. This represents nearly 2 years' worth of vehicle movements on one of the world's largest urban bus systems.

*Schema:* The [SIRI VehicleMonitoring feed](https://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring) is a complex, data-rich feed. We parse 23 fields, but also keep the full JSON responses (these can be made available on request). Note that coverage of some fields is not available for all periods. In particular, fields marked with a * are not available before May 2021.

    timestamp           	timestamp       	                    
    route_long          	string              	                    
    direction           	string              	                    
    trip_id             	string              	                    
    gtfs_shape_id       	string              	                    
    route_short         	string              	                    
    agency              	string              	                    
    origin_id           	string              	                    
    destination_name    	string              	                    
    next_stop_id        	string*              	                    
    next_stop_eta       	string*              	                    
    next_stop_d_along_route	double*              	                    
    next_stop_d         	double*              	                    
    lat                 	double              	                    
    lon                 	double              	                    
    bearing             	double              	                    
    progress_rate       	string              	                    
    vehicle_id          	string              	                    
    gtfs_block_id       	string              	                    
    passenger_count     	double*              	                    
    progress_status     	string              	                    
    route               	string              	                    
    service_date        	string    

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