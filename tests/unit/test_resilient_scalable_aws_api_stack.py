import aws_cdk as core
import aws_cdk.assertions as assertions

from resilient_scalable_aws_api.resilient_scalable_aws_api_stack import ResilientScalableAwsApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in resilient_scalable_aws_api/resilient_scalable_aws_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ResilientScalableAwsApiStack(app, "resilient-scalable-aws-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
