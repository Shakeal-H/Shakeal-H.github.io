import psycopg2
import psqlConfig as config
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend in the form of a list.
    '''

    def __init__(self):
        '''
        Initializes a connection to our pokemon database and initializes the instance
        variables queried_params and attribute_descriptors. queried_params is a variable
        that holds the parameters of our parametrized final query to our database based
        on user specifications. attribute_descriptors is a variable that holds the
        strings that describe a given attribute to a user.
        '''
        self.queried_params = []
        self.attribute_descriptors = []
        try:
            self.connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def final_user_query(self, base_dict, quant_dict, cat_dict, type_effect_dict):
        '''Returns the result of the entire query made by the user

        PARAMETERS:
            base_dict - a dictionary that holds the name of the base stat as a key
                        and a range of values (if the stat was selected) or nothing
                        if the stat was not selected
            quant_dict - a dictionary that holds the name of the quantitative stat as a key
                        and a list specifying the range of values selected (if the stat was selected)
                        or nothing if the stat was not selected
            cat_dict - a dictionary that holds the name of the categorical stat as a key
                        and a list specifying which values are selected (if the stat was selected)
                        or nothing if the stat was not selected
            type_effect_dict - a dictionary that holds the name of the type effectiveness as a key
                        and a range of values that represent the range of effectiveness (damage against)
                        specified by the user or nothing if the type effectiveness was not selected

        RETURN:
            a list that has the name, base stats, and all additional stats for pokemon
            that satisfy the query made by the user
        '''

        base_stats = self.get_base_stats(base_dict)
        base_cols = base_stats[0]
        base_queries = base_stats[1]

        quant_stats = self.get_additional_quant_stats(quant_dict)
        quant_cols = quant_stats[0]
        quant_queries = quant_stats[1]

        cat_stats = self.get_cat_stats(cat_dict)
        cat_cols = cat_stats[0]
        cat_queries = cat_stats[1]

        type_effect_stats = self.get_type_effectiveness(type_effect_dict)
        type_cols = type_effect_stats[0]
        type_queries = type_effect_stats[1]

        all_selected_cols = base_cols + quant_cols + cat_cols + type_cols
        all_queries = base_queries + quant_queries + cat_queries + type_queries

        #accounting for if no additional columns are selected
        if len(all_selected_cols) == 0:
            query = "SELECT name, image FROM pokemonattributes WHERE " + all_queries[0]
        #accounting for all other cases
        else:
            query = "SELECT name, image, "

            for i in range(len(all_selected_cols) - 1):
                query = query + all_selected_cols[i] + ", "

            query = query + all_selected_cols[-1]

            query = query + " FROM pokemonattributes WHERE "

            for j in range(len(all_queries) - 1):
                query = query + all_queries[j] + " AND "

            query = query + all_queries[-1] + ";"

        self.queried_params = tuple(self.queried_params)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, self.queried_params)
            query_results = cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

        return[query_results, self.attribute_descriptors]



    def get_base_stats(self, base_dict):
        '''
        Returns all base stats (hp, attack, defense, special attack, special defense, speed)
        for a named pokemon, or all pokemon if none are named, and filters by the base stats
        if the user has specified ranges for these stats

        PARAMETERS:
            base_dict - a dictionary that holds the name of the base stat as a key
                        and a range of values (if the stat was selected) or nothing
                        if the stat was not selected

        RETURN:
            a list that holds a list of column values with base stat data,
            a list containing parts of the final query
        '''
        queried_columns = []
        queried_values = []

        #if the user specified value(s) for a column, get the specification and
        #add the column to the queried column list while adding the specified
        #values to the queried values list for each base stat

        if not self.is_empty_key(base_dict, "name"):
            queried_values.append(self.get_name(base_dict["name"]))

        if not self.is_empty_key(base_dict, "hp"):
            queried_values.append(self.get_hp(base_dict["hp"][0], base_dict["hp"][1]))
            queried_columns.append("hp")
            self.attribute_descriptors.append("HP: ")


        if not self.is_empty_key(base_dict, "attack"):
            queried_values.append(self.get_attack(base_dict["attack"][0], base_dict["attack"][1]))
            queried_columns.append("attack")
            self.attribute_descriptors.append("Attack: ")

        if not self.is_empty_key(base_dict, "defense"):
            queried_values.append(self.get_defense(base_dict["defense"][0], base_dict["defense"][1]))
            queried_columns.append("defense")
            self.attribute_descriptors.append("Defense: ")

        if not self.is_empty_key(base_dict, "special_attack"):
            queried_values.append(self.get_special_attack(base_dict["special_attack"][0], base_dict["special_attack"][1]))
            queried_columns.append("special_attack")
            self.attribute_descriptors.append("Special Attack: ")

        if not self.is_empty_key(base_dict, "special_defense"):
            queried_values.append(self.get_special_defense(base_dict["special_defense"][0], base_dict["special_defense"][1]))
            queried_columns.append("special_defense")
            self.attribute_descriptors.append("Special Defense: ")

        if not self.is_empty_key(base_dict, "speed"):
            queried_values.append(self.get_speed(base_dict["speed"][0], base_dict["speed"][1]))
            queried_columns.append("speed")
            self.attribute_descriptors.append("Speed: ")

        return [queried_columns, queried_values]


    def get_additional_quant_stats(self, quant_dict):
        '''
        Returns all additional quantitative stats (that aren't base stats) for all
        pokemon that satsify the specified filters

        PARAMETERS:
            quant_dict - a dictionary that holds the name of the quantitative stat as a key
                        and a list specifying the range of values selected (if the stat was selected)
                        or nothing if the stat was not selected

        RETURN:
            a list of all pokemon and the specified additional quantitative stats that satisfy the specified filters
        '''
        queried_columns = []
        queried_values = []

        if not self.is_empty_key(quant_dict, "height"):
            queried_values.append(self.get_height(quant_dict["height"][0], quant_dict["height"][1]))
            queried_columns.append("height_m")
            self.attribute_descriptors.append("Height (m): ")

        if not self.is_empty_key(quant_dict, "weight"):
            queried_values.append(self.get_weight(quant_dict["weight"][0], quant_dict["weight"][1]))
            queried_columns.append("weight_kg")
            self.attribute_descriptors.append("Weight (kg): ")

        if not self.is_empty_key(quant_dict, "catch_rate"):
            queried_values.append(self.get_catch_rate(quant_dict["catch_rate"][0], quant_dict["catch_rate"][1]))
            queried_columns.append("catch_rate")
            self.attribute_descriptors.append("Catch Rate: ")

        if not self.is_empty_key(quant_dict, "experience"):
            queried_values.append(self.get_experience(quant_dict["experience"][0], quant_dict["experience"][1]))
            queried_columns.append("base_experience")
            self.attribute_descriptors.append("Base Experience: ")

        if not self.is_empty_key(quant_dict, "percentage_male"):
            queried_values.append(self.get_percentage_male(quant_dict["percentage_male"][0], quant_dict["percentage_male"][1]))
            queried_columns.append("percentage_male")
            self.attribute_descriptors.append("Percentage of Species that is Male: ")

        if not self.is_empty_key(quant_dict, "friendship"):
            queried_values.append(self.get_friendship(quant_dict["friendship"][0], quant_dict["friendship"][1]))
            queried_columns.append("base_friendship")
            self.attribute_descriptors.append("Base Friendship: ")

        return [queried_columns, queried_values]

    def get_cat_stats(self, cat_dict):
        '''
        Returns a list containing a list of the columns with categorical data selected
        by the user and a list containing the parts of a query used to select those columns
        while meeting the specifications given by the user. This information is then sent to
        the function that returns the final query.

        PARAMETERS:
            cat_dict - a dictionary that holds the name of the categorical stat as a key
                        and a list specifying which values are selected (if the stat was selected)
                        or nothing if the stat was not selected

        RETURN:
            a list that holds a list of column values with categorical data and a list containing parts of the final query
        '''

        #empty lists that will store the queried columns and specified values
        queried_columns = []
        queried_values = []

        #if the user specified value(s) for a column, get the specification and
        #add the column to the queried column list while adding the specified
        #values to the queried values list for each categorical variable
        if not self.is_empty_key(cat_dict, "primary_type"):
            queried_values.append(self.get_primary_type(cat_dict["primary_type"]))
            queried_columns.append("pokemon_type_1")
            self.attribute_descriptors.append("Primary Type: ")

        if not self.is_empty_key(cat_dict, "secondary_type"):
            queried_values.append(self.get_secondary_type(cat_dict["secondary_type"]))
            queried_columns.append("pokemon_type_2")
            self.attribute_descriptors.append("Secondary Type: ")

        if not self.is_empty_key(cat_dict, "generation"):
            queried_values.append(self.get_generation(cat_dict["generation"]))
            queried_columns.append("generation")
            self.attribute_descriptors.append("Generation: ")

        if not self.is_empty_key(cat_dict, "num_abilities"):
            queried_values.append(self.get_num_abilities(cat_dict["num_abilities"]))
            queried_columns.append("num_abilities")
            self.attribute_descriptors.append("Number of Abilities: ")

        if not self.is_empty_key(cat_dict, "growth_rate"):
            queried_values.append(self.get_growth_rate(cat_dict["growth_rate"]))
            queried_columns.append("growth_rate")
            self.attribute_descriptors.append("Growth Rate: ")

        if not self.is_empty_key(cat_dict, "egg_type"):
            queried_values.append(self.get_egg_type(cat_dict["egg_type"]))
            queried_columns.append("egg_type_1")
            queried_columns.append("egg_type_2")
            self.attribute_descriptors.append("Primary Egg Type: ")
            self.attribute_descriptors.append("Secondary Egg Type: ")

        return [queried_columns, queried_values]


    def get_type_effectiveness(self, type_effect_dict):
        '''
        Returns a list containing a list of all type effectivness' selected
        by the user and a list containing the parts of a query used to select those columns
        while meeting the specifications given by the user. This information is then sent to
        the function that returns the final query.

        PARAMETERS:
            type_effect_dict - a dictionary that holds the name of the type effectiveness as a key
                        and a range of values that represent the range of effectiveness (damage against)
                        specified by the user or nothing if the type effectiveness was not selected
        RETURN:
            a list that holds a list of column values with type effectivness data and
            a list containing parts of the final query
        '''
        #empty lists that will store the queried columns and specified values
        queried_columns = []
        queried_values = []

        #if the user specified value(s) for a column, get the specification and
        #add the column to the queried column list while adding the specified
        #values to the queried values list for each categorical variable
        if not self.is_empty_key(type_effect_dict, "against_normal"):
            queried_values.append(self.get_against_normal(type_effect_dict["against_normal"][0], type_effect_dict["against_normal"][1]))
            queried_columns.append("against_normal")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a normal type attack: ")


        if not self.is_empty_key(type_effect_dict, "against_fire"):
            queried_values.append(self.get_against_fire(type_effect_dict["against_fire"][0], type_effect_dict["against_fire"][1]))
            queried_columns.append("against_fire")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a fire type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_water"):
            queried_values.append(self.get_against_water(type_effect_dict["against_water"][0], type_effect_dict["against_water"][1]))
            queried_columns.append("against_water")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a water type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_electric"):
            queried_values.append(self.get_against_electric(type_effect_dict["against_electric"][0], type_effect_dict["against_electric"][1]))
            queried_columns.append("against_electric")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a electric type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_grass"):
            queried_values.append(self.get_against_grass(type_effect_dict["against_grass"][0], type_effect_dict["against_grass"][1]))
            queried_columns.append("against_grass")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a grass type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_ice"):
            queried_values.append(self.get_against_ice(type_effect_dict["against_ice"][0], type_effect_dict["against_ice"][1]))
            queried_columns.append("against_ice")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a ice type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_fight"):
            queried_values.append(self.get_against_fighting(type_effect_dict["against_fight"][0], type_effect_dict["against_fight"][1]))
            queried_columns.append("against_fight")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a fighting type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_poison"):
            queried_values.append(self.get_against_poison(type_effect_dict["against_poison"][0], type_effect_dict["against_poison"][1]))
            queried_columns.append("against_poison")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a poison type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_ground"):
            queried_values.append(self.get_against_ground(type_effect_dict["against_ground"][0], type_effect_dict["against_ground"][1]))
            queried_columns.append("against_ground")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a ground type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_flying"):
            queried_values.append(self.get_against_flying(type_effect_dict["against_flying"][0], type_effect_dict["against_flying"][1]))
            queried_columns.append("against_flying")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a flying type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_psychic"):
            queried_values.append(self.get_against_psychic(type_effect_dict["against_psychic"][0], type_effect_dict["against_psychic"][1]))
            queried_columns.append("against_psychic")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a psychic type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_bug"):
            queried_values.append(self.get_against_bug(type_effect_dict["against_bug"][0], type_effect_dict["against_bug"][1]))
            queried_columns.append("against_bug")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a bug type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_rock"):
            queried_values.append(self.get_against_rock(type_effect_dict["against_rock"][0], type_effect_dict["against_rock"][1]))
            queried_columns.append("against_rock")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a rock type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_ghost"):
            queried_values.append(self.get_against_ghost(type_effect_dict["against_ghost"][0], type_effect_dict["against_ghost"][1]))
            queried_columns.append("against_ghost")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a ghost type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_dragon"):
            queried_values.append(self.get_against_dragon(type_effect_dict["against_dragon"][0], type_effect_dict["against_dragon"][1]))
            queried_columns.append("against_dragon")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a dragon type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_dark"):
            queried_values.append(self.get_against_dark(type_effect_dict["against_dark"][0], type_effect_dict["against_dark"][1]))
            queried_columns.append("against_dark")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a dark type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_steel"):
            queried_values.append(self.get_against_steel(type_effect_dict["against_steel"][0], type_effect_dict["against_steel"][1]))
            queried_columns.append("against_steel")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a steel type attack: ")

        if not self.is_empty_key(type_effect_dict, "against_fairy"):
            queried_values.append(self.get_against_fairy(type_effect_dict["against_fairy"][0], type_effect_dict["against_fairy"][1]))
            queried_columns.append("against_fairy")
            self.attribute_descriptors.append("Damage multiplier applied when taking damage from a fairy type attack: ")

        return [queried_columns, queried_values]

    def get_name(self, name):
        '''
        Returns the name of the pokemon specified

        PARAMETERS:
            name - the name of the pokemon specified

        RETURN:
            the name of the pokemon specified
        '''

        query = "name in %s"
        self.queried_params.append(name)

        return query


    def get_hp(self, hp_min, hp_max):
        '''
        Returns a list of pokemon and their hp value for pokemon with hp values in the specified range

        PARAMETERS:
            hp_min - the minimum hp of pokemon queried
            hp_max - the maximum hp of pokemon queried

        RETURN:
            the part of the final query that filters by min and max HP
        '''

        query = "hp BETWEEN %s AND %s"
        self.queried_params.append(hp_min)
        self.queried_params.append(hp_max)

        return query

    def get_attack(self, attack_min, attack_max):
        '''
        Returns a section of the query that selects pokemon with attack
        values in the specified range

        PARAMETERS:
            attack_min - the minimum attack of pokemon queried
            attack_max - the maximum attack of pokemon queried

        RETURN:
            the part of the query that filters by min and max attack
        '''
        query = "attack BETWEEN %s AND %s"
        self.queried_params.append(attack_min)
        self.queried_params.append(attack_max)

        return query

    def get_defense(self, defense_min, defense_max):
        '''
        Returns a section of the query that selects pokemon with defense
        values in the specified range

        PARAMETERS:
            defense_min - the minimum defense of pokemon queried
            defense_max - the maximum defense of pokemon queried

        RETURN:
            the part of the query that filters by min and max defense
        '''
        query = "defense BETWEEN %s AND %s"
        self.queried_params.append(defense_min)
        self.queried_params.append(defense_max)

        return query


    def get_special_defense(self, special_defense_min, special_defense_max):
        '''
        Returns a section of the query that selects pokemon with special defense
        values in the specified range

        PARAMETERS:
            special_defense_min - the minimum special defense of pokemon queried
            special_defense_max - the maximum special defense of pokemon queried

        RETURN:
            the part of the query that filters by min and max special defense
        '''
        query = "special_defense BETWEEN %s AND %s"
        self.queried_params.append(special_defense_min)
        self.queried_params.append(special_defense_max)

        return query



    def get_special_attack(self, special_attack_min, special_attack_max):
        '''
        Returns a section of the query that selects pokemon with special attack
        values in the specified range

        PARAMETERS:
            special_attack_min - the minimum speical attack of pokemon queried
            special_attack_max - the maximum speical attack of pokemon queried

        RETURN:
            the part of the query that filters by min and max special attack
        '''
        query = "special_attack BETWEEN %s AND %s"
        self.queried_params.append(special_attack_min)
        self.queried_params.append(special_attack_max)

        return query



    def get_speed(self, speed_min, speed_max):
        '''
        Returns a section of the query that selects pokemon with speed values in the specified range

        PARAMETERS:
            speed_min - the minimum speed of pokemon queried
            speed_max - the maximum speed of pokemon queried

        RETURN:
            the part of the query that filters by min and max speed
        '''
        query = "speed BETWEEN %s AND %s"
        self.queried_params.append(speed_min)
        self.queried_params.append(speed_max)

        return query


    def get_catch_rate(self, catch_rate_min, catch_rate_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified catch_rate_min and catch_rate_max

        PARAMETERS:
            catch_rate_min - the minimum catch rate of pokemon queried
            catch_rate_max - the maximum catch rate of pokemon queried

        RETURN:
            a part of the query for pokemon with catch rate in the specified range and their catch rate value
        '''
        query = "catch_rate BETWEEN %s AND %s"
        self.queried_params.append(catch_rate_min)
        self.queried_params.append(catch_rate_max)

        return query

    def get_height(self, height_min, height_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified height_min and height_max

        PARAMETERS:
            height_min - the minimum height of pokemon queried
            height_max - the maximum height of pokemon queried

        RETURN:
            a part of the query for pokemon with height in the specified range and their height value
        '''
        query = "height_m BETWEEN %s AND %s"
        self.queried_params.append(height_min)
        self.queried_params.append(height_max)

        return query


    def get_weight(self, weight_min, weight_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified weight_min and weight_max

        PARAMETERS:
            weight_min - the minimum weight of pokemon queried
            weight_max - the maximum weight of pokemon queried

        RETURN:
            a part of the query for pokemon with weight in the specified range and their weight value
        '''
        query = "weight_kg BETWEEN %s AND %s"
        self.queried_params.append(weight_min)
        self.queried_params.append(weight_max)

        return query

    def get_friendship(self, friendship_min, friendship_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified friendship_min and friendship_max

        PARAMETERS:
            friendship_min - the minimum friendship of pokemon queried
            friendship_max - the maximum friendship of pokemon queried

        RETURN:
            a part of the query for  pokemon with friendship in the specified range and their friendship value
        '''
        query = "base_friendship BETWEEN %s AND %s"
        self.queried_params.append(friendship_min)
        self.queried_params.append(friendship_max)

        return query

    def get_experience(self, experience_min, experience_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified experience_min and experience_max

        PARAMETERS:
            experience_min - the minimum experience of pokemon queried
            experience_max - the maximum experience of pokemon queried

        RETURN:
            a part of the query for pokemon with experience in the specified range and their experience value
        '''
        query = "base_experience BETWEEN %s AND %s"
        self.queried_params.append(experience_min)
        self.queried_params.append(experience_max)

        return query

    def get_percentage_male(self, percentage_male_min, percentage_male_max):
        '''
        Returns a part of the query that filters pokemon between the range of the user's specified percentage_male_min and percentage_male_max

        PARAMETERS:
            percentage_male_min - the minimum percentage male of pokemon queried
            percentage_male_max - the maximum percentage male of pokemon queried

        RETURN:
            a part of the query for pokemon with percentage male in the specified range and their percentage male value
        '''
        query = "percentage_male BETWEEN %s AND %s"
        self.queried_params.append(percentage_male_min)
        self.queried_params.append(percentage_male_max)

        return query

    def get_primary_type(self, primary_types_selected):
        '''
        Returns the part of the final query that filters by the primary types

        PARAMETERS:
            primary_types_selected - a list of primary types selected by the user

        RETURN:
            a part of the final query that filters by the primary types
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(primary_types_selected) == 1:
            query =  "pokemon_type_1 = %s"
            self.queried_params.append(primary_types_selected[0])
        else:
            query = "pokemon_type_1 IN %s"
            self.queried_params.append(primary_types_selected)

        return query

    def get_secondary_type(self, secondary_types_selected):
        '''
        Returns the part of the final query that filters by the secondary types

        PARAMETERS:
            secondary_types_selected - a list of secondary types selected by the user

        RETURN:
            a part of the final query that filters by the secondary types
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(secondary_types_selected) == 1:
            query =  "pokemon_type_2 = %s"
            self.queried_params.append(secondary_types_selected[0])
        else:
            query = "pokemon_type_2 IN %s"
            self.queried_params.append(secondary_types_selected)

        return query

    def get_generation(self, generations_selected):
        '''
        Returns the part of the final query that filters by the generation value

        PARAMETERS:
            generations_selected - a list of generations selected by the user

        RETURN:
            a part of the final query that filters by the secondary types
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(generations_selected) == 1:
            query =  "generation = %s"
            self.queried_params.append(generations_selected[0])
        else:
            query = "generation IN %s"
            self.queried_params.append(generations_selected)

        return query


    def get_num_abilities(self, num_abilities_selected):
        '''
        Returns the part of the final query that filters by the number of abilities value

        PARAMETERS:
            num_abilities_selected - a list of number of abilities selected by the user

        RETURN:
            a part of the final query that filters by the number of abilities value
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(num_abilities_selected) == 1:
            query = "num_abilities = %s"
            self.queried_params.append(num_abilities_selected[0])
        else:
            query = "num_abilities IN %s"
            self.queried_params.append(num_abilities_selected)

        return query

    def get_growth_rate(self, growth_rate_selected):
        '''
        Returns the part of the final query that filters by the growth rate value

        PARAMETERS:
            growth_rate_selected - a list of growth rate selected by the user

        RETURN:
            a part of the final query that filters by the growth rate value
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(growth_rate_selected) == 1:
            query =  "growth_rate = %s"
            self.queried_params.append(growth_rate_selected[0])
        else:
            query = "growth_rate IN %s"
            self.queried_params.append(growth_rate_selected)

        return query

    def get_egg_type(self, egg_type_selected):
        '''
        Returns the part of the final query that filters by the egg type value

        PARAMETERS:
            egg_type_selected - a list of egg type selected by the user

        RETURN:
            a part of the final query that filters by the egg type value
        '''
        #use an "=" sign if there is only one value selected, use the IN operator otherwise
        if len(egg_type_selected) == 1:
            query = "(egg_type_1 = %s OR egg_type_2 = %s)"
            self.queried_params.append(egg_type_selected[0])
            self.queried_params.append(egg_type_selected[0])
        else:
            query = "(egg_type_1 IN %s OR egg_type_2 IN %s)"
            self.queried_params.append(egg_type_selected)
            self.queried_params.append(egg_type_selected)

        return query

    def get_against_normal(self, against_normal_min, against_normal_max):
        '''
        Returns the part of the query that filters by damage taken against normal type pokemon

        PARAMETERS:
            against_normal_min - the minimum against normal value of pokemon queried
            against_normal_max - the maximum against normal value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against normal type pokemon
        '''
        query = "against_normal BETWEEN %s AND %s"
        self.queried_params.append(against_normal_min)
        self.queried_params.append(against_normal_max)

        return query

    def get_against_fire(self, against_fire_min, against_fire_max):
        '''
        Returns the part of the query that filters by damage taken against fire type pokemon

        PARAMETERS:
            against_fire_min - the minimum against fire value of pokemon queried
            against_fire_max - the maximum against fire value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against fire type pokemon
        '''
        query = "against_fire BETWEEN %s AND %s"
        self.queried_params.append(against_fire_min)
        self.queried_params.append(against_fire_max)

        return query

    def get_against_water(self, against_water_min, against_water_max):
        '''
        Returns the part of the query that filters by damage taken against water type pokemon

        PARAMETERS:
            against_water_min - the minimum against water value of pokemon queried
            against_water_max - the maximum against water value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against water type pokemon
        '''
        query = "against_water BETWEEN %s AND %s"
        self.queried_params.append(against_water_min)
        self.queried_params.append(against_water_max)

        return query

    def get_against_electric(self, against_electric_min, against_electric_max):
        '''
        Returns the part of the query that filters by damage taken against electric type pokemon

        PARAMETERS:
            against_electric_min - the minimum against electric value of pokemon queried
            against_electric_max - the maximum against electric value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against electric type pokemon
        '''
        query = "against_electric BETWEEN %s AND %s"
        self.queried_params.append(against_electric_min)
        self.queried_params.append(against_electric_max)

        return query

    def get_against_grass(self, against_grass_min, against_grass_max):
        '''
        Returns the part of the query that filters by damage taken against grass type pokemon

        PARAMETERS:
            against_grass_min - the minimum against grass value of pokemon queried
            against_grass_max - the maximum against grass value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against grass type pokemon
        '''
        query = "against_grass BETWEEN %s AND %s"
        self.queried_params.append(against_grass_min)
        self.queried_params.append(against_grass_max)

        return query

    def get_against_ice(self, against_ice_min, against_ice_max):
        '''
        Returns the part of the query that filters by damage taken against ice type pokemon

        PARAMETERS:
            against_ice_min - the minimum against ice value of pokemon queried
            against_ice_max - the maximum against ice value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against ice type pokemon
        '''
        query = "against_ice BETWEEN %s AND %s"
        self.queried_params.append(against_ice_min)
        self.queried_params.append(against_ice_max)

        return query

    def get_against_fighting(self, against_fighting_min, against_fighting_max):
        '''
        Returns the part of the query that filters by damage taken against fighting type pokemon

        PARAMETERS:
            against_fighting_min - the minimum against fighting value of pokemon queried
            against_fighting_max - the maximum against fighting value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against fighting type pokemon
        '''
        query = "against_fight BETWEEN %s AND %s"
        self.queried_params.append(against_fighting_min)
        self.queried_params.append(against_fighting_max)

        return query

    def get_against_poison(self, against_poison_min, against_poison_max):
        '''
        Returns the part of the query that filters by damage taken against poison type pokemon

        PARAMETERS:
            against_poison_min - the minimum against poison value of pokemon queried
            against_poison_max - the maximum against poison value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against poison type pokemon
        '''
        query = "against_poison BETWEEN %s AND %s"
        self.queried_params.append(against_poison_min)
        self.queried_params.append(against_poison_max)

        return query

    def get_against_ground(self, against_ground_min, against_ground_max):
        '''
        Returns the part of the query that filters by damage taken against ground type pokemon

        PARAMETERS:
            against_ground_min - the minimum against ground value of pokemon queried
            against_ground_max - the maximum against ground value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against ground type pokemon
        '''
        query = "against_ground BETWEEN %s AND %s"
        self.queried_params.append(against_ground_min)
        self.queried_params.append(against_ground_max)

        return query

    def get_against_flying(self, against_flying_min, against_flying_max):
        '''
        Returns the part of the query that filters by damage taken against flying type pokemon

        PARAMETERS:
            against_flying_min - the minimum against flying value of pokemon queried
            against_flying_max - the maximum against flying value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against flying type pokemon
        '''
        query = "against_flying BETWEEN %s AND %s"
        self.queried_params.append(against_flying_min)
        self.queried_params.append(against_flying_max)

        return query

    def get_against_psychic(self, against_psychic_min, against_psychic_max):
        '''
        Returns the part of the query that filters by damage taken against psychic type pokemon

        PARAMETERS:
            against_psychic_min - the minimum against psychic value of pokemon queried
            against_psychic_max - the maximum against psychic value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against psychic type pokemon
        '''
        query = "against_psychic BETWEEN %s AND %s"
        self.queried_params.append(against_psychic_min)
        self.queried_params.append(against_psychic_max)

        return query

    def get_against_bug(self, against_bug_min, against_bug_max):
        '''
        Returns the part of the query that filters by damage taken against bug type pokemon

        PARAMETERS:
            against_bug_min - the minimum against bug value of pokemon queried
            against_bug_max - the maximum against bug value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against bug type pokemon
        '''
        query = "against_bug BETWEEN %s AND %s"
        self.queried_params.append(against_bug_min)
        self.queried_params.append(against_bug_max)

        return query

    def get_against_rock(self, against_rock_min, against_rock_max):
        '''
        Returns the part of the query that filters by damage taken against rock type pokemon

        PARAMETERS:
            against_rock_min - the minimum against rock value of pokemon queried
            against_rock_max - the maximum against rock value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against rock type pokemon
        '''
        query = "against_rock BETWEEN %s AND %s"
        self.queried_params.append(against_rock_min)
        self.queried_params.append(against_rock_max)

        return query

    def get_against_ghost(self, against_ghost_min, against_ghost_max):
        '''
        Returns the part of the query that filters by damage taken against ghost type pokemon

        PARAMETERS:
            against_ghost_min - the minimum against ghost value of pokemon queried
            against_ghost_max - the maximum against ghost value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against ghost type pokemon
        '''
        query = "against_ghost BETWEEN %s AND %s"
        self.queried_params.append(against_ghost_min)
        self.queried_params.append(against_ghost_max)

        return query

    def get_against_dragon(self, against_dragon_min, against_dragon_max):
        '''
        Returns the part of the query that filters by damage taken against dragon type pokemon

        PARAMETERS:
            against_dragon_min - the minimum against dragon value of pokemon queried
            against_dragon_max - the maximum against dragon value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against dragon type pokemon
        '''
        query = "against_dragon BETWEEN %s AND %s"
        self.queried_params.append(against_dragon_min)
        self.queried_params.append(against_dragon_max)

        return query

    def get_against_dark(self, against_dark_min, against_dark_max):
        '''
        Returns the part of the query that filters by damage taken against dark type pokemon

        PARAMETERS:
            against_dark_min - the minimum against dark value of pokemon queried
            against_dark_max - the maximum against dark value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against dark type pokemon
        '''
        query = "against_dark BETWEEN %s AND %s"
        self.queried_params.append(against_dark_min)
        self.queried_params.append(against_dark_max)

        return query

    def get_against_steel(self, against_steel_min, against_steel_max):
        '''
        Returns the part of the query that filters by damage taken against steel type pokemon

        PARAMETERS:
            against_steel_min - the minimum against bug value of pokemon queried
            against_steel_max - the maximum against bug value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against steel type pokemon
        '''
        query = "against_steel BETWEEN %s AND %s"
        self.queried_params.append(against_steel_min)
        self.queried_params.append(against_steel_max)

        return query

    def get_against_fairy(self, against_fairy_min, against_fairy_max):
        '''
        Returns the part of the query that filters by damage taken against fairy type pokemon

        PARAMETERS:
            against_fairy_min - the minimum against fairy value of pokemon queried
            against_fairy_max - the maximum against fairy value of pokemon queried

        RETURN:
            a part of the query that filters by damage taken against fairy type pokemon
        '''
        query = "against_fairy BETWEEN %s AND %s"
        self.queried_params.append(against_fairy_min)
        self.queried_params.append(against_fairy_max)

        return query

    def is_empty_key(self, dictionary, key):
        '''
        Returns whether a dictionary is empty

        PARAMETERS
            dictionary - a dictionary where we are checking if a key is empty
            key - the key we are checking

        RETURN:
            a True or False value based on if the key is empty
        '''

        return dictionary[key] == None

    def get_all_names(self):
        '''
        Returns a list of all pokemon names

        PARAMETERS
            NONE

        RETURN:
            a list of all pokemon names
        '''
        query = "SELECT name FROM pokemonattributes"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

## This commented code shows the process needed to make the radar charts.
    ## We iterated through the csv file and searched through each individual pokemon
    # We retrieved their HP, Attack, Special Attack, Special Defense, and Speed
    # then plotted these values into a radar plot. We added all radar plot images into a folder
    # called radar_plots, then placed the radar_plots folder in the static folder
    #----------------------------------------------------------------------------
    # pokedata = pd.read_csv("/Users/cheikhounagueye/Documents/Comps/pokedexf.csv")
    # number = 0
    #
    # for row in pokedata.itertuples():
    #     attributes=["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
    #     x = pokedata[pokedata["index"] == number]
    #     designation = pokedata.iloc[number][2]
    #     print(designation)
    #     img_name = x['image']
    #     img_name = str(img_name)
    #     pokemon=[x['hp'].values[0],x['attack'].values[0],x['defense'].values[0],x['sp_attack'].values[0],x['sp_defense'].values[0],x['speed'].values[0]]
    #     angles=np.linspace(0,2*np.pi,len(attributes), endpoint=False)
    #     angles=np.concatenate((angles,[angles[0]]))
    #     attributes.append(attributes[0])
    #     pokemon.append(pokemon[0])
    #     fig=plt.figure(figsize=(8,8))
    #     plt.rc('font', size= 15)
    #     labels = [attributes for _ in range(len(angles))]
    #     ax=fig.add_subplot(111, polar=True)
    #     ax.plot(angles,pokemon, 'o-', color='g', linewidth=.5)
    #     ax.fill(angles, pokemon, alpha=0.25, color='g')
    #     ax.set_thetagrids(angles * 180/np.pi, attributes)
    #     number = number + 1
    #     plt.savefig('/Users/cheikhounagueye/Desktop/All Radar Images/'"radar_chart_" + img_name[5:-31], transparent = True)
    #----------------------------------------------------------------------------


def main():
    data = DataSource()

    #create a base dictionary to test the code
    base_dict = {"name" : None, "hp" : None,
    "attack" : None, "defense" : None, "special_attack" : None,
    "special_defense" : None, "speed" : None}

    #create a categorical dictionary to test the code
    cat_dict = {"primary_type" : None, "secondary_type" : ("Water", "Fire"),
    "generation" : None, "num_abilities" : None, "growth_rate" : None,
    "egg_type" : ("Monster",)}

    # cat_dict = {"primary_type" : None, "secondary_type" : None,
    # "generation" : None, "species" : None, "num_abilities" : None, "growth_rate" : None,
    # "egg_type" : None}

    #create a quantitative dictionary to test the code
    quant_dict = {"height" : None, "weight" : None,
    "catch_rate" : None, "experience" : None, "percentage_male" : None, "friendship" : None}

    # quant_dict = {"height" : None, "weight" : None,
    # "catch_rate" : None, "experience" : None, "percentage_male" : None, "friendship" : None}

    #create a type effectivness dictionary to test the code
    # type_effect_dict = {"against_normal" : ("0", "1"), "against_fire" : (".5", ".5"),
    # "against_water" : ("0", "1"), "against_electric" : None, "against_grass" : ("0", "1.5"),
    # "against_ice" : None, "against_fight" : ("1", "1"), "against_poison" : ("1", "2"),
    # "against_ground" : ("0", "2"), "against_flying" : None, "against_psychic" : (".5", "1.5"),
    # "against_bug" : None, "against_rock" : ("1", "3"), "against_ghost" : (".33", "1"),
    # "against_dragon" : ("2", "2"), "against_dark" : None, "against_steel" : ("1", "2"),
    # "against_fairy" : None,}

    type_effect_dict = {"against_normal" : None, "against_fire" : None,
    "against_water" : None, "against_electric" : None, "against_grass" : None,
    "against_ice" : None, "against_fight" : None, "against_poison" : None,
    "against_ground" : None, "against_flying" : None, "against_psychic" : None,
    "against_bug" : None, "against_rock" : None, "against_ghost" : None,
    "against_dragon" : None, "against_dark" : None, "against_steel" : None,
    "against_fairy" : None,}



    # #run the function and see its output
    # test_base = data.getBaseStats(base_dict)
    # print(test_base)
    #
    # #run the function and see its output
    # test_cat = data.getCat(cat_dict)
    # print(test_cat)
    #
    # #run the function and see its output
    # test_quant = data.getAdditionalQuant(quant_dict)
    # print(test_quant)
    #
    # #run the function and see its output
    # test_type_effect = data.getTypeEffectiveness(type_effect_dict)
    # print(test_type_effect)

    test_final = data.final_user_query(base_dict, quant_dict, cat_dict, type_effect_dict)
    print(test_final)

    image_size_test = data.create_base_stats_radar_plot("Charizard")
    image_size_test.savefig("charizard_test.png")





if __name__ == '__main__':
    main()
