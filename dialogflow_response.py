import dotenv
import os

from google.cloud import dialogflow


def dialogflow_response(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback


if __name__ == "__main__":
    dotenv.load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    session_id = 1
    text = 'Hello'
    language_code = 'ru-RU'
    dialogflow_response(project_id, session_id, text, language_code)
