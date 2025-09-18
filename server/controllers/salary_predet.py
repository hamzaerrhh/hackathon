import pandas as pd
import pickle


def load_model(path: str):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"❌ Model file not found at: {path}")
        return None
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        return None

def prepare_input(data: dict, model):
    """Prepare input dict into the same format used for training."""
    input_df = pd.DataFrame([data])

    expected_location_cols = [
        "location_match_local",
        "location_match_relocate",
        "location_match_remoteok",
        "location_match_unknown",
    ]

    # Ensure location columns exist with zeros
    for col in expected_location_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    if "location_match" in input_df.columns:
        raw_loc = str(input_df.loc[0, "location_match"]).lower()
        if "local" in raw_loc:
            input_df.loc[0, "location_match_local"] = 1
        elif "relocat" in raw_loc:
            input_df.loc[0, "location_match_relocate"] = 1
        elif "remote" in raw_loc:
            input_df.loc[0, "location_match_remoteok"] = 1
        else:
            input_df.loc[0, "location_match_unknown"] = 1
        input_df = input_df.drop(columns=["location_match"])

    # Align with model’s expected features
    expected_cols = getattr(model, "feature_names_in_", None)
    if expected_cols is not None:
        for col in expected_cols:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df.reindex(columns=expected_cols, fill_value=0)

    return input_df


def predict(model_path: str, data: dict):
    """Load model, prepare input and return prediction."""
    model = load_model(model_path)
    if model is None:
        raise FileNotFoundError(f"Model not found at {model_path}")

    input_df = prepare_input(data, model)

    try:
        prediction = model.predict(input_df)
        return prediction[0] if hasattr(prediction, "__getitem__") else prediction
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")
