# /usr/bin/env python3

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def initialize_analyticsreporting(key_file_location, scopes):
    """Initializes an Analytics Reporting API V4 service object.p

   Returns:
     An authorized Analytics Reporting API V4 service object.
   """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, body):
    """Queries the Analytics Reporting API V4.

   Args:
     analytics: An authorized Analytics Reporting API V4 service object.
   Returns:
     The Analytics Reporting API V4 response.
   """
    return analytics.reports().batchGet(body=body).execute()


def data_extract(response, metrics_len, dimensions_len):
    columns = list()
    data = list()
    print(response.get('reports'))
    for report in response.get('reports'):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [0])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries')
        for number in range(dimensions_len):
            columns.append(dimensionHeaders[number])
        for number in range(metrics_len):
            columns.append(metricHeaders[number].get('name'))
        for report in response.get('reports'):
            for rows in report.get('data').get('rows'):
                for dimensions, metrics in zip([rows.get('dimensions')], rows.get('metrics')):
                    temp = []
                    for number in range(dimensions_len):
                        temp.append(dimensions[number])
                    for number in range(metrics_len):
                        temp.append(metrics.get('values')[number])
                    data.append(temp)
    # print(data)
    # print(columns)
    return data, columns


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ', dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range:', str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ':', value)


def create_csv_file(data, columns, end_date=None, start_date=None):
    df = pd.DataFrame(data=data, columns=columns)
    filename = f"./{start_date}_{end_date}.csv"
    df.to_csv(filename, index=False)
