#from raven.contrib.flask import Sentry


#sentry = Sentry(dsn="")

def loginfo(msg, extra=""):
    # sentry.captureMessage(msg, extra=extra)
    print(msg, extra)
