import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

from common.auth.credential_loader import AzureEnvLoader

# Get credentials from environment variables
loader = AzureEnvLoader()

def main():
    try:
        # Get Configuration Settings
        ai_endpoint = os.getenv('QNA_AZURE_LANGUAGE_RESOURCE_ENDPOINT')
        ai_key = os.getenv('QNA_AZURE_LANGUAGE_RESOURCE_KEY')
        ai_project_name = os.getenv('QNA_AZURE_LANGUAGE_SERVICE_PROJECT_NAME')
        ai_deployment_name = os.getenv('QNA_AZURE_LANGUAGE_SERVICE_KNOWLEDGE_BASE_DEPLOYMENT_NAME')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

        # Submit a question and display the answer
        user_question = ''
        while True:
            user_question = input('\nQuestion:\n')
            if user_question.lower() == "quit":                
                break
            response = ai_client.get_answers(question=user_question,
                                            project_name=ai_project_name,
                                            deployment_name=ai_deployment_name)
            for candidate in response.answers:
                print(candidate.answer)
                print("Confidence: {}".format(candidate.confidence))
                print("Source: {}".format(candidate.source))

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
