# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os
# from  bank_details import getBanks
import traceback
import urllib.error, urllib.request, urllib.parse
import requests
import json
import uuid
import config
from botbuilder.core import ActivityHandler, TurnContext, CardFactory, ConversationState, UserState
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes

from data_model import UserProfile

# url = "https://bank-country.azurewebsites.net/api/" \
#       "country?code=w7LXvmkwLHgSZ/UgRxNrULA3rzPW8qvrFOqAwcnh1piUvD5bAJENKQ==&bank-country="

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


def getBanks(country_id):

    request_url = 'https://bank-country.azurewebsites.net/api/country?code='+ config.ADMIN_FUNC_TOKEN+'&bank-country='+country_id
    response = requests.get(request_url)
    country = response.json()
    # findUrl=f"{url}{cc}"
    # data = urllib.request.urlopen(findUrl).read()
    # upData =

    # Remove other data
    #js = json.loads(data)

    new_dictArry = []
    for items in country:
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

                bank_id , bankName = bankCode.split(',')
                print("Got Bank ID  as " + bank_id)

                #---------------------------------------------------------------------------------------------------------------
                #                                        STEP 3 - CREATE AGREEMENT
                #---------------------------------------------------------------------------------------------------------------
                print('---------------------------------CREATE AGREEMENT ENDPOINT-----------------------------------')
                #---------------------------------------------------------------------------------------------------------------
                temp_user_id = str(uuid.uuid4())
                request_url = 'https://bank-country.azurewebsites.net/api/create-user-agreement?code='+ config.ADMIN_FUNC_TOKEN
                #payload = '&user-agreement=max_historical_days:90,enduser_id:'+str(turn_context.activity.from_property.name)+',aspsp_id:'+bankCode
                payload = '&user-agreement=max_historical_days:90,enduser_id:'+temp_user_id+',aspsp_id:'+bank_id
                create_agreement_url = request_url + payload

                #---------------------------------------------------------------------------------------------------------------
                #                                        STEP 3 - AGREEMENT REQUEST / RESPONSE
                #---------------------------------------------------------------------------------------------------------------

                response = requests.get(create_agreement_url)
                response_dict = json.loads(response.text)
                agreement_id = response_dict['id']

                #---------------------------------------------------------------------------------------------------------------
                #                                                   STEP 4 -  CREATE LINK ID 
                #---------------------------------------------------------------------------------------------------------------
                print('---------------------------------CREATE LINK ID ENDPOINT-----------------------------------')
                #---------------------------------------------------------------------------------------------------------------
                temp_order_id = str(uuid.uuid4())
                request_url = 'https://bank-country.azurewebsites.net/api/build-link?code='+ config.ADMIN_FUNC_TOKEN
                #payload = '&create-link=redirect:https://everst-add-bank.azurewebsites.net/profile,reference:'+ str(id_order) +',enduser_id:' + str(session.get("ms_id"))+ ',agreements:' + agreement_id
                payload = '&create-link=redirect:https://everst-add-bank.azurewebsites.net/profile,reference:'+ temp_order_id +',enduser_id:' + temp_user_id+ ',agreements:' + agreement_id
                create_link_url = request_url + payload

                #---------------------------------------------------------------------------------------------------------------
                #                                        STEP 4- LINK ID REQUEST / RESPONSE
                #---------------------------------------------------------------------------------------------------------------
                # Create Message activity for google
                response = requests.get(create_link_url)
                response_dict = json.loads(response.text)
                link_id = response_dict['id']
    
                #---------------------------------------------------------------------------------------------------------------
                #                                                   STEP 5 -  CREATE BANK URL 
                #---------------------------------------------------------------------------------------------------------------
                print('---------------------------------CREATE BANK URL ENDPOINT-----------------------------------')
                #---------------------------------------------------------------------------------------------------------------

                request_url = 'https://bank-country.azurewebsites.net/api/login-bank-link?code='+ config.ADMIN_FUNC_TOKEN
                payload = '&login-link=link_id:'+link_id+',aspsp_id:'+bank_id
                nordigen_link = request_url + payload

                #---------------------------------------------------------------------------------------------------------------
                #                                                   STEP 5 -  BANK URL REQUEST / RESPONSE
                #---------------------------------------------------------------------------------------------------------------

                response = requests.get(nordigen_link)
                response_dict = json.loads(response.text)
                nord_login_link = response_dict['initiate']

                print (f" Next URL needs bankCode {bank_id} bankTitle {bankName} "
                       f" UserID  countryCode {user_profile.country}")

                print (f""" You have selected  Bank {bankName} \n
                            with code {bank_id} \n
                            Country code {user_profile.country} \n
                            got user Name as {turn_context.activity.from_property.name} \n
                            and {turn_context.activity.from_property.id} \n
                            Please click on the URL information at: https://www.google.com \n
                            The payload url is {create_agreement_url} \n
                            create agreement url is {create_link_url} \n
                            create nordigen link {nordigen_link} """ )

                return  await turn_context.send_activity(nord_login_link)


                # # URL to show user
                # # url =

                # # Create Message activity for google

                # print (f" Next URL needs bankCode {bankCode} bankTitle {bankName} "
                #        f" UserID  countryCode {user_profile.country}")

                # updateMsg = f""" You have selected  Bank {bankName} with code =  {bankCode}
                #             Country code = {user_profile.country} 
                #             got user Name as {turn_context.activity.from_property.name} and USER ID = {turn_context.activity.from_property.id}
                #             Please click on the URL information at: https://www.google.com"""

                # return  await turn_context.send_activity(updateMsg)

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

            card_path = os.path.join(os.getcwd(), CARDS[0])
            with open(card_path, "rb") as in_file:
                card_data = json.load(in_file)
            #card_data = json.load(bank_country_card)
            #ard_data = bank_country_card
        else:
            card_data = bankCard
        return CardFactory.adaptive_card(card_data)



