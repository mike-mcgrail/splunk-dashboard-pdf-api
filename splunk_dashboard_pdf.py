# 3/17/2021
# Mike McGrail | mmcgrail@splunk.com
# Sourced from     # Source: https://community.splunk.com/t5/Getting-Data-In/Generate-PDF-from-View-in-REST-API/m-p/274786/highlight/true#M52699
# Changes:
#   Updated token list to easier dictionary
#   Changed pdfgen GET to POST due to version 8.2.5 logging "pdfgen GET is deprecated. Please use POST instead."

import argparse
import sys
import logging
import requests
import json


def get_credentials():
    # Hard coded for demo. In the real world use a credential vault!
    creds = ['admin', 'Changeme1']
    return creds


def define_tokens():
    # pdfgen does not support tokens; use dictionary to define token values prior to sending to pdfgen
    # Example:  {'$token_name1$':'value', '$token_name2$':'value'}
    updatedTokens = {'$tok_sourcetype$':'*'}
    return updatedTokens


def get_dashboard(hostName, userName, appName, dashboardName, creds):
    dashboard = 'https://' + hostName + ':8089/servicesNS/' + userName + '/' + appName + '/data/ui/views/' + dashboardName
    r = requests.get(dashboard, auth=(creds[0], creds[1]), params={'output_mode': 'json'}, verify=False)
    xmlDashboard = r.json()['entry'][0]['content']['eai:data']

    updatedTokens = define_tokens()
    for tokenName, tokenValue in updatedTokens.items():
        xmlDashboard = xmlDashboard.replace(tokenName, tokenValue) # Replace tokens

    # Send XML code to pdfgen. GET has been deprecated in favor of POST
    pdfDashboard = requests.post('https://' + hostName + ':8089/services/pdfgen/render', auth=(creds[0], creds[1]), params={'input-dashboard-xml':xmlDashboard,'paper-size':'a4-landscape'}, verify=False)

    if pdfDashboard.status_code == 200:  # If success
        with open('dashboard.pdf', 'wb') as pdffile:
            pdffile.write(pdfDashboard.content)
    else:
        print(pdfDashboard.status_code)


def main():
    parser = argparse.ArgumentParser()
    #Required arguments
    parser.add_argument('hostName', help="Splunk hostname")
    parser.add_argument('userName', help="Splunk Username")
    parser.add_argument('appName', help="Splunk App Name")
    parser.add_argument('dashboardName', help="Splunk Dashboard Name")

    try:
        args = parser.parse_args()

    except SystemExit:
        logging.error(sys.argv[1:])
        logging.error('failed to parse arguments')
        sys.exit(0)

    creds = get_credentials()
    dashboard = get_dashboard(args.hostName, args.userName, args.appName, args.dashboardName, creds)

if __name__ == '__main__':
    main()
