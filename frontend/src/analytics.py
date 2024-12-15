import requests


ANALYTICS_ENDPOINT = 'http://localhost:5002'


def get_expenses_by_group(group_id):
    response = requests.get(f"{ANALYTICS_ENDPOINT}/expenses_by_group", json={'group_id': group_id})
    if response.status_code == 200:
        return response.json()
    return {}


def get_reports_by_group(group_id):
    response = requests.get(f"{ANALYTICS_ENDPOINT}/reports_by_group", json={'group_id': group_id})
    if response.status_code == 200:
        return response.json()
    return {}


def create_report(group_id, start_date, end_date, total, mean, by_category):
    report_data = {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total": int(total),
        "mean": int(mean),
        "by_category": by_category
    }
    data = {
        'group_id': group_id,
        'report_data': report_data
    }

    response = requests.post(f"{ANALYTICS_ENDPOINT}/create_report", json=data)
    return response.status_code == 200


def get_report_by_id(report_id):
    response = requests.get(f"{ANALYTICS_ENDPOINT}/report_by_id", json={'report_id': report_id})
    if response.status_code == 200:
        return response.json()
    return {}
