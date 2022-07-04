from uszipcode import SearchEngine
from haversine import haversine, Unit
from app.configs.config import configuration

sa_sn = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming"
}


def distance(point_1: tuple, point_2: tuple)-> float:
    return haversine(point_1, point_2, unit=Unit.MILES)


def get_city_bounds(city: str, county: str, state: str)-> tuple:
    SimpleZipcode_objects = SearchEngine(db_file_path=configuration.DB_PATH).by_state(state=state, zipcode_type=None, returns=None)
    SimpleZipcode_objects = [SimpleZipcode_object for SimpleZipcode_object in SimpleZipcode_objects if SimpleZipcode_object.city == city]
    if county.lower() not in ["none", "nan"]:
        SimpleZipcode_objects = [SimpleZipcode_object for SimpleZipcode_object in SimpleZipcode_objects if SimpleZipcode_object.county == county]

    bounds_west, bounds_east, bounds_north, bounds_south = [], [], [], []

    for SimpleZipcode_object in SimpleZipcode_objects:

        if SimpleZipcode_object.bounds_west is not None:
            bounds_west.append(SimpleZipcode_object.bounds_west)

        if SimpleZipcode_object.bounds_east is not None:
            bounds_east.append(SimpleZipcode_object.bounds_east)

        if SimpleZipcode_object.bounds_north is not None:
            bounds_north.append(SimpleZipcode_object.bounds_north)

        if SimpleZipcode_object.bounds_south is not None:
            bounds_south.append(SimpleZipcode_object.bounds_south)

    north = max(bounds_north)
    south = min(bounds_south)
    west = min(bounds_west)
    east = max(bounds_east)

    return north, south, west, east


def get_city_centroid(city: str, county: str, state: str)-> tuple:
    north, south, west, east = get_city_bounds(city=city, county=county, state=state)

    lat = (north+south)/2
    lng = (west+east)/2

    centroid = lat, lng
    return centroid


def get_city_radius(city: str, county: str, state: str)-> float:
    n, s, w, e =  get_city_bounds(city=city, county=county, state=state)
    city_centroid = get_city_centroid(city=city, county=county, state=state)
    radius = []
    for point in ((n, w),(n, e),(s, w),(s, e)):
        radius.append(distance(city_centroid, point))
    radius = max(radius)
    return radius


def search_from_cordinate(lat: float, lng: float, radius: float)-> list:
    """
    Finds all the zipcodes that lie in a given radius around a given point(lat, lng).

    Args:
        lat (float): latitude of the geographical point
        lng (float): longitude of the geographical point
        radius (float): e.g 5. Should be given in miles

    Returns:
        list: list of zipcodes(str). 
    """
    radius +=2
    SimpleZipcode_objects = SearchEngine(db_file_path=configuration.DB_PATH).by_coordinates(
        lat=lat, 
        lng=lng, 
        radius=radius, 
        zipcode_type=None, 
        returns=None
        )
    zip_ls = [SimpleZipcode_object.zipcode for SimpleZipcode_object in SimpleZipcode_objects]
    
    return zip_ls


def format(*args):
    res = []

    import sqlite3
    con = sqlite3.connect(configuration.DB_PATH)

    counties = [c[0] for c in con.execute("select distinct county from simple_zipcode;").fetchall()]
    cities = [c[0] for c in con.execute("select distinct major_city from simple_zipcode;").fetchall()]
    
    if len(args) == 3:
        if args[0].replace("_", " ") in cities:
            city = args[0].replace("_", " ")
        elif args[0].replace("_", " ").title() in cities:
            city = args[0].replace("_", " ").title()
        else:
            city = "none"
        res.append(city)
        

        if args[0].replace("_", " ") in counties:
            county = args[0].replace("_", " ")
        elif args[0].replace("_", " ").title() in counties:
            county = args[0].replace("_", " ").title()
        else:
            county = "none"
        res.append(county)
                

        if args[-1].upper() in sa_sn.keys():
            state_abb = args[-1].upper()
        if args[-1].replace("_", " ") in sa_sn.values():
            state = args[-1].replace("_", " ")
            sn_sa = {sa_sn[key]: key for key in sa_sn.keys()}
            state_abb = sn_sa[state]  
            res.append(state_abb)
        res.append(state_abb)              
    
    elif len(args) == 2:
        if args[0].replace("_", " ") in counties:
            county = args[0].replace("_", " ")
        if args[0].replace("_", " ").title() in counties:
            county = args[0].replace("_", " ").title()
        else:
            county = "none"
        res.append(county)
                

        if args[-1].upper() in sa_sn.keys():
            state_abb = args[-1].upper()
        if args[-1].replace("_", " ") in sa_sn.values():
            state = args[-1].replace("_", " ")
            sn_sa = {sa_sn[key]: key for key in sa_sn.keys()}
            state_abb = sn_sa[state]  
            res.append(state_abb)
        res.append(state_abb)              
    
    con.close()

    return res