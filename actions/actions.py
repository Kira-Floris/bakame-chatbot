# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset

irembo_information_json = 'actions/temporary_irembo_information.json'
id_information_json = 'actions/national_id.json'
temporary_license_information_json = 'actions/temporary_driving_license.json'
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
        
class GetId:
    def __init__(self, id):
        self.id = id
        self.data = None
        try:
            with open(id_information_json, 'r') as f:
                information = json.load(f)
            self.data = information[self.id]
            f.close()
        except Exception as err:
            self.data = None
        if self.data:
            self.name = self.data["name"]
        else:
            self.name = None
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
class GetTemporaryLicenseInfo:
    def __init__(self, temporary_no):
        self.temporary_no = temporary_no
        self.data = None
        try:
            with open(temporary_license_information_json, 'r') as f:
                information = json.load(f)
            self.data = information[self.temporary_no]
            f.close()
        except Exception as err:
            self.data = None
        if self.data:
            self.id = self.data["id"]
        else:
            self.id = None
    
    def get_temporary_no(self):
        return self.temporary_no
    
    def get_id(self):
        return self.id
        
        
def buttonsToActionList(data, slot, entity):
    buttons = []
    for i in data:
        buttons.append({"title":i,"payload":"/"+slot+"{\""+entity+"\": \""+i+"\"}"})
    return buttons

class ValidatePermanentDrivingLicenseForm(FormValidationAction):
    def name(self)->Text:
        return "validate_permanent_driving_license_form"
    
    def validate_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        person = GetId(slot_value)
        names = person.get_name()
        if not names:
            dispatcher.utter_message(text="indangamuntu yawe ntitubashije kuyibona")
            return {"id": None}
        else:
            SlotSet("names", names)
            dispatcher.utter_message(text=f"amazina yawe ni {names}")
            return {"id": slot_value, "names": names}
        
    def validate_temporary_driving_license_number_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        doc = GetTemporaryLicenseInfo(slot_value)
        id_ = doc.get_id()
        if not id_:
            dispatcher.utter_message(text="nomero y'agateganyo ntabwo tuyizi")
            return {"temporary_driving_license_number_slot": None}
        else:
            return {"temporary_driving_license_number_slot": slot_value}
        
    
def ActionResetAllSlots(Action):
    def name(self):
        return "action_reset_all_slots"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    )-> List[Dict[Text, Any]]:
        all_slots = tracker.slots
        # for slot_name, slot_value in all_slots.items():
        #     SlotSet(slot_name, None)
        tracker.slots.clear()
        dispatcher.utter_message('Amakuru yawe yose yakuwemo')
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
        dispatcher.utter_message(text=f"murashaka gukorera mu kahe gace ka {district_slot}",buttons=buttons)
        return []
    
class ActionSubmit(Action):
    def name(self):
        return 'action_submit_yes_or_no'
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    )-> List[Dict[Text, Any]]:
        buttons = [
            {"payload":"/affirm","title":"yego"},
            {"payload":"/deny","title":"oya"}
        ]
    
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
        
        response = {
            "id": id_,
            "temporary driving license number": temporary_driving_license_number_slot,
            "date": permanent_driving_license_date_slot,
            "car category": permanent_driving_license_car_category_slot,
            "district": permanent_driving_license_district_slot,
            "location": permanent_driving_license_location_slot
        }
        
        dispatcher.utter_message(json_message=response, text="Amakuru yawe twayakiriye")
        return []