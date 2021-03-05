import requests
import os
import sys
import json
from tools.database import database as db

class Filtered_stream:
    
    def __init__(self,bearer_token, log):      
        self.__bearer_token = bearer_token
        self.__log = log
        self.__database = self.__get_database()
        self.__filter = self.__get_filter()
    
    def __get_database(self):
        database = db.Database.get_database_instance()
        self.__log.log('Twitter connection to the database is established')
        return database

    def __get_filter(self):
        with open('files/filter_word.json', 'r', encoding='utf-8') as file:
            filter = json.load(file)
        self.__log.log('Twitter filters are available')
        return filter


    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.__bearer_token)}
        return headers

    def get_rules(self,headers):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        self.__log.log('Retrieving the rules')
        return response.json()

    def delete_all_rules(self,headers, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        self.__log.log('Deleting the previously available rules')

    def set_rules(self, headers, delete):
        # You can adjust the rules if needed
        '''
        sample_rules = [
            {"value": "dog has:images", "tag": "dog pictures"},
            {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]
        '''
        rules = self.__generate_rules()
        payload = {"add": rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload,
        )
        self.__log.log('Setting the new rules')
        if response.status_code != 201:
            print(json.dumps(response.json()))
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )

    def get_stream(self, headers, set):
        self.__log.log('Receiving the stream ')
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                self.__log.log(json.dumps(json_response, indent=4, sort_keys=True))

    def __generate_rules(self):
        rules =  []
        file = self.__filter                    

        for item in file['rules']:
            rules.append({'value': item })

        return rules

#https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream-rules
