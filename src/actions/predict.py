from dataclasses import dataclass
import pickle
from pathlib import Path
import pandas as pd
from difflib import get_close_matches
from typing import Generator
import numpy as np
from sklearn import preprocessing
from loguru import logger
import enum


class Algoritms(str, enum.Enum):
    KNN = "KNN"
    COS_SIM = "COS_SIM"


@dataclass
class PredictValue:
    v: str
    conf: float


@dataclass
class Predict:
    def __post_init__(self) -> None:
        self.data = Path("data")
        dataset_path = self.data / "vgsales.csv"

        with open(self.data / "cos_sim.pkl", "rb") as f:
            self.cos_sim = pickle.load(f)

        with open(self.data / "knn.pkl", "rb") as f:
            self.knn = pickle.load(f)

        df = pd.read_csv(dataset_path)
        df = df[df["Year"].notna()]

        self.df = df
        self.df_processed = self.df_preprocess(df)
        self._names: list[str] = list(df["Name"].unique())
        self.algoritm = Algoritms.KNN

    def recomend_cos(self, target_name: str, top: int = 10) -> Generator[PredictValue, None, None]:
        idx = self.df[self.df["Name"] == target_name].index[0]
        score_series = pd.Series(self.cos_sim[idx]).sort_values(ascending=False)

        top = top + 1
        top_indexes = list(score_series.iloc[1:top].index)

        for i in top_indexes:
            yield PredictValue(v=self.df["Name"].iloc[i], conf=score_series[i])

    def df_preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_processed = pd.get_dummies(df, columns=["Platform", "Genre", "Publisher"])
        df_processed = df_processed.drop(columns=["Name", "Rank"])
        df_processed = df_processed.drop(columns=["Other_Sales", "JP_Sales", "EU_Sales", "NA_Sales"])

        x = df_processed.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df_processed = pd.DataFrame(x_scaled)

        return df_processed

    def recomend_knn(self, target_name: str, top: int = 10) -> Generator[PredictValue, None, None]:
        target_idx = self.df[self.df["Name"] == target_name].index[0]
        row = self.df_processed.iloc[target_idx]

        distances, idxs = self.knn.kneighbors([row], top + 1, return_distance=True)
        distances, idxs = distances[0], idxs[0]

        for i, idx in enumerate(idxs):
            yield PredictValue(v=self.df["Name"].iloc[idx], conf=distances[i])

    def recommend(self, target_name: str, count: int = 10) -> list[PredictValue]:
        if self.algoritm == Algoritms.COS_SIM:
            result = self.recomend_cos(target_name, count)
        else:
            result = self.recomend_knn(target_name, count)
        result = list(result)

        logger.debug(
            "recommendation done: target_name: {}, count: {}, algoritm: {}, result: {}",
            target_name,
            count,
            self.algoritm,
            result,
        )
        return result

    def find_names(self, name: str, count: int = 5) -> list[str]:
        names = get_close_matches(name, self._names, n=count)

        logger.debug("names found: name: {}, count: {}, found_names: {}", name, count, names)
        return names

    def best_from(self, count: int, field: str, name: str) -> list[str]:
        return list(self.df[self.df[field] == name].sort_values(by="Global_Sales", ascending=False).Name[:count])

    def find_name(self, name: str) -> str:
        found_names = self.find_names(name, count=1)
        if len(found_names) == 0:
            raise KeyError(f"Name not found: {name}")
        return found_names[0]
