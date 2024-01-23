from aws_cdk import aws_secretsmanager as secrets
from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sqs as _sqs
from aws_cdk import Duration
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_wafv2 as waf
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import CfnOutput
from aws_cdk import BundlingOptions
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from constructs import Construct
import aws_cdk


class GenAiMapAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Dead-Letter Queue (DLQ)
        dlq = _sqs.Queue(self, "MyDLQ")  # Adjust the timeout as needed

        queue = _sqs.Queue(
            self,
            "GenAiMapQueue",
            visibility_timeout=Duration.seconds(90),
            queue_name="LambdaToSqsQueue",
            dead_letter_queue=_sqs.DeadLetterQueue(max_receive_count=5, queue=dlq),
        )

        init_lambda = _lambda.Function(
            self,
            "InitFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            timeout=Duration.seconds(10),
            code=_lambda.Code.from_asset("functions/init_lambda"),
            environment={
                "SQS_QUEUE_URL": queue.queue_url  # Pass the SQS queue URL as an environment variable
            },
        )

        queue.grant_send_messages(init_lambda)

        agent_lambda = _lambda.Function(
            self,
            "AgentLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            timeout=Duration.seconds(90),
            memory_size=3600,
            code=_lambda.Code.from_asset(
                "./functions/agent_lambda",
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
        )

        # Add the SQS queue as a trigger for the Agent Lambda
        agent_lambda.add_event_source(
            SqsEventSource(
                queue=queue,
                batch_size=1,  # Adjust batch size as needed
            )
        )

        # Create an API Gateway
        api = apigateway.RestApi(self, "GenAiMap", rest_api_name="GenAiMap")

        # Add a resource and method
        resource = api.root.add_resource("myresource")
        integration = apigateway.LambdaIntegration(init_lambda)
        resource.add_method("POST", integration)

        open_ai_secret = secrets.Secret.from_secret_name_v2(
            scope=self, id="openAiSecret", secret_name="OPENAI_API_KEY"
        )
        open_ai_secret.grant_read(grantee=agent_lambda)

        serper_secret = secrets.Secret.from_secret_name_v2(
            scope=self, id="serperSecret", secret_name="SERPER_API_KEY"
        )
        serper_secret.grant_read(grantee=agent_lambda)
