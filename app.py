# /usr/bin/env python3

"""
References:
    https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
    https://big-data-demystified.ninja/2020/08/20/google-analytics-full-etl/
"""

import argparse
from ga_reporting.config import KEY_FILE_LOCATION, VIEW_ID
from ga_reporting.ga_extractor import (data_extract, create_csv_file,
                                       get_report, initialize_analyticsreporting)
from ga_reporting.reporting_query import ga_report

SCOPES = 'https://www.googleapis.com/auth/analytics.readonly'

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument('--start_date', type=str,
                           help=('Start date of the requested date range in '
                                 'YYYY-MM-DD format.'))
    argparser.add_argument('--end_date', type=str,
                           help=('End date of the requested date range in '
                                 'YYYY-MM-DD format.'))
    args = argparser.parse_args()

    start_date = args.start_date
    end_date = args.end_date

    # Running Reports
    body, metrics_len, dimensions_len = ga_report(VIEW_ID, start_date, end_date)

    analytics = initialize_analyticsreporting(KEY_FILE_LOCATION, SCOPES)

    response = get_report(analytics, body)

    data, columns = data_extract(response, metrics_len, dimensions_len)

    create_csv_file(data, columns, start_date, end_date)
