import pytest
from actions.predict import Predict, Algoritms


@pytest.fixture(scope="class")
def predict() -> Predict:
    return Predict()


class TestPredict:
    def test_find_name_ok(self, predict: Predict):
        assert "Call of Duty: Ghosts" == predict.find_name("Call of Duty")

    def test_find_names_ok(self, predict: Predict):
        print(predict.find_names("Need for speed", count=5))

        assert {
            "Need for Speed Underground",
            "Need for Speed Underground 2",
            "Need for Speed: Most Wanted",
            "Need for Speed: Hot Pursuit",
            "Need for Speed: Shift",
        } == set(predict.find_names("Need for speed", count=5))

    def test_recomend_cos_ok(self, predict: Predict):
        predict.algoritm = Algoritms.COS_SIM
        predict.recommend("Need for Speed Carbon", count=5)
        predict.recommend("Call of Duty: Black Ops", count=5)

    def test_recomend_knn_ok(self, predict: Predict):
        predict.algoritm = Algoritms.KNN
        predict.recommend("Need for Speed Carbon", count=5)
        predict.recommend("Call of Duty: Black Ops", count=5)

    def test_best_from_pablisher_ok(self, predict: Predict):
        assert {"Call of Duty: Modern Warfare 3", "Call of Duty: Black Ops"} == set(
            predict.best_from(count=2, field="Publisher", name="Activision")
        )

    def test_best_from_genre_ok(self, predict: Predict):
        assert {"Pokemon Stadium", "Warzone 2100"} == set(predict.best_from(count=2, field="Genre", name="Strategy"))
