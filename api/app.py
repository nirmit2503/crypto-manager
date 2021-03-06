import time
from flask import Flask, jsonify, request
import urllib
import os
from dotenv import load_dotenv
import json
import boto3
import time
import hashlib

# Load secret API file
load_dotenv()
CRYPTO_API_KEY = os.getenv('CRYPTO_API_KEY')
NOMICS_API_KEY = os.getenv('NOMICS_API_KEY')

# Errors
ERR_RESP = "Page Not Found"
ERR_ACC = "Account not created"
ERR_UPD = "Data not updated"
ERR_GET = "Data not found"

# Initialize database
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'crypto-manager'

app = Flask(__name__)

# TODO: Add SHA-256 or JSW token auth for secure APIs

########################
####### MetaData #######
########################

# Getting metadata for any crypto
# 			- Eg: Name, Description, Images, etc.
@app.route('/crypto/metadata/<tick>')
def getCryptoMetaData(tick):
	url = "https://api.nomics.com/v1/currencies?key=" + NOMICS_API_KEY + "&ids=" + tick
	try:
		response = urllib.urlopen(url).read()
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response

# Returns list of available cryptos
@app.route('/crypto/list')
def getCryptosList():
	url = "https://min-api.cryptocompare.com/data/blockchain/list?api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


##########################
####### OHLCV Data #######
##########################

# Daily tick data
@app.route('/crypto/data/daily', methods=['GET'])
def getDailyOHLCV():
	url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=" + request.form['tick'] + "&tsym=" + request.form['currency'] + "&limit=" + request.form['limit'] + "&api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response

# Hourly tick data
@app.route('/crypto/data/hourly', methods=['GET'])
def getHourlyOHLCV():
	url = "https://min-api.cryptocompare.com/data/v2/histohour?fsym=" + request.form['tick'] + "&tsym=" + request.form['currency'] + "&limit=" + request.form['limit'] + "&api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response

# Minute by minute tick data
@app.route('/crypto/data/minute', methods=['GET'])
def getMinuteOHLCV():
	url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=" + request.form['tick'] + "&tsym=" + request.form['currency'] + "&limit=" + request.form['limit'] + "&api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


#######################
####### Signals #######
#######################

# Trading signals for the provided tick
@app.route('/crypto/signal/<tick>')
def getTradingSignals(tick):
	url = "https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest?fsym=" + tick + "&api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


###########################
####### Social Data #######
###########################

# Latest social data for all active cryptos
@app.route('/crypto/social/latest')
def getLatestSocialData():
	url = "https://min-api.cryptocompare.com/data/social/coin/latest?api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response

# Historical social data for all active cryptos
@app.route('/crypto/social/historical', methods=['GET'])
def getHistoricalSocialData():
	url = "https://min-api.cryptocompare.com/data/social/coin/histo/day?limit=" + request.form['limit'] + "&api_key=" + CRYPTO_API_KEY
	try:
		resp = urllib.urlopen(url)
		jsonResp = json.load(resp)
		if jsonResp['Response'] == 'Success':
			response = jsonify(jsonResp['Data'])
		else:
			response = jsonResp['Response']
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


#############################
####### News Articles #######
#############################

# Returns latest news with crypto id as tags
@app.route('/crypto/news/latest')
def getLatestNews():
	url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key=" + CRYPTO_API_KEY
	try:
		response = urllib.urlopen(url).read()
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


##################################
####### Crypto Price Stats #######
##################################

# Returns price of single crypto in given currencies format
@app.route('/crypto/price/single', methods=['GET'])
def getSingleCryptoPriceConversions():
	url = "https://min-api.cryptocompare.com/data/price?fsym=" + request.form['tick'] + "&tsyms=" + request.form['currency_list'] + "&api_key=" + CRYPTO_API_KEY
	try:
		response = urllib.urlopen(url).read()
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response

# Returns price of provided cryptos in given currencies format
@app.route('/crypto/price/multiple', methods=['GET'])
def getMultiCryptosPriceConversions():
	url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + request.form['ticks'] + "&tsyms=" + request.form['currency_list'] + "&api_key=" + CRYPTO_API_KEY
	try:
		response = urllib.urlopen(url).read()
	except Exception as e:
		print(e)
		response = ERR_RESP
	return response


########################
####### Database #######
########################

# Ref for boto3 setup: https://medium.com/@aastha6348/easy-wizy-crud-operations-in-dynamodb-with-boto3-6d2844f150b5

# Creates a new account along with custom watchlist and portfolio
@app.route('/user/account/create', methods=['POST'])
def addNewUser():
	try:
		table = dynamodb.Table(TABLE_NAME)
		userID = str(int(time.time()))
		response = table.put_item(
			Item = {
				'userID': userID,
				'email': request.form['email'],
				'password': hashlib.sha256(request.form['email'].encode()).hexdigest(),
				'first_name': request.form['first_name'], 
				'last_name': request.form['last_name'],
				'aadhar_card_no': request.form['aadhar_card_no'],
				'pan_card_no': request.form['pan_card_no'],
				'funds': 0,
				'invested_amount': 0,
				'current_amount': 0,
				'p_and_l': 0
			} 
		)

		# TODO: Check if the entry is successful or not and then proceed with creating other tables

		# Create watchlist and portfolio tables
		table = dynamodb.create_table(
			TableName=userID + "_watchlist",
			KeySchema=[ 
				{
					'AttributeName': 'id',
					'KeyType': 'HASH'
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'id',
					'AttributeType': 'N'
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
    	)

		table = dynamodb.create_table(
			TableName=userID + "_portfolio",
			KeySchema=[ 
				{
					'AttributeName': 'id',
					'KeyType': 'HASH'
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'id',
					'AttributeType': 'N'
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
    	)
		
		# TODO: Wait until the table is created (show some loading) -> It takes some time to allocate resources for a table in DynamoDB

		response = jsonify(response['ResponseMetadata']['HTTPStatusCode'])
	except Exception as e:
		print(e)
		response = ERR_ACC
	return response

# Account Related Queries

# Updates funds
@app.route('/user/update/funds', methods=['POST'])
def updateUserFunds():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				userID = each['userID']
				response = table.update_item(
					Key = {
						'userID': userID
					},
					UpdateExpression = "set funds = :r",
					ExpressionAttributeValues = {
						':r': request.form['funds']
					},
					ReturnValues = "UPDATED_NEW"
				)
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_UPD
	return response

# Get funds
@app.route('/user/get/funds', methods=['GET'])
def getUserFunds():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				response = each['funds']
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_GET
	return response

# Updates invested amount
@app.route('/user/update/invested_amount', methods=['POST'])
def updateUserInvestedAmount():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				userID = each['userID']
				response = table.update_item(
					Key = {
						'userID': userID
					},
					UpdateExpression = "set invested_amount = :r",
					ExpressionAttributeValues = {
						':r': request.form['invested_amount']
					},
					ReturnValues = "UPDATED_NEW"
				)
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_UPD
	return response

# Get invested amount
@app.route('/user/get/invested_amount', methods=['GET'])
def getUserInvestedAmount():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				response = each['invested_amount']
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_GET
	return response

# Updates current amount
@app.route('/user/update/current_amount', methods=['POST'])
def updateUserCurrentAmount():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				userID = each['userID']
				response = table.update_item(
					Key = {
						'userID': userID
					},
					UpdateExpression = "set current_amount = :r",
					ExpressionAttributeValues = {
						':r': request.form['current_amount']
					},
					ReturnValues = "UPDATED_NEW"
				)
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_UPD
	return response

# Get current amount
@app.route('/user/get/current_amount', methods=['GET'])
def getUserCurrentAmount():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				response = each['current_amount']
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_GET
	return response

# Updates profit and loss
@app.route('/user/update/p_and_l', methods=['POST'])
def updateUserProfitAndLoss():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				userID = each['userID']
				response = table.update_item(
					Key = {
						'userID': userID
					},
					UpdateExpression = "set p_and_l = :r",
					ExpressionAttributeValues = {
						':r': request.form['p_and_l']
					},
					ReturnValues = "UPDATED_NEW"
				)
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_UPD
	return response

# Get profit and loss
@app.route('/user/get/p_and_l', methods=['GET'])
def getUserProfitAndLoss():
	try:
		table = dynamodb.Table(TABLE_NAME)
		scan = table.scan()
		response = ""
		for each in scan['Items']:
			if each['email'] == request.form['email'] and each['aadhar_card_no'] == request.form['aadhar_card_no'] and each['pan_card_no'] == request.form['pan_card_no']:
				response = each['p_and_l']
				break
		return json.dumps(response)
	except Exception as e:
		print(e)
		response = ERR_GET
	return response


# Porfolio related queries



# Temporary endpoint for checking Doughnut Chart functionality
@app.route('/temp/data')
def sendTempData():
	data = {
		"data": [
			{
				'coin': 'BTC',
				'percentage': 50
			},
			{
				'coin': 'ETH',
				'percentage': 25
			},
			{
				'coin': 'LTC',
				'percentage': 25
			}
		]
	}
	return jsonify(data)

if __name__ == '__main__':
    app.run()