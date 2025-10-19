from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        chapters_table = dynamodb.Table.from_table_name(
            self, "ChaptersTable", "Chapters"
        )
        end_table = dynamodb.Table.from_table_name(
            self, "EndTable", "End"
        )
        questions_table = dynamodb.Table.from_table_name(
            self, "QuestionsTable", "Questions"
        )

        test_fn = _lambda.Function(
            self,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="test_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        new_chapter_fn = _lambda.Function(
            self,
            "NewChapterFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="new_chapter_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
        )
        chapters_table.grant_read_write_data(new_chapter_fn)

        gen_questions_fn = _lambda.Function(
            self,
            "GenQuestionsFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="gen_questions_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(60)
        )
        chapters_table.grant_read_write_data(gen_questions_fn)
        end_table.grant_read_write_data(gen_questions_fn)
        questions_table.grant_read_write_data(gen_questions_fn)
        gen_questions_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonBedrockFullAccess"
            )
        )

        test_dyndb_fn = _lambda.Function(
            self,
            "TestDynDBFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="test_dyndb_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
        )
        chapters_table.grant_read_write_data(test_dyndb_fn)

        test_bedrock_fn = _lambda.Function(
            self,
            "TestBedrockFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="test_bedrock_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
        )
        chapters_table.grant_read_write_data(test_dyndb_fn)

        api = apigw.RestApi(self, "LehighApiGw", rest_api_name="LehighApiGw")

        test_resource = api.root.add_resource("test")
        test_resource.add_method("GET", apigw.LambdaIntegration(test_fn))

        new_resource = api.root.add_resource("new")
        new_resource.add_method("POST", apigw.LambdaIntegration(new_chapter_fn))

        questions_resource = api.root.add_resource("questions")
        questions_resource.add_method("POST", apigw.LambdaIntegration(gen_questions_fn))

        test_dyndb_resource = api.root.add_resource("testdyndb")
        test_dyndb_resource.add_method("POST", apigw.LambdaIntegration(test_dyndb_fn))

        test_bedrock_resource = api.root.add_resource("testbdrk")
        test_bedrock_resource.add_method(
            "GET", apigw.LambdaIntegration(test_bedrock_fn)
        )
