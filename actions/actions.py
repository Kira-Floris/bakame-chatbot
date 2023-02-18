# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

irembo_information_json = 'actions/temporary_irembo_information.json'
notFoundMessage = 'Mutwihanganire, ayo makuru ntitubashije kuyabona.'

class GetInformation:
    def __init__(self, service):
        self.service = service
        self.specific_information = None
        try:
            with open(irembo_information_json,'r') as f:
                information = json.load(f)
            self.specific_information = information[self.service]
            f.close()
        except Exception as err:
            print(err)
            self.specific_information = None
    
    def get_information(self):
        if self.specific_information:
            return self.specific_information
        else:
            return notFoundMessage
    
    def get_key(self, key):
        try:
            x = self.specific_information[key]
            return x
        except:
            return notFoundMessage
        
def buttonsToActionList(data):
    buttons = []
    for i in data:
        buttons.append({i:i})
    return buttons

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionInformationAboutPermanentDrivingLicense(Action):
    def name(self):
        return 'action_information_about_permanent_driving_license'
    def run(self, 
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        information = GetInformation('permanent_driving_license')
        information_description = information.get_key('description')
        dispatcher.utter_message(information_description)
        return []
    
class ActionPermanentDrivingLicenseDate(Action):
    def name(self):
        return 'action_ask_permanent_driving_license_date_slot'
    
    def run(self,
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        information = GetInformation('permanent_driving_license')
        dates = information.get_key('slots')['permanent_driving_license_date_choices']
        buttons = buttonsToActionList(dates)
        dispatcher.utter_message(text="murashaka gukora ku wuhe munsi",buttons=buttons)
        return []
    
class ActionPermanentDrivingLicenseCarCategory(Action):
    def name(self):
        return 'action_ask_permanent_driving_license_car_category_slot'
    
    def run(self,
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        information = GetInformation('permanent_driving_license')
        car_categories = information.get_key('slots')['permanent_driving_license_car_category_choices']
        buttons = buttonsToActionList(car_categories)
        dispatcher.utter_message(text="murashaka gukorera iyihe kategori yimodoka",buttons=buttons)
        return []
    
class ActionPermanentDrivingLicenseDistrict(Action):
    def name(self):
        return 'action_ask_permanent_driving_license_district_slot'
    
    def run(self,
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        information = GetInformation('permanent_driving_license')
        districts = [item['name'] for item in information.get_key('slots')['permanent_driving_license_district_choices']]
        buttons = buttonsToActionList(districts)
        dispatcher.utter_message(text="murashaka gukorera mu kahe karere",buttons=buttons)
        return []
    
class ActionPermanentDrivingLicenseLocation(Action):
    def name(self):
        return 'action_ask_permanent_driving_license_location_slot'
    
    def run(self,
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        print('hello world')
        district_slot = tracker.get_slot('permanent_driving_license_district_slot')
        information = GetInformation('permanent_driving_license')
        locations = []
        for item in information.get_key('slots')['permanent_driving_license_district_choices']:
            if item['name']==district_slot:
                locations.extend(item['locations'])
                break
        buttons = buttonsToActionList(locations)
        dispatcher.utter_message(text="murashaka gukorera iyihe kategori y'imodoka",buttons=buttons)
        return []
    
# class FormPermanentDrivingLicense(FormAction):
#     def name(self)->Text:
#         return 'permanent_driving_license_form_test'
    
#     @staticmethod
#     def required_slots(tracker:Tracker)->List[Text]:
#         return [
#             'id',
#             'temporary_driving_license_number_slot',
#             'permanent_driving_license_date_slot',
#             'permanent_driving_license_car_category_slot',
#             'permanent_driving_license_district_slot',
#             'permanent_driving_license_location'
#         ]
#     def slot_mappings(self)->Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "id": [self.from_entity(entity="id")],
#             "temporary_driving_license_number_slot": [self.from_entity(entity="temporary_driving_license_number_slot")],
#             "permanent_driving_license_date_slot": [self.]
#         }