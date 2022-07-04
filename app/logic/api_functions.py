from app.configs.logger import log
from uszipcode import SearchEngine
from app.logic.helping_functions import *
from app.configs.config import configuration


def get_zipcode_information(zipcode: str) -> dict:
    """
    Fetch all information for a given zipcode (str).

    Args:
        zipcode (str): e.g "10001"

    Returns:
        dict: {
            "success": True, 
            "zipcode_information": zipcode information (dict)

            }
    """
    zipcode_information = SearchEngine(db_file_path=configuration.DB_PATH).by_zipcode(zipcode).to_dict()
    return {"success": True, "zipcode_information": zipcode_information}


def search_for_zipcodes_from_the_center_of_the_city(city: str, county: str, state: str, radius: float) -> dict:
    """
    Finds all the zipcodes in a given radius around the centroid of the city.
    
    Args:
        city (str): e.g "New York City"
        state (str): e.g "NY"
        radius (float): e.g 5. Should be given in miles

    Returns:
        dict: {
            "success": True, 
            "zipcodes": list of zipcodes (list), 
            "count_zipcodes": number of zipcodes (int), 
            "lat": latitude of city (float), 
            "lng": longitude of city (float)

            }
    """
    lat, lng = get_city_centroid(city=city, county=county, state=state)
    zipcodes = search_from_cordinate(lat=lat, lng=lng, radius=radius)

    return {"success": True, "zipcodes": zipcodes, "count_zipcodes": len(zipcodes), "lat": lat, "lng": lng}
    

def search_for_zipcodes_from_the_center_of_the_city_info(city: str, county: str, state: str, radius: float) -> dict:
    """
    Finds all the zipcodes in a given radius around the centroid of the city. Also their information is included.
    
    Args:
        city (str): e.g "New York City"
        state (str): e.g "NY"
        radius (float): e.g 5. Should be given in miles

    Returns:
        dict: {
            "success": True, 
            "zipcodes_info": zipcodes and their respective information (dict)
            
            }
    """
    lat, lng = get_city_centroid(city=city, county=county, state=state)
    zip_ls = search_from_cordinate(lat=lat, lng=lng, radius=radius)
    zipcodes_info = get_information_for_zipcodes(zip_ls)

    return zipcodes_info


def is_close_from_the_center_of_the_city(zipcode: str, city: str, county: str, state: str, radius: float) -> dict:
    """
    Returns True if a given zipcode is not further from the city centroid than a given radius.
    Otherwise returns False.

    Args:
        zipcode (str): e.g "10001"
        city (str): e.g "New York City"
        state (str): e.g "NY"
        radius (float): e.g 5. Should be given in miles

    Returns:
        dict: {
            "success": True, 
            "is_close": True if zipcode is inside the radius otherwise False (bool), 
            "distance": distance of zipcode from the center of the city (float)
            
            }
    """
    zip_info = SearchEngine(db_file_path=configuration.DB_PATH).by_zipcode(zipcode)

    try:
        zip_n, zip_s, zip_w, zip_e = zip_info.bounds_north, zip_info.bounds_south, zip_info.bounds_west, zip_info.bounds_east
        zip_center = (zip_n+zip_s)/2, (zip_e+zip_w)/2
        log.info("Precise centroid calculated.")
    except TypeError:
        log.info("Default lat and lng used.")
        zip_center = zip_info.lat, zip_info.lng

    city_center = get_city_centroid(city=city, county=county, state=state)
    dist = distance(city_center, zip_center)

    if dist <= radius:
        return {"success": True, "is_close": True, "distance": dist}
    return {"success": True, "is_close": False, "distance": dist}


def get_information_for_zipcodes(zipcodes: list) -> dict:
    """Fetch information for each zipcode from a list of zipcodes

    Args:
        zipcodes (list): e.g ["10001", "10002"]

    Returns:
        dict: {
            "success": True, 
            "zipcodes_info": zipcodes and their respective information (dict)
            
            }
    """
    res = dict()
    for zipcode in zipcodes:
            zip_info = SearchEngine(db_file_path=configuration.DB_PATH).by_zipcode(zipcode).to_dict()
            res.update({f"{zipcode}": zip_info})
    return {"success": True, "zipcodes_info": res}


def search_for_zipcodes_by_city(city: str, county: str, state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_city_and_state(city=city, state=state, zipcode_type=None, returns=None)
    zipcodes = [z.zipcode for z in zipcodes] if county.lower() in ["none", "nan"] else [z.zipcode for z in zipcodes if z.county == county]
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}


def search_for_zipcodes_by_city_info(city: str, county: str, state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_city_and_state(city=city, state=state, zipcode_type=None, returns=None)
    zipcodes = [z.to_dict() for z in zipcodes] if county.lower() in ["none", "nan"] else [z.to_dict() for z in zipcodes if z.county == county]
    zipcodes = {zipcode["zipcode"]: zipcode for zipcode in zipcodes}
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}


def search_for_zipcodes_by_county(county: str, state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_state(state=state, zipcode_type=None, returns=None)
    zipcodes = [z.zipcode for z in zipcodes if z.county == county]
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}


def search_for_zipcodes_by_county_info(county: str, state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_state(state=state, zipcode_type=None, returns=None)
    zipcodes = [z.to_dict() for z in zipcodes if z.county == county]
    zipcodes = {zipcode["zipcode"]: zipcode for zipcode in zipcodes}
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}


def search_for_zipcodes_by_state(state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_state(state=state, returns=None, zipcode_type=None)
    zipcodes = [zipcode.zipcode for zipcode in zipcodes]
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}


def search_for_zipcodes_by_state_info(state: str) -> dict:
    zipcodes = SearchEngine(db_file_path=configuration.DB_PATH).by_state(state=state, returns=None, zipcode_type=None)
    zipcodes = [zipcode.to_dict() for zipcode in zipcodes]
    zipcodes = {zipcode["zipcode"]: zipcode for zipcode in zipcodes}
    return {"success": True, "number_of_zip_codes": len(zipcodes), "zipcodes": zipcodes}
