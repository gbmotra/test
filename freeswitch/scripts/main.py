# -*- coding: utf-8 -*-
import os
import sys

import freeswitch as fs

# --------------------------------------------------------------
# Freeswitch entry point
# --------------------------------------------------------------
def handler(session, args):

    fs.consoleLog("info", "-" * 100)
    fs.consoleLog("info", "\n")


    #dest_number = session.getVariable("destination_number")
    #fs.consoleLog("info", "FAIL: no config key for destination DID:" + dest_number)
    wait = 8000
    #digits_regex = "[0-9*]"
    digits_regex = ".*"

    session.answer()
    digit = session.playAndGetDigits(1, 1, 1, wait, "", "/var/ac/ivr/MOMM.wav", "", digits_regex)
    if digit == "#":
        fs.consoleLog("info", "transfer")
        transfer_sync(session, "3133551426", "3863346434")
    else:
        fs.consoleLog("info", "NO transfer")
        #session.streamFile("/var/ac/ivr/MOMM.wav")
        session.sleep(300)

        session.hangup()

def transfer_sync(session, phone, caller_id):

    if phone == caller_id:
        caller_id = ""
    if len(phone) == 10:
        phone = "1" + phone

    sessionT = fs.Session("{ignore_early_media=false,originate_timeout=60,origination_caller_id_name=,origination_caller_id_number=" + caller_id + "}sofia/gateway/sip.flowroute.com/" + "42331550*" + phone)

    dispoA = "None"
    cnt = 0
    while sessionT.ready() and dispoA != "ANSWER":

        # ------------------------------------------------------------------------------
        # fake ring the patient phone
        #     tone_stream://%(2000,4000,440,480)
        # set the silence to zero and loop 40x's to get 4000ms (4sec)
        # ------------------------------------------------------------------------------
        if cnt == 0:
            session.execute("playback", "tone_stream://%(2000,000,440,480)")
            cnt += 1
            if cnt > 40:
                cnt = 0
        # ------------------------------------------------------------------------------
        # If the patient hangs up, hangup the transfer call
        # ------------------------------------------------------------------------------
        if not session.ready():
            sessionT.hangup()
            break

        dispoA = sessionT.getVariable("endpoint_disposition")
        session.sleep(100)

    if not sessionT.ready():
        sessionT.hangup()
        hangup()
        return

    if not session.ready():
        sessionT.hangup()
        hangup()
        return

    fs.consoleLog("info", "bridge start")
    fs.bridge(session, sessionT)
    fs.consoleLog("info", "bridge stop")

    sessionT.hangup()
    session.hangup()
