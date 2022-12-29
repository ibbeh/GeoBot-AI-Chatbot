# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted


import pytz
import datetime

import requests




capitals = {
    'Afghanistan': 'Kabul',
    'Albania': 'Tirana',
    'Algeria': 'Algiers',
    'Andorra': 'Andorra la Vella',
    'Angola': 'Luanda',
    'Antigua and Barbuda': 'Saint John\'s',
    'Argentina': 'Buenos Aires',
    'Armenia': 'Yerevan',
    'Australia': 'Canberra',
    'Austria': 'Vienna',
    'Azerbaijan': 'Baku',
    'Bahamas': 'Nassau',
    'Bahrain': 'Manama',
    'Bangladesh': 'Dhaka',
    'Barbados': 'Bridgetown',
    'Belarus': 'Minsk',
    'Belgium': 'Brussels',
    'Belize': 'Belmopan',
    'Benin': 'Porto-Novo',
    'Bhutan': 'Thimphu',
    'Bolivia': 'La Paz (administrative) / Sucre (judicial)',
    'Bosnia and Herzegovina': 'Sarajevo',
    'Botswana': 'Gaborone',
    'Brazil': 'Brasília',
    'Brunei': 'Bandar Seri Begawan',
    'Bulgaria': 'Sofia',
    'Burkina Faso': 'Ouagadougou',
    'Burma': 'Naypyidaw',
    'Burundi': 'Bujumbura',
    'Cabo Verde': 'Praia',
    'Cambodia': 'Phnom Penh',
    'Cameroon': 'Yaoundé',
    'Canada': 'Ottawa',
    'Central African Republic': 'Bangui',
    'Chad': 'N\'Djamena',
    'Chile': 'Santiago',
    'China': 'Beijing',
    'Colombia': 'Bogotá',
    'Comoros': 'Moroni',
    'Congo (Brazzaville)': 'Brazzaville',
    'Congo (Kinshasa)': 'Kinshasa',
    'Costa Rica': 'San José',
    'Cote d\'Ivoire': 'Yamoussoukro (official) / Abidjan (de facto)',
    'Croatia': 'Zagreb',
    'Cuba': 'Havana',
    'Cyprus': 'Nicosia',
    'Czech Republic': 'Prague',
    'Denmark': 'Copenhagen',
    'Djibouti': 'Djibouti',
    'Dominica': 'Roseau',
    'Dominican Republic': 'Santo Domingo',
    'Ecuador': 'Quito',
    'Egypt': 'Cairo',
    'El Salvador': 'San Salvador',
    'Equatorial Guinea': 'Malabo',
    'Eritrea': 'Asmara',
    'Estonia': 'Tallinn',
    'Ethiopia': 'Addis Ababa',
    'Fiji': 'Suva',
    'Finland': 'Helsinki',
    'France': 'Paris',
    'Gabon': 'Libreville',
    'Gambia': 'Banjul',
    'Georgia': 'Tbilisi',
    'Germany': 'Berlin',
    'Ghana': 'Accra',
    'Greece': 'Athens',
    'Grenada': 'Saint George\'s',
    'Guatemala': 'Guatemala City',
    'Guinea': 'Conakry',
    'Guinea-Bissau': 'Bissau',
    'Guyana': 'Georgetown',
    'Haiti': 'Port-au-Prince',
    'Honduras': 'Tegucigalpa',
    'Hungary': 'Budapest',
    'Iceland': 'Reykjavik',
    'India': 'New Delhi',
    'Indonesia': 'Jakarta',
    'Iran': 'Tehran',
    'Iraq': 'Baghdad',
    'Ireland': 'Dublin',
    'Israel': 'Jerusalem (proclaimed as such, but with no internationally recognized borders) Tel Aviv (de facto capital)',
    'Italy': 'Rome',
    'Jamaica': 'Kingston',
    'Japan': 'Tokyo',
    'Jordan': 'Amman',
    'Kazakhstan': 'Astana',
    'Kenya': 'Nairobi',
    'Kiribati': 'Tarawa',
    'Kosovo': 'Pristina',
    'Kuwait': 'Kuwait City',
    'Kyrgyzstan': 'Bishkek',
    'Laos': 'Vientiane',
    'Latvia': 'Riga',
    'Lebanon': 'Beirut',
    'Lesotho': 'Maseru',
    'Liberia': 'Monrovia',
    'Libya': 'Tripoli',
    'Liechtenstein': 'Vaduz',
    'Lithuania': 'Vilnius',
    'Luxembourg': 'Luxembourg City',
    'Macedonia (FYROM)': 'Skopje',
    'Madagascar': 'Antananarivo',
    'Malawi': 'Lilongwe',
    'Malaysia': 'Kuala Lumpur',
    'Maldives': 'Malé',
    'Mali': 'Bamako',
    'Malta': 'Valletta',
    'Marshall Islands': 'Majuro',
    'Mauritania': 'Nouakchott',
    'Mauritius': 'Port Louis',
    'Mexico': 'Mexico City',
    'Micronesia': 'Palikir',
    'Moldova': 'Chisinau',
    'Monaco': 'Monaco',
    'Mongolia': 'Ulaanbaatar',
    'Montenegro': 'Podgorica',
    'Morocco': 'Rabat',
    'Mozambique': 'Maputo',
    'Namibia': 'Windhoek',
    'Nauru': 'Yaren',
    'Nepal': 'Kathmandu',
    'Netherlands': 'Amsterdam',
    'New Zealand': 'Wellington',
    'Nicaragua': 'Managua',
    'Niger': 'Niamey',
    'Nigeria': 'Abuja',
    'North Korea': 'Pyongyang',
    'Norway': 'Oslo',
    'Oman': 'Muscat',
    'Pakistan': 'Islamabad',
    'Palau': 'Ngerulmud',
    'Palestine': 'Ramallah',
    'Panama': 'Panama City',
    'Papua New Guinea': 'Port Moresby',
    'Paraguay': 'Asunción',
    'Peru': 'Lima',
    'Philippines': 'Manila',
    'Poland': 'Warsaw',
    'Portugal': 'Lisbon',
    'Qatar': 'Doha',
    'Romania': 'Bucharest',
    'Russia': 'Moscow',
    'Rwanda': 'Kigali',
    'Saint Kitts and Nevis': 'Basseterre',
    'Saint Lucia': 'Castries',
    'Saint Vincent and the Grenadines': 'Kingstown',
    'Samoa': 'Apia',
    'San Marino': 'San Marino',
    'Sao Tome and Principe': 'São Tomé',
    'Saudi Arabia': 'Riyadh',
    'Senegal': 'Dakar',
    'Serbia': 'Belgrade',
    'Seychelles': 'Victoria',
    'Sierra Leone': 'Freetown',
    'Singapore': 'Singapore',
    'Slovakia': 'Bratislava',
    'Slovenia': 'Ljubljana',
    'Solomon Islands': 'Honiara',
    'Somalia': 'Mogadishu',
    'South Africa': 'Pretoria (administrative) / Cape Town (legislative) / Bloemfontein (judicial)',
    'South Korea': 'Seoul',
    'South Sudan': 'Juba',
    'Spain': 'Madrid',
    'Sri Lanka': 'Colombo',
    'Sudan': 'Khartoum',
    'Suriname': 'Paramaribo',
    'Swaziland': 'Mbabane',
    'Sweden': 'Stockholm',
    'Switzerland': 'Bern',
    'Syria': 'Damascus',
    'Taiwan': 'Taipei',
    'Tajikistan': 'Dushanbe',
    'Tanzania': 'Dodoma (official) / Dar es Salaam (de facto)',
    'Thailand': 'Bangkok',
    'Timor-Leste': 'Dili',
    'Togo': 'Lomé',
    'Tonga': 'Nuku\'alofa',
    'Trinidad and Tobago': 'Port of Spain',
    'Tunisia': 'Tunis',
    'Turkey': 'Ankara',
    'Turkmenistan': 'Ashgabat',
    'Tuvalu': 'Funafuti',
    'Uganda': 'Kampala',
    'Ukraine': 'Kiev',
    'United Arab Emirates': 'Abu Dhabi',
    'United Kingdom': 'London',
    'United States': 'Washington, D.C.',
    'Uruguay': 'Montevideo',
    'Uzbekistan': 'Tashkent',
    'Vanuatu': 'Port Vila',
    'Vatican City': 'Vatican City',
    'Venezuela': 'Caracas',
    'Vietnam': 'Hanoi',
    'Yemen': 'Sana\'a',
    'Zambia': 'Lusaka',
    'Zimbabwe': 'Harare'
}

timezones = {
    "London": "UTC+1:00",
    "Sofia": "UTC+3:00",
    "Lisbon": "UTC+1:00",
    "Mumbai": "UTC+5:30"
}

#timezones = pytz.all_timezones

class ActionGiveCapital(Action):

    def name(self) -> Text:
        return "action_give_capital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        country = tracker.get_slot("country").title()
        capital = capitals.get(country)
    
        if capital is None:
            output = "Could not find the capital of {}".format(country)
        else:
            output = "The capital of {} is {}".format(country, capital)

        dispatcher.utter_message(text=output)

        return []


class ActionGiveTimeZone(Action):

    def name(self) -> Text:
        return "action_show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        timezone = pytz.timezone(city)
        current_time = datetime.datetime.now(timezone)
        timeInTimeZone = current_time.strftime("%H:%M:%S")


        # for i in range(len(timezones)-1):
        #     print(timezones[i])
        #     if city in timezones[i]:
        #         timezone = pytz.timezone(city)
        #         current_time = datetime.datetime.now(timezone)
        #         output = "The time zone of {} is {}".format(city, current_time)

        #     else:
        #         output = "The time zone of {} could not be found. Please try another time zone".format(city)
        #         timezone = None

    
        if timezone is None:
            output = "Could not find the time zone of {}".format(city)
        else:
            output = "The time in the time zone {} is {}".format(city, timeInTimeZone)

        dispatcher.utter_message(text=output)

        return []

class ActionGiveLargestCountry(Action):

    def name(self) -> Text:
        return "action_show_largest_country"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        region = tracker.get_slot("region")
    
        if region.upper() == "ASIA":
            output = "The largest country in {} by area is Russia and the largest country in {} by population is China".format(region, region)
        elif region.upper() == "AFRICA":
            output = "The largest country in {} by area is Algeria and the largest country in {} by population is Nigeria".format(region, region)
        elif region.upper() == "EUROPE":
            output = "The largest country in {} by area is Russia (or Ukraine) and the largest country in {} by population is Russia (or Germany)".format(region, region)
        elif region.upper() == "NORTH AMERICA":
            output = "The largest country in {} by area is Canada and the largest country in {} by population is the United States".format(region, region)
        elif region.upper() == "SOUTH AMERICA":
            output = "The largest country in {} by area is Brazil and the largest country in {} by population is Brazil".format(region, region)
        elif region.upper() == "ANTARCTICA":
            output = "There are no countries in Antarctica. However, the most populated area in Antarctica is McMurdo Station."
        elif region.upper() == "OCEANIA":
            output = "The largest country in {} by area is Australia and the largest country in {} by population is Australia".format(region, region)
        elif region.upper() == "AUSTRALIA":
            output = "The largest country in {} by area is Australia and the largest country in {} by population is Australia".format(region, region)
        elif region.upper() == "WORLD" or region.upper() == "PLANET" or region.upper() == "EARTH":
            output = "The largest country in {} by area is Russia and the largest country in {} by population is China".format(region, region)
        else:
            output = "Sorry, I could not find the largest country in {}".format(region)

        dispatcher.utter_message(text=output)

        return []


class HandleUnknownIntent(Action):
    def name(self) -> Text:
        return "action_handle_unknown_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Reset the conversation to the previous state
        dispatcher.utter_message(template="I am sorry, I do not understand what you are trying to do. Remember I have limited capabilities and I only have certain functionalities such as telling you the time of any time zone in the world, and the population and capital of any country in the world.")
        return [UserUtteranceReverted()]
