from dataclasses import dataclass
import pickle
from pathlib import Path
import pandas as pd
from difflib import get_close_matches
from typing import Generator
import numpy as np


@dataclass
class Predict:
    def __post_init__(self) -> None:
        self.data = Path("data")
        dataset_path = self.data / "vgsales.csv"

        self.cos_sim = self.load_cos_sim()

        df = pd.read_csv(dataset_path)
        df = df[df["Year"].notna()]

        self.df = df
        self._names: list[str] = list(df["Name"].unique())

    def load_cos_sim(self) -> np.ndarray:
        with open(self.data / "cos_sim.pkl", "rb") as f:
            cos_sim = pickle.load(f)
        return cos_sim

    def recomend_cos(self, target_name: str, top: int = 10) -> Generator[tuple[str, float], None, None]:
        idx = self.df[self.df["Name"] == target_name].index[0]
        score_series = pd.Series(self.cos_sim[idx]).sort_values(ascending=False)

        top = top + 1
        top_indexes = list(score_series.iloc[1:top].index)

        for i in top_indexes:
            yield self.df["Name"].iloc[i], score_series[i]

    def find_names(self, name: str, count: int = 5) -> list[str]:
        return get_close_matches(name, self._names, n=count)

    def best_from(self, count: int, field: str, name: str) -> list[str]:
        return list(self.df[self.df[field] == name].sort_values(by="Global_Sales", ascending=False).Name[:count])

    def find_name(self, name: str) -> str:
        found_names = self.find_names(name, count=1)
        if len(found_names) == 0:
            raise KeyError(f"Name not found: {name}")
        return found_names[0]
