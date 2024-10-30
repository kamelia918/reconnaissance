import psutil
import platform
import customtkinter

def get_cpu_info():
    cpu_brand = platform.processor()
    logical_cpus = psutil.cpu_count(logical=True)
    physical_cpus = psutil.cpu_count(logical=False)
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    cpu_times = psutil.cpu_times()
    cpu_load_avg = psutil.getloadavg()

    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            process_info = process.info
            processes.append({
                "PID": process_info['pid'],
                "Name": process_info['name'],
                "CPU (%)": process_info['cpu_percent'],
                "Memory (MB)": process_info['memory_info'].rss / (1024 ** 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "CPU Brand": cpu_brand,
        "Logical CPUs": logical_cpus,
        "Physical CPUs": physical_cpus,
        "Overall CPU Usage (%)": cpu_usage,
        "CPU Usage per Core (%)": cpu_usage_per_core,
        "Current Frequency (MHz)": cpu_freq.current,
        "Minimum Frequency (MHz)": cpu_freq.min,
        "Maximum Frequency (MHz)": cpu_freq.max,
        "User Time": cpu_times.user,
        "System Time": cpu_times.system,
        "Idle Time": cpu_times.idle,
        "Load Average (1, 5, 15 min)": cpu_load_avg,
        "Processes": processes,
    }


def display_system_cpu_info_f3(frame):
    info = get_cpu_info()

    # Title for CPU Information
    title_label = customtkinter.CTkLabel(
        master=frame,
        text="CPU Information",
        font=("Arial", 16, "bold"),
        text_color="black"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Display each piece of CPU information except "Processes"
    row = 1
    for key, value in info.items():
        if key != "Processes":
            label_key = customtkinter.CTkLabel(master=frame, text=f"{key}:", font=("Arial", 12, "bold"),text_color="black")
            label_key.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            label_value = customtkinter.CTkLabel(master=frame, text=value, font=("Arial", 12),text_color="black")
            label_value.grid(row=row, column=1, sticky="w", padx=10, pady=5)

            row += 1

    # Title for Process Table
    process_title = customtkinter.CTkLabel(
        master=frame,
        text="Running Processes",
        font=("Arial", 14, "bold"),
        text_color="black"
    )
    process_title.grid(row=row, column=0, columnspan=2, pady=(20, 10))

    # Create a scrollable frame for processes
    process_canvas = customtkinter.CTkCanvas(frame, width=600, height=200)
    scrollbar = customtkinter.CTkScrollbar(frame, orientation="vertical", command=process_canvas.yview)
    scrollable_frame = customtkinter.CTkFrame(process_canvas)

    # Configure canvas and scrollbar
    process_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    process_canvas.configure(yscrollcommand=scrollbar.set)
    process_canvas.grid(row=row + 1, column=0, columnspan=2, sticky="nsew", padx=(10, 0), pady=(10, 0))
    scrollbar.grid(row=row + 1, column=2, sticky="ns", pady=(10, 0))

    # Header for process table
    headers = ["PID", "Name", "CPU (%)", "Memory (MB)"]
    for col, header in enumerate(headers):
        header_label = customtkinter.CTkLabel(
            master=scrollable_frame,
            text=header,
            font=("Arial", 12, "bold"),
            text_color="black",
            anchor="w"
        )
        header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

    # Display each process in a new row within the scrollable frame
    for row_idx, process in enumerate(info["Processes"], start=1):
        values = [
            process["PID"],
            process["Name"],
            f"{process['CPU (%)']:.2f} %",
            f"{process['Memory (MB)']:.2f} MB"
        ]
        
        for col_idx, value in enumerate(values):
            value_label = customtkinter.CTkLabel(
                master=scrollable_frame,
                text=value,
                font=("Arial", 12),
                text_color="black"
            )
            value_label.grid(row=row_idx, column=col_idx, padx=10, pady=5, sticky="w")

    # Update the scroll region
    scrollable_frame.update_idletasks()
    process_canvas.config(scrollregion=process_canvas.bbox("all"))
