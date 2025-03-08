from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
)
from aws_cdk.lambda_layer_kubectl_v32 import KubectlV32Layer
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

        # Create a VPC with up to 3 Availability Zones
        vpc = ec2.Vpc(self, "EksVpc", max_azs=3)

        # Create the EKS cluster within the VPC
        cluster = eks.Cluster(
            self, "EksCluster",
            version=eks.KubernetesVersion.V1_32,
            kubectl_layer=KubectlV32Layer(self, "kubectl"),
            vpc=vpc,
            default_capacity = 0,
        )

        # Create a Managed Node Group in multiple AZs
        cluster.add_auto_scaling_group_capacity(
            "EksNodeGroup",
            instance_type=ec2.InstanceType("t3.micro"),
            min_capacity=3,
            desired_capacity=3,
            max_capacity=6,
            vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC}  # Multiple AZs
        )

        # Load external Kubernetes manifests
        deployment_manifest = self.load_yaml("k8s_manifests/deployment.yml")
        service_manifest = self.load_yaml("k8s_manifests/service.yml")
        hpa_manifest = self.load_yaml("k8s_manifests/hpa.yml")

        # Apply the Kubernetes manifests to the cluster
        cluster.add_manifest("ApiDeployment", deployment_manifest)
        cluster.add_manifest("ApiService", service_manifest)
        # TODO : Asegúrate de tener instalado el metrics-server en tu clúster, ya que el HPA lo requiere para obtener las métricas de CPU.
        cluster.add_manifest("ApiHpa", hpa_manifest)

        # TODO : Establecer alerting

    @staticmethod
    def load_yaml(file_path: str):
        """Utility method to load a YAML file and return its content as a dict."""
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(abs_path, "r") as file:
            return yaml.safe_load(file)
