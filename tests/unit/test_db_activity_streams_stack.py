import aws_cdk as core
import aws_cdk.assertions as assertions

from db_activity_streams.db_activity_streams_stack import DbActivityStreamsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in db_activity_streams/db_activity_streams_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DbActivityStreamsStack(app, "db-activity-streams")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
