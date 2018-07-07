# -*- coding: utf-8 -*-
""" simple alexa invocation"""

from __future__ import print_function

import random

SKILL_NAME = "My Teacher"
HELP_MESSAGE = "You can say tell me a my teacher, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The My Teacher skill can't help you with that."
FALLBACK_REPROMPT = 'What can I help you with?'

# --------------- App entry point -----------------

def lambda_handler(event, context):
    """  App entry point  """
    print("-------------------------")
    print(event['request']['type'])
    print("-------------------------")
    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']
    print("-------------------------")
    print(intent_name)
    print("-------------------------")

    if intent_name == "ReadNotifications":
        return read_notifications()
    elif intent_name == "ResumeSession":
        return resume_session()
    elif intent_name == "ShortNote":
        return save_short_note()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        print("invalid Intent reply with help")
        return get_help_response()

def save_short_note():
    cardcontent = "Short note saved under this course"
    speechOutput = "Short note saved under this course"
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def resume_session():
    cardcontent = "Chapter two,Introduction to keywords, volatile"
    speechOutput = "Chapter two,Introduction to keywords, volatile. The Java volatile keyword is used to mark a Java variable as 'being stored in main memory', so it guarantees visibility of changes to variables across threads."
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))
def get_help_response():
    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response():
    cardcontent = "welcome back Amith. You have one notifications, do you want me to read it for you ?"
    speechOutput = "welcome back Amith. You have one notifications, do you want me to read it for you ?"
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def read_notifications():
    cardcontent = "You have one assignment, from an introduction to algebra due on today, shall we complete it, or do you want me to resume to your last session ?"
    speechOutput = "You have one assignment, from an introduction to algebra due on today, shall we complete it, or do you want me to resume to your last session chapter 2, key words in introduction to java?"
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def get_stop_response():
    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")

def on_session_ended():
    """ called on session ends """
    #print("on_session_ended")

def on_launch(request):
    return get_launch_response()


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def dialog_response(endsession):
    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }

def speech_response_with_card(title, output, cardcontent, endsession):
    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }