from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns

class BusObservatoryAPI(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)


        # Create VPC
        self.vpc = ec2.Vpc(self, "BusObservatoryAPI_VPC", max_azs=3)

        # Create Fargate Cluster
        self.ecs_cluster = ecs.Cluster(
            self,
            "BusObservatoryAPI_ECSCluster",
            vpc=self.vpc,
        )

        # Create Fargate Service and ALB
        image = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(
                directory=".",
            )
        )
        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "BusObservatoryAPI_Service",
            cluster=self.ecs_cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            task_image_options=image,
        )
        
        #TODO: get the service role produced by the above self.ecs_service
            
        print(self.ecs_service)
        self.ecs_service.task_definition.add_to_task_role_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"))
        
        # Traceback (most recent call last):
        # File "<string>", line 1, in <module>
        # File "/Users/anthonytownsend/Dropbox/Desktop/code/cornell_tech/BusObservatory-API/.venv/lib/python3.9/site-packages/aws_cdk/aws_ecs/__init__.py", line 31711, in add_to_task_role_policy
        #     check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        # File "/Users/anthonytownsend/Dropbox/Desktop/code/cornell_tech/BusObservatory-API/.venv/lib/python3.9/site-packages/typeguard/__init__.py", line 785, in check_type
        #     raise TypeError(
        # TypeError: type of argument statement must be aws_cdk.aws_iam.PolicyStatement; got jsii._reference_map.InterfaceDynamicProxy instead

        
        
        
        
        #TODO: attach policies to whatever role is produced like " BusObservatoryAPIServiceTaskDefExecutionRole7D7F55E6"
        # by self.ecs_service

        # service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"))
        # ? service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSGlueConsoleFullAccess"))
        # ? service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"))

        #     - AWSSecretsManagerGetSecretValuePolicy:
        #         SecretArn: 'arn:aws:secretsmanager:us-east-1:870747888580:secret:auth0_api.busobservatory.org-Mx25l5'

        # Attach a Managed Policy to an IAM Role after Role Creation #
        # https://bobbyhadz.com/blog/aws-cdk-iam-role#attach-a-managed-policy-to-an-iam-role-after-role-creation
