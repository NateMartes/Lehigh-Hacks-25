from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = _lambda.Function(
            self,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="test_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        endpoint = apigw.LambdaRestApi(
            self,
            "ApiGwTest",
            handler=fn,
            rest_api_name="test"
        )