import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import json
import platform
import logging
import threading

CONFIG_FILE = 'config.json'
LOG_FILE = 'app.log'

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Load or save configuration for server addresses and file paths
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"Config file '{CONFIG_FILE}' not found. Creating a new one.")
        return {'configurations': []}


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    logging.info(f"Configurations saved to '{CONFIG_FILE}'.")


# Browse for files
def browse_file(var, label, file_type="file"):
    if file_type == "realmlist":
        file_path = filedialog.askopenfilename(title="Select realmlist.wtf", filetypes=[("Text Files", "*.wtf"),
                                                                                        ("All Files", "*.*")])
    else:
        file_path = filedialog.askopenfilename(title="Select WoW.exe", filetypes=[("Executable Files", "*.exe"),
                                                                                  ("All Files", "*.*")])
    if file_path:
        var.delete(0, tk.END)
        var.insert(0, file_path)
        label.config(text=os.path.basename(file_path))


# Update realmlist.wtf with selected server address
def update_realmlist(realmlist_path, server_address, version):
    try:
        with open(realmlist_path, 'w') as file:
            # Write realmlist
            file.write(f"set realmlist {server_address}\n")
            # Write portal
            file.write(f"set portal {server_address}\n")

            # If the version is Cataclysm, add patchlist
            if version == "Cataclysm (4.3.4)":
                file.write(f"set patchlist {server_address}\n")

        logging.info(f"Updated realmlist.wtf at {realmlist_path} with server address: {server_address}")
        logging.info(f"Updated realmlist.wtf at {realmlist_path} with portal address: {server_address}")

        if version == "Cataclysm (4.3.4)":
            logging.info(f"Added patchlist for Cataclysm: {server_address}")

    except Exception as e:
        logging.error(f"Failed to update realmlist.wtf: {e}")
        messagebox.showerror("Error", f"Failed to update realmlist.wtf: {e}")


# Function to run selected WoW
def run_selected_wow(config, listbox):
    try:
        selected_index = listbox.curselection()[0]
        selected_config = config['configurations'][selected_index]
        realmlist_path = selected_config['realmlist_path']
        server_address = selected_config['server_address']
        portal_address = selected_config['portal_address']
        wow_exe_path = selected_config['wow_exe_path']
        version = selected_config['version']

        # Ensure realmlist.wtf file exists
        if not os.path.exists(realmlist_path):
            logging.error(f"realmlist.wtf path not found: {realmlist_path}")
            messagebox.showerror("Error", "realmlist.wtf path is invalid or not selected.")
            return

        # Ensure WoW.exe file exists
        if not os.path.exists(wow_exe_path):
            logging.error(f"WoW.exe path not found: {wow_exe_path}")
            messagebox.showerror("Error", "WoW.exe path is invalid or not selected.")
            return

        # Update realmlist.wtf with server address
        update_realmlist(realmlist_path, server_address, version)

        # Run WoW.exe
        run_wow_async(wow_exe_path)

    except IndexError:
        messagebox.showwarning("No Configuration Selected", "Please select a configuration to run.")
    except Exception as e:
        logging.error(f"Error running WoW: {e}")
        messagebox.showerror("Error", f"An error occurred while trying to run WoW: {e}")


# Existing run_wow function
def run_wow(wow_exe_path):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(wow_exe_path, shell=True)
        elif platform.system() == "Linux":
            subprocess.run(['wine', wow_exe_path])
        else:
            logging.error(f"Unsupported OS: {platform.system()}")
            messagebox.showerror("Unsupported OS", "This operating system is not supported.")
        logging.info(f"WoW.exe run from: {wow_exe_path}")
    except Exception as e:
        logging.error(f"Failed to run WoW.exe: {e}")
        messagebox.showerror("Error", f"Failed to run WoW.exe: {e}")


def run_wow_async(wow_exe_path):
    thread = threading.Thread(target=run_wow, args=(wow_exe_path,))
    thread.start()


# Add a new configuration
def add_configuration(config, entry_fields, realmlist_label, wow_exe_label, listbox):
    name = entry_fields["name"].get()
    realmlist = entry_fields["realmlist"].get()
    wow_exe = entry_fields["wow_exe"].get()
    server_address = entry_fields["server_address"].get()
    portal_address = entry_fields["portal_address"].get()
    version = entry_fields["version"].get()

    if not name or not realmlist or not wow_exe or not server_address:
        messagebox.showwarning("Input Error", "Please fill in all fields.\n" + name + ", " + realmlist +
                               ", " + wow_exe + ", " + server_address)
        return

    for cfg in config['configurations']:
        if cfg['name'] == name:
            messagebox.showwarning("Duplicate Name", "A configuration with this name already exists.")
            return
    new_config = {
        'name': name,
        'realmlist_path': realmlist,
        'wow_exe_path': wow_exe,
        'server_address': server_address,
        'portal_address': portal_address,
        'version': version
    }
    config['configurations'].append(new_config)
    listbox.insert(tk.END, name)
    logging.info(f"Configuration '{name}' added.")

    save_config(config)
    clear_input_fields(entry_fields, realmlist_label, wow_exe_label)


# Clear input fields after adding/updating a configuration
def clear_input_fields(entry_fields, realmlist_label, wow_exe_label):
    # Clear the entry fields
    entry_fields['name'].delete(0, tk.END)  # Clear name field
    entry_fields['realmlist'].delete(0, tk.END)  # Clear realmlist field
    entry_fields['wow_exe'].delete(0, tk.END)  # Clear wow_exe field
    entry_fields['server_address'].delete(0, tk.END)  # Clear server_address field
    entry_fields['portal_address'].delete(0, tk.END)  # Clear portal_address field

    # Reset the labels for realmlist and wow_exe
    realmlist_label.config(text="No file selected")
    wow_exe_label.config(text="No file selected")

    # Optionally reset version variable if you need to
    entry_fields['version'].set("")  # Clear version field


# Main GUI setup
def main():
    config = load_config()

    root = tk.Tk()
    root.title("Realmlist Updater")

    # Frames for organization
    left_frame = tk.LabelFrame(root, text="Saved Configurations", padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = tk.LabelFrame(root, text="Add Configuration", padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Listbox for configurations
    listbox = tk.Listbox(left_frame, height=10, selectmode=tk.SINGLE)
    listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")
    for cfg in config['configurations']:
        listbox.insert(tk.END, cfg['name'])

    # Move buttons below the listbox
    move_up_button = tk.Button(left_frame, text="Move Up", command=lambda: move_config(config, listbox, direction='up'))
    move_up_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    move_down_button = tk.Button(left_frame, text="Move Down", command=lambda: move_config(config, listbox, direction='down'))
    move_down_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

    # Add a "Run WoW" Button in the Right Frame
    tk.Button(left_frame, text="Run WoW", command=lambda: run_selected_wow(config, listbox)
              ).grid(row=4, column=0, columnspan=2, pady=5, sticky="we")

    # Update Selected button
    update_button = tk.Button(left_frame, text="Update Selected",
                              command=lambda: update_selected(config, listbox, entry_fields, realmlist_label, wow_exe_label,
                                                              right_frame, add_button))
    update_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Add Delete Selected button below the Update Selected button
    delete_button = tk.Button(left_frame, text="Delete Selected", command=lambda: delete_configuration(config, listbox))
    delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Right Frame: Add New Configuration and Display Selected
    # Define fields in the right panel (Name, realmlist.wtf, WoW.exe, Server Address)
    entry_fields = {
        'name': tk.Entry(right_frame),
        'realmlist': tk.Entry(right_frame),
        'wow_exe': tk.Entry(right_frame),
        'server_address': tk.Entry(right_frame),
        'portal_address': tk.Entry(right_frame),
        'version': tk.StringVar(right_frame)
    }

    # Labels and Entry widgets for the form fields
    tk.Label(right_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
    entry_fields['name'].grid(row=0, column=1, pady=2)  # Use the existing entry field from the dictionary

    tk.Label(right_frame, text="Select realmlist.wtf:").grid(row=1, column=0, sticky=tk.W, pady=2)
    realmlist_label = tk.Label(right_frame, text="No file selected")
    realmlist_label.grid(row=1, column=1, pady=2, sticky=tk.W)
    tk.Button(right_frame, text="Browse", command=lambda: browse_file(entry_fields["realmlist"], realmlist_label,
                                                                      "realmlist")).grid(row=1, column=2, padx=5, pady=2)

    tk.Label(right_frame, text="Select WoW.exe:").grid(row=2, column=0, sticky=tk.W, pady=2)
    wow_exe_label = tk.Label(right_frame, text="No file selected")
    wow_exe_label.grid(row=2, column=1, pady=2, sticky=tk.W)
    tk.Button(right_frame, text="Browse", command=lambda: browse_file(entry_fields["wow_exe"], wow_exe_label, "exe")).grid(
        row=2, column=2, padx=5, pady=2)

    tk.Label(right_frame, text="Server Address:").grid(row=3, column=0, sticky=tk.W, pady=2)
    entry_fields['server_address'].grid(row=3, column=1, pady=2)  # Use the existing entry field from the dictionary

    tk.Label(right_frame, text="Portal Address:").grid(row=4, column=0, sticky=tk.W, pady=2)
    entry_fields['portal_address'].grid(row=4, column=1, pady=2)  # Use the existing entry field from the dictionary

    # Add a label and a dropdown (OptionMenu) for WoW version
    version_var = tk.StringVar(value="Vanilla (1.12.x)")  # Default value

    # Define the options for the dropdown
    version_options = [
        "Vanilla (1.12.x)",
        "The Burning Crusade (2.4.3)",
        "Wrath of the Lich King (3.3.5)",
        "Cataclysm (4.3.4)"
    ]

    # Add label and dropdown to the right frame
    tk.Label(right_frame, text="WoW Version:").grid(row=5, column=0, sticky=tk.W, pady=2)
    version_dropdown = tk.OptionMenu(right_frame, version_var, *version_options)
    version_dropdown.grid(row=5, column=1, pady=2)

    # Update the 'entry_fields' dictionary to include the version
    entry_fields['version'] = version_var

    # Add button, default state
    add_button = tk.Button(right_frame, text="Add", command=lambda: add_configuration(config, entry_fields, realmlist_label,
                                                                                      wow_exe_label, listbox))
    add_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="we")  # Stretched across the panel

    root.mainloop()


# Delete a configuration
def delete_configuration(config, listbox):
    if listbox.curselection():
        index = listbox.curselection()[0]
        del config['configurations'][index]
        listbox.delete(index)
        save_config(config)
        logging.info("Configuration deleted.")


# Function to move configuration up or down
def move_config(config, listbox, direction):
    try:
        selected_index = listbox.curselection()[0]

        # Determine new position
        if direction == 'up' and selected_index > 0:
            new_index = selected_index - 1
        elif direction == 'down' and selected_index < len(config['configurations']) - 1:
            new_index = selected_index + 1
        else:
            return  # Do nothing if already at top or bottom

        # Swap the configurations
        config['configurations'][selected_index], config['configurations'][new_index] = \
            config['configurations'][new_index], config['configurations'][selected_index]

        # Update the listbox
        update_listbox(listbox, config)

        # Set focus back to the moved item
        listbox.selection_set(new_index)
        listbox.activate(new_index)

        # Save updated configuration
        save_config(config)

    except IndexError:
        messagebox.showwarning("No Configuration Selected", "Please select a configuration to move.")
    except Exception as e:
        logging.error(f"Error moving configuration: {e}")
        messagebox.showerror("Error", f"An error occurred while moving the configuration: {e}")


# Helper function to update the listbox
def update_listbox(listbox, config):
    # Clear the listbox
    listbox.delete(0, tk.END)

    # Re-populate listbox with updated configurations
    for conf in config['configurations']:
        listbox.insert(tk.END, conf['name'])


def update_selected(config, listbox, entry_fields, realmlist_label, wow_exe_label, right_frame, add_button):
    try:
        # Get selected configuration index
        selected_index = listbox.curselection()[0]
        selected_config = config['configurations'][selected_index]

        # Update right panel label to "Edit Configuration"
        right_frame.config(text="Edit Configuration")

        # Ensure the fields are enabled and ready for input
        entry_fields['name'].config(state=tk.NORMAL)
        entry_fields['realmlist'].config(state=tk.NORMAL)
        entry_fields['wow_exe'].config(state=tk.NORMAL)
        entry_fields['server_address'].config(state=tk.NORMAL)
        entry_fields['portal_address'].config(state=tk.NORMAL)

        # Pre-fill the entry fields with the selected configuration's values
        entry_fields['name'].delete(0, tk.END)
        entry_fields['name'].insert(0, selected_config.get('name', ''))

        entry_fields['realmlist'].delete(0, tk.END)
        entry_fields['realmlist'].insert(0, selected_config.get('realmlist', ''))

        entry_fields['wow_exe'].delete(0, tk.END)
        entry_fields['wow_exe'].insert(0, selected_config.get('wow_exe', ''))

        entry_fields['server_address'].delete(0, tk.END)
        entry_fields['server_address'].insert(0, selected_config.get('server_address', ''))

        entry_fields['portal_address'].delete(0, tk.END)
        entry_fields['portal_address'].insert(0, selected_config.get('portal_address', ''))

        # Force the UI to update to reflect changes
        entry_fields['name'].update_idletasks()
        entry_fields['server_address'].update_idletasks()
        entry_fields['portal_address'].update_idletasks()

        # Update the labels to reflect the selected file paths
        realmlist_label.config(text=os.path.basename(selected_config.get('realmlist', '')))
        wow_exe_label.config(text=os.path.basename(selected_config.get('wow_exe', '')))

        # Replace the "Add" button with a "Save" button
        add_button.config(text="Save", command=lambda: save_configuration(config, listbox, entry_fields, selected_index,
                                                                          right_frame, add_button, realmlist_label,
                                                                          wow_exe_label))

    except IndexError:
        messagebox.showwarning("No Configuration Selected", "Please select a configuration to update.")

    except KeyError as e:
        print(f"KeyError: {e}. Check that the keys are correct in your selected configuration.")


def save_configuration(config, listbox, entry_fields, index, right_frame, add_button, realmlist_label, wow_exe_label):
    # Update the selected configuration with new values
    selected_version = entry_fields['version'].get()
    server_address = entry_fields['server_address'].get()

    config['configurations'][index] = {
        'name': entry_fields['name'].get(),
        'realmlist': entry_fields['realmlist'].get(),
        'wow_exe': entry_fields['wow_exe'].get(),
        'server_address': server_address,
        'portal_address': portal_address,
        'version': selected_version
    }

    # Check if version is Cataclysm and add patchlist if necessary
    if selected_version == "Cataclysm (4.3.4)":
        config['configurations'][index]['patchlist'] = server_address  # Add patchlist as server_address

    # Update listbox and save configuration
    update_listbox(listbox, config)
    save_config(config)

    # Revert back to "Add Configuration" mode
    right_frame.config(text="Add Configuration")
    add_button.config(text="Add", command=lambda: add_configuration(config, entry_fields, realmlist_label, wow_exe_label,
                                                                    listbox))

    # Clear the entry fields for a new entry
    clear_entry_fields(entry_fields)


def clear_entry_fields(entry_fields):
    for field in entry_fields.values():
        if isinstance(field, tk.Entry):
            field.delete(0, tk.END)  # Clear Entry fields
        elif isinstance(field, tk.StringVar):
            field.set('')  # Clear StringVar fields


if __name__ == "__main__":
    main()
