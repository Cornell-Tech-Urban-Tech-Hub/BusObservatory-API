# How to Get Data

The Bus Observatory API distributes bulk bus position and operational data. This data is sampled at one-minute intervals and bundled into containers covering one route for 60 minutes (referred to as a 'route-hour' below).

First, explore the schemas for our datasets so you understand what's in the data you're requesting. Links are above and in the top nav bar.

Then, retrieve the bulk data through several methods:

## 1. Download A Sample Data Set

We have prepared several data sets for data science explorations. All are extracted from the New York City Transit SIRI feed (`nyct_mta_bus_siri`):

- **One route-day.** July 5, 2022. M1 route only. [CSV](https://urbantech-public.s3.amazonaws.com/DONT_DELETE/api.busobservatory.org%E2%80%94sampledata/nyct_mta_buses_siri.M1.2022-07-05-daily.csv) (0.006 GB)
- **One route-month.** July 1-31, 2022. M1 route only. [CSV](https://urbantech-public.s3.amazonaws.com/DONT_DELETE/api.busobservatory.org%E2%80%94sampledata/nyct_mta_buses_siri.M1.2022-07-monthly.csv) (0.16 GB)
- **One system-day.** July 5, 2022. All routes. [CSV](https://urbantech-public.s3.amazonaws.com/DONT_DELETE/api.busobservatory.org%E2%80%94sampledata/nyct_mta_buses_siri.all_routes.2022-07-05-daily.csv) (0.71 GB)
- **One system-month.** [CSV](https://urbantech-public.s3.amazonaws.com/DONT_DELETE/api.busobservatory.org%E2%80%94sampledata/nyct_mta_buses_siri.all_routes.2022-07-monthly.csv) (17.1 GB)

## 2. Get Data From the Web Console

The easiest way to explore the Bus Observatory API bulk retrieval endpoint is through the [Swagger UI]("/docs"). 

 1. Follow [this link]("https://api.buswatcher.org/docs") 
 2. Click on the first highlighted row ("GET /buses/bulk/...")
 3. Click `Try It Out`
 4. Fill out the form. Allowed values are:
    - system_id: `nyct_mta_bus_siri, nyct_mta_bus_gtfsrt, njtransit_bus`
    - route: Any valid route on the system selected.
    - year, month, day, hour: No leading zeros.
5. Click `Execute`
6. Results are presented as JSON in the browser, and can be downloaded as well.
## 3. Get Data Directly By Browser

Data can also be accessed directly via the API endpoint.

The format (with same restrictions as above) is:

    https://api/buswatcher.org/buses/bulk/{system_id}/{route}/{year}/{month}/{day}/{hour}

For example, to get all of the positions recorded from the New York City MTA Buses SIRI feed between 9pm and 10pm on July 4, 2022.

    https://api.buswatcher.org/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/21

## 4. Get Data Directly From A Command Line Interface (CLI)

The [Swagger UI]("/docs") provides sample code for retrieval via `curl`. For example:

    curl -X 'GET' \
        'https://api.buswatcher.org/buses/bulk/nyct_mta_bus_siri/M1/2022/7/4/21' \
        -H 'accept: application/json'

## 5. Get More Data With A Python Script 

Those who want to retrieve more route-hour bulk data sets are encouraging to develop their own programmatic approaches to requesting hour sequences or multiple routes. For example, the following Python function:

- takes a system id, a route, and a start and end time in ISO8501 format as arguments;
- generates a list of dates and hours within this interval;
- retrieves the bulk data for each our from the Bus Observatory API;
- combines these responses into a single Pandas dataframe; and,
- writes the combined dataframe to a Parquet file.


    import pandas as pd
    import requests

    def get_buses(system_id, route, start, end):

        df = pd.DataFrame()

        times = (
            pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq="1H")
            .to_pydatetime()
            .tolist()
        )

        for t in times:

            print(t)
            url = f"https://api.buswatcher.org/buses/bulk/{system_id}/{route}/{t.year}/{t.month}/{t.day}/{t.hour}"
            print(url)
            r = requests.get(url).json()
            print(r["query"])
            newdata = pd.DataFrame.from_dict(r["result"])
            df = pd.concat([df, newdata], ignore_index=True, sort=False)

        return df

## Performance, Restricitons, and Technical API Details

#### Rate Limiting
This service is not intended to be a backend for web services, and is implemented entirely through serverless technologies. You may experience response times in excess of 60 seconds for bulk data requests.
#### Restrictions
We are not currently implementing any access restrictions for this service. However, API access is rate limited. If you receive a `429 Too Many Requests` error, please wait and try again later.
####  API Technical Documentation
For full details on endpoints, required arguments, and response formats, see our [Swagger UI]("https://api.buswatcher.org/docs") and [Redoc]("https://api.buswatcher.org/redoc") pages.
