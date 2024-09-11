import os
import shutil
import time
import ctypes
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressBar, QCheckBox, QTextEdit

# Function to check if the script is running with admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to create a backup with progress tracking and logging
def create_backup(source_folder, destination_folder, progress_bar, log_textedit, show_log):
    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        # Get current time and format the folder name
        current_time = time.strftime("%m-%d-%Y-%H-%M-%S")
        backup_folder_name = f"backup-{current_time}"
        backup_path = os.path.join(destination_folder, backup_folder_name)

        # Create the backup folder
        os.makedirs(backup_path, exist_ok=True)

        # Count total files for progress tracking
        total_files = sum(len(files) for _, _, files in os.walk(source_folder))
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
                if show_log:
                    log_textedit.append(f"Created folder: {dest_dir}")
                    QtCore.QCoreApplication.processEvents()

            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(backup_path, os.path.relpath(source_file, source_folder))
                shutil.copy2(source_file, dest_file)

                # Log the copied file
                if show_log:
                    log_textedit.append(f"Copied file: {source_file}")
                    QtCore.QCoreApplication.processEvents()

                # Update progress bar
                files_copied += 1
                progress = int((files_copied / total_files) * 100)
                progress_bar.setValue(progress)

        # Hide the progress bar after completion
        progress_bar.hide()

        # Display success message
        QMessageBox.information(None, "Backup Success", f"Backup created at: {backup_path}")
    except Exception as e:
        progress_bar.hide()  # Hide progress bar in case of error
        if show_log:
            log_textedit.append(f"Error: {e}")
        QMessageBox.critical(None, "Backup Error", f"Failed to create backup: {e}")

# Main GUI Application
class BackupApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("GMod Data Backup Tool")
        self.setGeometry(300, 300, 400, 300)

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
        self.progress_bar.hide()  # Hide the progress bar initially

        # Checkbox to show log
        self.show_log_checkbox = QCheckBox("Show live log")
        self.show_log_checkbox.setChecked(False)

        # TextEdit for log display (hidden initially)
        self.log_textedit = QTextEdit(self)
        self.log_textedit.setReadOnly(True)
        self.log_textedit.hide()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label_source)
        layout.addWidget(self.input_source)
        layout.addWidget(self.btn_browse_source)
        layout.addWidget(self.label_dest)
        layout.addWidget(self.input_dest)
        layout.addWidget(self.btn_browse_dest)
        layout.addWidget(self.btn_backup)
        layout.addWidget(self.progress_bar)  # Add progress bar to the layout
        layout.addWidget(self.show_log_checkbox)
        layout.addWidget(self.log_textedit)  # Add log display to the layout
        self.setLayout(layout)

        # Signal connections
        self.btn_browse_source.clicked.connect(self.browse_source_folder)
        self.btn_browse_dest.clicked.connect(self.browse_destination_folder)
        self.btn_backup.clicked.connect(self.start_backup)

    def browse_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.input_source.setText(folder)

    def browse_destination_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.input_dest.setText(folder)

    def start_backup(self):
        source_folder = self.input_source.text()
        destination_folder = self.input_dest.text()

        if not source_folder or not destination_folder:
            QMessageBox.warning(self, "Input Error", "Both source and destination folders must be selected.")
            return

        if not is_admin():
            # Display error message with brief instructions
            QMessageBox.critical(self, "Admin Privileges Required",
                                 "This application must be run as an administrator to perform the backup.\n\n"
                                 "To run as administrator:\n"
                                 "1. Right-click the .exe file.\n"
                                 "2. Select 'Run as administrator'.\n\n"
                                 "Disclaimer: Running unknown apps as an administrator can carry risks. "
                                 "Only run trusted apps with elevated privileges.")
        else:
            self.progress_bar.setValue(0)  # Reset progress bar
            QtCore.QCoreApplication.processEvents()  # Force UI update before starting
            show_log = self.show_log_checkbox.isChecked()  # Check if log is enabled
            create_backup(source_folder, destination_folder, self.progress_bar, self.log_textedit, show_log)

# Main entry point
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = BackupApp()

    # Check if arguments are passed (source folder and destination)
    if len(sys.argv) == 3:
        source_folder = sys.argv[1]
        destination_folder = sys.argv[2]
        create_backup(source_folder, destination_folder, None, None, False)
    else:
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
