"""
Reproducible ML Evaluation Script for IntelliICU.

Evaluates the production RandomForestClassifier against an explicitly
provided labeled CSV dataset without fabricating metrics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from app.ai.feature_builder import FEATURE_ORDER
from app.ai.model_loader import MODEL
from app.ai.predictor import Predictor


def evaluate(dataset_path: Path, target_col: str = "sepsis_label") -> dict:
    df = pd.read_csv(dataset_path)
    missing_cols = [c for c in [*FEATURE_ORDER, target_col] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset missing required columns: {missing_cols}")

    X = df[FEATURE_ORDER].astype(float)
    y_true = df[target_col].astype(int)

    probs = MODEL.predict_proba(X)[:, 1]
    y_pred = (probs >= Predictor.THRESHOLD).astype(int)

    metrics = {
        "dataset": str(dataset_path),
        "samples": int(len(df)),
        "threshold": Predictor.THRESHOLD,
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, probs)), 4) if len(y_true.unique()) > 1 else None,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate IntelliICU ML model on a labeled CSV dataset.")
    parser.add_argument("--dataset", required=True, type=Path, help="Path to labeled evaluation CSV")
    parser.add_argument("--target", default="sepsis_label", help="Target binary column name")
    args = parser.parse_args()

    result = evaluate(args.dataset, args.target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
