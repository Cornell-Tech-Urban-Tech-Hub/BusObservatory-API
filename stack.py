from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_secretsmanager as sm
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
        
        #Add the policies we need to the ECS Task Role
        
        self.ecs_service.task_definition.task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"))
        # self.ecs_service.task_definition.task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSGlueConsoleFullAccess"))

        # import the bucket and grant full access
        s3_busobservatory_bucket = s3.Bucket.from_bucket_name(self,
                                                              'BusObservatoryBucket',
                                                              'busobservatory')
        s3_busobservatory_bucket.grant_read(self.ecs_service.task_definition.task_role)
        
        # needed for pyathena to garbage collect query results
        # dangerous workaround for testing
        self.ecs_service.task_definition.task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        ##TODO: scope it back? this doesnt fully work
        # s3_busobservatory_bucket.grant_delete(self.ecs_service.task_definition.task_role)
        
        # get the secret and grant access to the ECS Task Role
        secret = sm.Secret.from_secret_attributes(self, "ImportedSecret",
            secret_complete_arn="arn:aws:secretsmanager:us-east-1:870747888580:secret:auth0_api.busobservatory.org-Mx25l5"
            )
        secret.grant_read(self.ecs_service.task_definition.task_role)
       