# BusObservatory-API (containerized version)

## TODO

1. debug AWS role
    - what are the rights that the Lambda SAM template used?
    - this container can only use the service role of the enclosing EC2 container
        - maybe just update that for now
        - then later during the ECS deployment figure out how to give it its own service role in ECS with well-fitted rights


# 1. Run locally

`docker-compose` is used to run locally.

```bash
$ docker-compose up
```

Check it works with...
```bash
$ curl http://127.0.0.1:80
```

# 2. Deploy on AWS: ECS Fargate + ALB
From [https://github.com/eliasbrange/aws-fastapi](https://github.com/eliasbrange/aws-fastapi)

This sample installs FastAPI in a Docker container and runs it on ECS Fargate that is fronted by an Application Load Balancer.



## a. Deploy

The CDK CLI is used to deploy the application.

```bash
$ cd deploy
$ cdk deploy

...

Outputs:
FastAPIStack.FastAPIServiceLoadBalancerDNS12345678 = XXXX.eu-west-1.elb.amazonaws.com
FastAPIStack.FastAPIServiceServiceURL12345678 = http://XXXX.eu-west-1.elb.amazonaws.com

Stack ARN:
arn:aws:cloudformation:eu-west-1:***********:stack/FastAPIStack/aaaaaaaa-1111-bbbb-2222-cccccccccccc
```

## b. Verify Deployment
```bash
$ curl http://XXXX.eu-west-1.elb.amazonaws.com

```



# 3. Debugging in a Remote Container on EC2

## a. start remote EC2 server

    ```
    start-queens
    ```
    
    or

    ```
    aws ec2 start-instances --instance-ids='\''i-02c021f07d618fd47'\'
    ```

## b. ssh to EC2 server and make sure to pull latest code

    ```
    cd dev/BusObservatory-API
    git pull
    ```

## c. open remote folder in VSCode dev container

    - Cmd-P: `Remote-SSH: Connect to Host...`
    - Cmd-P: `Open Folder in Dev container` TK
    - Open `dev/BusObservatory-API` folder
    - Checkout `dev/containerization` branch

## d. drop to shell in container

    ```
        cd app
        uvicorn main:app
    ```

## e. verify deployment

    Local ports are mapped to the remote container on EC2
    - Home [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - sample SIRI feed request[http://127.0.0.1:8000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4](http://127.0.0.1:8000/buses/bypath/nyct_mta_bus_siri/M1/2022/7/4/4)
