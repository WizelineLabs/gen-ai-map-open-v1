import aws_cdk as core
import aws_cdk.assertions as assertions

from gen_ai_map_agent.gen_ai_map_agent_stack import GenAiMapAgentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in gen_ai_map_agent/gen_ai_map_agent_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GenAiMapAgentStack(app, "gen-ai-map-agent")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
