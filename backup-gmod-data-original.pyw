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

if True:
    try:
        import os
        import shutil
        import time
        import ctypes
        import sys
        import json
        from PyQt5 import QtWidgets, QtCore
        from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressBar, QCheckBox, QTextEdit, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox

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
                # If the file doesn't exist, return default settings
                print("Settings file not found. Loading default settings...")
                return {
                    "backup_folder_format": "backup-{date}-{time}",
                    "size_restriction": True,
                    "enable_logging": False  # New setting for logging
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
            except Exception as general_error:
                print(f"Unexpected error loading settings: {general_error}")
                setting_error_type = type(general_error).__name__
                setting_error_code = error_codes.get(setting_error_type, "unknown")
                QtWidgets.QMessageBox.critical(
                    None,
                    "Unexpected Error",
                    f"An unexpected error has occurred!\n\n"
                    f"Error info:\n"
                    f"type: {setting_error_type}\ncode: {setting_error_code}\ndetails: {str(general_error)}"
                )
            sys.exit(1)  # Exit the application after showing the error

        # Function to save settings to a JSON file
        def save_settings(settings):
            try:
                print("Saving settings to settings.json...")
                with open('settings.json', 'w') as f:
                    json.dump(settings, f)
                print("Settings saved successfully.")
            except Exception as e:
                print(f"Failed to save settings: {e}")

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
        def create_backup(source_folder, destination_folder, progress_bar, log_textedit, show_log, backup_folder_format, size_restriction, enable_logging):
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

        # Settings Dialog
        class SettingsDialog(QDialog):
            def __init__(self, settings, parent=None):
                super().__init__(parent)
                
                print("Initializing Settings Dialog...")
                self.settings = settings
                self.setWindowTitle("Additional Backup Settings")
                self.setGeometry(300, 300, 400, 150)

                # Folder name format label and input
                self.label_format = QLabel("Backup folder name format:")
                self.input_format = QLineEdit(self)
                self.input_format.setText(self.settings['backup_folder_format'])
                self.label_format_guide = QLabel("Use {date} for current date and {time} for current time.")

                # Folder size restriction checkbox
                self.size_restriction_checkbox = QCheckBox("folder size restriction (disabling this may cause the tool to crash if folder is larger than 1GB)", self)
                self.size_restriction_checkbox.setChecked(self.settings['size_restriction'])

                # Logging option checkbox
                self.enable_logging_checkbox = QCheckBox("Enable logging folder", self)
                self.enable_logging_checkbox.setChecked(self.settings['enable_logging'])

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
                layout.addWidget(self.button_box)
                self.setLayout(layout)

            def accept(self):
                print("Saving settings from Settings Dialog...")
                # Update settings when OK is pressed
                self.settings['backup_folder_format'] = self.input_format.text()
                self.settings['size_restriction'] = self.size_restriction_checkbox.isChecked()
                self.settings['enable_logging'] = self.enable_logging_checkbox.isChecked()  # Save the logging setting
                save_settings(self.settings)  # Save settings to JSON
                print("Settings updated and saved successfully.")
                super().accept()

        # Main GUI Application
        class BackupApp(QtWidgets.QWidget):
            def __init__(self):
                super().__init__()

                print("Initializing Backup Application GUI...")
                # Load settings from JSON file
                self.settings = load_settings()

                # Window properties
                self.setWindowTitle("GMod Data Backup Tool")
                self.setGeometry(300, 300, 400, 100)

                # Default source directory
                default_source_directory = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data"

                # Labels
                self.label_source = QtWidgets.QLabel("Source Folder (GMod Data):")
                self.label_dest = QtWidgets.QLabel("Destination Folder for Backup:")

                # Input fields with default source directory
                self.input_source = QtWidgets.QLineEdit(self)
                self.input_source.setText(default_source_directory)  # Set default value
                self.input_dest = QtWidgets.QLineEdit(self)

                # Browse buttons
                self.btn_browse_source = QtWidgets.QPushButton("Browse", self)
                self.btn_browse_dest = QtWidgets.QPushButton("Browse", self)

                # Backup button
                self.btn_backup = QtWidgets.QPushButton("Create Backup", self)

                # Progress bar
                self.progress_bar = QProgressBar(self)
                self.progress_bar.setValue(0)
                self.progress_bar.show()  # Show the progress bar initially

                # Settings button
                self.btn_settings = QtWidgets.QPushButton("Additional Settings", self)

                # Checkbox to show log
                self.show_log_checkbox = QCheckBox("Show live log")
                self.show_log_checkbox.setChecked(False)

                # TextEdit for log display (hidden initially)
                self.log_textedit = QTextEdit(self)
                self.log_textedit.setReadOnly(True)
                self.log_textedit.hide()

                # Layout
                layout = QtWidgets.QVBoxLayout()

                # Create horizontal layout for source input and browse button
                source_layout = QHBoxLayout()
                source_layout.addWidget(self.input_source)
                source_layout.addWidget(self.btn_browse_source)

                # Create horizontal layout for destination input and browse button
                dest_layout = QHBoxLayout()
                dest_layout.addWidget(self.input_dest)
                dest_layout.addWidget(self.btn_browse_dest)

                # Create horizontal layout for settings and backup button
                options_layout = QHBoxLayout()
                options_layout.addWidget(self.btn_settings)
                options_layout.addWidget(self.btn_backup)

                # Add source label and horizontal layout for input and button
                layout.addWidget(self.label_source)
                layout.addLayout(source_layout)

                # Add destination label and horizontal layout for input and button
                layout.addWidget(self.label_dest)
                layout.addLayout(dest_layout)

                # Add options layout (settings and create backup button)
                layout.addLayout(options_layout)

                # Add the rest of the widgets
                layout.addWidget(self.progress_bar)  # Add progress bar to the layout
                layout.addWidget(self.show_log_checkbox)
                layout.addWidget(self.log_textedit)  # Add log display to the layout
                self.setLayout(layout)

                # Signal connections
                self.btn_browse_source.clicked.connect(self.browse_source_folder)
                self.btn_browse_dest.clicked.connect(self.browse_destination_folder)
                self.btn_backup.clicked.connect(self.start_backup)
                self.btn_settings.clicked.connect(self.open_settings)

                # Connect checkbox to toggle visibility and resize
                self.show_log_checkbox.stateChanged.connect(self.toggle_log_visibility)

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

            def show_admin_warning(self):
                print("Admin privileges not detected. Showing admin warning...")
                # Create a dialog to display the warning
                dialog = QDialog(self)
                dialog.setWindowTitle("Admin Privileges Required")
                
                # Message explaining why admin privileges are needed
                warning_label = QLabel("This application may need to be run as an administrator to perform the backup.\n\n"
                                    "To run as administrator:\n"
                                    "1. Right-click the .exe file.\n"
                                    "2. Select 'Run as administrator'.\n\n"
                                    "Caution: Running unknown1 apps as an administrator can carry risks. "
                                    "Only run apps you can trust with elevated privileges.", dialog)

                # Notice for running without admin
                notice_label = QLabel("Warning: The backup process may not work correctly if you proceed without admin rights.", dialog)
                
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
                    create_backup(self.input_source.text(), self.input_dest.text(), self.progress_bar, self.log_textedit, show_log, self.settings['backup_folder_format'], self.settings['size_restriction'], self.settings['enable_logging'])

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
                    create_backup(source_folder, destination_folder, self.progress_bar, self.log_textedit, show_log, self.settings['backup_folder_format'], self.settings['size_restriction'], self.settings['enable_logging'])

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
                else:
                    print("Log visibility disabled.")
                    self.log_textedit.hide()
                    self.setMinimumHeight(150)
                    self.setMinimumWidth(400)

                # Adjust the window size to fit the content
                self.adjustSize()

        # Main entry point
        def main():
            import sys
            print("Starting application...")
            app = QtWidgets.QApplication(sys.argv)
            window = BackupApp()

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
    except Exception as e:
        unex_error_type = type(e).__name__
        unex_error_code = error_codes.get(unex_error_type, "unknown")
        print(f"Unexpected error occurred: {e}")
        QtWidgets.QMessageBox.critical(
                    None,
                    "Unexpected Error",
                    f"An unexpected error has occurred!\n\nError details:\ntype: '{unex_error_type}'\ncode: '{unex_error_code}'\ndetails: '{e}'",
                )
        sys.exit(1)