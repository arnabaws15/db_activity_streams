from aws_cdk import (
    # Duration,
    App,
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    CfnOutput,
    RemovalPolicy,
    aws_iam as iam
    # aws_sqs as sqs,
)
from aws_cdk.aws_opensearchservice import (
    Domain,
    EngineVersion,
    EbsOptions,
    EncryptionAtRestOptions,
    ZoneAwarenessConfig,
    CapacityConfig
)


from constructs import Construct

class DbActivityStreamsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        # define the vpc with 3 public and 3 private subnets

        vpc = ec2.Vpc(self, "DbActivityStreamsVPC", max_azs=3, enable_dns_hostnames=True, enable_dns_support=True, nat_gateways=1)
        
        # Public subnets
        public_subnet_1 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PUBLIC,
            name="public1",
            cidr_mask=24
        )

        public_subnet_2 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PUBLIC,
            name="public2",
            cidr_mask=24
        )

        public_subnet_3 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PUBLIC,
            name="public3",
            cidr_mask=24
        )

        # Private subnets  
        private_subnet_1 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            name="private1",
            cidr_mask=24
        )

        private_subnet_2 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            name="private2",
            cidr_mask=24
        )

        private_subnet_3 = ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            name="private3", 
            cidr_mask=24            
        )
        
        #CfnOutput(self, "Vpc", values=vpc.vpc_id)
        
        # Configure the Aurora Postgres DB Cluster
        aurora_cluster = rds.DatabaseCluster(self, "Database",
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_15_2),
            credentials=rds.Credentials.from_generated_secret("adminuser"),
            instance_props=rds.InstanceProps(
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE),
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                vpc=vpc
            ),
            storage_type=rds.DBClusterStorageType.AURORA_IOPT1
        )
        
        #CfnOutput(self,'AuroraCluster', values=cluster.cluster_identifier)
        # Lets now provision a bastion host to connect to db
        bastion_host = ec2.BastionHostLinux(self, "BastionHost",
            vpc=vpc,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sdh",
                volume=ec2.BlockDeviceVolume.ebs(10,
                    encrypted=True
                )
            )],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
            subnet_selection=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )
        
        # Add a security group rule to allow the bastion host to connect to the RDS database instance.
        aurora_cluster.connections.allow_default_port_from(bastion_host)
        
        # Now lets provision an opensearch cluster in private subnets
        # Engine Version: OPENSEARCH_2_7
        # Need to create a service linked role when deploying in a vpc
        slr = iam.CfnServiceLinkedRole(self, "Service Linked Role for OS",
            aws_service_name="es.amazonaws.com"
        )
        #slr.apply_removal_policy(RemovalPolicy.DESTROY)
        
        domain = Domain(self, "DBActivityOSDomain",
            version=EngineVersion.OPENSEARCH_2_7,
            ebs=EbsOptions(
                volume_size=50,
                volume_type=ec2.EbsDeviceVolumeType.GP3
            ),
            node_to_node_encryption=True,
            encryption_at_rest=EncryptionAtRestOptions(
                enabled=True
            ),
            removal_policy=RemovalPolicy.DESTROY,
            enforce_https=True,
            vpc=vpc,
            zone_awareness=ZoneAwarenessConfig(
                enabled=True,
                availability_zone_count=3
            ),
            capacity=CapacityConfig(
                data_nodes=3,
               # master_nodes=1,
                multi_az_with_standby_enabled=False
            )
        )
        
        domain.connections.allow_from(bastion_host,ec2.Port.tcp(443))
        
        
