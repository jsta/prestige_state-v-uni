import itertools
import pandas as pd

# https://gist.github.com/rogerallen/1583593
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
state_names = [x for x in us_state_to_abbrev.keys()]


def grep_name(y, state_names):
    res = [x if x in y else "" for x in state_names]
    if all([len(x) == 0 for x in res]):
        manual_key = {"UT Austin": "Texas", "UW": "Washington"}
        return manual_key[y]

    res = [x for x in itertools.compress(res, [len(x) > 0 for x in res])][0]
    return res


# ---
dt = pd.read_csv("us-faculty-hiring-networks/data/institution-stats.csv")
dt = dt[dt["TaxonomyLevel"] == "Academia"].sort_values("OrdinalPrestigeRank")

# ---
states = dt[["State" in x for x in dt["InstitutionName"]]].copy()
states.loc[:, "state"] = [
    states["InstitutionName"].iloc[i].split(" ")[0] for i in range(states.shape[0])
]
states = states[[x in state_names for x in states["state"]]]
states = states[["InstitutionName", "OrdinalPrestigeRank", "state"]]
state_names = [x for x in states.state]

# ---
unis = dt[["University of" in x for x in dt["InstitutionName"]]].copy()
unis = unis[[any([x in y for x in state_names]) for y in unis["InstitutionName"]]]
#
unis_manual = dt[
    [x in ["UT Austin", "Ohio University", "UW"] for x in dt["InstitutionName"]]
].copy()
unis = pd.concat([unis_manual, unis])
unis.loc[:, "state"] = [grep_name(y, state_names) for y in unis["InstitutionName"]]
unis = unis.sort_values("OrdinalPrestigeRank")
unis = unis.drop_duplicates("state")
unis = unis[["InstitutionName", "OrdinalPrestigeRank", "state"]]

# ---
# dt[["UW" in x for x in dt["InstitutionName"]]].head()

res = states.merge(unis, how="left", on=["state"])
sum(res["OrdinalPrestigeRank_x"] < res["OrdinalPrestigeRank_y"])

res[res["OrdinalPrestigeRank_y"] > res["OrdinalPrestigeRank_x"]]
