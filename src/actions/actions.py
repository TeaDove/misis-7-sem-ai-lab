from typing import Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.predict import Predict

predict = Predict()


class ActionClosestTo(Action):
    def name(self) -> Text:
        return "action_get_closest_to"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[Text, Any]) -> list[dict[Text, Any]]:
        target_name = tracker.get_slot("target_name")
        # count = tracker.get_slot("count")
        count = 5

        if not isinstance(target_name, str):
            dispatcher.utter_message("Неправильный формат:(")

        try:
            count = int(count)
        except ValueError:
            dispatcher.utter_message("Неправильный формат:(")

        try:
            real_name = predict.find_name(target_name)
        except KeyError:
            dispatcher.utter_message("Такую игру я не знаю:(")

        predictions = predict.recomend_cos(real_name, top=count)

        message = "Похожие игры:\n"
        for prediction in predictions:
            message += f"{prediction[0]}\n"
        dispatcher.utter_message(message)

        return []
