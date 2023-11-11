from typing import Any, Text
from numpy import real
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.predict import Predict
from loguru import logger

predict = Predict()


class ActionClosestTo(Action):
    def name(self) -> Text:
        return "action_get_closest_to"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[Text, Any]) -> list[dict[Text, Any]]:
        target_name = str(tracker.get_slot("target_name"))
        # count = tracker.get_slot("count")
        count = 5

        try:
            count = int(count)
        except ValueError:
            dispatcher.utter_message("Неправильный формат:(")

        found_name = "Call of Duty"
        try:
            found_name = predict.find_name(target_name)
        except Exception:
            dispatcher.utter_message("Такую игру я не знаю:(")
            return []

        predictions = list(predict.recomend(found_name, top=count))

        message = "Похожие игры:\n"
        for prediction in predictions:
            message += f"{prediction.v}\n"
        dispatcher.utter_message(message)

        return []
