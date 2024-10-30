import platform
import psutil
import socket
import urllib.request
import uuid
import customtkinter


def get_memory_info_f2():
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = ram.used / (1024 ** 3)
    ram_percent = ram.percent

    partitions = psutil.disk_partitions()
    storage_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        partition_type = "SSD" if "SSD" in partition.fstype else "HDD"
        storage_info.append({
            "Device": partition.device,
            "Total": f"{usage.total / (1024 ** 3):.2f} Go",
            "Used": f"{usage.used / (1024 ** 3):.2f} Go",
            "Free": f"{usage.free / (1024 ** 3):.2f} Go",
            "Type": partition_type
        })

    return {
        "RAM Total": f"{ram_total:.2f} Go",
        "RAM Used": f"{ram_used:.2f} Go ({ram_percent}%)",
        "Storage": storage_info
    }


def display_memory_info_f2(frame):
    # Title label for memory info
    memory_title_label = customtkinter.CTkLabel(
        master=frame,
        text="Taille de Mémoire",
        font=("Arial", 16, "bold"),
        text_color="black"
    )
    memory_title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Retrieve memory information
    memory_info = get_memory_info_f2()
    
    # Display RAM Total and RAM Used
    ram_total_label = customtkinter.CTkLabel(
        master=frame,
        text="RAM Total:",
        font=("Arial", 12, "bold"),
        text_color="black"
    )
    ram_total_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
    ram_total_value = customtkinter.CTkLabel(
        master=frame,
        text=memory_info["RAM Total"],
        font=("Arial", 12),
        text_color="black"
    )
    ram_total_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    ram_used_label = customtkinter.CTkLabel(
        master=frame,
        text="RAM Used:",
        font=("Arial", 12, "bold"),
        text_color="black"
    )
    ram_used_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    
    ram_used_value = customtkinter.CTkLabel(
        master=frame,
        text=memory_info["RAM Used"],
        font=("Arial", 12),
        text_color="black"
    )
    ram_used_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    # Title label for storage info
    storage_title_label = customtkinter.CTkLabel(
        master=frame,
        text="Storage Information",
        font=("Arial", 16, "bold"),
        text_color="black"
    )
    storage_title_label.grid(row=3, column=0, columnspan=5, pady=(20, 10))

    # Define column headers with bold styling
    headers = ["Device", "Total", "Used", "Free", "Type"]
    for col, header in enumerate(headers):
        header_label = customtkinter.CTkLabel(
            master=frame,
            text=header,
            font=("Arial", 12, "bold"),
            text_color="black",
            anchor="w"
        )
        header_label.grid(row=4, column=col, padx=10, pady=5, sticky="w")

    storage_info = memory_info["Storage"]  # Extract storage information

    # Display each storage device as a row
    for row_idx, storage in enumerate(storage_info, start=5):
        # For each attribute in the storage dictionary, create a label and place it in the grid
        values = [
            storage["Device"],
            storage["Total"],
            storage["Used"],
            storage["Free"],
            storage["Type"]
        ]
        
        for col_idx, value in enumerate(values):
            value_label = customtkinter.CTkLabel(
                master=frame,
                text=value,
                font=("Arial", 12),
                text_color="black"
            )
            value_label.grid(row=row_idx, column=col_idx, padx=10, pady=5, sticky="w")
