from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import commit_on_success
from django.conf import settings

from Backend.assets.models import *

import os
import httplib
import urllib
import xml.sax


# =============================
# = BaseCommand import_assets =
# =============================

class Command(BaseCommand):
	args = ''
	help = 'Imports the current CorpAssetList from the EVE api'

	def handle(self, *args, **options):
		print "Starting your import ..."

		
		# ===================
		# = Connect to CPP  =
		# ===================
		
		parameters 	= urllib.urlencode({'apiKey': settings.EVEAPI["APIKEY"], 'userID': settings.EVEAPI["USERID"], 'characterID': settings.EVEAPI["CHARID"]})
		headers 	= {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

		eve_api_connection = httplib.HTTPSConnection(settings.EVEAPI["APIURL"], 443)
		eve_api_connection.request("POST", "/corp/AssetList.xml.aspx", parameters, headers)

		eve_api_response = eve_api_connection.getresponse()
		print "Eve api response : ", eve_api_response.status, eve_api_response.reason 
		
		# ==================================================================
		# = Check if the response is OK  and Download the the new XML file =
		# ==================================================================
		
		if eve_api_response.status == 200:
			os.remove("assets/management/xml_cache/corpAssetList.xml")
					
			assets_xml_file = open("assets/management/xml_cache/corpAssetList.xml", "w")
			assets_xml_file.write(eve_api_response.read())
			assets_xml_file.close()

			eve_api_connection.close()
		
		# =========================================
		# = Open the XML File hope for a new one  =
		# =========================================

		try:
			assets_xml_file = open("assets/management/xml_cache/corpAssetList.xml", "r")

			# =======================================
			# = Clean up the corpAssetList Database =
			# =======================================
			
			corpAssetList.objects.all().delete()

			# ==========================================
			# = Insert all the Data into corpAssetList =
			# ==========================================
			
			asset_list_parser = xml.sax.make_parser()
			asset_list_parser.setContentHandler(AssetListHandler())
			asset_list_parser.parse(assets_xml_file)

		except IOError:
			print "There is no XML file check if the EVE API is online"



# ====================================================
# = XML Parser using a stack to model the hierarchie =
# ====================================================

class AssetListHandler(xml.sax.handler.ContentHandler):

	def __init__(self):
		self.batchCommitSize = 1000
		self.parentStack = []
		self.assetStack  = []


	# ====================================================================
	# = startElement is called everytime the xml parsers sees a open tag =
	# ====================================================================
	
	def startElement(self, name, attributes):
		
		# ===================================================================
		# = if we have a row with a locationID this is a possible container =
		# ===================================================================
		
		if name == "row" and "locationID" in attributes:
			
			# ==========================================================================
			# = officeID to stationID conversion refer to eve dev for more information =
			# ==========================================================================
			
			locationID = int(attributes["locationID"])
			
			if locationID >= 66000000 and locationID < 67000000:
				locationID -= 6000001
		
			# ===============================================
			# = get the location object from mapDenormalize =
			# ===============================================
		
			location = mapDenormalize.objects.get(itemID=locationID)
			
			# ========================================================================
			# = create the corpAssetList abject and store it as a possible container =
			# ========================================================================
			
			invType 	= invTypes.objects.get(typeID=attributes["typeID"])
			corpAsset	= corpAssetList(itemID=attributes["itemID"], locationID=location, typeID=invType, quantity=attributes["quantity"], flag=invFlags.objects.get(pk=attributes["flag"]), singleton=attributes["singleton"])
			self.assetStack.append(corpAsset)
		
		# =============================================================================================================
		# = if we have a row without a locationID the item must be inside a container also it is a possible container =
		# =============================================================================================================
		
		if name == "row" and "locationID" not in attributes:
			
			# ========================================================================
			# = create the corpAssetList abject and store it as a possible container =
			# ========================================================================
			
			invType		= invTypes.objects.get(typeID=attributes['typeID'])
			corpAsset	= corpAssetList(itemID=attributes["itemID"], parentID=self.parentStack[-1] , typeID=invType, quantity=attributes["quantity"], flag=invFlags.objects.get(pk=attributes["flag"]), singleton=attributes["singleton"])
			self.assetStack.append(corpAsset)
		
		# =============================================================================
		# = if we have a rowset with name="contents" the privious row was a container =
		# =============================================================================
		
		if name =="rowset" and attributes["name"] == "contents":
			
			# ===================================================================
			# = change the parent isContainer = True and push it onto the stack =
			# ===================================================================
			
			self.assetStack[-1].isContainer=True
			self.parentStack.append(self.assetStack[-1])

	# ===================================================================
	# = endElement is called everytime the xml parsers sees a close tag =
	# ===================================================================

	def endElement(self, name):
		
		# ===============================================================================================
		# = if we see a closing rowset tag and we still have something on our stack pop out the element =
		# ===============================================================================================
		if name == "rowset" and len(self.parentStack) > 0:
			self.parentStack.pop()
			
		# ===============================================================
		# = if we see a closing row tag we try to commit a object batch =
		# ===============================================================
		
		if name == "row" and len(self.assetStack) > self.batchCommitSize:
			
			# =========================================
			# = Commit all object accept the last one =
			# =========================================
			CommitTransaction(self.assetStack[0:-1])
			
			# =========================
			# = Resize the assetStack =
			# =========================
			self.assetStack = [self.assetStack[-1]]

	# ===========================================================================
	# = endDocument is called when the xmls parsers sees the document close tag =
	# ===========================================================================
	def endDocument(self):
		
		# ================================
		# = Commit all remaining objects =
		# ================================
		CommitTransaction(self.assetStack)
		
@commit_on_success
def CommitTransaction(queryset):
	print "Commiting ", len(queryset), " transactions"
	for query in queryset:
		query.save()
