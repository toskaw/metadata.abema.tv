from lib import Cache, create_tables
import re
import xbmc
import xbmcaddon


            
if __name__ == '__main__':
    #initialize DB
    create_tables()
    
    # cache warming
    cache = Cache()
    cache.delete_expired()
