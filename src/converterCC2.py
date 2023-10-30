import json


def process_codes(properties_list, collapse_levels=True):
    codes = {"topic": [],
             "language": None,
             "artist": [],
             "character": [],
             "experience": [],
             "city": None,
             "nature": [],
             "place": {},
             "period": [],
             "artwork": {}
             }

    if collapse_levels:
        codes["place"] = []
        codes["artwork"] = []

    for property in properties_list:
        property = property.split(":")

        property_label = property[0]
        property_values = [x.replace("-", " ") for x in property[1:] if x]

        if property_label == "NATURE":
            codes["nature"].append(property_values[0])
            _FULL_NATURE.add(property_values[0])

        if property_label == "TEM":
            codes["topic"].append(property_values[0])
            _FULL_TOPICS.add(property_values[0])

        if property_label == "LINGUA":
            codes["language"] = property_values[0]
            _FULL_LANGUAGE.add(property_values[0])

        if property_label == "ART":
            codes["artist"].append(property_values[0])
            _FULL_ARTIST.add(property_values[0])

        if property_label == "PERS":
            codes["character"].append(property_values[0])
            _FULL_CHARACTER.add(property_values[0])

        if property_label == "ESPERIENZA":
            codes["experience"].append(property_values[0])
            _FULL_EXPERIENCE.add(property_values[0])

        if property_label == "CITTAePAESI":
            codes["city"] = property_values[0]
            _FULL_CITY.add(property_values[0])

        if property_label == "PE":
            codes["period"].append(property_values[0])
            _FULL_PERIOD.add(property_values[0])

        if property_label == "OPA":

            if collapse_levels:
                if len(property_values) > 1:
                    codes["artwork"].append(f"{property_values[0]} - {property_values[1]}")
                    _FULL_ARTWORK.add(f"{property_values[0]} - {property_values[1]}")
                else:
                    codes["artwork"].append(property_values[0])
                    _FULL_ARTWORK.add(property_values[0])

            else:
                type_artwork = property_values[0]
                _FULL_ARTWORKTYPE.add(property_values[0])
                if not type_artwork in codes["artwork"]:
                    codes["artwork"][type_artwork] = []

                if len(property_values) > 1:
                    codes["artwork"][type_artwork].append(property_values[1])
                    _FULL_ARTWORK.add(property_values[1])

        if property_label == "LU":
            if collapse_levels:
                if len(property_values) > 1:
                    codes["place"].append(f"{property_values[0]} - {property_values[1]}")
                    _FULL_PLACE.add(f"{property_values[0]} - {property_values[1]}")
                else:
                    codes["place"].append(property_values[0])
                    _FULL_PLACE.add(property_values[0])

            else:
                type_place = property_values[0]
                _FULL_PLACETYPE.add(property_values[0])
                if not type_place in codes["place"]:
                    codes["place"][type_place] = []
                    

                if len(property_values) > 1:
                    codes["place"][type_place].append(property_values[1])
                    _FULL_PLACE.add(property_values[1])
    return codes


_FULL_TOPICS = set()
_FULL_LANGUAGE = set()
_FULL_ARTIST = set()
_FULL_CHARACTER = set()
_FULL_EXPERIENCE = set()
_FULL_CITY = set()
_FULL_NATURE = set()
_FULL_PLACE = set()
_FULL_PERIOD = set()
_FULL_ARTWORK = set()
_FULL_AUTORE = set()
_FULL_ARTWORKTYPE = set()
_FULL_PLACETYPE = set()


def convert_to_json(collapse_leves=False):
    quotes_list = []
    with open("dati30-10_trattini.tsv", encoding="utf-8") as fin:
        fin.readline()
        for line in fin:
            quot_object = {}
            # print(line)
            line = line.strip().split("\t")

            si_cod, quot_name, _, _, quot_content, codes, autore, bib_ref, bib_link = line

            quot_object["id"] = si_cod
            quot_object["name"] = quot_name
            quot_object["fragment"] = quot_content
            #        quot_object["language"] = docgroup.split()[0]
            quot_object["bibliographic_reference"] = bib_ref
            quot_object["bibliographic_link"] = bib_link
            autore = autore.split('#')  # NEW VERSION
            quot_object["autore"] = autore
            for aut in autore:
                _FULL_AUTORE.add(aut)


            ret = process_codes(codes.split(), collapse_levels=collapse_leves)
            ################################
            # da fare la geo-location (bologna default)
            ################################
            quot_object["main_location"] = "44.496599, 11.351678"
            #quot_object["main_location"] = (44.496599, 11.351678)

            for d, v in ret.items():
                quot_object[d] = v
            quotes_list.append(quot_object)

    out_file = open("prova_output.json", "w", encoding="utf-8")

    json.dump(quotes_list, out_file, indent=4, ensure_ascii=False)

    out_file.close()


    dict_labels = {"TOPICS": _FULL_TOPICS,
    "LANGUAGE": _FULL_LANGUAGE,
    "ARTIST": _FULL_ARTIST,
    "CHARACTER": _FULL_CHARACTER,
    "EXPERIENCE": _FULL_EXPERIENCE,
    "CITY": _FULL_CITY,
    "NATURE": _FULL_NATURE,
    "PLACE": _FULL_PLACE,
    "PERIOD": _FULL_PERIOD,
    "ARTWORK": _FULL_ARTWORK,
    "AUTORE": _FULL_AUTORE,
    "ARTWORKTYPE": _FULL_ARTWORKTYPE,
    "PLACETYPE": _FULL_PLACETYPE}

    for label, data_set in dict_labels.items():
        print(label)
        with open(f"data/{label}.txt", "w", encoding="utf-8") as fout:
            print("\n".join(list(data_set)), file=fout)



if __name__ == "__main__":
    convert_to_json(collapse_leves=True)