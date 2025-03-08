from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_cloudwatch as cloudwatch, Duration,
)
from constructs import Construct
import yaml
import os


class ResilientScalableAwsApiStack(Stack):
    """
    This stack provisions a VPC with multiple Availability Zones,
    an EKS cluster within the VPC, and deploys Kubernetes
    manifests for the API (deployment and service) to the cluster.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with a maximum of 2 Availability Zones.
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create an ECS cluster within the VPC.
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # Create a Fargate service with an Application Load Balancer.
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "MyFargateService",
            cluster=cluster,
            cpu=256,
            min_healthy_percent=50,
            memory_limit_mib=512,
            desired_count=2,
            public_load_balancer=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("fntkg/serverless-api:0.1.0")
            ),
        )

        # Configure auto scaling for the service based on CPU utilization.
        scaling = fargate_service.service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=10
        )
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=50,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        # Set up a CloudWatch Alarm to monitor high CPU usage.
        cloudwatch.Alarm(
            self,
            "HighCpuAlarm",
            metric=fargate_service.service.metric_cpu_utilization(),
            threshold=80,
            evaluation_periods=2,
            datapoints_to_alarm=2,
            alarm_description="Alarm when CPU exceeds 80%",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
