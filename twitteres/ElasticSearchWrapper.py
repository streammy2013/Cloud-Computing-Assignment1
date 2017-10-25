import simplejson as json
import requests

from configparser import ConfigParser


class ElasticSearchWrapper():

	def __init__(self):
		config = ConfigParser()
		config.read("twitteres/config.cfg")
		service = 'es'
		self.end_point = config.get('elasticsearch', 'end_point')
		self.index = config.get('elasticsearch', 'index')
		self.mapping_type = config.get('elasticsearch', 'mapping_type')        
		self.address = 'http://%s/%s/%s' % (self.end_point, self.index, self.mapping_type)
		self.ciaddress = 'http://%s/%s' % (self.end_point, self.index)
	
	def create_index(self):
		data = {
			"mappings" : {
				self.mapping_type : {
					"properties" : {
						"name" : {"type" : "text"},
						"text" : {"type" : "text"},
						"time" : {"type" : "date", "format": "yyyy-MM-dd HH:mm:ss"},
						"location" : {"type" : "geo_point"},
						"profile_image_url" : {"type" : "text"}
					}
				}
			}
		}
		response = requests.put(self.ciaddress, json.dumps(data))
		#print(response)
		return response.text
		

	def count(self):		
		data = {
			"query": {
				"match_all": {}
			}
		}
		count_address = '%s/_count' % (self.address)
		response = requests.post(count_address, data = json.dumps(data))
		response = response.json()
		return response["count"]

	def upload(self, data, id):
		
		upload_address = '%s/%s' %(self.address,id)
		response = requests.put(upload_address, json = data)
		return response

	def search(self, keyword): 

		keydata = {
			"size": 10000,
			"query" : {
				"query_string": {"query" : keyword}
			}
			
		}
		search_address = '%s/_search' % (self.address)
		response = requests.post(search_address, data = json.dumps(keydata))
		return response.json()
	

	def fetch_stored(self, num):
		data = {
            "query": {
                "match_all": {}
            },
            "size": num,
            "sort": [
            	{
            		"time": {
            			"order": "desc"
            		}
            	}
            ]

        }
		search_address = '%s/_search' % (self.address)
		response = requests.post(search_address, data=json.dumps(data))
		return response.json()


	def geosearch(self, distance, location):
		data = {
			"size" : 10000,
			"query": {
        		"bool" : {
            		"must" : {
                		"match_all" : {}
            		},
            		"filter" : {
                		"geo_distance" : {
                    		"distance" : "%skm" % (distance),
                    		"location" : location
                		}
            		}
        		}
   			}
		}
		search_address = '%s/_search' % (self.address)
		response = requests.post(search_address, data = json.dumps(data))
		#print(response.json())
		return response.json()


#es = ElasticSearchWrapper()
#es.create_index()
#es.count()