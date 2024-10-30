import platform
import psutil
import socket
import urllib.request
import uuid
import customtkinter

def get_system_info_f1():
    system_version = platform.platform()
    system_name = platform.node()
    battery = psutil.sensors_battery()
    battery_percentage = battery.percent if battery else "N/A"
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    return {
        "System Version": system_version,
        "System Name": system_name,
        "Battery": f"{battery_percentage}%",
        "État de la Batterie": "Chargée" if battery.power_plugged else "Déchargée",
        "Capacité Totale (Wh)": battery.secsleft,
        "IP Address": ip_address,
        "Public ip address": external_ip,
        "MAC Address": mac_address
    }



# affichage 

# def display_system_info_f1(frame):
#     info = get_system_info_f1()
#     for idx, (key, value) in enumerate(info.items()):
#         label = customtkinter.CTkLabel(master=frame, text=f"{key}: {value}")
#         label.pack(pady=5)


# def display_system_info_f1(frame):
#     # Title label with a bold font
#     title_label = customtkinter.CTkLabel(
#         master=frame,
#         text="General Information",
#         font=("Arial", 16, "bold"),
#         text_color="black"
#     )
#     title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

#     info = get_system_info_f1()

#     # Loop to display keys and values with distinct font styles
#     for idx, (key, value) in enumerate(info.items(), start=1):  # Start at 1 to avoid title row
#         # Key label (bold and dark)
#         key_label = customtkinter.CTkLabel(
#             master=frame,
#             text=f"{key}:",
#             font=("Arial", 12, "bold"),
#             text_color="black"
#         )
#         key_label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

#         # Value label (semi-bold)
#         value_label = customtkinter.CTkLabel(
#             master=frame,
#             text=f"{value}",
#             font=("Arial", 12, "normal"),
#             text_color="black"
#         )
#         value_label.grid(row=idx, column=1, sticky="w", padx=10, pady=5)



# import customtkinter

# def display_system_info_f1(frame):
#     # Title label with a bold font
#     title_label = customtkinter.CTkLabel(
#         master=frame,
#         text="General Information",
#         font=("Arial", 16, "bold"),
#         text_color="black"
#     )
#     title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

#     info = get_system_info_f1()

#     # Dropdown for system names
#     system_names = ["Local", "System B", "System C"]  # Replace with your actual system names
#     selected_system = customtkinter.StringVar(value=system_names[0])  # Default value

#     system_dropdown = customtkinter.CTkOptionMenu(
#         master=frame,
#         variable=selected_system,
#         values=system_names,
#         command=lambda x: print(f"Selected system: {x}")  # Replace with your logic to switch systems
#     )
#     system_dropdown.grid(row=1, column=0, columnspan=2, pady=(10, 20))

#     # Loop to display keys and values with distinct font styles
#     for idx, (key, value) in enumerate(info.items(), start=2):  # Start at 2 to account for the title and dropdown
#         # Key label (bold and dark)
#         key_label = customtkinter.CTkLabel(
#             master=frame,
#             text=f"{key}:",
#             font=("Arial", 12, "bold"),
#             text_color="black"
#         )
#         key_label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

#         # Value label (semi-bold)
#         value_label = customtkinter.CTkLabel(
#             master=frame,
#             text=f"{value}",
#             font=("Arial", 12, "normal"),
#             text_color="black"
#         )
#         value_label.grid(row=idx, column=1, sticky="w", padx=10, pady=5)



import tkinter
import customtkinter

def display_system_info_f1(frame):
    # Title label with a bold font
    title_label = customtkinter.CTkLabel(
        master=frame,
        text="General Information",
        font=("Arial", 16, "bold"),
        text_color="black"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Dropdown for system names
    system_names = ["Local", "System B", "System C"]  # Replace with your actual system names
    selected_system = customtkinter.StringVar(value=system_names[0])  # Default value

    # Create a frame to hold the dropdown and the refresh button
    dropdown_refresh_frame = tkinter.Frame(frame, bg="gray")
    dropdown_refresh_frame.grid(row=1, column=0, columnspan=2, pady=(10, 20))

    # System dropdown menu
    system_dropdown = customtkinter.CTkOptionMenu(
        master=dropdown_refresh_frame,
        variable=selected_system,
        values=system_names,
        command=lambda x: print(f"Selected system: {x}")  # Replace with your logic to switch systems
    )
    system_dropdown.grid(row=0, column=0, padx=5)

    # Refresh button
    refresh_button = customtkinter.CTkButton(
        master=dropdown_refresh_frame,
        text="Refresh",
        command=lambda: refresh_info(frame)  # Call the refresh function
    )
    refresh_button.grid(row=0, column=1, padx=5)

    # Display system info
    display_info_labels(frame, start_row=2)

def refresh_info(frame):
    """Clears and updates the displayed system information."""
    # Clear current labels (if any)
    for widget in frame.grid_slaves():
        if int(widget.grid_info()["row"]) >= 2:  # Keep title and dropdown row intact
            widget.destroy()
    # Display updated information
    display_info_labels(frame, start_row=2)

def display_info_labels(frame, start_row):
    """Helper function to display system information labels."""
    info = get_system_info_f1()
    for idx, (key, value) in enumerate(info.items(), start=start_row):
        key_label = customtkinter.CTkLabel(
            master=frame,
            text=f"{key}:",
            font=("Arial", 12, "bold"),
            text_color="black"
        )
        key_label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

        value_label = customtkinter.CTkLabel(
            master=frame,
            text=f"{value}",
            font=("Arial", 12, "normal"),
            text_color="black"
        )
        value_label.grid(row=idx, column=1, sticky="w", padx=10, pady=5)
