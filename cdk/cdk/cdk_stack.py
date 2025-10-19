from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigw,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = cognito.UserPool.from_user_pool_id(
            self, "UserPool", user_pool_id="us-east-1_Mq1Lp3b0h"
        )

        authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer", cognito_user_pools=[user_pool]
        )

        chapters_table = dynamodb.Table.from_table_name(
            self, "ChaptersTable", "Chapters"
        )
        end_table = dynamodb.Table.from_table_name(self, "EndTable", "End")
        questions_table = dynamodb.Table.from_table_name(
            self, "QuestionsTable", "Questions"
        )
        intro_table = dynamodb.Table.from_table_name(self, "IntroTable", "End")

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
            timeout=Duration.seconds(60),
        )
        chapters_table.grant_read_write_data(gen_questions_fn)
        end_table.grant_read_write_data(gen_questions_fn)
        questions_table.grant_read_write_data(gen_questions_fn)
        gen_questions_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
        )

        gen_intro_fn = _lambda.Function(
            self,
            "GenIntroFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="gen_intro_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(60),
        )
        chapters_table.grant_read_write_data(gen_intro_fn)
        end_table.grant_read_write_data(gen_intro_fn)
        questions_table.grant_read_write_data(gen_intro_fn)
        intro_table.grant_read_write_data(gen_intro_fn)
        gen_intro_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
        )

        get_intro_fn = _lambda.Function(
            self,
            "GetIntroFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="get_intro_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(60),
        )
        intro_table.grant_read_write_data(get_intro_fn)

        get_questions_fn = _lambda.Function(
            self,
            "GetQuestionsFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="get_questions_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
        )
        questions_table.grant_read_write_data(get_questions_fn)

        gen_end_fn = _lambda.Function(
            self,
            "GenEndFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="gen_end_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(60),
        )
        intro_table.grant_read_write_data(gen_end_fn)
        end_table.grant_read_write_data(gen_end_fn)
        gen_end_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
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

        api = apigw.RestApi(
            self,
            "LehighApiGw",
            rest_api_name="LehighApiGw",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                allow_credentials=True,
                status_code=200,
            ),
        )

        test_resource = api.root.add_resource("test")
        test_resource.add_method("GET", apigw.LambdaIntegration(test_fn))

        new_resource = api.root.add_resource("new")
        new_resource.add_method(
            "POST",
            apigw.LambdaIntegration(new_chapter_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO,
        )

        gen_intro_resource = api.root.add_resource("gen-intro")
        gen_intro_resource.add_method(
            "POST",
            apigw.LambdaIntegration(gen_intro_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO,
        )

        get_intro_resource = api.root.add_resource("get-intro")
        get_intro_resource.add_method(
            "GET",
            apigw.LambdaIntegration(get_intro_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO,
        )

        questions_resource = api.root.add_resource("questions")
        questions_resource.add_method(
            "POST",
            apigw.LambdaIntegration(gen_questions_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO,
        )
        questions_resource.add_method(
            "GET",
            apigw.LambdaIntegration(get_questions_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        end_resource = api.root.add_resource("end")
        end_resource.add_method(
            "POST",
            apigw.LambdaIntegration(gen_end_fn),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO,
        )

        test_dyndb_resource = api.root.add_resource("testdyndb")
        test_dyndb_resource.add_method("POST", apigw.LambdaIntegration(test_dyndb_fn))

        test_bedrock_resource = api.root.add_resource("testbdrk")
        test_bedrock_resource.add_method(
            "GET", apigw.LambdaIntegration(test_bedrock_fn)
        )
