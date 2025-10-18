from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        test_fn = _lambda.Function(
            self,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="test_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        new_chapter_fn = _lambda.Function(
            self,
            "NewChapterFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="new_chapter_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        api = apigw.RestApi(
            self,
            "LehighApiGw",
            rest_api_name="LehighApiGw"
        )

        test_resource = api.root.add_resource("test")
        test_resource.add_method(
            "GET",
            apigw.LambdaIntegration(test_fn)
        )

        new_resource = api.root.add_resource("new")
        new_resource.add_method(
            "POST",
            apigw.LambdaIntegration(new_chapter_fn)
        )