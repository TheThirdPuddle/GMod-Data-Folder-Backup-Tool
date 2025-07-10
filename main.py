# This file is part of GMod Data Folder Backup Tool (GMDFBT).
#
# GMDFBT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GMDFBT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GMDFBT. If not, see <https://www.gnu.org/licenses/>.


# error code dictionary (for the exceptions around the entire script)
error_codes = {
    "ValueError": 1001,
    "TypeError": 1002,
    "ZeroDivisionError": 1003,
    "IndexError": 1004,
    "KeyError": 1005,
    "FileNotFoundError": 1006,
    "IOError": 1007,
    "ImportError": 1008,
    "AttributeError": 1009,
    "NameError": 1010,
    "OSError": 1011,
    "RuntimeError": 1012,
    "NotImplementedError": 1013,
    "MemoryError": 1014,
    "OverflowError": 1015,
    "RecursionError": 1016,
    "UnboundLocalError": 1017,
    "JSONDecodeError": 1018,
    "KeyboardInterrupt": 1019,
    "SystemExit": 1020,
    "StopIteration": 1021,
    "StopAsyncIteration": 1022,
    "GeneratorExit": 1023,
    # Add more exception types as needed
}
# Updated DARK_THEME
DARK_THEME = """
    QWidget {
        background-color: #1E1E1E;
        color: #DDDDDD;
    }
    QLabel {
        font-size: 14px;
        font-family: Arial, sans-serif;
        color: #DDDDDD;
    }
    QLineEdit, QTextEdit {
        border: 2px solid #666666;
        border-radius: 5px;
        padding: 5px;
        font-size: 12px;
        background-color: #333333;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #0078D7;
        color: white;
        border-radius: 8px;  /* Rounded buttons */
        padding: 8px 12px;
    }
    QPushButton:hover {
        background-color: #005A9E;
    }
    QProgressBar {
        text-align: center;
        font-size: 12px;
        height: 20px;
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        border-radius: 8px;  /* Rounded progress bar */
    }
    QProgressBar::chunk {
        background-color: #0078D7;
        border-radius: 8px;  /* Rounded progress fill */
    }
    QCheckBox {
        font-size: 12px;
        color: #AAAAAA;
    }
    QComboBox {
    text-align: center;
    font-size: 12px;
    height: 20px;
    background-color: #333333;
    color: #ffffff;
    border: 2px solid #ffffff;
    border-radius: 8px;
    }

    QComboBox::drop-down {
        border: none;  /* Removes the border around the arrow */
        width: 20px;  /* Adjust as needed */
    }

    QComboBox::down-arrow {
        color: #FFFFFF;
        font-size: 10px;
    }
"""

# Updated LIGHT_THEME
LIGHT_THEME = """
    QWidget {
        background-color: #FFFFFF;
        color: #000000;
    }
    QLabel {
        font-size: 14px;
        font-family: Arial, sans-serif;
        color: #000000;
    }
    QLineEdit, QTextEdit {
        border: 2px solid #AAAAAA;
        border-radius: 5px;
        padding: 5px;
        font-size: 12px;
        background-color: #F0F0F0;
        color: #000000;
    }
    QPushButton {
        background-color: #0078D7;
        color: white;
        border-radius: 8px;  /* Rounded buttons */
        padding: 8px 12px;
    }
    QPushButton:hover {
        background-color: #005A9E;
    }
    QProgressBar {
        text-align: center;
        font-size: 12px;
        height: 20px;
        background-color: #F0F0F0;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 8px;  /* Rounded progress bar */
    }
    QProgressBar::chunk {
        background-color: #0078D7;
        border-radius: 8px;  /* Rounded progress fill */
    }
    QCheckBox {
        font-size: 12px;
        color: #333333;
    }
    QComboBox {
    text-align: center;
    font-size: 12px;
    height: 20px;
    background-color: #F0F0F0;
    color: #000000;
    border: 2px solid #000000;
    border-radius: 8px;
    }

    QComboBox::drop-down {
        border: none;  /* Removes the border around the arrow */
        width: 20px;  /* Adjust as needed */
    }

    QComboBox::down-arrow {
        color: #000000;
        font-size: 10px;
    }
"""




# Error popups
def critical(e, allow_continue):
    from PyQt5.QtWidgets import QMessageBox
    import traceback
    import sys
    unex_error_type = type(e).__name__
    unex_error_code = error_codes.get(unex_error_type, "unknown")
    error_message = (
        "An unexpected error has occurred!\n\n"
        f"Error details:\n"
        f"type: '{unex_error_type}'\n"
        f"code: '{unex_error_code}'\n"
        f"details: '{e}'"
    )
    if allow_continue:
        error_message += (
            "\n\nThe app will continue to run, but it is recommended to fix the error!"
        )

    QMessageBox.critical(
        None,
        "Unexpected Error",
        error_message
    )
    traceback.print_exc()
    if allow_continue:
        print("continuing...")
    else:
        print("force closing app...")
        sys.exit(1)


def warning(title, message):
    from PyQt5.QtWidgets import QMessageBox
    QMessageBox.warning(
        None,
        title,
        message
    )


if True:
    try:
        import os
        import shutil
        import time
        import ctypes
        import sys
        import json
        import traceback
        import zipfile
        import folderutils
        import requests
        from PyQt5 import QtWidgets, QtCore
        from PyQt5.QtWidgets import QFileDialog, QMessageBox, QCheckBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QDialog, QDialogButtonBox
        from PyQt5.QtGui import QIcon
        from PyQt5.QtSvg import QSvgWidget
        
        rawVersion = f"1.1.0-beta.2"

        # Check if the script is running as a compiled binary
        if getattr(sys, 'frozen', False):
            build_type = "Binary Build"
        else:
            build_type = "Python Build"

        version = f"{rawVersion} ({build_type})"
        
        

        # Print the result (optional)
        print(f"Running as: {build_type}")
        print(f"Version: {version}")

        # Function to check if the script is running with admin privileges
        def is_admin():
            try:
                print("Checking if the script is running with admin privileges...")
                return ctypes.windll.shell32.IsUserAnAdmin()
            except Exception as e:
                print(f"Failed to check admin privileges: {e}")
                return False

        def load_settings():
            try:
                print("Loading settings from settings.json...")
                if os.path.exists('settings.json'):
                    with open('settings.json', 'r') as f:
                        settings = json.load(f)
                        print("Settings loaded successfully.")
                        return settings
                print("Settings file not found. Loading default settings...")
                return {
                    "backup_folder_format": "backup-{date}-{time}",
                    "size_restriction": True,
                    "enable_logging": False,
                    "compress_backup": False,
                    "theme": "dark"  # New theme setting, default to dark
                }
            except json.JSONDecodeError as json_error:
                print(f"Error loading settings: {json_error}")
                setting_error_type = type(json_error).__name__
                setting_error_code = error_codes.get(setting_error_type, "unknown")
                QtWidgets.QMessageBox.critical(
                    None,
                    "Corrupted Settings",
                    f"The settings.json file may be corrupted and is preventing the application from starting.\n"
                    "Please correct or delete the settings.json file and restart the application.\n\n"
                    f"Error info:\n"
                    f"type: {setting_error_type}\ncode: {setting_error_code}\ndetails: {str(json_error)}"
                )
            except Exception as e:
                print(f"Unexpected error loading settings: {e}")
                critical(e, False)

        # Function to save settings to a JSON file
        def save_settings(settings):
            try:
                print("Saving settings to settings.json...")
                with open('settings.json', 'w') as f:
                    json.dump(settings, f)
                print("Settings saved successfully.")
            except Exception as e:
                print(f"Failed to save settings: {e}")

        def apply_theme(app, settings):
            theme = settings.get("theme", "dark")
            app.setStyleSheet(DARK_THEME if theme == "dark" else LIGHT_THEME)

        # Function to create a log file if logging is enabled
        def create_log_file():
            try:
                print("Creating log file...")
                logs_dir = os.path.join(os.getcwd(), "logs")
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir)  # Create the logs directory if it doesn't exist

                current_time = time.strftime("%m-%d-%Y-%H-%M-%S")
                log_filename = f"LOG_{time.strftime('%m-%d-%Y-%H-%M-%S')}.log"
                log_filepath = os.path.join(logs_dir, log_filename)

                print(f"Log file created: {log_filepath}")
                return log_filepath
            except Exception as e:
                print(f"Failed to create log file: {e}")
                return None

        # Function to create a backup with progress tracking and logging
        def create_backup(source_folder, destination_folder, progress_bar, log_textedit, show_log, backup_folder_format, size_restriction, enable_logging, compress_backup):
            try:
                print("Starting backup process...")
                print(f"Source folder: {source_folder}")
                print(f"Destination folder: {destination_folder}")
                # Check if the source folder exists
                if not os.path.exists(source_folder):
                    print("Error: Source folder does not exist.")
                    raise FileNotFoundError("Source folder does not exist.")

                # Check folder size if restriction is enabled
                if size_restriction:
                    print("Checking folder size...")
                    total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(source_folder) for file in files)
                    if total_size > 1024 * 1024 * 1024:  # 1GB limit
                        print("Error: Folder exceeds size restriction of 1GB.")
                        raise ValueError("Folder exceeds size restriction of 1GB.")

                # Get current time and format the folder name
                current_time = time.strftime("%m-%d-%Y-%H-%M-%S")
                backup_folder_name = backup_folder_format.replace("{date}", time.strftime("%m-%d-%Y")).replace("{time}", time.strftime("%H-%M-%S"))
                backup_path = os.path.join(destination_folder, backup_folder_name)
                print(f"Backup folder name: {backup_folder_name}")
                print(f"Backup path: {backup_path}")

                # Create the backup folder
                os.makedirs(backup_path, exist_ok=True)
                print("Backup folder created successfully.")

                # Set up logging if enabled
                log_file = None
                if enable_logging:
                    log_file = create_log_file()
                    if log_file:
                        with open(log_file, 'a') as f:
                            f.write(f"Backup started at: {current_time}\n")
                            f.write(f"Source: {source_folder}\n")
                            f.write(f"Destination: {backup_path}\n\n")

                # Count total files for progress tracking
                total_files = sum(len(files) for _, _, files in os.walk(source_folder))
                print(f"Total files to be backed up: {total_files}")
                files_copied = 0

                # Show progress bar and reset it
                progress_bar.setValue(0)
                progress_bar.show()

                # Clear the log text edit if showing
                if show_log:
                    log_textedit.clear()
                    log_textedit.show()

                # Improved copying logic - Copy files individually to ensure permissions are handled
                for root, dirs, files in os.walk(source_folder):
                    for dir in dirs:
                        dest_dir = os.path.join(backup_path, os.path.relpath(os.path.join(root, dir), source_folder))
                        os.makedirs(dest_dir, exist_ok=True)
                        print(f"Created folder: {dest_dir}")
                        if show_log:
                            log_textedit.append(f"Created folder: {dest_dir}")
                            QtCore.QCoreApplication.processEvents()

                        if log_file:
                            with open(log_file, 'a') as f:
                                f.write(f"Created folder: {dest_dir}\n")

                    for file in files:
                        source_file = os.path.join(root, file)
                        dest_file = os.path.join(backup_path, os.path.relpath(source_file, source_folder))
                        shutil.copy2(source_file, dest_file)
                        print(f"Copied file: {source_file} to {dest_file}")

                        # Log the copied file
                        if show_log:
                            log_textedit.append(f"Copied file: {source_file}")
                            QtCore.QCoreApplication.processEvents()

                        if log_file:
                            with open(log_file, 'a') as f:
                                f.write(f"Copied file: {source_file}\n")

                        # Update progress bar
                        files_copied += 1
                        progress = int((files_copied / total_files) * 100)
                        progress_bar.setValue(progress)

                # Compress the backup into a .zip file if enabled
                if compress_backup:
                    zip_filename = f"{backup_path}.zip"
                    print(f"Compressing backup to: {zip_filename} (The application may freeze briefly...)")
                    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(backup_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zipf.write(file_path, os.path.relpath(file_path, backup_path))
                    print(f"Backup compressed successfully to: {zip_filename}")

                # Write completion message to log if logging is enabled
                if log_file:
                    with open(log_file, 'a') as f:
                        f.write(f"\nBackup completed at {time.strftime('%m-%d-%Y %H:%M:%S')}\n")

                print("Backup completed successfully.")
                # Display success message
                QMessageBox.information(None, "Backup Success", f"Backup created at: {backup_path}")
                progress_bar.setValue(0)

            except Exception as e:
                backupfail_error_type = type(e).__name__
                backupfail_error_code = error_codes.get(backupfail_error_type, "unknown")
                print(f"Backup failed: {e}")
                if show_log:
                    log_textedit.append(f"Error: {e}")
                QMessageBox.critical(None, "Backup Error", f"Failed to create backup\n\nerror info:\ntype: {backupfail_error_type}\ncode: {backupfail_error_code}\ndetails: {str(e)}")
                progress_bar.setValue(0)
        def restore_backup(backup_folder, restore_target, progress_bar, log_textedit, show_log):
            try:
                print("Starting restore process...")
                print(f"checking permissions for {restore_target}...")
                # Dangerously critical system folders that should never be used as restore targets
                PROTECTED_PATHS = [
                    os.environ.get("SYSTEMROOT", r"C:\Windows"),
                    r"C:\Windows",
                    r"C:\Program Files",
                    r"C:\Program Files (x86)",
                    r"C:\Users",
                    r"C:\.",  # root is too risky
                    r"c:\test\path"
                ]

                def is_protected_path(path):
                    abs_path = os.path.abspath(path).lower()
                    for protected in PROTECTED_PATHS:
                        protected_abs = os.path.abspath(protected).lower()
                        if abs_path == protected_abs:
                            return True  # Exact match (e.g. trying to restore directly into C:\Windows)
                        if os.path.commonpath([abs_path, protected_abs]) == protected_abs and abs_path != protected_abs:
                            # Only block immediate children, not deeper subfolders
                            if os.path.relpath(abs_path, protected_abs).count(os.sep) == 0:
                                return True

                    return False
                if is_protected_path(restore_target):
                    raise PermissionError(f"{restore_target} is a protected system directory. Operation aborted.")
                print(f"Backup folder: {backup_folder}")
                print(f"Restore target: {restore_target}")

                # Check if the backup source exists
                if not os.path.exists(backup_folder):
                    raise FileNotFoundError("Backup source does not exist.")

                # Clear the restore target first
                if os.path.exists(restore_target):
                    shutil.rmtree(restore_target)
                os.makedirs(restore_target, exist_ok=True)

                # Count total files for progress tracking
                total_files = sum(len(files) for _, _, files in os.walk(backup_folder))
                files_copied = 0
                progress_bar.setValue(0)
                progress_bar.show()

                if show_log:
                    log_textedit.clear()
                    log_textedit.show()

                # Copy files from backup to destination
                for root, dirs, files in os.walk(backup_folder):
                    for dir in dirs:
                        target_dir = os.path.join(restore_target, os.path.relpath(os.path.join(root, dir), backup_folder))
                        os.makedirs(target_dir, exist_ok=True)
                        if show_log:
                            log_textedit.append(f"Created folder: {target_dir}")
                            QtCore.QCoreApplication.processEvents()

                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(restore_target, os.path.relpath(src_file, backup_folder))
                        shutil.copy2(src_file, dest_file)
                        files_copied += 1
                        progress = int((files_copied / total_files) * 100)
                        progress_bar.setValue(progress)

                        if show_log:
                            log_textedit.append(f"Restored file: {src_file}")
                            QtCore.QCoreApplication.processEvents()

                QMessageBox.information(None, "Restore Success", "Backup has been successfully restored.")
                progress_bar.setValue(0)

            except Exception as e:
                if show_log:
                    log_textedit.append(f"Error: {e}")
                progress_bar.setValue(0)
                critical(e, True)


        # Settings Dialog
        class SettingsDialog(QDialog):
            def __init__(self, settings, parent=None):
                super().__init__(parent)

                print("Initializing Settings Dialog...")
                self.settings = settings
                self.setWindowTitle("Additional Backup Settings")
                self.setGeometry(300, 300, 400, 180)

                # Folder name format label and input
                self.label_format = QLabel("Backup folder name format:")
                self.input_format = QLineEdit(self)
                self.input_format.setText(self.settings['backup_folder_format'])
                self.label_format_guide = QLabel("Use {date} for current date and {time} for current time.")

                # Folder size restriction checkbox
                self.size_restriction_checkbox = QCheckBox("Enforce 1 GB folder size limit (disable to allow larger folders).", self)
                self.size_restriction_checkbox.setChecked(self.settings['size_restriction'])

                # Logging option checkbox
                self.enable_logging_checkbox = QCheckBox("Enable logging folder", self)
                self.enable_logging_checkbox.setChecked(self.settings['enable_logging'])

                # Compress backup option checkbox
                self.compress_backup_checkbox = QCheckBox("Compress backup into .zip file", self)
                self.compress_backup_checkbox.setChecked(self.settings['compress_backup'])

                # Add theme selection dropdown
                self.theme_label = QLabel("Select Theme:")
                self.theme_dropdown = QtWidgets.QComboBox(self)
                self.theme_dropdown.addItems(["Dark", "Light"])
                self.theme_dropdown.setCurrentText("Dark" if self.settings["theme"] == "dark" else "Light")

                # OK and Cancel buttons
                self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
                self.button_box.accepted.connect(self.accept)
                self.button_box.rejected.connect(self.reject)

                # Layout
                layout = QVBoxLayout()
                layout.addWidget(self.label_format)
                layout.addWidget(self.input_format)
                layout.addWidget(self.label_format_guide)
                layout.addWidget(self.size_restriction_checkbox)
                layout.addWidget(self.enable_logging_checkbox)
                layout.addWidget(self.compress_backup_checkbox)
                layout.addWidget(self.theme_label)
                layout.addWidget(self.theme_dropdown)
                layout.addWidget(self.button_box)
                self.setLayout(layout)

            def accept(self):
                print("Saving settings from Settings Dialog...")
                # Update settings when OK is pressed
                self.settings['backup_folder_format'] = self.input_format.text()
                self.settings['size_restriction'] = self.size_restriction_checkbox.isChecked()
                self.settings['enable_logging'] = self.enable_logging_checkbox.isChecked()  # Save the logging setting
                self.settings['compress_backup'] = self.compress_backup_checkbox.isChecked()  # Save the compress backup setting
                self.settings['theme'] = "dark" if self.theme_dropdown.currentText() == "Dark" else "light"
                save_settings(self.settings)  # Save settings to JSON
                QMessageBox.information(None, "Successfully saved settings!", f"Your settings have been saved successfully!\n\nYou may need to restart the application for some settings to take effect.")
                print("Settings updated and saved successfully.")
                super().accept()

        # Main GUI Application
        class BackupApp(QtWidgets.QMainWindow):  # Inherit from QMainWindow
            def __init__(self):
                super().__init__()

                print("Initializing Backup Application GUI...")
                # Load settings from JSON file
                self.settings = load_settings()
                apply_theme(self, self.settings)

                # Window properties
                self.setWindowTitle("GMod Data Backup Tool")
                self.setGeometry(300, 300, 400, 100)
                self.setWindowIcon(QIcon(r'assets\GMODICON.ico'))

                # Hard-Coded directories
                default_source_directory = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data"
                default_dest_directory = (str(folderutils.get_documents_folder()) + r"\GMod Data Folder Backups")

                self.default_backup_source = default_source_directory
                self.default_backup_dest = default_dest_directory

                self.default_restore_source = ""  # leave blank for user to choose backup
                self.default_restore_dest = default_source_directory  # restoring into game folder


                # Create a menu bar (using QMainWindow's menuBar method)
                self.menu_bar = self.menuBar()

                # Create a file menu
                self.file_menu = self.menu_bar.addMenu("File")
                self.help_menu = self.menu_bar.addMenu("Help")

                # Add actions to the file menu
                self.exit_action = QtWidgets.QAction("Exit", self)
                self.file_menu.addAction(self.exit_action)

                # Connect the exit action to the close event
                self.exit_action.triggered.connect(self.close)

                # Add actions to the help menu
                self.about_action = QtWidgets.QAction("About", self)
                self.help_menu.addAction(self.about_action)
                self.changelog_action = QtWidgets.QAction("Changelog", self)
                self.help_menu.addAction(self.changelog_action)

                # Connect the About action to the about menu
                self.about_action.triggered.connect(self.show_about_dialog)

                # Labels
                self.label_source = QtWidgets.QLabel("Source Folder (GMod Data):")
                self.label_dest = QtWidgets.QLabel("Destination Folder for Backup:")

                # Input fields with default source directory
                self.input_source = QtWidgets.QLineEdit(self)
                self.input_source.setText(default_source_directory)  # Set default value
                self.input_dest = QtWidgets.QLineEdit(self)
                self.input_dest.setText(default_dest_directory)  # Set default value

                # Browse buttons
                self.btn_browse_source = QtWidgets.QPushButton("Browse", self)
                self.btn_browse_dest = QtWidgets.QPushButton("Browse", self)

                # Backup button
                self.btn_backup = QtWidgets.QPushButton("Create Backup", self)

                # Restore button (hidden initially)
                self.btn_restore = QtWidgets.QPushButton("Restore Backup", self)
                self.btn_restore.hide()

                # Progress bar
                self.progress_bar = QtWidgets.QProgressBar(self)
                self.progress_bar.setValue(0)
                self.progress_bar.show()  # Show the progress bar initially

                # Settings button
                self.btn_settings = QtWidgets.QPushButton("Additional Settings", self)

                # Checkbox to show log
                self.show_log_checkbox = QtWidgets.QCheckBox("Show live log")
                self.show_log_checkbox.setChecked(False)

                # Mode selection dropdown
                self.mode_label = QtWidgets.QLabel("Mode:")
                self.mode_dropdown = QtWidgets.QComboBox(self)
                self.mode_dropdown.addItems(["Backup", "Restore"])

                # TextEdit for log display (hidden initially)
                self.log_textedit = QtWidgets.QTextEdit(self)
                self.log_textedit.setReadOnly(True)
                self.log_textedit.hide()

                # Layout
                layout = QtWidgets.QVBoxLayout()

                # Create horizontal layout for source input and browse button
                source_layout = QtWidgets.QHBoxLayout()
                source_layout.addWidget(self.input_source)
                source_layout.addWidget(self.btn_browse_source)

                # Create horizontal layout for destination input and browse button
                dest_layout = QtWidgets.QHBoxLayout()
                dest_layout.addWidget(self.input_dest)
                dest_layout.addWidget(self.btn_browse_dest)

                # Create horizontal layout for settings and backup button
                options_layout = QtWidgets.QHBoxLayout()
                options_layout.addWidget(self.btn_settings)
                options_layout.addWidget(self.btn_backup)
                options_layout.addWidget(self.btn_restore)  # Will be hidden unless in Restore mode


                # Add source label and horizontal layout for input and button
                layout.addWidget(self.label_source)
                layout.addLayout(source_layout)

                # Add destination label and horizontal layout for input and button
                layout.addWidget(self.label_dest)
                layout.addLayout(dest_layout)

                # Mode selector layout
                mode_layout = QtWidgets.QHBoxLayout()
                mode_layout.addWidget(self.mode_label)
                mode_layout.addWidget(self.mode_dropdown)
                layout.addLayout(mode_layout)

                # Add options layout (settings and create backup button)
                layout.addLayout(options_layout)

                # Add the rest of the widgets
                layout.addWidget(self.progress_bar)  # Add progress bar to the layout
                layout.addWidget(self.show_log_checkbox)
                layout.addWidget(self.log_textedit)  # Add log display to the layout

                # Create a central widget and set layout (since QMainWindow needs a central widget)
                central_widget = QtWidgets.QWidget(self)  # Create a central widget
                central_widget.setLayout(layout)  # Set the layout on the central widget
                self.setCentralWidget(central_widget)  # Set the central widget for the QMainWindow

                # Signal connections
                self.btn_browse_source.clicked.connect(self.browse_source_folder)
                self.btn_browse_dest.clicked.connect(self.browse_destination_folder)
                self.btn_backup.clicked.connect(self.start_backup)
                self.btn_settings.clicked.connect(self.open_settings)
                self.btn_restore.clicked.connect(self.show_restore_warning)


                # Connect checkbox to toggle visibility and resize
                self.show_log_checkbox.stateChanged.connect(self.toggle_log_visibility)

                self.mode_dropdown.currentIndexChanged.connect(self.switch_mode)

            def run_restore(self):
                backup_folder = self.input_source.text()
                restore_target = self.input_dest.text()
                show_log = self.show_log_checkbox.isChecked()

                if not backup_folder or not restore_target:
                    QMessageBox.warning(self, "Input Error", "Both backup and restore paths must be selected.")
                    return

                QtCore.QCoreApplication.processEvents()
                restore_backup(backup_folder, restore_target, self.progress_bar, self.log_textedit, show_log)

            def switch_mode(self):
                selected_mode = self.mode_dropdown.currentText().lower()
                if selected_mode == "backup":
                    self.btn_backup.show()
                    self.btn_restore.hide()
                    self.label_source.setText("Source Folder (GMod Data):")
                    self.label_dest.setText("Destination Folder for Backup:")
                    self.input_source.setText(self.default_backup_source)
                    self.input_dest.setText(self.default_backup_dest)
                    self.btn_settings.setEnabled(True)
                elif selected_mode == "restore":
                    self.btn_backup.hide()
                    self.btn_restore.show()
                    self.label_source.setText("Backup Source (Zip or Folder):")
                    self.label_dest.setText("Restore Target (GMod Data Folder):")
                    self.input_source.setText(self.default_restore_source)
                    self.input_dest.setText(self.default_restore_dest)
                    self.btn_settings.setEnabled(False)


            def browse_source_folder(self):
                print("Browsing for source folder...")
                folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
                if folder:
                    print(f"Selected source folder: {folder}")
                    self.input_source.setText(folder)

            def browse_destination_folder(self):
                print("Browsing for destination folder...")
                folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
                if folder:
                    print(f"Selected destination folder: {folder}")
                    self.input_dest.setText(folder)

            def show_restore_warning(self):
                print("Showing restore warning dialog...")
                dialog = QDialog(self)
                dialog.setWindowTitle("Warning")

                warning_text = QLabel(
                    "This feature is in early beta and is not confirmed to be fully safe! \n"
                    "For safety, it is recommended to manually restore through the file manager itself.\n\n"
                    "This process will delete everything in './garrysmod/data/'\n"
                    "and replace them with your selected backup.\n\n"
                    "This action is permanent and CANNOT BE UNDONE!\n\n"
                    "Only proceed if you understand these risks!"
                )
                warning_text.setWordWrap(True)

                restore_button = QPushButton("Restore Anyway", dialog)
                cancel_button = QPushButton("Cancel", dialog)

                button_box = QDialogButtonBox(QtCore.Qt.Horizontal)
                button_box.addButton(restore_button, QDialogButtonBox.AcceptRole)
                button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)

                cancel_button.clicked.connect(dialog.reject)
                restore_button.clicked.connect(dialog.accept)

                layout = QVBoxLayout(dialog)
                layout.addWidget(warning_text)
                layout.addWidget(button_box)

                if dialog.exec_() == QDialog.Accepted:
                    print("User confirmed restore. Proceeding to restoration...")
                    self.run_restore()  # Stub for next phase
                else:
                    print("User canceled the restore operation.")

            def show_admin_warning(self):
                try:
                    print("Admin privileges not detected. Showing admin warning...")
                    # Create a dialog to display the warning
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Admin Privileges Required")

                    # Message explaining why admin privileges are needed
                    warning_label = QLabel("This application may need to be run as an administrator to perform the backup.\n\n"
                                        "To run as administrator:\n"
                                        "1. Right-click the .exe file.\n"
                                        "2. Select 'Run as administrator'.\n\n"
                                        "Caution: Running unknown apps as an administrator can carry risks. "
                                        "Only run apps you can trust with elevated privileges.", dialog)

                    # Notice for running without admin
                    notice_label = QLabel("Warning: The backup process may not work correctly if you proceed without admin rights. Continue?", dialog)

                    # Create 'Run Anyway' and 'Cancel' buttons
                    run_anyway_button = QPushButton("Run Anyway (not recommended)", dialog)
                    cancel_button = QPushButton("Cancel", dialog)

                    # Button box for organizing the buttons
                    button_box = QDialogButtonBox(QtCore.Qt.Horizontal)
                    button_box.addButton(run_anyway_button, QDialogButtonBox.AcceptRole)
                    button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)

                    # Connect buttons
                    cancel_button.clicked.connect(dialog.reject)
                    run_anyway_button.clicked.connect(dialog.accept)

                    # Layout for the dialog
                    layout = QVBoxLayout(dialog)
                    layout.addWidget(warning_label)
                    layout.addWidget(notice_label)
                    layout.addWidget(button_box)

                    # Execute the dialog and check the result
                    if dialog.exec_() == QDialog.Accepted:
                        print("User chose to run anyway without admin privileges.")
                        # User clicked "Run Anyway", proceed with backup
                        self.progress_bar.setValue(0)  # Reset progress bar
                        QtCore.QCoreApplication.processEvents()  # Force UI update before starting
                        show_log = self.show_log_checkbox.isChecked()  # Check if log is enabled
                        create_backup(self.input_source.text(), self.input_dest.text(), self.progress_bar, self.log_textedit, show_log, self.settings['backup_folder_format'], self.settings['size_restriction'], self.settings['enable_logging'], self.settings['compress_backup'])
                except Exception as e:
                    unex_error_type = type(e).__name__
                    unex_error_code = error_codes.get(unex_error_type, "unknown")
                    print(f"Error occurred: {e}")
                    QtWidgets.QMessageBox.critical(
                        None,
                        "Unexpected Error",
                        f"An unexpected error has occurred!\n\nError details:\ntype: '{unex_error_type}'\ncode: '{unex_error_code}'\ndetails: '{e}'",
                    )
                    traceback.print_exc()
                    sys.exit(1)
            # Update the `start_backup` function to show the dialog when admin privileges are not detected

            def start_backup(self):
                print("Start backup button clicked.")
                source_folder = self.input_source.text()
                destination_folder = self.input_dest.text()

                if not source_folder or not destination_folder:
                    print("Input Error: Both source and destination folders must be selected.")
                    QMessageBox.warning(self, "Input Error", "Both source and destination folders must be selected.")
                    return

                if not is_admin():
                    self.show_admin_warning()  # Show the warning dialog with the new button
                else:
                    print("Admin privileges detected. Proceeding with backup...")
                    self.setMinimumHeight(200)  # Expand window during the backup process
                    self.progress_bar.setValue(0)  # Reset progress bar
                    QtCore.QCoreApplication.processEvents()  # Force UI update before starting
                    show_log = self.show_log_checkbox.isChecked()  # Check if log is enabled
                    create_backup(source_folder, destination_folder, self.progress_bar, self.log_textedit, show_log, self.settings['backup_folder_format'], self.settings['size_restriction'], self.settings['enable_logging'], self.settings['compress_backup'])

            def open_settings(self):
                print("Opening settings dialog...")
                settings_dialog = SettingsDialog(self.settings, self)
                if settings_dialog.exec_() == QDialog.Accepted:
                    print("Settings dialog accepted and settings saved.")
                    # Settings are saved in the dialog, no need to handle it here
                    pass

            def toggle_log_visibility(self, state):
                print("Toggling log visibility...")
                if state == QtCore.Qt.Checked:
                    print("Log visibility enabled.")
                    self.log_textedit.show()
                    self.setMinimumHeight(470)
                    self.setMinimumWidth(400)
                    self.adjustSize()
                else:
                    print("Log visibility disabled.")
                    self.log_textedit.hide()
                    self.setMinimumHeight(150)
                    self.setMinimumWidth(400)
                    self.adjustSize()

                # Adjust the window size to fit the content
                self.adjustSize()

            def show_about_dialog(self):
                print("Showing about dialog...")
                about_dialog = AboutDialog(self)
                about_dialog.exec_()

        class AboutDialog(QtWidgets.QDialog):
            def __init__(self, parent=None):
                try:
                    super().__init__(parent)
                    self.setWindowTitle("About")
                    self.setGeometry(300, 300, 700, 500)

                    # Create a QLabel with the version number
                    version_label = QtWidgets.QLabel(str(version))
                    version_label.setAlignment(QtCore.Qt.AlignRight)  # Align to the right

                    # Create a QLabel with rich text to display the README contents
                    readme_content = r"""
                    <h1>Thank you for your interest in this tool...application...whatever it is!</h1>
                    <h4>with additional help with ChatGPT for building the code (yes, I know, I'm lazy AF)</h4>
                    <hr>

                    <h3>About This App:</h3>
                    <ul>
                    <li>This app is made to reduce the amount of clicks to back up your Gmod's <code>data</code> folder down to 1 (Powered by PyQt5)</li>
                    </ul>

                    <hr>

                    <h3>Notice:</h3>
                    <p>You may need to run this app as an administrator to perform backups correctly. You don't need to, but it's recommended so you won't encounter problems when backing up.</p>
                    <ul>
                    <li>Right-click on the executable, and press <strong>"Run as Administrator"</strong></li>
                    </ul>

                    <hr>

                    <h3>How to use:</h3>
                    <ol>
                    <li>Run <code>GMDFBT</code> as 'Administrator' (if you have to) (refer to the notice)</li>
                    <li>(optional) Select your GMod's <code>data</code> directory</li>
                    <li>(optional) Select your backup directory</li>
                    <li>Press <strong>Create backup</strong> (app may freeze during the process)</li>
                    <li>Close app once done</li>
                    </ol>

                    <hr>

                    <h3>Disclaimer:</h3>
                    <p>This software is provided "as is", without any warranties, guarantees, or certainties of any kind, neither express, nor implied. By downloading and/or using this software, you acknowledge that it is a new software, and, as a result, may contain bugs or issues that could potentially cause harm to your data and/or system.</p>
                    <p>We do <strong>not</strong> accept any liability for any data loss, damage, or corruption that may occur as a result of using this software, including during the backup process. <strong>You</strong> are required to take full responsibility for any actions from using this tool, and you agree to claim any and all potential risks.</p>
                    <p>By proceeding with the download and use of this software, you agree to these terms above, and confirm that you understand the potential risks involved.</p>

                    <hr>

                    <h3>Software Credits:</h3>
                    <ul>
                    <li><strong>Thethirdpuddle</strong>: for the general idea of this software and most of the <code>README.md</code> contents.</li>
                    <li><strong>ChatGPT</strong>: For help with building the code and refining the disclaimer. (don't ask why I used ChatGPT.)</li>
                    </ul>

                    <hr>
                    <h4>Any questions? DM <strong>thethirdpuddle</strong> on Discord!</h4>

                    <div style="height: 50px;"></div>
                    """


                    # Create a QLabel to display the README contents
                    about_label = QtWidgets.QLabel(readme_content)
                    about_label.setWordWrap(True)
                    about_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                    about_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # Allows text selection

                    # Create SVG widgets for images
                    gpl_svg_widget = QSvgWidget(r"assets\gpl-v3-logo.svg")
                    gpl_svg_widget.setFixedSize(90, 90)
                    pyqt_svg_widget = QSvgWidget(r"assets\Python_and_Qt.svg")
                    pyqt_svg_widget.setFixedSize(85, 85)

                    # Layout for README content and SVG images
                    scroll_content_layout = QtWidgets.QVBoxLayout()
                    scroll_content_layout.addWidget(about_label)

                    # Horizontal layout for SVG images inside the scroll area
                    svg_layout = QtWidgets.QHBoxLayout()
                    svg_layout.addStretch()
                    svg_layout.addWidget(gpl_svg_widget)
                    svg_layout.addWidget(pyqt_svg_widget)

                    # Add SVG layout to the scrollable area
                    scroll_content_layout.addLayout(svg_layout)

                    # Create a widget to hold the content inside the scroll area
                    scroll_content_widget = QtWidgets.QWidget()
                    scroll_content_widget.setLayout(scroll_content_layout)

                    # Create a QScrollArea to make the content scrollable
                    scroll_area = QtWidgets.QScrollArea()
                    scroll_area.setWidgetResizable(True)  # Allow the content to resize with the window
                    scroll_area.setWidget(scroll_content_widget)

                    # Close button
                    close_button = QtWidgets.QPushButton("Close")
                    close_button.clicked.connect(self.close)

                    # Layout for the close button and version label
                    button_version_layout = QtWidgets.QHBoxLayout()
                    button_version_layout.addWidget(version_label)  # Version label on the left
                    button_version_layout.addStretch()
                    button_version_layout.addWidget(close_button)  # Close button on the right

                    # Main layout for the dialog
                    main_layout = QtWidgets.QVBoxLayout()
                    main_layout.addWidget(scroll_area)  # Add the scrollable content
                    main_layout.addLayout(button_version_layout)  # Add version and close button layout

                    # Set the final layout
                    self.setLayout(main_layout)
                except Exception as e:
                    critical(e, False)



        # Main entry point
        def main():
            import sys
            print("Starting application...")

            app = QtWidgets.QApplication(sys.argv)
            window = BackupApp()
            def check_for_updates_gui(rawVersion):
                from PyQt5.QtWidgets import QMessageBox
                try:
                    url = "https://api.github.com/repos/TheThirdPuddle/GMod-Data-Folder-Backup-Tool/tags"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    tags = response.json()
                    if tags:
                        latest = tags[0]["name"]
                        if latest != rawVersion:
                            QMessageBox.information(window, "Update Available", f"An update is available!\n\nLatest: {latest}\nCurrent: {rawVersion}")
                        else:
                            print("You're up to date.")
                    else:
                        QMessageBox.warning(window, "Update Check Failed", "No tags found on the repository.")
                except requests.RequestException:
                    QMessageBox.warning(window, "Update Check Failed", "Could not check for updates.\nPlease try again later.")
            
            print("checking for updates...")
            check_for_updates_gui(rawVersion)
            
            # Check if arguments are passed (source folder and destination)
            if len(sys.argv) == 3:
                source_folder = sys.argv[1]
                destination_folder = sys.argv[2]
                print(f"Arguments provided. Source: {source_folder}, Destination: {destination_folder}")
                create_backup(source_folder, destination_folder, None, None, False, "backup-{date}-{time}", True, False)
            else:
                window.show()
                sys.exit(app.exec_())

        if __name__ == "__main__":
            main()
            print("exiting program...")
    except Exception as e:
        critical(e, False)
