#!/usr/bin/env python3
import os

import aws_cdk as cdk

from resilient_scalable_aws_api.resilient_scalable_aws_api_stack import ResilientScalableAwsApiStack


app = cdk.App()
ResilientScalableAwsApiStack(app, "ResilientScalableAwsApiStack",
    env=cdk.Environment(account='863518461037', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
