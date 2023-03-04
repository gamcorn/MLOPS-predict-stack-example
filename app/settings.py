from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_APP_PATH: str = "/volume/p7svr"
    LOGGED_MODEL: str = "app/models/PlainRegression_Model"
    MLFLOW_URL: str = "http://localhost:8968"
    PREDICTION_ENDPOINT: str = "http://localhost:8080/make_prediction"
    AUTH_FILE_PATH: str = "auth_config.yaml"


conf = Settings()
