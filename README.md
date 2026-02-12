# Multicore CPU Scheduling Simulator

## 📌 Project Description

The **Multicore CPU Scheduling Simulator** is a Python-based simulation tool developed to demonstrate and analyze how operating systems schedule processes across multiple CPU cores.
The simulator allows users to input processes and observe how different scheduling algorithms affect system performance.

This project also stores execution results and performs Machine Learning analysis to predict efficient scheduling behavior.

---

## 🎯 Objectives

* Simulate real CPU process scheduling
* Compare different scheduling algorithms
* Calculate performance metrics
* Visualize execution results
* Apply Machine Learning for performance prediction

---

## ⚙️ Features

* Supports **2 or 4 CPU cores**
* User process input (Arrival Time, Burst Time, Priority)
* Multiple scheduling algorithms
* Performance calculation
* Graphical visualization
* CSV result storage
* ML prediction module

---

## 🧠 Scheduling Algorithms Implemented

* FCFS (First Come First Serve)
* SJF (Shortest Job First - Non Preemptive)
* Round Robin (Time Quantum Based)
* Priority Scheduling

---

## 📊 Performance Metrics

The simulator calculates:

* Waiting Time
* Turnaround Time
* Throughput
* CPU Utilization

---

## 🤖 Machine Learning Module

The system stores simulation outputs as a dataset (`simulation_results.csv`) and uses ML algorithms to:

* Analyze performance
* Predict best scheduling algorithm

---

## 🛠️ Technologies Used

* Python 3
* Tkinter (GUI)
* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* Seaborn

---

## 📂 Project Structure

```
AOS_PROJECT/
│── MAIN.py
│── analytics.py
│── ml_analysis.py
│── simulation_results.csv
│── requirements.txt
```

---

## 💻 Installation

### Step 1: Clone Repository

```
git clone https://github.com/Ykalaiselvi/Multicore-CPU-Scheduling-Simulator.git
cd Multicore-CPU-Scheduling-Simulator
```

### Step 2: Install Dependencies

```
pip install -r requirements.txt
```

### Step 3: Run Project

```
python MAIN.py
```

---

## 📷 Output

The simulator displays:

* Scheduling execution
* Graph visualization
* Performance comparison charts

---

## 📌 Applications

* Operating System learning
* Educational demonstrations
* Algorithm performance comparison
* Research & academic projects

---

## 👩‍💻 Author

**Kalaiselvi Y**
M.E. Computer Science and Engineering (AL & ML) Project

---

## 📄 License

This project is developed for educational purposes.
