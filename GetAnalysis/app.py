import pandas as pd
import json
import flask, flask_restplus, flask_jwt
import flask_jwt
import requests
import sqlalchemy
import datetime
import pytz
import common.AzHelper as azhelper
import config
from datetime import timedelta
from sqlalchemy import create_engine
from flask_jwt import JWT
from flask import Flask, Blueprint, Response
from flask_restplus import Resource, Api
from pandas.io.json import json_normalize
from azure.storage.queue import QueueService


app = Flask(__name__)

@app.route("/")
def home():
    #get the queue setting from config.py
    azureQueueAccountName = config.AnalysisResultsQueue.account_name
    azureQueueKey = config.AnalysisResultsQueue.account_key
    azureQueueAnalysisResults = config.AnalysisResultsQueue.queue_name

    #Connect to queue
    queue_service = azhelper.CreateQueue(azureQueueAccountName, azureQueueKey,azureQueueAnalysisResults)

    #write the analysis JSON to queue
    azhelper.WriteToQueue(queue_service,azureQueueAnalysisResults, page_parse())
             
    return("Directive included for docker...!!!")

def page_parse():
    page_list = []
    page_list.append(config.AnalysisResultsURL.analysis_page)
    apikey = ""
    headers = {"Authorization": apikey}
    page_list.append(config.AnalysisResultsURL.analysis_detail_page)
    return page_list

if __name__ == "__main__":
    app.run(host='0.0.0.0')