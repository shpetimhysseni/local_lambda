from flask import Blueprint, request
import app.logic.api_functions as api_functions
from app.logic.helping_functions import format
from app.configs.logger import log


api = Blueprint("api", __name__)


@api.route("/")
def base():
    return "API is working", 200


@api.route("/get_zipcode_information/<zipcode>", methods = ["GET"])
def get_zipcode_information(zipcode: str):
    try:
        response = api_functions.get_zipcode_information(zipcode)
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_from_the_center_of_the_city/<city>/<county>/<state>/<radius>", methods = ["GET"])
def search_for_zipcodes_from_the_center_of_the_city(city: str, county: str, state: str, radius: float):
    print(200*"=")
    print(city, county, state)
    print(format(city, county, state))
    try:
        response = api_functions.search_for_zipcodes_from_the_center_of_the_city(*format(city, county, state), float(radius))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_from_the_center_of_the_city_info/<city>/<county>/<state>/<radius>", methods = ["GET"])
def search_for_zipcodes_from_the_center_of_the_city_info(city: str, county: str, state: str, radius: float):
    try:
        response = api_functions.search_for_zipcodes_from_the_center_of_the_city_info(*format(city, county, state), float(radius))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/is_close_from_the_center_of_the_city/<zipcode>/<city>/<county>/<state>/<radius>", methods = ["GET"])
def is_close_from_the_center_of_the_city(zipcode: str, city: str, county: str, state: str, radius: float):
    try:
        response = api_functions.is_close_from_the_center_of_the_city(zipcode ,*format(city, county, state), float(radius))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/get_information_for_zipcodes", methods = ["POST"])
def get_information_for_zipcodes():
    try:
        zipcodes = request.get_json()["zipcodes"]
        response = api_functions.get_information_for_zipcodes(zipcodes)
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_city/<city>/<county>/<state>", methods = ["GET"])
def search_for_zipcodes_by_city(city: str, county: str, state: str):
    try:
        response = api_functions.search_for_zipcodes_by_city(*format(city, county, state))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_city_info/<city>/<county>/<state>", methods = ["GET"])
def search_for_zipcodes_by_city_info(city: str, county: str, state: str):
    try:
        response = api_functions.search_for_zipcodes_by_city_info(*format(city, county, state))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_county/<county>/<state>", methods = ["GET"])
def search_for_zipcodes_by_county(county: str, state: str):
    try:
        response = api_functions.search_for_zipcodes_by_county(*format(county, state))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_county_info/<county>/<state>", methods = ["GET"])
def search_for_zipcodes_by_county_info(county: str, state: str):
    try:
        response = api_functions.search_for_zipcodes_by_county_info(*format(county, state))
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_state/<state>", methods = ["GET"])
def search_for_zipcodes_by_state(state: str):
    try:
        response = api_functions.search_for_zipcodes_by_state(state)
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400


@api.route("/search_for_zipcodes_by_state_info/<state>", methods = ["GET"])
def search_for_zipcodes_by_state_info(state: str):
    try:
        response = api_functions.search_for_zipcodes_by_state_info(state)
        return response, 200
    except Exception as e:
        log.error(e)
        return {"success": False, "error": e}, 400

