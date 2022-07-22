import flask
from flask import render_template, request
import json
import sys
import datasource

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def basic_home():
    '''
    This should render the template for the basic home page
    which allows the user to search a pokemon by name
    '''
    return render_template('basic_home_page.html')

@app.route('/home_page', methods=['GET', 'POST'])
def advanced_home():
    '''
    This should render the template for the advanced home page
    which allows the user to search a pokemon by name and other
    attributes
    '''
    return render_template('home_page.html')

@app.route('/about_data')
def about_data():
    '''
    This should render the template for the page explaining the data
    and the link to the laggle dataset
    '''
    return render_template('data_page.html')

@app.route('/general_info')
def general_info():
    '''
    This should render the template for the basic home page
    which allows the user to search a pokemon by name
    '''
    return render_template('general_info_page.html')

def is_empty_dict(dict):
    '''
    Checks if a dictionary has all empty values
    '''
    is_empty = True
    for i in dict.values():
        if not i == None:
            is_empty = False
    return is_empty

def name_list(name):
    '''
    Creates a list of all Pokemon names that have partial matches
    '''

    #creates a list of all pokemon names in our database
    model = datasource.DataSource()
    all_pokemon_names = model.get_all_names()
    all_pokemon_list = []
    for i in range(len(all_pokemon_names)):
        pokemon_list = all_pokemon_names[i]
        pokemon_list = list(pokemon_list)
        all_pokemon_list.append(pokemon_list[0])

    #copy of the list because we remove from the list later in the function
    all_pokemon_copy = all_pokemon_list.copy()
    length = len(all_pokemon_list)

    #check if user input name matches any START of pokemon names
    for j in range(0, length):
        names_equal = True
        current_pokemon = all_pokemon_list[j]
        #make checks letter by letter
        if len(name) <= len(current_pokemon) and len(name) > 0:
            for k in range(0, len(name)):
                if not name[k] == current_pokemon[k]:
                    names_equal = False
        else:
            names_equal = False

        #remove from list if there is not a match
        if not names_equal:
            all_pokemon_copy.remove(current_pokemon)

    return tuple(all_pokemon_copy)


def create_base_dict():
    '''
    Gets all input of base stats from the user and creates our dictionary of
    base stats to pass to our querying function
    '''

    base_dict = {"name" : None, "hp" : None,
    "attack" : None, "defense" : None, "special_attack" : None,
    "special_defense" : None, "speed" : None}

    min_greater = False

    if request.method == 'POST':
        name = request.form["name"]
        name = name.title()

        names = name_list(name)

        #failing gracefully if name does not yield any matches
        if len(names) == 0 and not len(name) == 0:
            base_dict["name"] = tuple(name)

        if not len(names) == 0:
            base_dict["name"] = names

        #for each stat get the min and max and check if it is included in the final query
        attack_selected = request.form.getlist("add_attack")
        if not attack_selected == []:
            min_attack = request.form["min_attack"]
            max_attack = request.form["max_attack"]
            #check if min > max
            if int(min_attack) > int(max_attack):
                min_greater = True
            #update dictionary accordingly
            base_dict["attack"] = (min_attack, max_attack)

        defense_selected = request.form.getlist("add_defense")
        if not defense_selected == []:
            min_defense = request.form["min_defense"]
            max_defense = request.form["max_defense"]
            if int(min_defense) > int(max_defense):
                min_greater = True
            base_dict["defense"] = (min_defense, max_defense)

        special_attack_selected = request.form.getlist("add_special_attack")
        if not special_attack_selected == []:
            min_special_attack = request.form["min_special_attack"]
            max_special_attack = request.form["max_special_attack"]
            if int(min_special_attack) > int(max_special_attack):
                min_greater = True
            base_dict["special_attack"] = (min_special_attack, max_special_attack)

        special_defense_selected = request.form.getlist("add_special_defense")
        if not special_defense_selected == []:
            min_special_defense = request.form["min_special_defense"]
            max_special_defense = request.form["max_special_defense"]
            if int(min_special_defense) > int(max_special_defense):
                min_greater = True
            base_dict["special_defense"] = (min_special_defense, max_special_defense)

        hp_selected = request.form.getlist("add_hp")
        if not hp_selected == []:
            min_hp = request.form["min_hp"]
            max_hp = request.form["max_hp"]
            if int(min_hp) > int(max_hp):
                min_greater = True
            base_dict["hp"] = (min_hp, max_hp)

        speed_selected = request.form.getlist("add_speed")
        if not speed_selected == []:
            min_speed = request.form["min_speed"]
            max_speed = request.form["max_speed"]
            if int(min_speed) > int(max_speed):
                min_greater = True
            base_dict["speed"] = (min_speed, max_speed)


    return [base_dict, min_greater]

def create_quant_dict():
    '''
    Gets all input of quantitative stats from the user and creates our dictionary of
    quantitative stats to pass to our querying function
    '''
    quant_dict = {"height" : None, "weight" : None, "catch_rate" : None,
                    "experience" : None, "percentage_male" : None, "friendship" : None}

    min_greater = False

    if request.method == 'POST':
        height_selected = request.form.getlist("add_height")
        if not height_selected == []:
            min_height = request.form["min_height"]
            max_height = request.form["max_height"]
            if int(min_height) > int(max_height):
                min_greater = True
            quant_dict["height"] = (min_height, max_height)

        weight_selected = request.form.getlist("add_weight")
        if not weight_selected == []:
            min_weight = request.form["min_weight"]
            max_weight = request.form["max_weight"]
            if int(min_weight) > int(max_weight):
                min_greater = True
            quant_dict["weight"] = (min_weight, max_weight)

        catch_rate_selected = request.form.getlist("add_catch_rate")
        if not catch_rate_selected == []:
            min_catch_rate = request.form["min_catch_rate"]
            max_catch_rate = request.form["max_catch_rate"]
            if int(min_catch_rate) > int(max_catch_rate):
                min_greater = True
            quant_dict["catch_rate"] = (min_catch_rate, max_catch_rate)

        experience_selected = request.form.getlist("add_experience")
        if not experience_selected == []:
            min_experience = request.form["min_experience"]
            max_experience = request.form["max_experience"]
            if int(min_experience) > int(max_experience):
                min_greater = True
            quant_dict["experience"] = (min_experience, max_experience)

        percentage_male_selected = request.form.getlist("add_percentage_male")
        if not percentage_male_selected == []:
            min_percentage_male = request.form["min_percentage_male"]
            max_percentage_male = request.form["max_percentage_male"]
            if int(min_percentage_male) > int(max_percentage_male):
                min_greater = True
            quant_dict["percentage_male"] = (min_percentage_male, max_percentage_male)

        friendship_selected = request.form.getlist("add_friendship")
        if not friendship_selected == []:
            min_friendship = request.form["min_friendship"]
            max_friendship = request.form["max_friendship"]
            if int(min_friendship) > int(max_friendship):
                min_greater = True
            quant_dict["friendship"] = (min_friendship, max_friendship)

    return [quant_dict, min_greater]

def create_cat_dict():
    '''
    Gets all input of categorical stats from the user and creates our dictionary of
    categorical stats to pass to our querying function
    '''
    cat_dict = {"primary_type" : None, "secondary_type" : None,
    "generation" : None, "num_abilities" : None, "growth_rate" : None,
    "egg_type" : None}

    if request.method == 'POST':
        #check if any stat values selected and update dictionary accordingly
        primary_type = request.form.getlist("primary_type")
        if not primary_type == []:
            cat_dict["primary_type"] = tuple(primary_type)

        secondary_type = request.form.getlist("secondary_type")
        if not secondary_type == []:
            cat_dict["secondary_type"] = tuple(secondary_type)

        generation = request.form.getlist("generation")
        if not generation == []:
            cat_dict["generation"] = tuple(generation)

        num_abilities = request.form.getlist("num_abilities")
        if not num_abilities == []:
            cat_dict["num_abilities"] = tuple(num_abilities)

        growth_rate = request.form.getlist("growth_rate")
        if not growth_rate == []:
            cat_dict["growth_rate"] = tuple(growth_rate)

        egg_type = request.form.getlist("egg_type")
        if not egg_type == []:
            cat_dict["egg_type"] = tuple(egg_type)

    return cat_dict

def create_type_effect_dict():
    '''
    Gets all input of type effectiveness stats from the user and creates our dictionary of
    type effectivness stats to pass to our querying function
    '''
    type_effect_dict = {"against_normal" : None, "against_fire" : None,
    "against_water" : None, "against_electric" : None, "against_grass" : None,
    "against_ice" : None, "against_fight" : None, "against_poison" : None,
    "against_ground" : None, "against_flying" : None, "against_psychic" : None,
    "against_bug" : None, "against_rock" : None, "against_ghost" : None,
    "against_dragon" : None, "against_dark" : None, "against_steel" : None,
    "against_fairy" : None}

    min_greater = False

    if request.method == 'POST':
        against_normal_selected = request.form.getlist("add_against_normal")
        if not against_normal_selected == []:
            min_against_normal = request.form["min_against_normal"]
            max_against_normal = request.form["max_against_normal"]
            if int(min_against_normal) > int(max_against_normal):
                min_greater = True
            type_effect_dict["against_normal"] = (min_against_normal, max_against_normal)

        against_fire_selected = request.form.getlist("add_against_fire")
        if not against_fire_selected == []:
            min_against_fire = request.form["min_against_fire"]
            max_against_fire = request.form["max_against_fire"]
            if int(min_against_fire) > int(max_against_fire):
                min_greater = True
            type_effect_dict["against_fire"] = (min_against_fire, max_against_fire)

        against_water_selected = request.form.getlist("add_against_water")
        if not against_water_selected == []:
            min_against_water = request.form["min_against_water"]
            max_against_water = request.form["max_against_water"]
            if int(min_against_water) > int(max_against_water):
                min_greater = True
            type_effect_dict["against_water"] = (min_against_water, max_against_water)

        against_electric_selected = request.form.getlist("add_against_electric")
        if not against_electric_selected == []:
            min_against_electric = request.form["min_against_electric"]
            max_against_electric = request.form["max_against_electric"]
            if int(min_against_electric) > int(max_against_electric):
                min_greater = True
            type_effect_dict["against_electric"] = (min_against_electric, max_against_electric)

        against_grass_selected = request.form.getlist("add_against_grass")
        if not against_grass_selected == []:
            min_against_grass = request.form["min_against_grass"]
            max_against_grass = request.form["max_against_grass"]
            if int(min_against_grass) > int(max_against_grass):
                min_greater = True
            type_effect_dict["against_grass"] = (min_against_grass, max_against_grass)

        against_ice_selected = request.form.getlist("add_against_ice")
        if not against_ice_selected == []:
            min_against_ice = request.form["min_against_ice"]
            max_against_ice = request.form["max_against_ice"]
            if int(min_against_ice) > int(max_against_ice):
                min_greater = True
            type_effect_dict["against_ice"] = (min_against_ice, max_against_ice)

        against_fight_selected = request.form.getlist("add_against_fight")
        if not against_fight_selected == []:
            min_against_fight = request.form["min_against_fight"]
            max_against_fight = request.form["max_against_fight"]
            if int(min_against_fight) > int(max_against_fight):
                min_greater = True
            type_effect_dict["against_fight"] = (min_against_fight, max_against_fight)

        against_poison_selected = request.form.getlist("add_against_poison")
        if not against_poison_selected == []:
            min_against_poison = request.form["min_against_poison"]
            max_against_poison = request.form["max_against_poison"]
            if int(min_against_poison) > int(max_against_poison):
                min_greater = True
            type_effect_dict["against_poison"] = (min_against_poison, max_against_poison)

        against_ground_selected = request.form.getlist("add_against_ground")
        if not against_ground_selected == []:
            min_against_ground = request.form["min_against_ground"]
            max_against_ground = request.form["max_against_ground"]
            if int(min_against_ground) > int(max_against_ground):
                min_greater = True
            type_effect_dict["against_ground"] = (min_against_ground, max_against_ground)

        against_flying_selected = request.form.getlist("add_against_flying")
        if not against_flying_selected == []:
            min_against_flying = request.form["min_against_flying"]
            max_against_flying = request.form["max_against_flying"]
            if int(min_against_flying) > int(max_against_flying):
                min_greater = True
            type_effect_dict["against_flying"] = (min_against_flying, max_against_flying)

        against_psychic_selected = request.form.getlist("add_against_psychic")
        if not against_psychic_selected == []:
            min_against_psychic = request.form["min_against_psychic"]
            max_against_psychic = request.form["max_against_psychic"]
            if int(min_against_psychic) > int(max_against_psychic):
                min_greater = True
            type_effect_dict["against_psychic"] = (min_against_psychic, max_against_psychic)

        against_bug_selected = request.form.getlist("add_against_bug")
        if not against_bug_selected == []:
            min_against_bug = request.form["min_against_bug"]
            max_against_bug = request.form["max_against_bug"]
            if int(min_against_bug) > int(max_against_bug):
                min_greater = True 
            type_effect_dict["against_bug"] = (min_against_bug, max_against_bug)

        against_rock_selected = request.form.getlist("add_against_rock")
        if not against_rock_selected == []:
            min_against_rock = request.form["min_against_rock"]
            max_against_rock = request.form["max_against_rock"]
            if int(min_against_rock) > int(max_against_rock):
                min_greater = True
            type_effect_dict["against_rock"] = (min_against_rock, max_against_rock)

        against_ghost_selected = request.form.getlist("add_against_ghost")
        if not against_ghost_selected == []:
            min_against_ghost = request.form["min_against_ghost"]
            max_against_ghost = request.form["max_against_ghost"]
            if int(min_against_ghost) > int(max_against_ghost):
                min_greater = True
            type_effect_dict["against_ghost"] = (min_against_ghost, max_against_ghost)

        against_dragon_selected = request.form.getlist("add_against_dragon")
        if not against_dragon_selected == []:
            min_against_dragon = request.form["min_against_dragon"]
            max_against_dragon = request.form["max_against_dragon"]
            if int(min_against_dragon) > int(max_against_dragon):
                min_greater = True
            type_effect_dict["against_dragon"] = (min_against_dragon, max_against_dragon)

        against_dark_selected = request.form.getlist("add_against_dark")
        if not against_dark_selected == []:
            min_against_dark = request.form["min_against_dark"]
            max_against_dark = request.form["max_against_dark"]
            if int(min_against_dark) > int(max_against_dark):
                min_greater = True
            type_effect_dict["against_dark"] = (min_against_dark, max_against_dark)

        against_steel_selected = request.form.getlist("add_against_steel")
        if not against_steel_selected == []:
            min_against_steel = request.form["min_against_steel"]
            max_against_steel = request.form["max_against_steel"]
            if int(min_against_steel) > int(max_against_steel):
                min_greater = True
            type_effect_dict["against_steel"] = (min_against_steel, max_against_steel)

        against_fairy_selected = request.form.getlist("add_against_fairy")
        if not against_fairy_selected == []:
            min_against_fairy = request.form["min_against_fairy"]
            max_against_fairy = request.form["max_against_fairy"]
            if int(min_against_fairy) > int(max_against_fairy):
                min_greater = True
            type_effect_dict["against_fairy"] = (min_against_fairy, max_against_fairy)

    return [type_effect_dict, min_greater]

@app.route('/results', methods=['GET', 'POST'])
def results():
    '''
    Displays the results page based on user inputs or lets the user know if their
    inputs do not meet any search criteria
    '''
    #create all dictionaries and variables to check if there is a min greater than a max input
    base_dict = create_base_dict()[0]
    base_dict_min_greater = create_base_dict()[1]
    cat_dict = create_cat_dict()
    quant_dict = create_quant_dict()[0]
    quant_dict_min_greater = create_base_dict()[1]
    type_effect_dict = create_type_effect_dict()[0]
    type_effect_dict_min_greater = create_base_dict()[1]

    #check if all dictionaries are empty
    all_dicts_empty = False
    if is_empty_dict(base_dict) and is_empty_dict(cat_dict) and is_empty_dict(quant_dict) and is_empty_dict(type_effect_dict):
        all_dicts_empty = True

    model = datasource.DataSource()

    all_names = []
    all_filenames = []
    all_radar_charts = []
    all_additional_stats = []

    #check to see if any input given
    if not all_dicts_empty:
        #query based on user specifications and break into data and attribute attribute_descriptors
        data_and_attribute_descriptors = model.final_user_query(base_dict, quant_dict, cat_dict, type_effect_dict)
        pokemon_data = data_and_attribute_descriptors[0]
        attribute_descriptors = data_and_attribute_descriptors[1]

        #check to see if any pokemon met the query specifications
        if not pokemon_data == []:
            #populate lists of names, image filenames, radar chart filenames, and additional stats
            #with the values generated from our query
            for i in range(len(pokemon_data)):
                additional_stats_list = []
                all_names.append(pokemon_data[i][0])
                all_filenames.append("static/all_pokemon_images/" + pokemon_data[i][1])
                img_name = pokemon_data[i][1]
                all_radar_charts.append("static/radar_plots/radar_chart_" + img_name)
                for j in range(2, len(pokemon_data[i])):
                    additional_stats = ""
                    additional_stats = additional_stats + attribute_descriptors[j-2] + str(pokemon_data[i][j])
                    additional_stats_list.append(additional_stats)
                #check to see if user input any additional stats (other than name)
                if additional_stats_list == []:
                    additional_stats = "No Additional Stats Requested"
                    additional_stats_list.append(additional_stats)
                all_additional_stats.append(additional_stats_list)
        else:
            #if query failed due to min > max
            if base_dict_min_greater or quant_dict_min_greater or type_effect_dict_min_greater:
                all_names.append("There are no Pokemon that meet the specified criteria; you input a minumum value greater than a maximum value you input")
                all_filenames.append("static/all_pokemon_images/sadPikachu.png")
                all_radar_charts.append("static/all_pokemon_images/sadPikachu.png")
                all_additional_stats.append(["No Search Results"])
            #all other reasons for failed query
            else:
                all_names.append("There are no Pokemon that meet the specified criteria")
                all_filenames.append("static/all_pokemon_images/sadPikachu.png")
                all_radar_charts.append("static/all_pokemon_images/sadPikachu.png")
                all_additional_stats.append(["No Search Results"])
    #case when no user input is given
    else:
        all_names.append("No Search Criteria Input")
        all_filenames.append("static/all_pokemon_images/sadPikachu.png")
        all_radar_charts.append("static/all_pokemon_images/sadPikachu.png")
        all_additional_stats.append(["No Search Criteria Input"])


    return render_template('results.html', all_names = all_names, all_filenames = all_filenames, all_radar_charts = all_radar_charts, all_additional_stats = all_additional_stats, num_pokemon = len(all_names), num_add_stats = len(all_additional_stats[0]))


'''
Run the program by typing 'python3 localhost [port]', where [port] is one of
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
