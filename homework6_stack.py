import os.path

import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2


from aws_cdk.aws_s3_assets import Asset as S3asset



from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    App, CfnOutput, Stack
    # aws_sqs as sqs,
)
from constructs import Construct

dirname = os.path.dirname(__file__)

class Homework6Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, EngineeringVpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Instance Role and SSM Managed Policy
        InstanceRole = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        InstanceRole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # Create two web ec2 instances
        web1 = ec2.Instance(self, "web1", vpc=EngineeringVpc,
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)


        web2 = ec2.Instance(self, "web2", vpc=EngineeringVpc,
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)



        # Script in S3 as Asset(x2)
        web1initscriptasset = S3asset(self, "Web1Asset", path=os.path.join(dirname, "configure.sh"))
        asset_path = web1.user_data.add_s3_download_command(
            bucket=web1initscriptasset.bucket,
            bucket_key=web1initscriptasset.s3_object_key
        )

        web2initscriptasset = S3asset(self, "Web2Asset", path=os.path.join(dirname, "configure.sh"))
        asset_path = web2.user_data.add_s3_download_command(
            bucket=web2initscriptasset.bucket,
            bucket_key=web2initscriptasset.s3_object_key
        )



        # Userdata executes script from S3 on each web server (web1 and web2)
        web1.user_data.add_execute_file_command(
            file_path=asset_path
            )
        web1initscriptasset.grant_read(web1.role)
        
        web2.user_data.add_execute_file_command(
            file_path=asset_path
            )
        web2initscriptasset.grant_read(web2.role)
        
        
        # Allow inbound HTTP traffic in security groups
        web1.connections.allow_from_any_ipv4(ec2.Port.tcp(80)),
        web2.connections.allow_from_any_ipv4(ec2.Port.tcp(80))

        
        WebserversSG = ec2.SecurityGroup(self, "SecurityGroup", vpc=EngineeringVpc)
        autoscaling.AutoScalingGroup(self, "ASG",
            vpc=EngineeringVpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=WebserversSG
        )
        
        
        # Target group with duration-based stickiness with load-balancer generated cookie
        tg1 = elbv2.ApplicationTargetGroup(self, "TG1",
            target_type=elbv2.TargetType.INSTANCE,
            port=80,
            vpc=EngineeringVpc
        )
        
        # Target group with application-based stickiness
        tg2 = elbv2.ApplicationTargetGroup(self, "TG2",
            target_type=elbv2.TargetType.INSTANCE,
            port=80,
            vpc=EngineeringVpc
        )