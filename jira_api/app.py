import http.client
import json

import requests
from flask import Flask,jsonify,request
from requests.auth import HTTPBasicAuth

app=Flask(__name__)

@app.route('/', methods=["POST"])


def abc():
  flag = 0
  input_json = request.get_json(force=True)
  conn = http.client.HTTPSConnection("log-analysis.atlassian.net")

  auth = HTTPBasicAuth("keerthanadm.is20@rvce.edu.in",
                       "ATATT3xFfGF0LwFUrHqHOWKdZu_zgXJSLO8V87Mynfd6qSJIVHFekz_CL_PqFWXwaCriLjLZLyl0z02L3VUyAEW_qIQ3MI7apx-Z9c2gBaGtaBa2mYrd1ByW_Br_GZwjoyaUa-JMLmXpIMKX7folxrI-cWIfyoYeHa_yYbWztA7x8EszOs7xt6g=8F6B89F0")

  headers = {
    'Content-Type': 'application/json',
    'Authorization':'Basic a2VlcnRoYW5hZG0uaXMyMEBydmNlLmVkdS5pbjpBVEFUVDN4RmZHRjBMd0ZVckhxSE9XS2RadV96Z1hKU0xPOFY4N015bmZkNnFTSklWSEZla3pfQ0xfUHFGV1h3YUNyaUxqTFpMeWwwejAyTDNWVXlBRVdfcUlRM01JN2FweC1aOWMyZ0JhR3RhQmEybVlyZDFCeVdfQnJfR1p3am95YVVhLUpNTG1YcElNS1g3Zm9seHJJLWNXSWZ5b1llSGFfeVliV3p0QTd4OEVzek9zN3h0Nmc9OEY2Qjg5RjA=',
    'Cookie': 'atlassian.xsrf.token=2ce4f5e8-4fa2-44be-a47e-9a2b5b3c24f0_4e22051a201d1b197a173c602d4d6cbf789df1c4_lin'
  }

  query = {
    'jql': '',
    'maxResults': 100
  }

  url = "https://log-analysis.atlassian.net/rest/api/3/search"

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    auth=auth,
    verify=False
  )
  # print(response.text)
  a = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
  a = json.loads(a)
  a = a['issues']
  for each in a:
    if(each['fields']['issuetype']['name']=='Sub-task'):
      continue
    elif (each['fields']['description']['content'][0]['content'][0]['text'] == input_json["text"] ):
      if each['fields']['status']['name']=='Done':
        flag==0
        break
      else:
        flag = 1
        payload = json.dumps({
          "fields": {
            "project": {
              "key": input_json['key']
            },
            "parent": {
              "key": each['key']
            },
            "summary": input_json['summary'],
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": input_json['text']
                    }
                  ]
                }
              ]
            },
            "issuetype": {
              "name": "Sub-task"
            }
          }
        })
        break

  if flag==0:
    payload = json.dumps({
    "fields": {
      "project": {
        "key":input_json['key']
      },
      "summary": input_json['summary'],
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": input_json['text']
              }
            ]
          }
        ]
      },

      "issuetype": {
        "name": input_json['issue']
      }
    }
  })



  conn.request("POST", "/rest/api/3/issue", payload, headers)
  res = conn.getresponse()
  data = res.read()
  return jsonify(payload)
