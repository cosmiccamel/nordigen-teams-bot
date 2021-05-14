# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os
import random
# from  bank_details import getBanks
import traceback
import urllib.error, urllib.request, urllib.parse
import json

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, ConversationState, UserState
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes

from data_model import UserProfile

url = "https://bank-country.azurewebsites.net/api/" \
      "country?code=w7LXvmkwLHgSZ/UgRxNrULA3rzPW8qvrFOqAwcnh1piUvD5bAJENKQ==&bank-country="

bankCardJson = """{
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [

        {
            "type": "TextBlock",
            "text": "Select Bank",
            "wrap": true
        },
        {
            "type": "Input.ChoiceSet",
            "id": "bankID",
            "value": "be",
            "choices": [
                {
                    "title": "ICICI",
                    "value": "ic"
                },
                {
                    "title": "HDFC",
                    "value": "hd"
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "id": "2"
            }
        }
    ]
}
"""


def getBanks(cc):

    findUrl=f"{url}{cc}"
    data = urllib.request.urlopen(findUrl).read()
    # upData =

    # Remove other data
    js = json.loads(data)

    new_dictArry = []
    for items in js:
        # new_dictArry.append({key:val for key, val in items.items() if key not in ('bic' , 'countries' , 'countries') })

        new_dictArry.append({'value' : f"{items.get('id')},{items.get('name')}" ,
                             'title': items.get('name')})


    # print(new_dictArry)

    bankJson = json.loads(bankCardJson)

    bankJson["body"][1]["choices"] = new_dictArry



    return  bankJson



CARDS = [
    "resources/DropdownCard.json"
]


class AdaptiveCardsBot(ActivityHandler):
    """
    This bot will respond to the user's input with an Adaptive Card. Adaptive Cards are a way for developers to
    exchange card content in a common and consistent way. A simple open card format enables an ecosystem of shared
    tooling, seamless integration between apps, and native cross-platform performance on any device. For each user
    interaction, an instance of this class is created and the OnTurnAsync method is called.  This is a Transient
    lifetime service. Transient lifetime services are created each time they're requested. For each Activity
    received, a new instance of this class is created. Objects that are expensive to construct, or have a lifetime
    beyond the single turn, should be carefully managed.
    """

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        # dialog: Dialog,
    ):
        if conversation_state is None:
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        # if dialog is None:
        #     raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        # self.dialog = dialog

        self.conversation_data_accessor = self.conversation_state.create_property(
            "ConversationData"
        )
        self.user_profile_accessor = self.user_state.create_property("UserProfile")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Welcome to Adaptive Cards Bot  {member.name}. This bot will "
                    f"introduce you to Adaptive Cards. Type anything to see an Adaptive "
                    f"Card."
                )

    async def on_message_activity(self, turn_context: TurnContext):

        user_profile = await self.user_profile_accessor.get(turn_context, UserProfile)

        if (turn_context.activity.value is not None):
            if (turn_context.activity.value.get('id') == '1'):

                countryCode = turn_context.activity.value['CompactSelectVal']
                print("Got Country code as " + countryCode)

                user_profile.country = countryCode
                try:
                    cardDetail = getBanks(countryCode)

                    message = Activity(
                        text="Select bank account:",
                        type=ActivityTypes.message,
                        attachments=[self._create_adaptive_card_attachment(bankCard=cardDetail)],
                    )
                except Exception:
                    traceback.print_exc()
                    message = """Unable to access site try again"""

            elif (turn_context.activity.value.get('id') == '2'):
                bankCode = str(turn_context.activity.value['bankID'])

                bankCode , bankName = bankCode.split(',')
                print("Got Bank ID  as " + bankCode)

                # URL to show user
                # url =

                # Create Message activity for google

                print (f" Next URL needs bankCode {bankCode} bankTitle {bankName} "
                       f" UserID  countryCode {user_profile.country}")

                updateMsg = f""" You have selected  Bank {bankName} with code {bankCode}
                            Country code {user_profile.country}
                            got user Name as {turn_context.activity.from_property.name} and {turn_context.activity.from_property.id}
                            Please click on the URL information at: https://www.google.com"""

                return  await turn_context.send_activity(updateMsg)

        else:
            message = Activity(
                text="Please select Country :",
                type=ActivityTypes.message,
                attachments=[self._create_adaptive_card_attachment()],
            )

        await turn_context.send_activity(message)

    def _create_adaptive_card_attachment(self, bankCard = None) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        if bankCard is None:

            bank_country_card = """"
            {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.3",
                "body": [

                    {
                        "type": "TextBlock",
                        "text": "Select Country",
                        "wrap": true
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "CompactSelectVal",
                        "value": "be",
                        "choices": [
                            {
                                "title": "Belgium",
                                "value": "be"
                            },
                            {
                                "title": "Czech Republic",
                                "value": "cz"
                            },
                            {
                                "title": "Denmark",
                                "value": "dk"
                            },
                                    {
                                "title": "Estonia",
                                "value": "ee"
                            },
                                    {
                                "title": "Finland",
                                "value": "fi"
                            },
                                    {
                                "title": "France",
                                "value": "fr"
                            },
                                    {
                                "title": "Germany",
                                "value": "de"
                            },
                                    {
                                "title": "Ireland",
                                "value": "ie"
                            },
                                    {
                                "title": "Latvia",
                                "value": "lv"
                            },
                                    {
                                "title": "Lithuania",
                                "value": "lt"
                            },
                                    {
                                "title": "Netherlands",
                                "value": "nl"
                            },
                                    {
                                "title": "Norway",
                                "value": "no"
                            },
                                    {
                                "title": "Portugal",
                                "value": "pt"
                            },
                                    {
                                "title": "Spain",
                                "value": "es"
                            },
                                    {
                                "title": "Sweden",
                                "value": "se"
                            },
                                    {
                                "title": "United Kingdom",
                                "value": "gb"
                            }
                        ]
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {
                            "id": "1"
                        }
                    }
                ]
            }
            """
            # card_path = os.path.join(os.getcwd(), CARDS[0])
            # with open(card_path, "rb") as in_file:
            #     card_data = json.load(in_file)
            #card_data = json.load(bank_country_card)
            card_data = bank_country_card
        else:
            card_data = bankCard
        return CardFactory.adaptive_card(card_data)



bank_country_card = """"
{
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [

        {
            "type": "TextBlock",
            "text": "Select Country",
            "wrap": true
        },
        {
            "type": "Input.ChoiceSet",
            "id": "CompactSelectVal",
            "value": "be",
            "choices": [
                {
                    "title": "Belgium",
                    "value": "be"
                },
                {
                    "title": "Czech Republic",
                    "value": "cz"
                },
                {
                    "title": "Denmark",
                    "value": "dk"
                },
				        {
                    "title": "Estonia",
                    "value": "ee"
                },
				        {
                    "title": "Finland",
                    "value": "fi"
                },
				        {
                    "title": "France",
                    "value": "fr"
                },
				        {
                    "title": "Germany",
                    "value": "de"
                },
				        {
                    "title": "Ireland",
                    "value": "ie"
                },
				        {
                    "title": "Latvia",
                    "value": "lv"
                },
				        {
                    "title": "Lithuania",
                    "value": "lt"
                },
				        {
                    "title": "Netherlands",
                    "value": "nl"
                },
				        {
                    "title": "Norway",
                    "value": "no"
                },
				        {
                    "title": "Portugal",
                    "value": "pt"
                },
				        {
                    "title": "Spain",
                    "value": "es"
                },
				        {
                    "title": "Sweden",
                    "value": "se"
                },
				        {
                    "title": "United Kingdom",
                    "value": "gb"
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "id": "1"
            }
        }
    ]
}
"""
