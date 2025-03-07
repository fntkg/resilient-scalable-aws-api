from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
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

        # Create a VPC with up to 3 Availability Zones
        vpc = ec2.Vpc(self, "EksVpc", max_azs=3)

        # Create the EKS cluster within the VPC
        cluster = eks.Cluster(
            # TODO : Revisar que este usando las instancias gratis
            # TODO : Configurar autoscaling
            self, "EksCluster",
            version=eks.KubernetesVersion.V1_21,
            vpc=vpc,
            default_capacity=2,  # Adjust the default capacity if needed
            default_capacity_instance="t2.large"
        )

        # Load external Kubernetes manifests
        deployment_manifest = self.load_yaml("manifests/deployment.yaml")
        service_manifest = self.load_yaml("manifests/service.yaml")
        hpa_manifest = self.load_yaml("manifests/hpa.yaml")

        # Apply the Kubernetes manifests to the cluster
        cluster.add_manifest("ApiDeployment", deployment_manifest)
        cluster.add_manifest("ApiService", service_manifest)
        cluster.add_manifest("ApiHpa", hpa_manifest)

    @staticmethod
    def load_yaml(file_path: str):
        """Utility method to load a YAML file and return its content as a dict."""
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(abs_path, "r") as file:
            return yaml.safe_load(file)
