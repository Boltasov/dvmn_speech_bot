import json
import dotenv
import os
import argparse

from google.cloud import dialogflow


def get_train_phrases(filepath):
    with open(filepath, "r", encoding="UTF-8") as train_file:
        phrases_json = train_file.read()

    phrases = json.loads(phrases_json)

    return phrases


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='TrainDialogFlow',
        description='Учит DialogFlow фразам из заданного файла',
    )
    parser.add_argument("--filepath", help='Путь к файлу, откуда взять учебные фразы', type=str, required=True)
    args = parser.parse_args()

    filepath = args.filepath
    phrases = get_train_phrases(filepath)

    dotenv.load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    for phrase, training_values in phrases.items():
        display_name = phrase
        training_phrases_parts = training_values.get("questions")
        message_texts = training_values.get("answer")
        create_intent(project_id, display_name, training_phrases_parts, message_texts)
