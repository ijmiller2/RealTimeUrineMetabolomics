import xmltodict
import re

#Downloaded from: http://www.urinemetabolome.ca/downloads
with open('../../data/urine_metabolites.xml') as fd:
    doc = xmltodict.parse(fd.read())

metabolites = doc['hmdb']['metabolite']
metabolite = doc['hmdb']['metabolite'][0]
name = doc['hmdb']['metabolite'][1]['name']
#Appears to be a set
synonyms = doc['hmdb']['metabolite'][1]['synonyms']['synonym']
diseases = doc['hmdb']['metabolite'][1]['diseases']['disease']
disease_name = doc['hmdb']['metabolite'][1]['diseases']['disease'][0]['name']

#There can be multiple reported contcentrations,bio_specimen types
normal_concentrations = doc['hmdb']['metabolite'][1]['normal_concentrations']['concentration'][0]
normal_concentration = doc['hmdb']['metabolite'][1]['normal_concentrations']['concentration'][0]['concentration_value']
concentration_units = doc['hmdb']['metabolite'][1]['normal_concentrations']['concentration'][0]['concentration_units']
biospecimen_for_concentration = doc['hmdb']['metabolite'][1]['normal_concentrations']['concentration'][0]['biospecimen']

#Open the list of identified metabolites:
detected_metabolites = {}
with open("updated_metabolite_id_list.txt") as infile:
    for line in infile:
        #Omit last two items (# TMS)
        ion = " ".join(line.rstrip().split()).lower()
        #Need a regex for: any amount of characters, followed by "tms", followed by any number
        if re.search(r'.* \d* tms.*',ion):
            metabolite_name = " ".join(line.rstrip().split()[:-2]).lower()
        elif re.search(r'.* tms.*',ion):
            metabolite_name = " ".join(line.rstrip().split()[:-1]).lower()
        else:
            metabolite_name = ion
        detected_metabolites[ion] = metabolite_name
        #print(ion,metabolite_name)

detected_metabolite_dict = {}
## TODO: Could probably invert this loop for efficiency
for metabolite in metabolites:
    name = metabolite['name'].lower()
    hmdb_id = metabolite['accession']

    #If there are entries for diseases
    if metabolite['diseases']:
        diseases = metabolite['diseases']['disease']
        disease_list = [i for i in diseases]
        #if list(disease_list).count('name') >= 1:
        #If there is just one disease entry, since top level dictionary
        if "name" in metabolite['diseases']['disease']:
            disease = metabolite['diseases']['disease']['name']
        #Else there is list of dictionaries
        ## TODO: work on a more robust way of detecting multiple disease associations
        elif "name" in metabolite['diseases']['disease'][0]:
            disease = metabolite['diseases']['disease'][0]['name']
        else:
            disease = None
    else:
        disease = None

    normal_concentration = None
    units = None
    #If there's concentration info
    if metabolite['normal_concentrations']:
        if metabolite['normal_concentrations']['concentration']:
            #If there's only one entry for concenration and it's from urine
            if 'biospecimen' in metabolite['normal_concentrations']['concentration']:
                if metabolite['normal_concentrations']['concentration']['biospecimen'] == "Urine":
                    normal_concentration = metabolite['normal_concentrations']['concentration']['concentration_value']
                    units = metabolite['normal_concentrations']['concentration']['concentration_units']
                #Continue if it's a single case but not urine
                continue
            #Otherwise search all concentrations until you find first instance of Urine concentration
            for concentration in metabolite['normal_concentrations']['concentration']:
                if concentration['biospecimen'] == "Urine":
                    if concentration['concentration_value']:
                        normal_concentration = concentration['concentration_value']
                        units = concentration['concentration_units']
                    else:
                        normal_concentration = None

    for detected_metabolite in detected_metabolites:
        detected_metabolite_name = detected_metabolites[detected_metabolite]
        if detected_metabolite_name == name:
            #print("same name: ",detected_metabolite, name)
            detected_metabolite_dict[detected_metabolite_name] = {
            'disease':disease,
            'hmdb_id':hmdb_id,
            'hmdb_name':name,
            'detected_species':detected_metabolite,
            'normal_concentration':normal_concentration,
            'normal_concentration_units':units
            }

        #This list of synonyms can evalute to None
        elif metabolite['synonyms']:
            #print("Searching synonymns for {}...".format(name))
            synonyms = metabolite['synonyms']['synonym']
            processed_synonymns = [synonym.lower() for synonym in synonyms]
            for synonym in processed_synonymns:
                if detected_metabolite_name == synonym:
                    #print("synonym: ",detected_metabolite_name, name)

                    detected_metabolite_dict[detected_metabolite_name] = {
                    'disease':disease,
                    'hmdb_id':hmdb_id,
                    'hmdb_name':name,
                    'detected_species':detected_metabolite,
                    'normal_concentration':normal_concentration,
                    'normal_concentration_units':units
                    }

with open("updated_metabolite_id_list.txt") as infile:
    for line in infile:
        #Omit last two items (# TMS)
        ion = " ".join(line.rstrip().split()).lower()
        if re.search(r'.* \d* tms.*',ion):
            metabolite_name = " ".join(line.rstrip().split()[:-2]).lower()
        elif re.search(r'.* tms.*',ion):
            metabolite_name = " ".join(line.rstrip().split()[:-1]).lower()
        else:
            metabolite_name = ion
        if metabolite_name in detected_metabolite_dict:
            detected_species = detected_metabolite_dict[metabolite_name]['detected_species']
            hmdb_name = detected_metabolite_dict[metabolite_name]['hmdb_name']
            hmdb_id = detected_metabolite_dict[metabolite_name]['hmdb_id']
            normal_concentration = detected_metabolite_dict[metabolite_name]['normal_concentration']
            normal_concentration_units = detected_metabolite_dict[metabolite_name]['normal_concentration_units']
            disease = detected_metabolite_dict[metabolite_name]['disease']
            outlist = [
                ion,
                hmdb_name,
                hmdb_id,
                normal_concentration,
                normal_concentration_units,
                disease ]
            outlist = ["" if i == None else i for i in outlist]
            outline = "\t".join(outlist)
            print(outline)
        else:
            print(metabolite_name)
