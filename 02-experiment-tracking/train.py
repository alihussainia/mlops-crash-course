import os
import pickle
import click
import mlflow
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-taxi-experiment")

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run():
        mlflow.set_tag("developer","muhammad ali")
        mlflow.log_param("train-data-path",data_path)

        max_depth=10
        random_state=0
        mlflow.log_param("max_depth",max_depth)
        mlflow.log_param("random_state",random_state)

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        mlflow.log_param("min_samples_split", rf.min_samples_split)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse",rmse)

        with open("models/rf.bin","wb") as f_out:
            pickle.dump(rf, f_out)
        
        mlflow.log_artifact(local_path="models/rf.bin", artifact_path="artifacts")



if __name__ == '__main__':
    run_train()
