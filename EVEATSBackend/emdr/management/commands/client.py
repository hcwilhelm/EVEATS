import zlib
import zmq
import json
import dateutil.parser
from sys import exit
from collections import namedtuple
from time import sleep
from datetime import datetime
import multiprocessing
from django.conf import settings

# ===========================================================================
# = Logging                                                                 =
# ===========================================================================
import logging
logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = 'Starts the EMDR client'
    detach_process = True
    prevent_core = True
    stdin = None
    stdout = None
    stderr = None
    pidfile = None
    uid = None
    gid = None 
    
    def handle(self, *args, **options):
        if getattr(settings, 'EMDR_SYNCINT', 0) <= 0:
            self.stderr.write("EMDR_SYNCINT not set (or not greater 0)!\n")
            exit(1)
        
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        
        # Connect to the first publicly available relay.
        subscriber.connect('tcp://relay-eu-germany-1.eve-emdr.com:8050')
        
        # Disable filtering.
        subscriber.setsockopt(zmq.SUBSCRIBE, "")
        
        marketOrders = {}

        lastExport = datetime.now()

        while True:
            delta = datetime.now() - lastExport
            if delta.total_seconds() > settings.EMDR_SYNCINT:
                self.stdout.write( "Would export to Database now!\n" )
                lastExport = datetime.now()
            elif (int(delta.total_seconds()) % 5) == 0:
                self.stdout.write("markteOrders in Hashtable: %s\n" % len(marketOrders))
                sleep(1)
                    

            # Receive raw market JSON strings.
            market_json = zlib.decompress(subscriber.recv())
            # deserialize the JSON data to a python dict.
            marketData = json.loads(market_json)
            
            if marketData['resultType'] == 'orders':                    
                # as columns in rows have no fixed order,
                # we have to do some position mappings later 
                Columns = namedtuple('Columns', marketData['columns'])
                     
                # i've never seen messages with more then 1 rowset
                # but documentation says this messages may exists
                for rowset in marketData['rowsets']:
                    generatedAt = dateutil.parser.parse(rowset['generatedAt'])
                    typeID = rowset['typeID']
                    regionID = rowset['regionID']
                    for row in rowset['rows']:
                        row = Columns(*row)
                        if row.orderID not in marketOrders:
                            rowDict = row._asdict()
                            rowDict['generatedAt'] = generatedAt
                            rowDict['typeID'] = typeID
                            rowDict['regionID'] = regionID
                            rowDict['seenCounter'] = 1
                            marketOrders[row.orderID] = rowDict
                        else:
                            if generatedAt > marketOrders[row.orderID]['generatedAt']:
                                self.stdout.write("\t... and it's newer!\n")
                            else:
                                # same or older marketOrder again.
                                # so just inc. seenCounter if itemType and regionID match
                                if marketOrders[row.orderID]['typeID'] == typeID and marketOrders[row.orderID]['regionID'] == regionID:
                                    marketOrders[row.orderID]['seenCounter'] = marketOrders[row.orderID]['seenCounter'] + 1
