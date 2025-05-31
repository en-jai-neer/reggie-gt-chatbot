from openai import OpenAI
from canvasapi import Canvas
import json
from datetime import datetime
import pytz

class CanvasAPI():
    def __init__(self, api_key):
        API_URL = "https://canvas.instructure.com/"
        self.canvas = Canvas(API_URL, api_key)

        self.courses = {}
        self.assignments = {}
        self.course_names = []
        self.assignment_names = []

        self.build_course_db()

    def convert_date_to_est(self, date_str):
        input_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_tz = pytz.utc
        est_tz = pytz.timezone("US/Eastern")
        # Localize the datetime to UTC and then convert to EST
        utc_datetime = utc_tz.localize(input_datetime)
        est_datetime = utc_datetime.astimezone(est_tz)
        return est_datetime

    def get_course_assignments(self, course_name, assignment_type):
        try:
            course = self.courses[course_name]['course_object']
            assignments = course.get_assignments(bucket=assignment_type, include='submission')
            assignments = [a for a in assignments]
            res = f"For Course: {course_name}"
            for assignment in assignments:
                print(assignment.due_at)
                res += f"\nAssignment: {assignment.name}"
                if assignment.submission:
                    due_date = assignment.submission['cached_due_date']
                    res += f"\nDue at: {self.convert_date_to_est(due_date)}"
                
                    submitted_at = assignment.submission['submitted_at']
                    if submitted_at:
                        res += f"\nSubmitted at: {self.convert_date_to_est(submitted_at)}"
                        if assignment.submission['workflow_state'] == 'graded': 
                            score = assignment.submission['score']
                            res += f"\nUser's Score: {score}, Out of: {assignment.points_possible}"
                        else:
                            res += "\nAssignment not graded"
                else:
                    res += "\nAssignment not submitted"
                res += "\n-------------------------------------------"
            return res
        except:
            return "Unable to gather information"

    def get_grades(self, course_name, assignment_name):
        try:
            assignment = self.assignments[assignment_name]
            res = f"For Course: {course_name}, Assignment: {assignment_name}"
            if assignment.submission:
                submitted_at = assignment.submission['submitted_at']
                if submitted_at:
                    res += f"\nSubmitted at: {self.convert_date_to_est(submitted_at)}"
                    if assignment.submission['workflow_state'] == 'graded': 
                        score = assignment.submission['score']
                        res += f"\nUser's Score: {score}, Out of: {assignment.points_possible}"
                    else:
                        res += "\nAssignment not graded"
                else:
                    res += "\nAssignment not submitted"

            return res
        except:
            return "Unable to get information"

    def get_assignment_details(self, course_name, assignment_name):
        try:
            assignment = self.assignments[assignment_name]
            res = f"For Course: {course_name}, Assignment: {assignment_name}"
            res += f"\nDescription: {assignment.description}"
            if assignment.submission:
                due_date = assignment.submission['cached_due_date']
                res += f"\nDue at: {self.convert_date_to_est(due_date)}"

                submitted_at = assignment.submission['submitted_at']
                if submitted_at:
                    res += f"\nSubmitted at: {self.convert_date_to_est(submitted_at)}"
                    if assignment.submission['workflow_state'] == 'graded': 
                        score = assignment.submission['score']
                        res += f"\nUser's Score: {score}, Out of: {assignment.points_possible}"
                        if assignment.score_statistics:
                            res += f"\nClass Performance:"
                            res += f"\nAverage Score: {assignment.score_statistics['mean']}"
                            res += f"\nMinimum Score: {assignment.score_statistics['min']}"
                            res += f"\nMaximum Score: {assignment.score_statistics['max']}"
                            res += f"\nMedian Score: {assignment.score_statistics['median']}"
                            res += f"\nUpper Quartile Score: {assignment.score_statistics['upper_q']}"
                            res += f"\nLower Quartile Score: {assignment.score_statistics['lower_q']}"
                    else:
                        res += "\nAssignment not graded"
                else:
                    res += "\nAssignment not submitted"

            return res
        except:
            return "Unable to find information"

    def build_course_db(self):
        course_list = self.canvas.get_courses()
        course_list = [course for course in course_list]
        for course in course_list:
            if not hasattr(course, "name"): continue
            course_name = course.name
            assignment_list = course.get_assignments(include=['submission', 'score_statistics'])
            assignment_list = [a for a in assignment_list]
            self.courses[course_name] = {
            "course_object": course,
            "assignments": [{'assignment_name': assignment.name, 'assignment_id': assignment.id } for assignment in assignment_list]
            }
            self.course_names.append(course_name)
            self.assignment_names.extend([assignment.name for assignment in assignment_list])
            for assignment in assignment_list:
                self.assignments[assignment.name] = assignment