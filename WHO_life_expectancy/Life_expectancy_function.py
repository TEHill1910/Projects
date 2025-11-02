def life_expectancy_calculator():
    """
    Using data from 2000 to 2015, a linear regression
    model has been created to predict life expectancy
    on a country level. 
    Two models have been made, with one using a wider
    range of data and the other made after omitting more
    sensitive data.
    """

    import math
    import statistics

    def confirm_advanced():
        '''
        Confirm whether the user is happy to continue with 
        advanced information or the more basic model.
        '''
        while True:
            print(
                """
                This tool uses statistical models to estimate life expectancy
                based on patterns found in national data. There are two versions
                of the model: one that uses a full range of inputs for higher accuracy,
                and another that excludes more sensitive information to prioritise privacy.
                Both models process the data in the same way, such as scaling the inputs,
                applying varying weights to each feature, and combining the results,
                in order to produce a transparent, evidence-based prediction.
                """
            )
            try:
                answer = input(
                    "Do you consent to using advanced population data, "
                    "which may include protected information, for better accuracy? (y/n) "
                ).strip().lower()
                if answer == 'y':
                    print("Thank you for your selection.\n")
                    break
                elif answer == 'n':
                    print("Thank you for your selection.\n")
                    break
                else:
                    print("This input is not recognised, please enter (y/n)")
            except Exception as e:
                print(f"Something went wrong: {e}")
        return answer

    def advanced_model():
        '''
        Gather data from the user to use in the advanced model
        Return a list or the results.
        '''

        while True:
            Country = (input(
                "\nWhat is your country: "
            )).strip().title()
            try:
                answer = input(
                    f"You have entered {Country}. "
                    "Is this correct? (y/n) "
                    ).strip().lower()
                if answer == 'y':
                    break
                elif answer not in ['y', 'n']:
                    print("Please enter y or n.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                print(
                    '''
                    1. Africa
                    2. Asia
                    3. Central America and Caribbean
                    4. European Union
                    5. Middle East
                    6. North America
                    7. Oceania
                    8. Rest of Europe
                    9. South America
                    '''
                )
                answer = int(input(
                    "\nPlease choose your region from the list "
                    "Enter the number: "
                ))
                if 1 <= answer <= 9:
                    Region = Regions_list[answer -1]
                    break
                else:
                    print("Please enter a number between 1 and 9.") 
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Under_five_deaths = float(input(
                    "\nUNDER FIVE DEATHS:\n"
                    "Please enter the number of deaths recorded "
                    "for children under the age of 5, per 1000 population: "
                ))
                if Under_five_deaths >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Adult_mortality = float(input(
                    "\nADULT MORTALITY RATE:\n"
                    "Please enter the Adult Mortality Rates of both sexes "
                    "as a probability of dying between the ages of 15 and 60 "
                    "years per 1000 population: "
                ))
                if Adult_mortality >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                BMI = float(input(
                    "\nAVERAGE BMI:\n"
                    "Please enter the average BMI "
                    "for the entire population: "
                ))
                if BMI > 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Incidents_HIV = float(input(
                    "\nCHILD HIV MORTALITY:\n"
                    "Please enter the number of deaths, per 1 000 live births, "
                    "from HIV/AIDS amongst 0-4 year olds: "
                ))
                if Incidents_HIV >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Measles = float(input(
                    "\nRATE OF MEASLES:\n"
                    "Please enter the number of reported cases, "
                    "per 1000 population, of the measles: "
                ))
                if Measles >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                GDP = float(input(
                    "\nGDP:\n"
                    "Please enter the GDP per capita for your country: "
                ))
                if GDP > 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Schooling = float(input(
                    "\nYEARS IN SCHOOL:\n"
                    "Please enter the number of years "
                    "children have of Schooling: "
                ))
                if Schooling >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                answer = (input(
                    "\nIs your country recognised as a developed country? (y/n) "
                )).strip().lower()
                if answer == 'y':
                    Economy_status_Developed = 1
                    Economy_status_Developing = 0
                    break
                elif answer == 'n':
                    Economy_status_Developed = 0
                    Economy_status_Developing = 1
                    break
                else:
                    print("This input is not recognised, please enter (y/n)")
            except Exception as e:
                print(f"Something went wrong: {e}")

        return ([
            Country,
            Region,
            Under_five_deaths,
            Adult_mortality,
            BMI,
            Incidents_HIV,
            Measles,
            GDP,
            Schooling,
            Economy_status_Developed,
            Economy_status_Developing
        ])

    def simple_model():
        '''
        Gather data from the user to use in the simple model
        Return a list or the results.
        '''

        while True:
            Country = (input(
                "\nWhat is your country: "
            )).strip().title()
            try:
                answer = input(
                    f"You have entered {Country}. "
                    "Is this correct? (y/n) "
                    ).strip().lower()
                if answer == 'y':
                    break
                elif answer not in ['y', 'n']:
                    print("Please enter y or n.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                print(
                    '''
                    1. Africa
                    2. Asia
                    3. Central America and Caribbean
                    4. European Union
                    5. Middle East
                    6. North America
                    7. Oceania
                    8. Rest of Europe
                    9. South America
                    '''
                )
                answer = int(input(
                    "\nPlease choose your region from the list "
                    "Enter the number: "
                ))
                if 1 <= answer <= 9:
                    Region = Regions_list[answer -1]
                    break
                else:
                    print("Please enter a number between 1 and 9.") 
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                BMI = float(input(
                    "\nAVERAGE BMI:\n"
                    "Please enter the average BMI "
                    "for the entire population: "
                ))
                if BMI > 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                GDP = float(input(
                    "\nGDP:\n"
                    "Please enter the GDP per capita for your country: "
                ))
                if GDP > 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                Schooling = float(input(
                    "\nYEARS IN SCHOOL:\n"
                    "Please enter the number of years "
                    "children have of Schooling: "
                ))
                if Schooling >= 0:
                    break
                else:
                    print("This number needs to be a positive value")
            except ValueError:
                print("Please enter a number.")
            except Exception as e:
                print(f"Something went wrong: {e}")

        while True:
            try:
                answer = (input(
                    "\nIs your country recognised as a developed country? (y/n) "
                )).strip().lower()
                if answer == 'y':
                    Economy_status_Developed = 1
                    Economy_status_Developing = 0
                    break
                elif answer == 'n':
                    Economy_status_Developed = 0
                    Economy_status_Developing = 1
                    break
                else:
                    print("This input is not recognised, please enter (y/n)")
            except Exception as e:
                print(f"Something went wrong: {e}")
        return [
            Country,
            Region,
            BMI,
            GDP,
            Schooling,
            Economy_status_Developed,
            Economy_status_Developing
        ]

    def region_conversion(x):
        """
        Return the Regions in the format used 
        for the model (one-hot encoded).
        """
        regions_dict = {
            "Region_Africa": 0,
            "Region_Asia": 0,
            "Region_Central America and Caribbean": 0,
            "Region_European Union": 0,
            "Region_Middle East": 0,
            "Region_North America": 0,
            "Region_Oceania": 0,
            "Region_Rest of Europe": 0,
            "Region_South America": 0
        }
        j = "Region_" + x
        if j in regions_dict:
            regions_dict[j] = 1

        return regions_dict

    def fe_and_scaling(x,med,iqr):
        """
        Modify the parameters so they match the 
        format as expected in the model. 
        Regions converted to a one-hot encoded format
        All values are scaled using the RobustScalar metrics.
        """

        x["log_BMI"] = math.log(x["BMI"])
        x["log_GDP"] = math.log(x["GDP"])

        region_value = x["Region"]
        x.update(region_conversion(region_value))

        for k, v in x.items():
            if k in med and k in iqr:
                x[k] = (x[k] - med[k])/iqr[k]

        return x

    # Confirm which model the user prefers to use
    answer_ethics = confirm_advanced()

    # List of the regions used for one-hot encoding and aiding choice
    Regions_list = [
        "Africa",
        "Asia",
        "Central America and Caribbean",
        "European Union",
        "Middle East",
        "North America",
        "Oceania",
        "Rest of Europe",
        "South America"
    ]

    # Data from the RobustScalar Model
    median_dict = {
        "Infant_deaths": 19.8,
        "Under_five_deaths": 23.3,
        "Adult_mortality": 164.1015,
        "Alcohol_consumption": 4.05,
        "Measles": 83.0,
        "Incidents_HIV": 0.16,
        "Thinness_ten_nineteen_years": 3.3,
        "Schooling": 7.9,
        "log_GDP": 8.347353,
        "log_BMI": 3.238678,
        "log_under_five_deaths": 3.148453,
        "disease": 91.666667
    }

    iqr_dict = {
        "Infant_deaths": 39.9,
        "Under_five_deaths": 57.15,
        "Adult_mortality": 142.96425,
        "Alcohol_consumption": 6.56,
        "Measles": 29.0,
        "Incidents_HIV": 0.4,
        "Thinness_ten_nineteen_years": 5.8,
        "Schooling": 5.3,
        "log_GDP": 2.233373,
        "log_BMI": 0.129212,
        "log_under_five_deaths": 1.948163,
        "disease": 16.333333
    }


    # Advanced Model Calculations
    if answer_ethics == "y":

        # Gather data for advanced linear regression model
        Feature_list = advanced_model()

        # The required fields for this model
        Required_fields = [
            "Country",
            "Region",
            "Under_five_deaths",
            "Adult_mortality",
            "BMI",
            "Incidents_HIV",
            "Measles",
            "GDP",
            "Schooling",
            "Economy_status_Developed",
            "Economy_status_Developing"
        ]

 
        # Assign each feature to its value
        Feature_dict = dict(zip(Required_fields, Feature_list))

        # Engineer and scale the features
        Feature_dict = fe_and_scaling(Feature_dict, median_dict, iqr_dict)

        # The linear regression equation with calculated coefficents
        Life_expectancy = (
        70.9191
        - 4.2765 * Feature_dict["Under_five_deaths"]
        - 6.7703 * Feature_dict["Adult_mortality"]
        + 0.0199 * Feature_dict["Measles"]
        + 0.0315 * Feature_dict["Incidents_HIV"]
        + 0.7762 * Feature_dict["Schooling"]
        + 1.8788 * Feature_dict["Economy_status_Developed"]
        + 0.9612 * Feature_dict["log_GDP"]
        - 0.5318 * Feature_dict["log_BMI"]
        + 1.7073 * Feature_dict["Region_Central America and Caribbean"]
        - 0.8333 * Feature_dict["Region_Oceania"]
        + 1.3974 * Feature_dict["Region_South America"]
        )

        print(
            f"\nThe life expectancy for {Feature_dict['Country']} "
            f"is {round(Life_expectancy, 2)} years of age.\n"
        )

    # Simple Model Calculations
    else:

        # Gather data for simple linear regression model
        Feature_list = simple_model()

        # The required fields for this model
        Required_fields = [
            "Country",
            "Region",
            "BMI",
            "GDP",
            "Schooling",
            "Economy_status_Developed",
            "Economy_status_Developing"
        ]

        # Assign each feature to its value
        Feature_dict = dict(zip(Required_fields, Feature_list))

        # Engineer and scale the features
        Feature_dict = fe_and_scaling(Feature_dict, median_dict, iqr_dict)

        # The linear regression equation with calculated coefficents
        Life_expectancy = (
            62.5700
            + 0.4332 * Feature_dict["Schooling"]
            + 2.3882 * Feature_dict["Economy_status_Developed"]
            + 6.5311 * Feature_dict["log_GDP"]
            + 1.3559 * Feature_dict["log_BMI"]
            + 9.1652 * Feature_dict["Region_Asia"]
            + 8.7169 * Feature_dict["Region_Central America and Caribbean"]
            + 7.4275 * Feature_dict["Region_European Union"]
            + 7.7692 * Feature_dict["Region_Middle East"]
            + 7.3873 * Feature_dict["Region_North America"]
            + 5.9455 * Feature_dict["Region_Oceania"]
            + 9.1373 * Feature_dict["Region_Rest of Europe"]
            + 8.8346 * Feature_dict["Region_South America"]
        )

        print(
            f"\nThe life expectancy for {Feature_dict['Country']} "
            f"is {round(Life_expectancy, 2)} years of age.\n"
        )

    print("https://www.danjmbacon.co.uk/who\n")

life_expectancy_calculator()
