from flask import Flask, request, jsonify
import sys
import xmltodict
import logging

#Setting up the logging
logging.basicConfig(level=logging.DEBUG)

#Creating an intance of the class flask in the variable called 'app'
app = Flask(__name__)

#Going to load the positional_data and sighting_data, they are both going to be global variables, both variables are empty to begin with
positional_data = {}
sighting_data = {}

#This function will populate the two global varaibles, 'positional_data' and 'sighting_data' with data from the xml files that were provided
@app.route('/data', methods=['POST', 'GET'])
def set_variables():
    '''
    This function will set the global variables with the correspoding XML data

    Args:
        postional_data_file (string): It is a string that is the name of the file for positional_data.
        sighting_data_file (string): It is a string that is the name of the file for sighting_data.

    Returns:
        This function will return nothing, it will only set the global varaibles with the correct data.
    '''
    #If statement incase the user inputs a method anything other than Post
    if(request.method != 'POST'):
        logging.warning('The user inputted the incorrect method')
        return  '''
        \n
This is a route for gathering the data that was downloaded and inputted to variables
a POST request to this route to get it to work, for example:
        
curl -X POST localhost:5036/reset
        \n
        '''
    #Creating the global variables
    global positional_data
    global sighting_data

    #Trying a new approach in order to read the file for position data
    with open ('position_data.xml', 'r') as f:
        #'xmltodict' turns the xml file to a dictionary like if it was a json file, this variable is a dictionary now
        positional_data = xmltodict.parse(f.read())

    #Trying a new approach in order to read the file for sighting data
    with open ('sighting_data.xml', 'r') as f:
        #'xmltodict' turns the xml file to a dictionary like if it was a json file, this variable is a dictionary now
        sighting_data = xmltodict.parse(f.read())
    
    return '\nData has been read from the file\n'

#The purpose of this route: Retuns information on how to interact with the application, (GET)
@app.route('/', methods=['GET', 'POST'])
def welcome_message():
    '''
    This function will display a welcoem messsage to the user, and will tell the user how to use this application

    Returns:
         (string): It is a string that has the welcome message for the user to read in order to understand how to use this application
    '''
   
    return '''
    \n
### ISS Tracker 9000 ###

Instructions on how to use this application:

1.- '/'                                                    (GET) prints welcome screen info
2.- '/data'                                                (POST) gathers data from the two files

Routes for querying positional and velocity data:

3.- '/epochs'                                              (GET) list all epochs
4.- '/epochs/<epoch>'                                      (GET) info concerning a specific <epoch>

Routes for querying sighting data:

5.- '/countries'                                           (GET) List of all countries
6.- '/countries/<country>'                                 (GET) All data associated with <country>
7.- '/countries/<country>/regions'                         (GET) List of all regions for <country>
8.- '/countries/<country>/regions/<regions>/cities'        (GET) List of all cities in that region
9.- '/countries/<country>/regions/<regions>/cities/<city>' (GET) All data for the <city>
    \n
    '''
    
#The purpose of this route: Returns all Epochs in the positional data, I am assuming that I will return a list of dictionary that each contain data of all Epochs in poistional data. (GET)
@app.route('/get_epochs', methods=['GET', 'POST'])
def get_all_epochs():
    '''
    This function will display all of the epoch information for the user to see

    Returns:
        list_of_epochs (list) it will be list that contains all the epoch starting time. But to prevent
        errors from happening we are to use jsonify to turn the list into JSON data
    '''
    
    #In case the query is not handled as a "GET", and this string is returned and displayed
    if(request.method != 'GET'):
        logging.warning('The user inputted the incorrect method')
        return '''
        \n
        This is a route for displaying all the data concerning epoch. You must perform
        a GET request to this route to get it to work, for example:

        curl -X GET localhost:5036/get_epochs
        
        or 

        curl localhost:5036/get_epochs
        \n
        '''

    #Checks that the varibles that store the data is not empty
    if(len(positional_data) == 0):
        logging.warning('The global variable, positional_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of 
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then repeat the command you just did.
        \n
        '''

    #Going to create a list and will iterate through the positional_data to get all the epochs data
    list_of_epochs = []

    #Going to create a variable that has access to all the positional_data 
    list_of_state_vectors = positional_data['ndm']['oem']['body']['segment']['data']['stateVector']

    #Loop through the list and get the epoch data and append it to the list, 'list_of_epochs'
    for state_vector in list_of_state_vectors:
        list_of_epochs.append(state_vector['EPOCH'])

    if(len(list_of_epochs) == 0):
        logging.warning('The returned list is empty, and it will return a None, hence an error will be commited')
        return '''
        \n
        The function returned nothing, make sure you inputted the correct URL address,
        when curling to this route
        \n
        '''
    
    return jsonify(list_of_epochs)

#The purpose of this route: Returns all the information about a specific Epoch in the positional data, (GET)
@app.route('/get_epochs/<extra_info>', methods=['GET', 'POST'])
def get_extra_info_for_epoch(extra_info):
    '''
    This function will take an argument for a specific epoch time, and it will return extra 
    information about htat epoch and that specific extra informantion

    Args:
        extra_info (string): This an arugment inputted that contains the information that we are 
        looking for. 

    Return:
        state_of_vector (dictionary): It is a dictioanry that pertains to the epoch taking into account
        the inputted extra_info by the user. In this dictionary it will contain information like:
        X, Y , Z, X_DOT, Y_DOT, Z_DOT information that will be acceptable for the user to look at
    '''
    
    #Incase they use the incorrect method, then this message will be displayed telling the user what to do instead of getting an ugly error message
    if(request.method != 'GET'):
        logging.warning('The user inputted the incorrect method')
        return '''
        This is a route is for displaying the information of a specific epoch given the extra info
        about that epoch instance. A GET request is needed for this route to work, for example:

        curl -X GET localhost:5036/epoch/<extra_info>

        or 

        curl localhost:5036/epoch/<extra_info>
        '''

    #Checks that the varibles that store the data is not empty
    if(len(positional_data) == 0):
        logging.warning('The global variable, positional_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''
    #This is the variable that contains all the possible epoch information
    vector =  positional_data['ndm']['oem']['body']['segment']['data']['stateVector']

    #We are going to loop through the vector variable and look for an epoch id that matches the 'extra_info' and then we will return the dictionary 
    for vector_state in vector:
        if(vector_state["EPOCH"] == extra_info):
            return vector_state

    logging.warning('The returned dictionary is empty, hence an error will be commited')
    #This string will be returned if the 'extra_info' is incorrect
    return '''
    \n
    The function was not able to return the information the user wanted. 
    Make sure that the <extra_info> is correct.
    \n
    '''
    

#The purpose of this route: Returns all the countries from the sighting data, (GET)
@app.route('/countries', methods=['GET', 'POST'])
def all_countries():
    '''
    This function will return a list of all the countries that are in the sighting_data

    Returns:
        list_of_countries (list): This list will contain all the countries that are found in the 
        sightings_data variable
    '''
    #If statement when the user accidently inputs the incorrect method for this route
    if(request.method != 'GET'):
        logging.warning('The user inputted the incorrect method')
        return '''
        This is a route for displaying all the countries that are in the sighting_data file.
        In order for this route to work please use these command:

        curl -X GET localhost:5036/countries

        or 

        curl localhost:5036/countries
        '''

    #Checks that the varibles that store the data is not empty
    if(len(sighting_data) == 0):
        logging.warning('The global variable, sighting_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''

    #Going to create a varaible that will have all the information, so it can be easy to loop through
    var = sighting_data['visible_passes']['visible_pass']

    #Going ot create an empty list to append data into
    country_list = []

    #We are going to loop through the data and add the country to a list
    for spotting in var:
        if(spotting['country'] not in country_list):
            country_list.append(spotting['country'])

    #Incase the returning list is empty 
    if(len(country_list) == 0):
        logging.warning('The returned list is empty, and it will return a None, hence an error will be commited')
        return '''
        \n
        The function returned an empty list, make sure that the correct URL was inputted
        when calling this function.
        \n
        '''
    #It returns a list that can be passed as a json object
    return jsonify(country_list)

#The purpose of this route: Returns all information about a specific Country in the sighting data, (GET)
@app.route('/countries/<country_name>', methods=['GET', 'POST'])
def get_country_info(country_name):
    '''
    This function will return extra information concerning the country name that was inputted.

    Args:
        country_name (string): It is a string that contain the name of the country

    returns:
       list_of_dicts (list): It is a list that returns a list of dictionaries that contain information
       regarding the country that was inputted to the function
    '''
    
    #This is the message when the user inputs the incorrect method
    if(request.method != 'GET'):
        logging.warning('The user inputted the incorrect method')
        return '''
        \n
        This function returns more information concerning the counctry that was inputted to the
        function. To get the right information use this commnad:

        curl -X GET localhost:5036/countries/<country>

        or 

        curl localhost:5036/countries/<country>     
        \n
        '''
    #Checks that the varibles that store the data is not empty
    if(len(sighting_data) == 0):
        logging.warning('The global variable, sighting_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''
    #This is a variable that will contain all the information concerning the inputted county
    country_list = []
    
    #This is the variable that contains the correct path to the country subset
    var = sighting_data['visible_passes']['visible_pass']
    
    #This is a loop that will look for the country
    for spotting in var:
        if(spotting['country'] == country_name):
            country_list.append(spotting)
    
    #This is to check that there are items inside the list
    if(len(country_list) == 0):
        logging.warning('The returning list is empty, and is causing an error')
        return '''
        \n
        The function is returning an empty list, therfore the inputted <country_name> 
        was spelled incorrectly. Mkae sure you spelled the name correctly
        \n
        '''

    #Returns a dictionary after it was jsonified, by the jsonify function
    return jsonify(country_list)


#The purpose of this route: Returns all information about a specific Region in the sighting data, (GET)
@app.route('/countries/<country>/regions', methods=['GET', 'POST'])
def get_country_regions(country):
    '''
    This function will return all the regions in for the inputted <country>

    Args:
        country (string): It is a string varible that contains the name of the country

    return:
        list_of_regions (list): It returns a list that contains the regions for that country
    '''
    #in case the user inputs the incorrect method
    if(request.method != 'GET'):
        return '''
        \n
        This function returns all the regions for the inputted country. To use this command use this 
        command:

        curl -X GET localhost:5036/countries/<country>/regions

        of

        curl localhost:5036/countries/<country>/regions        
        \n
        '''
    #Checks that the varibles that store the data is not empty
    if(len(sighting_data) == 0):
        logging.warning('The global variable, sighting_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''
    #Empty list
    empty_list = []

    #path to the country
    var = sighting_data['visible_passes']['visible_pass']

    #loops through the data
    for current in var:
        if(current['country'] == country):
            if(current['region'] not in empty_list):
                empty_list.append(current['region'])

    #Incase the returning list is empty
    if(len(empty_list) == 0):
        logging.warning('The returning list is empty, causing an error')
        return '''
        \n
        The function is returning an emoty list, make sure that the name of the country was
        spelled correctly. If not, make sure it is spelled correctly.
        \n
        '''

    #Returns a list after it has been jsonify
    return jsonify(empty_list)

#The purpose of this route: Returns all cities associated with a given Country nad Region in the sighting data, (GET)
@app.route('/countries/<country>/regions/<region>', methods=['GET', 'POST'])
def get_region_info(country, region):
    '''
    Thic function will return info about that country with the mathing region type given by the user.

    Args:
        country (string): It is the name of the country
        region (string): It is the region type for that country

    return:
        list_of_dict (list): It returns a list of dictionaries that have more data about that region 
        and country provided by the user.
    '''

    #Incase the user inputs the incorrect method
    if(request.method != 'GET'):
        return '''
        This route returns more information about the country and region. To use this route use the 
        following command: 

        curl -X GET localhost:5036/countries/<country>/regions/<region>

        or 

        curl localhost:5036/countries/<country>/regions/<regions>
        '''

    #Checks that the varibles that store the data is not empty
    if(len(sighting_data) == 0):
        logging.warning('The global variable, sighting_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''

    #empty list
    empty_list = []

    #This is the path to the countries
    var = sighting_data['visible_passes']['visible_pass']
    
    for instance in var:
        if(instance['country'] == country):
            if(instance['region'] == region):
                empty_list.append(instance)

    #Checks the returning list is not empty
    if(len(empty_list) == 0):
        loggin.warning('The returning list is empty, and an error will be returned')
        return '''
        \n
        This function is returning an empty list, make sure that the country and the type of 
        region is spelled corrently. If not, make sure those parameters are spelled correctly.
        \n
        '''
    #Returns a list that has been jsonify
    return jsonify(empty_list)
    

#The purpose of this route: Returns all information about a specific City in the sighting data, (GET)
@app.route('/countries/<country>/regions/<region>/cities', methods=['GET', 'POST'])
def get_cities(country, region):
    '''
    This function gathers all the cities that fit in to the description of the wated coutry and type 
    of region that the user wanted

    Args:
        country (string): It is the name of the country
        region (string): It is the type of region that the user wants

    result:
        list_of_cities (list): It is a list that contains all the cities that are in the country and
        have that specific type of region that the user was lookign for.
    '''

    #Incase the user inputs the incorrect method 
    if(request.method != 'GET'):
        return '''
        \n
        This function returns a list of all the cities for the inputted country with the specfic 
        region. To use this function use the following command:

        curl -X GET localhost:5036/countries/<country>/regions/<regions>/cities

        or 

        curl localhost:5036/countries/<country>/regions/<regions>/cities
        \n
        '''
    #Checks that the varibles that store the data is not empty
    if(len(sighting_data) == 0):
        logging.warning('The global variable, sighting_data, is empty')
        return '''
        \n
        The positional_data.xml file was not passed in, hence the function of
        this route cannot be completed. Therefore, use this command first:

        curl -X POST localhost:5036/data

        Then use the the previous command again.
        \n
        '''
        
    #This is an empty list
    list_of_cities = []

    #This is the path to the country
    var = sighting_data['visible_passes']['visible_pass']

    #This is the loop
    for instance in var:
        if(instance['country'] == country):
            if(instance['region'] == region):
                if(instance['city'] not in list_of_cities):
                    list_of_cities.append(instance['city'])

    if(len(list_of_cities) == 0):
        logging.warning('The returning list is empty, therefore an error is being raised')
        return '''
        \n
        This function is returning an empty list, make sure the inputs:
        country, and region type are spelled correctly. If they are not, make sure they are spelled correctly.
        \n
        '''
    #Returns a jsonified list
    return jsonify(list_of_cities)


def main():
    #This will get the server started
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    main()
