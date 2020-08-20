# /usr/bin/env python3


def ga_report(view_id, start_date, end_date):
    body = {
        'reportRequests': [
            {
                'viewId': view_id,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': [{'expression': 'ga:users'}, {'expression': 'ga:sessions'}],
                'dimensions': [{'name': 'ga:date'}, {'name': 'ga:country'}]
            }]
    }

    metrics_len = len(body.get('reportRequests')[0].get('metrics'))
    dimensions_len = len(body.get('reportRequests')[0].get('dimensions'))
    return body, metrics_len, dimensions_len
