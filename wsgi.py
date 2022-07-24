from app import app
from machine_learning.training import training

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = training()
    app.run(host="0.0.0.0", port=9000, use_reloader=True)