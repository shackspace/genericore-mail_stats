#!/usr/bin/python2
from genericore import MongoConnect
from datetime import datetime,timedelta,tzinfo
import logging,pytz

MODULE_NAME = 'mail_stats'

log = logging.getLogger(MODULE_NAME)

DEFAULT_CONFIG = {
  MODULE_NAME : {
    "database" : {
      "collection" : MODULE_NAME
    }
  }
}

class mail_stats(MongoConnect): #mongoconnect derives from Configurable!
  
  def __init__(self,conf=None):
    MongoConnect.__init__(self,MODULE_NAME,DEFAULT_CONFIG) 
    #TODO write a Genericore Class which provides stuff like AMQP or MongoDB
    self.load_conf(conf)

  def generate_stats(self):
    ret = { "type" : "mail", "subtype" : 1, "data" : {} }
    ret['data']['num_mail_abs'] = self._generate_num_mail()
    return ret
  def _generate_num_mail(self):
    """ returns a dictionary with :
    monthly ( - 30 days ) 
    weekly ( - 7 days)
    daily ( - 1 day )
    hourly ( -1 hour )

    stats with the number of mails in time frame.

    These numbers are absolute (meaning the do not count from "beginning of
    the month/week/day" even though this should not be too much of a
    problem
    """
    ret= {'month': 0,'week':0,'day':0,'hour':0}
    coll = self.config[MODULE_NAME]['database']['collection']

    mails = self.db[coll].find( {} )
    for i in mails:
      print str(i)
      today = datetime.now(pytz.utc)
      dat = i['Header-Fields']['Date']
      dat['tzinfo'] = pytz.utc
      log.debug(str(dat))
      maildate = datetime(**dat)

      if today-timedelta(days=30) < maildate:
        ret['month'] += 1
      if today-timedelta(days=7) < maildate:
        ret['week'] += 1
      if today-timedelta(days=1) < maildate:
        ret['day'] += 1
      if today-timedelta(hours=1) < maildate:
        ret['hour'] += 1

    return ret

    
  def process(self,msg):
    coll = self.config[MODULE_NAME]['database']['collection']
    mail = msg['data']
    db = self.db
    hdr = mail['Header-Fields']
    log.debug (hdr)

    log.debug('adding new %s' % repr(mail))
    db[coll].save(mail)
    return self.generate_stats()

  def populate_parser(self,parser): 
    MongoConnect.populate_parser(self,parser)
    #placeholder for parser options

  def eval_parser(self,parsed): 
    MongoConnect.eval_parser(self,parsed)
    #placeholder for parser evaluator

