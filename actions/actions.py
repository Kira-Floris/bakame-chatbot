# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker
# from rasa_sdk.forms import FormAction
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
        
def buttonsToActionList(data, slot, entity):
    buttons = []
    for i in data:
        buttons.append({"title":i,"payload":"/"+slot+"{\""+entity+"\": \""+i+"\"}"})
    return buttons
    
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
        buttons = buttonsToActionList(dates,"permanent_driving_license_date","permanent_driving_license_date_slot")
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
        buttons = buttonsToActionList(car_categories, "permanent_driving_license_category", "permanent_driving_license_car_category_slot")
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
        buttons = buttonsToActionList(districts, "permanent_driving_license_district", "permanent_driving_license_district_slot")
        dispatcher.utter_message(text="murashaka gukorera mu kahe karere",buttons=buttons)
        return []
    
class ActionPermanentDrivingLicenseLocation(Action):
    def name(self):
        return 'action_ask_permanent_driving_license_location_slot'
    
    def run(self,
            dispatcher:CollectingDispatcher, 
            tracker:Tracker, 
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        district_slot = tracker.get_slot('permanent_driving_license_district_slot')
        information = GetInformation('permanent_driving_license')
        locations = []
        for item in information.get_key('slots')['permanent_driving_license_district_choices']:
            if item['name']==district_slot:
                locations.extend(item['locations'])
                break
        buttons = buttonsToActionList(locations, "permanent_driving_license_location", "permanent_driving_license_location_slot")
        dispatcher.utter_message(text="murashaka gukorera iyihe kategori y'imodoka",buttons=buttons)
        return []
    
class ActionSubmitPermanentDrivingLicenseForm(Action):
    def name(self):
        return 'action_submit_permanent_driving_license_form'
    
    def run(
        self,
        dispatcher:CollectingDispatcher,
        tracker:Tracker,
        domain: Dict[Text,Any]
    ) -> List[Dict[Text, Any]]:
        id_ = tracker.get_slot('id')
        temporary_driving_license_number_slot = tracker.get_slot('temporary_driving_license_number_slot')
        permanent_driving_license_date_slot = tracker.get_slot('permanent_driving_license_date_slot')
        permanent_driving_license_car_category_slot = tracker.get_slot('permanent_driving_license_car_category_slot')
        permanent_driving_license_district_slot = tracker.get_slot('permanent_driving_license_district_slot')
        permanent_driving_license_location_slot = tracker.get_slot('permanent_driving_license_location_slot')
        submit = f"""
        indangamuntu: {id_}\n
        nomero y'agateganyo: {temporary_driving_license_number_slot}\n
        itariki yo gukoreraho: {permanent_driving_license_date_slot}\n
        akarere ko gukoreramo: {permanent_driving_license_district_slot}\n
        location yo gukoreramo: {permanent_driving_license_location_slot}
        """
        dispatcher.utter_message(text=submit)
        return []