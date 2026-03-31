"""
eval/datasets/mtsamples.py
MTSamples interim benchmark loader.
Provides identical interface to the future MIMIC-III loader —
eval/runner.py never needs to know which dataset it is running on.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ClinicalNote:
    note_id: str
    specialty: str
    description:str
    transcription: str
    sample_name: str

def load_mtsamples(
    csv_path: str | Path ="data/mtsamples/mtsamples.csv",
    specialities: list[str] | None = None, 
    max_notes: int | None = None,
) -> list[ClinicalNote]:  
    """
    Load MTSamples clinical notes with optional specialty filter. 
    Returns List[ClinicalNote] not DataFrame - keeps loader interface 
    identical to the future MIMIC-III loader.
    """

    df = pd.read_csv(csv_path).dropna(subset=["transcription"])

    if specialities:
        df = df[df["medical_specialty"].isin(specialities)]

    if max_notes:
        df = df.head(max_notes)

    return [
        ClinicalNote(
            note_id=str(row["Unnamed: 0"]),
            specialty=str(row["medical_specialty"]).strip(),
            description=str(row["description"]).strip(),
            transcription=str(row["transcription"]).strip(),
            sample_name=str(row["sample_name"]).strip(),
        )
        for _,row in df.iterrows()
    ]

def iter_notes(
    csv_path: str | Path = "data/mtsamples/mtsamples.csv",
    batch_size: int = 20,
) -> Iterator[list[ClinicalNote]]:
    """
    Yield notes in batches for memory-efficient eval runs.    

    Args:
        csv_path (str | Path, optional): _description_. Defaults to "data/mtsamples/mtsamples.csv".
        batch_size (int, optional): _description_. Defaults to 20.

    Yields:
        Iterator[list[ClinicalNote]]: _description_
    """
    notes = load_mtsamples(csv_path)
    for i in range(0, len(notes), batch_size):
        yield notes[i: i+batch_size]

if __name__ =="__main__":
    notes = load_mtsamples(max_notes=5)
    for n in notes:
        print(f"[{n.note_id}] {n.specialty} - {n.sample_name}")
        print(f" {n.transcription[:120]}...")
        print()

