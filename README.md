# splunk-dashboard-pdf-api
Utility to export Splunk dashboards to PDF via API

Required arguments: hostname, username, Splunk app name, dashboard name

Usage: splunk_dashboard_pdf.py "localhost" "admin" "search" "test_dashboard"

Environment: Tested in Splunk Enterprise version 8.2.5

Example: test_dashboard.xml has a dropdown which passes token $tok_sourcetype$ and a panel of events which references that token.
