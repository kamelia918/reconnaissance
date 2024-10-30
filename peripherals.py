# import psutil
# import subprocess
# import customtkinter

# def get_system_perif():
#     system_perif_info = {}

#     usb_devices = []
#     for device in psutil.disk_partitions(all=False):
#         if 'removable' in device.opts:
#             usb_devices.append(device.device)

#     audio_devices = []
#     network_info = psutil.net_if_addrs()
#     network_cards = {iface: addrs for iface, addrs in network_info.items()}

#     system_perif_info["Périphériques USB"] = usb_devices
#     system_perif_info["Périphériques Audio"] = audio_devices
#     system_perif_info["Cartes Réseau"] = network_cards

#     connection_type = "Inconnu"
#     for iface in psutil.net_if_stats():
#         if "Wi-Fi" in iface:
#             connection_type = "Wi-Fi"
#             break
#         elif "Ethernet" in iface:
#             connection_type = "Ethernet"

#     system_perif_info["Type de Connexion"] = connection_type

#     graphics_info = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().splitlines()
#     resolution = subprocess.check_output("wmic path win32_videocontroller get CurrentHorizontalResolution, CurrentVerticalResolution", shell=True).decode().splitlines()

#     if len(resolution) > 1:
#         res = resolution[1].strip().split()
#         if len(res) >= 2:
#             resolution_info = f"{res[0]} x {res[1]}"
#         else:
#             resolution_info = "Résolution non disponible"
#     else:
#         resolution_info = "Résolution non disponible"

#     system_perif_info["Carte Graphique"] = graphics_info[1] if len(graphics_info) > 1 else "Non disponible"
#     system_perif_info["Résolution d'Écran"] = resolution_info
#     system_perif_info["Taux de Rafraîchissement"] = "Non disponible"

#     return system_perif_info



# def display_system_perif_f4(frame):
#     info = get_system_perif()
#     for key, value in info.items():
#         if isinstance(value, list):
#             label = customtkinter.CTkLabel(master=frame, text=f"{key}: {', '.join(value) if value else 'Aucun'}")
#             label.pack(pady=5)
#         elif isinstance(value, dict):
#             label = customtkinter.CTkLabel(master=frame, text=f"{key}:")
#             label.pack(pady=5)
#             for sub_key, sub_value in value.items():
#                 sub_label = customtkinter.CTkLabel(master=frame, text=f"  {sub_key}: {sub_value}")
#                 sub_label.pack(pady=2)
#         else:
#             label = customtkinter.CTkLabel(master=frame, text=f"{key}: {value}")
#             label.pack(pady=5)



import psutil
import subprocess
import socket
import customtkinter

def get_system_perif():
    system_perif_info = {}

    usb_devices = []
    for device in psutil.disk_partitions(all=False):
        if 'removable' in device.opts:
            usb_devices.append(device.device)

    audio_devices = []
    network_info = psutil.net_if_addrs()
    network_cards = {iface: addrs for iface, addrs in network_info.items()}

    system_perif_info["Périphériques USB"] = usb_devices
    system_perif_info["Périphériques Audio"] = audio_devices
    system_perif_info["Cartes Réseau"] = network_cards

    connection_type = "Inconnu"
    for iface in psutil.net_if_stats():
        if "Wi-Fi" in iface:
            connection_type = "Wi-Fi"
            break
        elif "Ethernet" in iface:
            connection_type = "Ethernet"

    system_perif_info["Type de Connexion"] = connection_type

    graphics_info = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().splitlines()
    resolution = subprocess.check_output("wmic path win32_videocontroller get CurrentHorizontalResolution, CurrentVerticalResolution", shell=True).decode().splitlines()

    if len(resolution) > 1:
        res = resolution[1].strip().split()
        if len(res) >= 2:
            resolution_info = f"{res[0]} x {res[1]}"
        else:
            resolution_info = "Résolution non disponible"
    else:
        resolution_info = "Résolution non disponible"

    system_perif_info["Carte Graphique"] = graphics_info[1] if len(graphics_info) > 1 else "Non disponible"
    system_perif_info["Résolution d'Écran"] = resolution_info
    system_perif_info["Taux de Rafraîchissement"] = "Non disponible"

    return system_perif_info



def display_system_perif_f4(frame):
    info = get_system_perif()

    # Title for Peripheral Information
    title_label = customtkinter.CTkLabel(
        master=frame,
        text="Informations sur les Périphériques",
        font=("Arial", 16, "bold"),
        text_color="black"  # Set title color to black
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    row = 1
    for key, value in info.items():
        if isinstance(value, list):  # For USB and Audio Devices
            label_key = customtkinter.CTkLabel(master=frame, text=f"{key}:", font=("Arial", 12, "bold"), text_color="black")  # Set label color to black
            label_key.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            label_value = customtkinter.CTkLabel(
                master=frame, 
                text=", ".join(value) if value else "Aucun", 
                font=("Arial", 12), 
                text_color="black"  # Set value color to black
            )
            label_value.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            row += 1

        elif isinstance(value, dict):  # For Network Cards
            label_key = customtkinter.CTkLabel(master=frame, text=f"{key}:", font=("Arial", 12, "bold"), text_color="black")  # Set label color to black
            label_key.grid(row=row, column=0, sticky="w", padx=10, pady=5)
            row += 1

            # Scrollable table for network cards
            canvas = customtkinter.CTkCanvas(frame, width=600, height=150)
            scrollbar = customtkinter.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
            scrollable_frame = customtkinter.CTkFrame(canvas)

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=(10, 0), pady=(10, 0))
            scrollbar.grid(row=row, column=2, sticky="ns", pady=(10, 0))

            # Display each network card in the scrollable frame
            for sub_key, sub_value in value.items():
                iface_label = customtkinter.CTkLabel(scrollable_frame, text=f"{sub_key}:", font=("Arial", 12, "bold"), text_color="black")  # Set label color to black
                iface_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                addr_list = ", ".join([addr.address for addr in sub_value if addr.family == socket.AF_INET])
                addr_label = customtkinter.CTkLabel(scrollable_frame, text=addr_list, font=("Arial", 12), text_color="black")  # Set value color to black
                addr_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")

                row += 1

            # Update the scroll region
            scrollable_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        else:  # For other single values
            label_key = customtkinter.CTkLabel(master=frame, text=f"{key}:", font=("Arial", 12, "bold"), text_color="black")  # Set label color to black
            label_key.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            label_value = customtkinter.CTkLabel(master=frame, text=value, font=("Arial", 12), text_color="black")  # Set value color to black
            label_value.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            row += 1
