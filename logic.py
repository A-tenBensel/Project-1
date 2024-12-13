from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        """
        Method to set default state of the window.
        """
        super().__init__()
        self.setupUi(self)
        self.button_submit.clicked.connect(lambda: self.submit())
        self.label_error.setText("")
        with (open('voted.csv', 'r') as file):
            self.voted = file.read()
        self.candidates: list[str] = ['John', 'Jane', 'NA']

    def submit(self) -> None:
        """
        Method to submit voter id and who they have voted for. If an invalid option, displays error message.
        """
        try:
            person_id: int = int(self.input_id.text().strip())
            if len(str(person_id)) != 5:
                raise ValueError
            if str(person_id) in self.voted:
                raise KeyError
            if self.candidates[self.radio_answer.checkedId()] == 'NA':
                raise IndexError

            with open('voted.csv', 'a', newline='') as file:
                content = csv.writer(file)
                content.writerow((person_id, self.candidates[self.radio_answer.checkedId()]))
            self.voted += f"{person_id},{self.candidates[self.radio_answer.checkedId()]}\n"
            self.input_id.clear()
            self.label_error.setText("")
        except ValueError:
            self.label_error.setText("Invalid ID")
        except KeyError:
            self.label_error.setText("Already Voted")
        except IndexError:
            self.label_error.setText("Select Candidate")
        finally:
            if self.radio_answer.checkedButton() is not None:
                self.radio_answer.setExclusive(False)
                self.radio_answer.checkedButton().setChecked(False)
                self.radio_answer.setExclusive(True)
