import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox

FILE = "simulation_results.csv"


# ================= LOAD DATA =================
def load_dataset():
    try:
        data = pd.read_csv(FILE)
        return data
    except:
        messagebox.showerror("Error", "Run some simulations first!")
        return None


# ================= VISUALIZATION =================
def visualize_data():
    data = load_dataset()
    if data is None:
        return

    plt.figure(figsize=(8,5))
    plt.scatter(data["Avg_WT"], data["CPU_Util"])
    plt.xlabel("Average Waiting Time")
    plt.ylabel("CPU Utilization")
    plt.title("CPU Utilization vs Waiting Time")
    plt.grid(True)
    plt.show()


# ================= MACHINE LEARNING =================
def train_model():
    data = load_dataset()
    if data is None:
        return

    # Convert Algorithm names to numbers
    le = LabelEncoder()
    data["Algorithm"] = le.fit_transform(data["Algorithm"])

    X = data[["Avg_WT","Avg_TAT","Avg_RT","Throughput","CPU_Util"]]
    y = data["Algorithm"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)

    messagebox.showinfo("Model Trained",
                        f"Prediction Accuracy: {acc*100:.2f}%")

    return model, le


# ================= PREDICT BEST ALGORITHM =================
def predict_best():
    result = train_model()
    if result is None:
        return

    model, le = result

    # Sample test case
    sample = [[5, 10, 3, 0.4, 80]]

    pred = model.predict(sample)
    algo = le.inverse_transform(pred)

    messagebox.showinfo("Best Algorithm Prediction",
                        f"Recommended Algorithm: {algo[0]}")
