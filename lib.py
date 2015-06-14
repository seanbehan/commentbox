import requests
from urllib import urlencode
import json
import dataset

# os.environ.get('DATABASE_URL')
db = dataset.connect('sqlite:///development.db')

def search_places(lat=None, lng=None, place_id=None):
    if place_id:
        return get_place(place_id=place_id)

    return [dict(name=p['name'], place_id=p['place_id']) for p in google_places(lat=lat, lng=lng)['results']]

def get_place(place_id):
    '''
    return place from database or google places api
    '''
    place = db['places'].find_one(place_id=place_id)

    if not place:
        result = google_place(place_id)['result']

        place = dict(place_id=result['place_id'], name=result['name'])
        db['places'].insert(place)

    return place

PARAMS = dict(
        key="AIzaSyA2t1lVBkuAWzSZuiymfYZ1xOQ1XKMhiqc",
        rankby="distance",
        types="accounting|airport|amusement_park|aquarium|art_gallery|atm|bakery|bank|bar|beauty_salon|bicycle_store|book_store|bowling_alley|bus_station|cafe|campground|car_dealer|car_rental|car_repair|car_wash|casino|cemetery|church|city_hall|clothing_store|convenience_store|courthouse|dentist|department_store|doctor|electrician|electronics_store|embassy|establishment|finance|fire_station|florist|food|funeral_home|furniture_store|gas_station|general_contractor|grocery_or_supermarket|gym|hair_care|hardware_store|health|hindu_temple|home_goods_store|hospital|insurance_agency|jewelry_store|laundry|lawyer|library|liquor_store|local_government_office|locksmith|lodging|meal_delivery|meal_takeaway|mosque|movie_rental|movie_theater|moving_company|museum|night_club|painter|park|parking|pet_store|pharmacy|physiotherapist|place_of_worship|plumber|police|post_office|real_estate_agency|restaurant|roofing_contractor|rv_park|school|shoe_store|shopping_mall|spa|stadium|storage|store|subway_station|synagogue|taxi_stand|train_station|travel_agency|university|veterinary_care|zoo",
        sensor="true",
    )

def google_places(lat=None,lng=None):
    PARAMS['location']='%2f,%2f' % (lat,lng)
    url = "https://maps.googleapis.com/maps/api/place/search/json?%s" % urlencode(PARAMS)

    return json.loads(requests.get(url).text)

def google_place(place_id):
    PARAMS['placeid'] = place_id
    url = "https://maps.googleapis.com/maps/api/place/details/json?%s" % urlencode(PARAMS)

    return json.loads(requests.get(url).text)
