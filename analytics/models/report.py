import json


class Report:
    def __init__(self, report_id, group_id, name, generated_date, data):
        self.report_id = report_id
        self.group_id = group_id
        self.name = name
        self.generated_date = generated_date
        self.data = data

    @staticmethod
    def get_reports_by_group(cursor, group_id):
        query = """
        SELECT report_id, group_id, created_date, report_data 
        FROM report
        WHERE group_id = %s 
        ORDER BY created_date DESC
        """
        cursor.execute(query, (group_id,))
        result = cursor.fetchall()
        return [{
            'report_id': report[0], 
            'group_id': report[1], 
            'created_date': report[2], 
            'report_data': report[3]
        } for report in result]


    @staticmethod
    def get_report_by_id(cursor, report_id):
        query = """
        SELECT report_id, created_date, report_data 
        FROM report
        WHERE report_id = %s 
        ORDER BY created_date DESC
        """
        cursor.execute(query, (report_id,))
        result = cursor.fetchall()[0]
        return {
            'report_id': result[0], 
            'created_date': result[1], 
            'report_data': result[2]
        } 
    

    @staticmethod
    def create_report(cursor, group_id, report_data):
        query = """
        INSERT INTO report (group_id, report_data)
        VALUES (%s, %s)
        """
        cursor.execute(query, (group_id, json.dumps(report_data)))
