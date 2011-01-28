Mail\_stats
=========

Generates Statistics from the given mails, e.g. how many mails sent per
week,day,hour.

The base source code is from mail\_proc.

It uses the python-genericore library version 5


Statistics
=========

currently the following things are generated:
    {
      "type" : "mail",
      "subtype" : 1,
      "data" : {
        "num_mail_abs" : { # absolute number of mails in...
          "month" : 4,     # the last 30,7,1 days and last hour
          "week" : 3,
          "day" : 2,
          "hour" : 1
          }
       }
    }
    see protocols/mail_stats/
