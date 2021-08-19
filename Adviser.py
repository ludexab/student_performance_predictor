from kivymd.app import MDApp
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from AdviserDSS import mymodel
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
import sqlite3
import datetime

Window.size = (800, 700)


class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def string_to_list(self, result):
        result = str(result)
        split_result = result.split(',')
        list_result = [float(i) for i in split_result]
        if len(list_result) < 9:
            for i in range(9 - len(list_result)):
                list_result.append(0.0)
        return list_result

    def load_details(self, matric_no):

        self.ids.student_details.clear_widgets()
        try:
            db = sqlite3.connect('student_db.db')
            csr = db.cursor()
            details = csr.execute("select * from details where matric = :matric",
                               {'matric': matric_no}).fetchall()[0]

            name = 'Name: ' + details[0]
            mat_no = 'Matric No: ' + details[1]
            department = 'Department: ' + details[2]
            level = 'Level: ' + str(details[3])
            grades = 'Grades: ' + details[4]

            name_label = MDLabel()
            name_label.text = name.upper()

            mat_label = MDLabel()
            mat_label.text = mat_no.upper()

            dep_label = MDLabel()
            dep_label.text = department.upper()

            level_label = MDLabel()
            level_label.text = level.upper()

            grade_label = MDLabel()
            grade_label.text = ''

            gpas = details[4].split(',')
            gpa_years = []
            for i, gpa in enumerate(gpas):
                if i == 0:
                    gpa_years.append('EntryPoint: ' + gpa)
                else:
                    gpa_years.append('gpa{}: '.format(i) + gpa)
            for gpa_year in gpa_years:
                grade_label.text = grade_label.text + gpa_year + '   '

            labels = [name_label, mat_label, dep_label, level_label, grade_label]
            for label in labels:
                self.ids.student_details.add_widget(label)

            self.ids.predict_button.disabled = False

        except Exception:
            dialog = MDDialog(title='INVALID INPUT', text='Detail not in database')
            dialog.size_hint_x = .5
            dialog.open()

    def comment(self, comment):
        matric = self.ids.matric.text
        try:
            db = sqlite3.connect('student_db.db')
            csr = db.cursor()
            is_matric = csr.execute("select matric from details where matric = :matric",
                        {'matric': matric}).fetchone()
            if is_matric:
                csr.execute("""insert into comments (cid, comment, cdate)
                            values(:cid, :comment, :cdate)""",
                          {'cid': matric, 'comment': comment, 'cdate':datetime.datetime.now()})
                db.commit()
                db.close()
                dialog = MDDialog(title='SUCCESS', text='comment added successfully')
                dialog.size_hint_x = .5
                dialog.open()
            else:
                db.close()
                dialog = MDDialog(title='ERROR', text='failed to add comment')
                dialog.size_hint_x = .5
                dialog.open()
        except Exception:
            dialog = MDDialog(title='ERROR', text='Failed to connect to database')
            dialog.size_hint_x = .5
            dialog.open()

    def predict(self, student_detail):
        try:
            if student_detail != '':
                if '/' in student_detail:
                    db = sqlite3.connect('student_db.db')
                    csr = db.cursor()
                    cgpa = csr.execute("select grades from details where matric = :matric",
                                {'matric': student_detail}).fetchone()[0]
                    cgpa = self.string_to_list(cgpa)
                    cgpa = mymodel.make_prediction(cgpa)
                    cgpa = float(cgpa[0][0])
                    self.ids.next_cgpa.text = str(round(cgpa, 2))
                else:
                    cgpa = self.string_to_list(student_detail)
                    cgpa = mymodel.make_prediction(cgpa)
                    cgpa = float(cgpa[0][0])
                    self.ids.next_cgpa.text = str(round(cgpa, 2))
            else:
                self.ids.next_cgpa.text = ''
                dialog = MDDialog(title='Please enter inputs')
                dialog.size_hint_x = .5
                dialog.open()
        except Exception:
            dialog = MDDialog(title='INVALID INPUT', text='Please check inputs and try again')
            dialog.size_hint_x = .5
            dialog.open()


class AdviserApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = '900'
        self.theme_cls.accent_palette = 'Blue'
        return HomePage()


AdviserApp().run()
