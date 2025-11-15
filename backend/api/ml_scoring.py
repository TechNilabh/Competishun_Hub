import pandas as pd
import os
from django.conf import settings

def evaluate_submission(upload_file):
    submission = pd.read_csv(upload_file)

    truth_path = os.path.join(settings.BASE_DIR, "api", "original.csv")
    truth = pd.read_csv(truth_path)

    mse = ((submission["target"] - truth["target"]) ** 2).mean()
    score = 1 / (1 + mse)

    return score
