import tkinter as tk
from tkinter import ttk, messagebox
import random
import analytics
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ml_analysis

# ===================== LOGIN CREDENTIALS =====================
VALID_USER = "admin"
VALID_PASS = "1234"

# ===================== UTIL =====================
def random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# ===================== SCHEDULING ALGORITHMS =====================
def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    gantt = []
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        p['start'] = time
        p['response'] = p['start'] - p['arrival']
        p['waiting'] = time - p['arrival']
        time += p['burst']
        p['completion'] = time
        p['turnaround'] = p['completion'] - p['arrival']
        gantt.append((p, p['start'], p['burst']))
    return processes, gantt

def sjf(processes):
    time = 0
    completed, ready = [], []
    processes.sort(key=lambda x: x['arrival'])
    gantt = []
    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['burst'])
            p = ready.pop(0)
            p['start'] = time
            p['response'] = p['start'] - p['arrival']
            p['waiting'] = time - p['arrival']
            time += p['burst']
            p['completion'] = time
            p['turnaround'] = p['completion'] - p['arrival']
            completed.append(p)
            gantt.append((p, p['start'], p['burst']))
        else:
            time += 1
    return completed, gantt

def priority_sched(processes):
    time = 0
    completed, ready = [], []
    processes.sort(key=lambda x: x['arrival'])
    gantt = []
    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['priority'])
            p = ready.pop(0)
            p['start'] = time
            p['response'] = p['start'] - p['arrival']
            p['waiting'] = time - p['arrival']
            time += p['burst']
            p['completion'] = time
            p['turnaround'] = p['completion'] - p['arrival']
            completed.append(p)
            gantt.append((p, p['start'], p['burst']))
        else:
            time += 1
    return completed, gantt

def round_robin(processes, tq):
    queue = deque()
    processes.sort(key=lambda x: x['arrival'])
    remaining = {p['id']: p['burst'] for p in processes}
    gantt = []
    time, i = 0, 0   
    started = set()

    while i < len(processes) or queue:
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i])
            i += 1
        if queue:
            p = queue.popleft()
            if p['id'] not in started:
                p['start'] = time
                p['response'] = p['start'] - p['arrival']
                started.add(p['id'])

            run = min(tq, remaining[p['id']])
            gantt.append((p, time, run))
            time += run
            remaining[p['id']] -= run
            while i < len(processes) and processes[i]['arrival'] <= time:
                queue.append(processes[i])
                i += 1
            if remaining[p['id']] > 0:
                queue.append(p)
            else:
                p['completion'] = time
                p['turnaround'] = p['completion'] - p['arrival']
                p['waiting'] = p['turnaround'] - p['burst']
        else:
            time += 1
    return processes, gantt

# ===================== METRICS =====================
def calculate_metrics(processes, total_time, cores):
    avg_wt = sum(p['waiting'] for p in processes)/len(processes)
    avg_tat = sum(p['turnaround'] for p in processes)/len(processes)
    avg_rt = sum(p['response'] for p in processes) / len(processes)
    throughput = len(processes)/total_time if total_time else 0
    cpu_util = sum(p['burst'] for p in processes)/(cores*total_time)*100 if total_time else 0
    return avg_wt, avg_tat,avg_rt, throughput, cpu_util

# ===================== MAIN APPLICATION =====================
def open_main_app():
    login_window.destroy()

    global root, pid_entries, arrival_entries, burst_entries, priority_entries
    global algo_var, core_var, tq_var, chart_frame, legend_frame, metrics_label, table

    root = tk.Tk()
    root.title("🌈 Advanced Multicore CPU Scheduler")
    root.geometry("1200x650")
    root.configure(bg="#e6f2ff")

    title = tk.Label(root, text="Multicore CPU Scheduling Simulator",
                     bg="#007acc", fg="white", font=("Segoe UI",16,"bold"))
    title.pack(fill='x')

    main_frame = tk.Frame(root, bg="#e6f2ff")
    main_frame.pack(fill='both', expand=True)

    # LEFT PANEL
    left = tk.LabelFrame(main_frame, text="Process Input", bg="#f0f8ff", font=("Segoe UI",10,"bold"))
    left.pack(side='left', fill='y', padx=10, pady=10)

    pid_entries=[]; arrival_entries=[]; burst_entries=[]; priority_entries=[]
    for i in range(4):
        tk.Label(left, text=f"P{i+1}", bg="#f0f8ff").grid(row=i,column=0,padx=5,pady=5)
        pid=tk.Entry(left,width=5); pid.grid(row=i,column=1); pid_entries.append(pid)
        at=tk.Entry(left,width=5); at.grid(row=i,column=2); arrival_entries.append(at)
        bt=tk.Entry(left,width=5); bt.grid(row=i,column=3); burst_entries.append(bt)
        pr=tk.Entry(left,width=5); pr.grid(row=i,column=4); priority_entries.append(pr)

    # MIDDLE PANEL
    mid = tk.LabelFrame(main_frame, text="Scheduler Settings", bg="#f0f8ff", font=("Segoe UI",10,"bold"))
    mid.pack(side='left', fill='y', padx=10)

    algo_var = tk.StringVar()
    ttk.Combobox(mid, textvariable=algo_var, values=["FCFS","SJF","Priority","RR"]).pack(pady=5)

    core_var = tk.StringVar(value="2")
    ttk.Combobox(mid, textvariable=core_var, values=["1","2","3","4"]).pack(pady=5)

    tq_var = tk.StringVar()
    tk.Entry(mid, textvariable=tq_var).pack(pady=5)

    tk.Button(mid, text="▶ Run Simulation", bg="#28a745", fg="white",
              command=run_simulation, font=("Segoe UI",10,"bold")).pack(pady=15)
    tk.Button(mid, text="📊 Analytics Dashboard", bg="#ff9800", fg="white",
          command=analytics.show_analytics, font=("Segoe UI",10,"bold")).pack(pady=5)
    tk.Button(mid, text="🤖 ML Prediction",
          bg="#6f42c1", fg="white",
          command=ml_analysis.predict_best,
          font=("Segoe UI",10,"bold")).pack(pady=5)

    tk.Button(mid, text="📈 Visualize Dataset",
          bg="#17a2b8", fg="white",
          command=ml_analysis.visualize_data,
          font=("Segoe UI",10,"bold")).pack(pady=5)

    # RIGHT PANEL
    chart_frame = tk.LabelFrame(main_frame, text="Gantt Chart", bg="white")
    chart_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    legend_frame = tk.Frame(root, bg="#e6f2ff")
    legend_frame.pack()

    bottom = tk.LabelFrame(root, text="Performance Metrics", bg="#f0f8ff")
    bottom.pack(fill='x', padx=10, pady=5)

    metrics_label = tk.Label(bottom, text="Metrics will appear here", bg="#f0f8ff", font=("Segoe UI",10,"bold"))
    metrics_label.pack()

    table = ttk.Treeview(bottom, columns=("PID","WT","TAT","RT"), show='headings', height=5)
    for col in ("PID","WT","TAT","RT"):
        table.heading(col,text=col)
    table.pack()

    root.mainloop()

# ===================== RUN SIM =====================
def run_simulation():
    processes = []
    for i in range(4):
        try:
            processes.append({
                'id': pid_entries[i].get(),
                'arrival': int(arrival_entries[i].get()),
                'burst': int(burst_entries[i].get()),
                'priority': int(priority_entries[i].get()),
                'color': random_color()
            })
        except:
            messagebox.showerror("Error","Invalid Input")
            return

    algo = algo_var.get()
    cores = int(core_var.get())

    if algo == "FCFS":
        processes, gantt = fcfs(processes)
    elif algo == "SJF":
        processes, gantt = sjf(processes)
    elif algo == "Priority":
        processes, gantt = priority_sched(processes)
    elif algo == "RR":
        processes, gantt = round_robin(processes, int(tq_var.get()))
    else:
        return

    total_time = max(p['completion'] for p in processes)
    avg_wt, avg_tat,avg_rt, th, cpu = calculate_metrics(processes, total_time, cores)
    analytics.save_experiment(algo, avg_wt, avg_tat, avg_rt, th, cpu)

    metrics_label.config(text=f"Avg WT={avg_wt:.2f}   Avg TAT={avg_tat:.2f}  Avg RT={avg_rt:.2f}  Throughput={th:.2f}   CPU Util={cpu:.2f}%")

    for row in table.get_children():
        table.delete(row)
    for p in processes:
        table.insert('', 'end', values=(p['id'], p['waiting'], p['turnaround'], p['response']))

    draw_gantt(processes, gantt, cores)

def draw_gantt(processes, gantt, cores):
    for w in chart_frame.winfo_children():
        w.destroy()
    fig, ax = plt.subplots(figsize=(8,4))
    for i, (p, start, dur) in enumerate(gantt):
        core = i % cores
        ax.barh(core, dur, left=start, color=p['color'])
        ax.text(start + dur/2, core, p['id'], ha='center', va='center', color='white')
    ax.set_yticks(range(cores))
    ax.set_yticklabels([f'CPU {i+1}' for i in range(cores)])
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    plt.close(fig)

# ===================== LOGIN WINDOW =====================
login_window = tk.Tk()
login_window.title("Login - CPU Scheduler")
login_window.geometry("350x250")
login_window.configure(bg="#007acc")

tk.Label(login_window, text="CPU Scheduler Login", bg="#007acc",
         fg="white", font=("Segoe UI",14,"bold")).pack(pady=20)

tk.Label(login_window, text="Username", bg="#007acc", fg="white").pack()
user_entry = tk.Entry(login_window)
user_entry.pack()

tk.Label(login_window, text="Password", bg="#007acc", fg="white").pack()
pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack()

def login():
    if user_entry.get() == VALID_USER and pass_entry.get() == VALID_PASS:
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

tk.Button(login_window, text="Login", bg="#28a745", fg="white", command=login).pack(pady=15)

login_window.mainloop()
