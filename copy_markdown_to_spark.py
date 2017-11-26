#!/usr/bin/python3

#####################################################################
#																	#
#	Module: 		copy_markdown_to_spark.py			 			#
#	Author: 		Joshua Matthews 2017							#
#	Company: 		Cisco Systems									#
#	Description:	Copy contents of Python script to clipboard		#
#					in Markdown format 								#
#																	#
#####################################################################

#####################################################################
#						Dependancy Imports							#
#####################################################################
import argparse
import os
import requests
import json
import pyperclip



#####################################################################
#						Environment Settings						#
#####################################################################

# Used to form absolute path of code file to parse
basedir = os.getcwd()

# Assign Spark auth token and room id to post markdown output to Spark room
SPARK_TOKEN = ''
SPARK_ROOM = ''

# Set to True to automatically post markdown to Spark
# NOTE - Code colorization not yet supported through Spark APIs
SPARK_POST = False



#####################################################################
#						Function Definitions						#
#####################################################################
"""
Function: 	postSpark
Arguments:	message 	- Message to post to Spark room with markdown format
			room_id		- Room id of Spark room for which to post message 
			token 		- Spark Auth Token
Return:		response 	- Requests response object
"""
def postSpark(message, room_id, token):

	auth = 'Bearer ' + token
	headers = {'Authorization': auth, "content-type": "application/json; charset=utf-8"}
	payload = {'roomId': room_id, 'markdown': message}
	uri = 'https://api.ciscospark.com/v1/messages'
	response = requests.post(uri, headers=headers, data=json.dumps(payload))

	return response



"""
Function: 	parseCode
Arguments:	title 		- Title for the post - will appear at top of message in bold font
			comment		- Will appear below title in italics 
			code_file 	- Relative path to file to parse into markdown code string
Return:		parsed_str 	- Markdown formatted string ready for Spark message post
"""
def parseCode(code_file, title="", comment=""):

	# Initiate return string
	parsed_str = ""

	# Add title if it exists
	if title:
		parsed_str += '\n\n**' + title + '**'
		parsed_str += '\n\n'

	# Add comment if it exists
	if comment:
		parsed_str += '*' + comment + '*'
		parsed_str += '\n'

	# Code Block
	parsed_str += '\n``` python\n'

	# Parse contents of file
	with open(code_file) as f:
		read_data = f.read()
		parsed_str += read_data

	# Ending Code Block
	parsed_str += '\n```\n' 

	return parsed_str



#####################################################################
#						Main Exectuion								#
#####################################################################
if __name__ == '__main__':

	# Parse CLI Arguments
	parser = argparse.ArgumentParser(description='Parse Filename')
	parser.add_argument('-f', action="store", dest="filename", type=str, required=True)
	parser.add_argument('-t', action="store", dest="title", type=str, required=False)
	parser.add_argument('-c', action="store", dest="comment", type=str, required=False)
	given_args = parser.parse_args()

	# Get Filename
	code_file = given_args.filename
	code_file = os.path.join(basedir, code_file)

	# Get Comment
	comment = ""
	comment = given_args.comment

	# Get Title
	title = ""
	title = given_args.title
	
	# Process Code into Markdown String
	parsed_str = parseCode(title=title, comment=comment, code_file=code_file )
	pyperclip.copy(parsed_str)
	print(parsed_str)

	# Post to Spark
	if SPARK_POST:
		response = postSpark(message=parsed_str, room_id=SPARK_ROOM, token=SPARK_TOKEN)
		print(response)
	