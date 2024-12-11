import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QHBoxLayout, \
    QPushButton, QFrame, QGroupBox, QDateEdit, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QMessageBox

import json
import csv


class MainWindow(QWidget):
    def __init__(self):
        color = "#FFFFFF"
        super().__init__()
        self.setWindowTitle("PowerPoint MVP")  # Set window title
        self.setStyleSheet(f"background-color: {color}	;")
        self.setGeometry(0, 10, 1430, 0)  # Set window size and position

        self.completed_setups = set()  # Track completed setups by their names
        self.user_details = {}  # Store the user's details (Device SN, Operator, Date)

        # Initialize UI components
        self.main_layout = QVBoxLayout()
        self.top_button_layout = QHBoxLayout()
        # set Css for the top button

        self.form_layout = QFormLayout()
        # set background color for the form layout
        self.top_row_layout = QHBoxLayout()

        # Mapping screens
        self.screens = {
            "Test Setup #2:Telescope: Range, manual.": SetupScreen2(self),
            "Test Setup #3:Lift: Range, powered": SetupScreen3(self),
            "Test Setup #4:Deflection, vertical": SetupScreen4(self),
            "Test Setup #5:(Right Bracket) Deflection, horizontal": SetupScreen5(self),
            "Test Setup #6:(Right Bracket) Lift: Behavior, motion": SetupScreen6(self),
            "Test Setup #7:(Left Bracket) Deflection, horizontal": SetupScreen7(self),
            "Test Setup #8:(Left Bracket) Lift: Behavior, motion": SetupScreen8(self)
        }

        self.device_sn = QLineEdit()
        self.operator = QLineEdit()
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.device_sn.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")
        self.operator.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")
        self.date.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")

        # Set up the UI
        self.setup_top_button()
        self.setup_form_layout()
        self.setup_test_select_section()
        self.main_layout.setSpacing(40)  # Remove spacing between widgets

        # Set the layout for the window
        self.setLayout(self.main_layout)

    def setup_top_button(self):
        """Set up the 'Generate Report' button at the top-right corner."""
        self.top_button_layout.setAlignment(Qt.AlignRight)  # Align the button to the right
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px;")
        self.top_button_layout.addWidget(generate_report_button)

        # Add the top button layout to the main layout
        self.main_layout.addLayout(self.top_button_layout)

    def setup_form_layout(self):
        # Top Form Color Background (Device SN, Operator, Date)
        color = "#3D75A2"
        """Set up the form layout with labels and input fields."""
        self.top_row_layout.addWidget(QLabel("Device SN:"))
        self.top_row_layout.addWidget(self.device_sn)
        self.top_row_layout.addWidget(QLabel("Operator:"))
        self.top_row_layout.addWidget(self.operator)
        self.top_row_layout.addWidget(QLabel("Date:"))
        self.top_row_layout.addWidget(self.date)

        # Add the top row layout to the form layout
        self.form_layout.addRow(self.top_row_layout)

        # Submit button (initially disabled)
        submit_button = QPushButton("Submit")
        # submit_button.setStyleSheet("""
        #     background-color: #808080; color: white; padding: 10px; border-radius: 5px;
        #     transition: background-color 0.3s;
        # """)
        submit_button.setEnabled(False)  # Disable initially
        submit_button.clicked.connect(self.submit_details)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3b7e99;
            }
        """)

        self.submit_button = submit_button  # Save reference to button

        self.top_row_layout.addWidget(submit_button)

        # Add a horizontal line for separation
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        self.form_layout.addRow(horizontal_line)

        # Wrap the form layout inside a QWidget to apply a stylesheet
        form_widget = QWidget()
        form_widget.setLayout(self.form_layout)
        form_widget.setStyleSheet(f"background-color:{color};")  # Set background color for the form section

        # Add the form widget to the main layout
        self.main_layout.addWidget(form_widget)

        # Connect signals to validate form fields
        self.device_sn.textChanged.connect(self.update_submit_button_state)
        self.operator.textChanged.connect(self.update_submit_button_state)
        self.date.dateChanged.connect(self.update_submit_button_state)

    def update_submit_button_state(self):
        """Enable or disable the submit button based on whether all fields are filled."""
        if self.device_sn.text() and self.operator.text() and self.date.date():
            self.submit_button.setEnabled(True)  # Enable the button when all fields are filled
            self.submit_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #3b7e99;
                }
            """)
        else:
            self.submit_button.setEnabled(False)  # Disable the button if any field is empty
            self.submit_button.setStyleSheet("""
                QPushButton {
                    background-color: grey;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: grey;
                }
            """)

    def setup_test_select_section(self):
        # Setups form color Background (Setup #2 to Setup #8)
        color = "#3D75A2"
        """Set up the test selection section with button-like rows and checkboxes."""
        test_select_group = QGroupBox("Select Test Setup")
        test_select_group.setStyleSheet(f"background-color:{color} ; color: white; padding: 100px;")
        test_select_layout = QVBoxLayout()

        test_setups = [
            "Test Setup #2:Telescope: Range, manual.",
            "Test Setup #3:Lift: Range, powered",
            "Test Setup #4:Deflection, vertical",
            "Test Setup #5:(Right Bracket) Deflection, horizontal",
            "Test Setup #6:(Right Bracket) Lift: Behavior, motion",
            "Test Setup #7:(Left Bracket) Deflection, horizontal",
            "Test Setup #8:(Left Bracket) Lift: Behavior, motion"
        ]

        self.setup_buttons = {}  # Store buttons for dynamic style updates

        # Create buttons for each test setup
        for setup in test_setups:
            button = QPushButton(setup)
            self.setup_buttons[setup] = button  # Store the button for later reference
            self.update_button_style(setup)  # Apply the appropriate style based on completion status

            button.setEnabled(False)  # Disable the buttons initially
            button.setStyleSheet("background-color: #cccccc; color: black; padding: 10px; border-radius: 5px;")
            button.clicked.connect(lambda checked, text=setup: self.redirect_to_screen(text))
            test_select_layout.addWidget(button)

        # Set the layout for the test select group
        test_select_group.setLayout(test_select_layout)

        # Add the test select group to the main layout
        self.main_layout.addWidget(test_select_group)

    def update_button_style(self, setup):
        """Update the button's color based on its completion status."""
        if setup in self.completed_setups:
            self.setup_buttons[setup].setStyleSheet(
                "background-color: orange; color: white; padding: 10px; border-radius: 5px;"
            )
        else:
            self.setup_buttons[setup].setStyleSheet(
                """
                QPushButton {
                    background-color: #3b7e99; 
                    color: white; 
                    padding: 10px; 
                    margin-bottom: 5px; 
                    border-radius: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #2a697e;
                }
                QPushButton:pressed {
                    background-color: #1e4d5f;
                }
                """
            )

    def submit_details(self):
        """Save the user details to a JSON file and enable the test setup section."""
        self.user_details["device_sn"] = self.device_sn.text()
        self.user_details["operator"] = self.operator.text()
        self.user_details["date"] = self.date.date().toString()
        self.user_details["Setup2 - Unit Reach Marker"] = None
        self.user_details["Setup2 - Measured Max Height"] = None
        self.user_details["Setup3 - Unit Reach Marker"] = None
        self.user_details["Setup3 - Measured Max Height"] = None
        self.user_details["Setup4 - Click to Zero Vertical Position Dial"] = False
        self.user_details["Setup4 - Click to record vertical deflection"] = False

        # Save the data to a JSON file
        if os.path.exists("user_details.json"):
            # If the file exists, read the existing data
            with open("user_details.json", "r") as f:
                existing_data = json.load(f)
        else:
            # If the file doesn't exist, initialize an empty list
            existing_data = []

            # Append the new data to the existing data
        existing_data.append(self.user_details)

        # Save the updated data to the JSON file
        with open("user_details.json", "w") as f:
            json.dump(existing_data, f, indent=4)
        # Show the popup
        self.show_popup("Data Saved! Setups enabled now")

        # Enable the test setup buttons after submitting
        for button in self.setup_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet("background-color: #3b7e99; color: white; padding: 10px; border-radius: 5px;")

        # Optionally, disable the form section after submission
        self.device_sn.setEnabled(False)
        self.operator.setEnabled(False)
        self.date.setEnabled(False)

    def show_popup(self, message):
        """Show a popup dialog with the given message."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Info")
        dialog.setStyleSheet("background-color: lightgreen; color: black;")
        layout = QVBoxLayout(dialog)

        label = QLabel(message)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def redirect_to_screen(self, setup_text):
        """Handle redirection based on the setup selected."""
        if setup_text in self.screens:
            self.hide()  # Hide the main window
            self.screens[setup_text].show()

            # Mark the setup as completed when the user exits the setup screen
            self.screens[setup_text].go_back = lambda: (
                self.mark_setup_completed(setup_text),

                super(self.screens[setup_text].__class__, self.screens[setup_text]).go_back()
            )

        else:
            print(f"No screen defined for: {setup_text}")

    def mark_setup_completed(self, setup):
        """Mark a setup as completed and update its button style."""
        self.completed_setups.add(setup)
        self.update_button_style(setup)

    import csv

    def generate_csv_report(self):
        """Generate a CSV report from the user_details.json file."""
        # Check if the JSON file exists
        if not os.path.exists("user_details.json"):
            self.show_popup("No data available to generate report.")
            return

        # Read data from the JSON file
        with open("user_details.json", "r") as json_file:
            user_data = json.load(json_file)

        # Define the CSV file path
        csv_file_path = "user_details_report.csv"

        # Open the CSV file for writing
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # Write the header row based on the keys of the first dictionary
            if user_data:
                header = list(user_data[0].keys())
                writer.writerow(header)

                # Write the data rows
                for entry in user_data:
                    writer.writerow(entry.values())

        # Notify the user
        self.show_popup(f"Report generated successfully: {csv_file_path}")

    def setup_top_button(self):
        """Set up the 'Generate Report' button at the top-right corner."""
        self.top_button_layout.setAlignment(Qt.AlignRight)  # Align the button to the right
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Lighter green on hover */
            }
        """)
        generate_report_button.clicked.connect(self.generate_csv_report)  # Connect to the report generation method
        self.top_button_layout.addWidget(generate_report_button)

        # Add the top button layout to the main layout
        self.main_layout.addLayout(self.top_button_layout)


# ==============================================================
class SetupScreenInside(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Reference to the main screen
        self.setGeometry(0, 10, 1430, 0)
        self.setStyleSheet("background-color: lightblue;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add a Back button
        back_button = QPushButton("Back to Main Screen")
        back_button.setStyleSheet(
            "background-color: #f44336; color: white; padding: 10px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)

    def go_back(self):
        """Go back to the main screen."""
        self.hide()
        self.parent.show()


class SetupScreen2(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #2")

        # Welcome label
        welcome_label = QLabel("Setup #2 : Telescope: Range, manual")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.layout.addWidget(welcome_label)

        # Add an image
        image_label = QLabel(self)
        image_label.setPixmap(
            QPixmap("img.png").scaled(1000, 1300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)

        # Create a horizontal layout for dropdown and submit button
        dropdown_row_layout_label = QHBoxLayout()
        dropdown_row_layout = QHBoxLayout()
        self.dropdown_label = QLabel("Unit Reach Marker:")
        self.dropdown_label.setStyleSheet("font-size: 14px; color: #333; margin-right: 10px;")

        # Dropdown (combo box) with Yes and No options
        self.dropdown = QComboBox()
        self.dropdown.addItems(["---", "No", "Yes"])
        self.dropdown.setStyleSheet(
            """
            QComboBox {
                background-color: white; 
                padding: 5px; 
                border: 1px solid #ccc; 
                border-radius: 3px;
                color: #333;
            }
            QComboBox::drop-down {
                border-left: 1px solid #ccc;
            }
            """
        )
        self.measured_max_height_label = QLabel("Measured Max Height:")
        self.measured_max_height_input = QLineEdit()
        self.measured_max_height_input.setVisible(False)  # Hidden by default
        self.measured_max_height_label.setVisible(False)  # Hide label as well # Disabled by default
        self.dropdown.currentTextChanged.connect(self.update_submit_button_state)  # Connect dropdown to handler

        dropdown_row_layout_label.addWidget(self.dropdown_label)
        dropdown_row_layout.addWidget(self.dropdown)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: grey; 
                color: #ddd;
            }
            """
        )
        self.submit_button.clicked.connect(self.submit_and_redirect)
        dropdown_row_layout.addWidget(self.submit_button)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(dropdown_row_layout_label)
        self.layout.addLayout(dropdown_row_layout)
        self.layout.addWidget(self.measured_max_height_label)
        self.layout.addWidget(self.measured_max_height_input)

        # Initialize button state
        self.update_submit_button_state()
        self.dropdown.currentTextChanged.connect(self.on_marker_value_changed)

    def on_marker_value_changed(self, value):
        """Show or hide the Measured Max Height field based on the marker value."""
        if value == "No":
            self.measured_max_height_label.setVisible(True)  # Show label
            self.measured_max_height_input.setVisible(True)  # Show field
            self.measured_max_height_label.setStyleSheet("color: black;")
            self.measured_max_height_input.setStyleSheet("background-color: white; color:black")
        else:
            self.measured_max_height_label.setVisible(False)  # Hide label
            self.measured_max_height_input.setVisible(False)  # Hide field
            self.measured_max_height_input.clear()  # Clear the field value

    def update_submit_button_state(self):
        """Enable or disable the submit button based on the dropdown selection."""
        self.submit_button.setEnabled(self.dropdown.currentText() != "---")

    def submit_and_redirect(self):
        """Handle submit button click."""
        selected_option = self.dropdown.currentText()
        print(f"Selected option: {selected_option}")
        # save data in the json file
        if selected_option == "Yes":
            data = {
                "Setup2 - Unit Reach Marker": selected_option,
                "Setup2 - Measured Max Height": None

            }
        else:
            data = {
                "Setup2 - Unit Reach Marker": selected_option,
                "Setup2 - Measured Max Height": self.measured_max_height_input.text()
            }
        # open user_details.json file and save data with last record
        with open("user_details.json", "r") as f:
            existing_data = json.load(f)
            existing_data[-1].update(data)
        with open("user_details.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        # Optional: Print for debug
        self.go_back()  # Redirect to the main screen


class SetupScreen3(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #3")

        # Welcome label
        welcome_label = QLabel("Setup #2 : Lift: Range, Powered")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.layout.addWidget(welcome_label)

        # Add an image
        image_label = QLabel(self)
        image_label.setPixmap(
            QPixmap("img.png").scaled(1000, 1300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)

        # Create a horizontal layout for dropdown and submit button
        dropdown_row_layout_label = QHBoxLayout()
        dropdown_row_layout = QHBoxLayout()
        self.dropdown_label = QLabel("Unit Reach Marker:")
        self.dropdown_label.setStyleSheet("font-size: 14px; color: #333; margin-right: 10px;")

        # Dropdown (combo box) with Yes and No options
        self.dropdown = QComboBox()
        self.dropdown.addItems(["---", "No", "Yes"])
        self.dropdown.setStyleSheet(
            """
            QComboBox {
                background-color: white; 
                padding: 5px; 
                border: 1px solid #ccc; 
                border-radius: 3px;
                color: #333;
            }
            QComboBox::drop-down {
                border-left: 1px solid #ccc;
            }
            """
        )
        self.measured_max_height_label = QLabel("Measured Max Height:")
        self.measured_max_height_input = QLineEdit()
        self.measured_max_height_input.setVisible(False)  # Hidden by default
        self.measured_max_height_label.setVisible(False)  # Hide label as well # Disabled by default
        self.dropdown.currentTextChanged.connect(self.update_submit_button_state)  # Connect dropdown to handler
        dropdown_row_layout_label.addWidget(self.dropdown_label)
        dropdown_row_layout.addWidget(self.dropdown)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: grey; 
                color: #ddd;
            }
            """
        )
        self.submit_button.clicked.connect(self.submit_and_redirect)
        dropdown_row_layout.addWidget(self.submit_button)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(dropdown_row_layout_label)
        self.layout.addLayout(dropdown_row_layout)
        self.layout.addWidget(self.measured_max_height_label)
        self.layout.addWidget(self.measured_max_height_input)

        # Initialize button state
        self.update_submit_button_state()
        self.dropdown.currentTextChanged.connect(self.on_marker_value_changed)

    def on_marker_value_changed(self, value):
        """Show or hide the Measured Max Height field based on the marker value."""
        if value == "No":
            self.measured_max_height_label.setVisible(True)  # Show label
            self.measured_max_height_input.setVisible(True)  # Show field
            self.measured_max_height_label.setStyleSheet("color: black;")
            self.measured_max_height_input.setStyleSheet("background-color: white; color:black")
        else:
            self.measured_max_height_label.setVisible(False)  # Hide label
            self.measured_max_height_input.setVisible(False)  # Hide field
            self.measured_max_height_input.clear()  # Clear the field value

    def update_submit_button_state(self):
        """Enable or disable the submit button based on the dropdown selection."""
        self.submit_button.setEnabled(self.dropdown.currentText() != "---")

    def submit_and_redirect(self):
        """Handle submit button click."""
        selected_option = self.dropdown.currentText()
        print(f"Selected option: {selected_option}")  # Optional: Print for debug

        # save data in the json file
        if selected_option == "Yes":
            data = {
                "Setup3 - Unit Reach Marker": selected_option,
                "Setup3 - Measured Max Height": None

            }
        else:
            data = {
                "Setup3 - Unit Reach Marker": selected_option,
                "Setup3 - Measured Max Height": self.measured_max_height_input.text()
            }
        # open user_details.json file and save data with last record
        with open("user_details.json", "r") as f:
            existing_data = json.load(f)
            existing_data[-1].update(data)
        with open("user_details.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        self.go_back()  # Redirect to the main screen


class SetupScreen4(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.current_step = 0  # Track the current step
        self.steps = [  # Define the steps with images and labels
            {"image": "img_2.png", "label": "Step 1: Check this first."},
            {"image": "img_3.png", "label": "Step 2: Click to Zero Vertical Position Dial. "},
            {"image": "img_4.png", "label": "Click to record vertical deflection."}
        ]

        # Create UI elements
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.update_image()  # Load and scale the first image

        self.checkbox = QCheckBox(self.steps[self.current_step]["label"])
        self.checkbox.setStyleSheet("color: black; font-size: 14px;")
        self.checkbox.stateChanged.connect(self.update_button_state)

        self.next_button = QPushButton("Next")
        self.style_button(self.next_button, enabled=False)  # Set initial grey style
        self.next_button.clicked.connect(self.next_step)

        # Layout setup
        self.step_layout = QVBoxLayout()
        self.step_layout.addWidget(self.image_label)
        self.step_layout.addWidget(self.checkbox)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.next_button)

        self.layout.addLayout(self.step_layout)
        self.layout.addLayout(self.button_layout)

    def style_button(self, button, enabled):
        """Update the button's color based on its state."""
        if enabled:
            button.setEnabled(True)
            button.setStyleSheet(
                "background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;"
            )
        else:
            button.setEnabled(False)
            button.setStyleSheet(
                "background-color: grey; color: white; padding: 10px; border-radius: 5px;"
            )

    def update_button_state(self):
        """Enable the button if the checkbox is checked, otherwise disable it."""
        if self.checkbox.isChecked():
            self.style_button(self.next_button, enabled=True)
        else:
            self.style_button(self.next_button, enabled=False)

    def update_image(self):
        """Update the displayed image with proper scaling."""
        pixmap = QPixmap(self.steps[self.current_step]["image"])
        self.image_label.setPixmap(
            pixmap.scaled(1000, 1300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def next_step(self):
        """Handle the transition to the next step."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_image()  # Update to the new image
            self.checkbox.setText(self.steps[self.current_step]["label"])
            self.checkbox.setChecked(False)  # Reset the checkbox
            is_last_step = self.current_step == len(self.steps) - 1
            self.next_button.setText("Submit" if is_last_step else "Next")
            self.style_button(self.next_button, enabled=False)  # Disable the button until checkbox is checked
        else:
            self.submit()

    def submit(self):
        """Redirect to the main screen and mark this setup as completed."""
        self.parent.mark_setup_completed("Test Setup #4:Deflection, vertical")  # Mark as completed
        # save data in the json file
        data = {
            "Setup4 - Click to Zero Vertical Position Dial": "Yes",
            "Setup4 - Click to record vertical deflection": "Yes"
        }
        # open user_details.json file and save data with last record
        with open("user_details.json", "r") as f:
            existing_data = json.load(f)
            existing_data[-1].update(data)
        with open("user_details.json", "w") as f:
            json.dump(existing_data, f, indent=4)
        self.hide()
        self.parent.show()


class SetupScreen5(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #5")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen6(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #6")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen7(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #7")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen8(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #8")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
