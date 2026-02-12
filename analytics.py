import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os

# file name
RESULT_FILE = "simulation_results.csv"

# ================= SAVE EXPERIMENT =================
def save_experiment(algo, avg_wt, avg_tat, avg_rt, th, cpu):

    file_exists = os.path.isfile(RESULT_FILE)

    with open(RESULT_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Algorithm","Avg_WT","Avg_TAT","Avg_RT","Throughput","CPU_Util"
        ])
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Algorithm": algo,
            "Avg_WT": avg_wt,
            "Avg_TAT": avg_tat,
            "Avg_RT": avg_rt,
            "Throughput": th,
            "CPU_Util": cpu
        })


# ================= LOAD DATA =================
def load_data():
    data = []

    if not os.path.exists(RESULT_FILE):
        return data

    with open(RESULT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    return data


# ================= DASHBOARD =================
def show_analytics():

    data = load_data()

    if not data:
        messagebox.showinfo("No Data", "Run simulations first!")
        return

    algos = [d["Algorithm"] for d in data]
    wt = [float(d["Avg_WT"]) for d in data]
    tat = [float(d["Avg_TAT"]) for d in data]
    cpu = [float(d["CPU_Util"]) for d in data]

    win = tk.Toplevel()
    win.title("Scheduler Analytics Dashboard")
    win.geometry("900x600")

    fig, ax = plt.subplots(figsize=(9,5))

    ax.plot(algos, wt, marker='o', label="Waiting Time")
    ax.plot(algos, tat, marker='s', label="Turnaround Time")
    ax.plot(algos, cpu, marker='^', label="CPU Utilization")

    ax.set_title("CPU Scheduling Algorithm Comparison")
    ax.set_xlabel("Algorithms")
    ax.set_ylabel("Metrics")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
