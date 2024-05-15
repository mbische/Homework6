import os.path

from aws_cdk.aws_s3_assets import Asset as S3asset

from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
    # aws_sqs as sqs,
)

from constructs import Construct

class Homework6NetworkStack(Stack):

    @property
    def vpc(self):
        return self.EngineeringVpc
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC. CDK by default creates and attaches internet gateway for VPC
        self.EngineeringVpc = ec2.Vpc(self, "EngineeringVpc", 
                            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/18"),
                            max_azs=2,
                            subnet_configuration=[ec2.SubnetConfiguration(name="PublicSubnet01",subnet_type=ec2.SubnetType.PUBLIC),
                                                  ec2.SubnetConfiguration(name="PublicSubnet02", subnet_type=ec2.SubnetType.PUBLIC)]
        )
        
        # self.EngineeringVpc= ec2.Vpc(self, "EngineeringVpc",
        #                 ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/18"),
        #                 max_azs=2,
        #                 subnetConfiguration=[ { cidrMask=24, name="PublicSubnet01", subnetType=ec2.SubnetType.PUBLIC }, 
        #                 {cidrMask=24, name="PublicSubnet02", subnetType=ec2.SubnetType.PUBLIC } ] 
        # );
        
        
        # Vpc = new Vpc(this, "copilot-vpc", new VpcProps
        #     {
        #         Cidr = "172.0.3.0/16",
        #         NatGateways = 1,
        #         MaxAzs = 2,
        #         SubnetConfiguration = new ISubnetConfiguration[]
        #         {
        #             new SubnetConfiguration{ SubnetType = SubnetType.PUBLIC, CidrMask = 24, Name = "public-" },
        #             new SubnetConfiguration{ SubnetType = SubnetType.PRIVATE_WITH_EGRESS, CidrMask = 24, Name = "private-" },
        #             new SubnetConfiguration{ SubnetType = SubnetType.PRIVATE_ISOLATED, CidrMask = 24, Name = "isolated" }
        #         }
        #     });