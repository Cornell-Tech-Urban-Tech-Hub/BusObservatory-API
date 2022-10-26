# BusObservatory-API (containerized version)

## TODO

1. debug AWS role
    - what are the rights that the Lambda SAM template used?
    - this container can only use the service role of the enclosing EC2 container, maybe just update that for now

## debugging in remote 

1. start remote EC2 server

    ```
    aws ec2 start-instances --instance-ids='\''i-02c021f07d618fd47'\'
    ```

2. open remote folder in VSCode dev container

    - Cmd-P: `Remote-SSH: Connect to Host...`
    - Cmd-P: `Open Folder in Dev container` TK
    - Open `dev/BusObservatory-API` folder
    - Checkout `dev/containerization` branch

3. drop to shell in container

    ```
        cd app
        uvicorn main:app
    ```

4. open url

    Local ports are mapped to the remote container on EC2
    - Home [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - sample SIRI feed request[http://127.0.0.1:8000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4](http://127.0.0.1:8000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4)
