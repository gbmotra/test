import freeswitch as fs                 # from freeswitch import *


def hangup_hook(session, what):
    fs.consoleLog("info", "hangup hook for %s!!\n\n" % what)
    return


def input_callback(session, what, obj):
    """
    # INPUT CALLBACK
    #
    # session is a session object
    # what is "dtmf" or "event"
    # obj is a dtmf object or an event object depending on the 'what' var.
    # if you pass an extra arg to setInputCallback then append 'arg' to get that value
    # def input_callback(session, what, obj, arg):
    #
    #
    # https://wiki.freeswitch.org/wiki/CoreSession_Constructor
    # input_callback return values:
    # pause
    # restart
    # stop
    # seek:1000
    # speed:1000
    # speed:+1
    # speed:0
    # speed:-1
    # break

    :param session:
    :param what:
    :param obj:
    :return:
    """

    if what == "dtmf":
        fs.consoleLog("info", ("_" * 80) + "\n")
        fs.consoleLog("info", what + " " + obj.digit + "\n")
        fs.consoleLog("info", ("_" * 80) + "\n")
        return "stop"

    if what == "event":
        fs.consoleLog("info ------------> ", what + " " + obj.serialize() + "\n")
        session.execute("avmd", "stop")
        return "stop"

    return "stop"        # "pause"


def handler(session, args):
    session.answer()
    session.setHangupHook(hangup_hook)
    session.setInputCallback(input_callback)
    #session.execute("avmd", "start")
    # session.execute("playback", session.getVariable("hold_music"))
    #import sys
    #for i,d in enumerate(sys.path):
    #    fs.consoleLog("info", str(i) + " " + d)
    # while "/usr/local/wsgi" in sys.path:
    #     fs.consoleLog("info", ">>> removing")
    #     sys.path.remove("/usr/local/wsgi")

    #session.streamFile("/var/ac/snd/test.wav")
    #common.phone.say_xml("<tts><english>Hello World!</english><spanish>Hola Mundo!</spanish></tts>")

    # fs.consoleLog("info", "1\n")
    # session.streamFile("/var/ac/snd/test.wav")
    # fs.consoleLog("info", "2\n")
    # session.streamFile("/var/ac/snd/test.wav")
    # fs.consoleLog("info", "3\n")
    session.sleep(2000)
    #session.streamFile("/var/ac/ivr/moh_vd-5.wav")
    session.streamFile("/var/ac/ivr/MOMM.wav")
    session.sleep(2000)


def fsapi(session, stream, env, args):
    """
    # FSAPI CALL FROM CLI, DP HTTP etc
    #
    # default name for python FSAPI is "fsapi" it can be overridden with <modname>::<function>
    # stream is a switch_stream, anything written with stream.write() is returned to the caller
    # env is a switch_event
    # args is all the args passed after the module name
    # session is a session object when called from the dial plan or the string "na" when not.

    :param session:
    :param stream:
    :param env:
    :param args:
    :return:
    """

    stream.write("w00t!\n" + env.serialize())
    

def runtime(args):
    """
    # RUN A FUNCTION IN A THREAD
    #
    # default name for pyrun is "runtime" it can be overridden with <modname>::<function>
    # args is all the args passed after the module name

    :param args:
    :return:
    """

    print args + "\n"






