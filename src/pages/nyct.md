*Date Coverage:*
October 16, 2020 through present, once per minute.

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

 Note that coverage of some fields is not available for all periods. Fields marked with an asterisk (*) are not available before May 2021.