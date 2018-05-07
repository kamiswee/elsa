# crawl.py
# authors:
#    k
# purpose:
#    Elsa uses crawl.py within the  Crawl Starbase app to scour JPL's Starbase Repository for PDS4 
#    Label information.

from lxml import etree
import urllib2, urllib
from chocolate import replace_all
from .forms import *
from .models import Facility


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# The following crawlers are used to make lists or tuples for user Choices.  These are generated on the fly to ensure ELSA is always up to date with Starbase.

# crawl.mission_list is used to crawl the Starbase repository's PDS4 investigation products for a full list of missions listed.
def mission_list():

    starbase_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/investigation/Product/'
    list_of_missions = []
    lines = urllib.urlopen(starbase_url).readlines()

    # This prints the start of a table row that contains table data like a link, an img, etc.  
    for lina in lines:
        if 'PDS4_mission' in lina:        
            #print lina

            # We would like to retrieve simply the mission name from the link.  
            # We can easily retrieve this data by turning each line into an etree.
            # Notice, that an etree from a string returns a root and not the whole tree.
            root = etree.fromstring(lina)

            # We then would like to parse the tree to find our wanted data.
            tag_i_want = root[0][0]
            tag_i_want = tag_i_want.attrib.get('href')

            mission_name = tag_i_want[13:]
            mission_name = mission_name[:-8]
            list_of_missions.append(mission_name)

    return list_of_missions

# crawl.mission_tuple takes in a mission_list and turns the list into 2-tuples.
def mission_tuple():
    list_of_missions = mission_list()
    tuple_of_missions = ((k, k.title()) for k in list_of_missions)
    return tuple_of_missions


# crawl.facility_list():
def facility_list():

    starbase_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/facility/Product/'
    list_of_facilities_for_url = []
    list_of_facilities_title = []
    lines = urllib.urlopen(starbase_url).readlines()

    # Find lina (spanish word for line) containing PDS4_faciliy.
    for lina in lines:

        if 'PDS4_facility' in lina:  

            # Create a subtree that only contains the contents of the lina.
            # attribute_i_want is the completion of the link to get the new_starbase_url.  
            root = etree.fromstring(lina)
            tag_i_want = root[0][0]
            attribute_i_want = tag_i_want.attrib.get('href')
            list_of_facilities_for_url.append(attribute_i_want)


            # Add the contents of the attribute to the end of the given starbase url and then navigate to said page.
            new_starbase_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/facility/Product/{0}'.format(attribute_i_want)
            tree = etree.ElementTree(file=urllib2.urlopen(new_starbase_url))
            root = tree.getroot()
            facility_lid = root[0][0]
            facility_title = root[0][2]
             
            tag_in_question = root[1]
            tag_in_question = etree.QName(tag_in_question)

            if tag_in_question.localname == 'Facility':
                facility_name = root[1][0]
                facility_type_of = root[1][1]

            # This else statement might require future changes.  Currently, this is used for Facility DSN because it has a reference list before the facility tag.  This might require future changes as the facility context products mature.
            else:
                facility_name = root[2][0]
                facility_type_of = root[2][1]
            
            list_of_facilities_title.append(facility_title.text)

            # Get or Create facility object
            facility, created = Facility.objects.get_or_create(title=facility_title.text)
            if created:
                facility.lid = facility_lid.text
                facility.name = facility_name.text
                facility.type_of = facility_type_of.text
                facility.save()
            

    return [list_of_facilities_for_url, list_of_facilities_title]
                

def facility_tuple():

    facilities = facility_list()
    list_of_facilities_for_url = facilities[0]
    list_of_facilities_title = facilities[1]

    tuple_of_facilities = zip(list_of_facilities_for_url, list_of_facilities_title)
    return tuple_of_facilities


    










# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# The following are crawlers used to obtain information specific to the build a bundle process.

# crawl.investigation is used to crawl the investigation products for a given mission's instrument 
# host(s).  A new entry, instrument_host_string_list is added to context_dict and then context_dict
# is returned
def investigation(context_dict):

    # Dictionary Extractions
    Mission = context_dict['Mission']

    # DEBUG
    print '\n\ncrawl.investigation debug--------------'
    print Mission.name ############################################

    # Declarations
    count = 0
    instrument_host_string_list = []
    lidvid_reference = '{http://pds.nasa.gov/pds4/pds/v1}Reference_List/{http://pds.nasa.gov/pds4/pds/v1}Internal_Reference/{http://pds.nasa.gov/pds4/pds/v1}lidvid_reference' 

    # Create etree from XML label found at mission investigation URL
    #  NOTE: Mission.name should already be in the correct format, all uppercase with underscores
    investigation_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/investigation/Product/PDS4_mission_{0}_1.0.xml'.format(Mission.name)
    investigation = urllib2.urlopen(investigation_url)
    investigation_tree = etree.ElementTree(file=investigation)

    # Find mission's instrument host(s)
    for element in investigation_tree.findall(lidvid_reference):
        if element.text[21:36] == 'instrument_host':
            count += 1
            # Then lidvid_reference identifies an instrument_host so add to list
            instrument_host = element.text[48:]
            instrument_host_string_list.append(instrument_host)


    # DEBUG
    print '\n\n--instrument_host_string_list------------'
    print '{0} has {1} associated instrument hosts.'.format(Mission, count)  
    print 'The instrument hosts are listed as follows: '
    for instrument_host in instrument_host_string_list:
        print instrument_host


    # Update context_dict and return
    context_dict['lidvid_reference'] = lidvid_reference
    context_dict['instrument_host_string_list'] = instrument_host_string_list
    #context_dict['instrument_host_url_list'] = instrument_host_url_list
    return context_dict

# crawl.instrument_host is used to crawl a mission's instrument host(s) for instrument host data and
# associated instruments and targets.  This data is then used to create InstrumentHost, Instrument, and 
# Target models.  A new entry, instrument_host_list, is added to context_dict and then context_dict is
# returned.  instrument_host_list is a list of InstrumentHost models.
def instrument_host(context_dict):

    # Dictionary Extractions
    instrument_host_string_list = context_dict['instrument_host_string_list']
    lidvid_reference = context_dict['lidvid_reference']
    Mission = context_dict['Mission']

    # Declarations
    count_inst = 0
    count_targs = 0
    instrument_host_list = []
    #instrument_string_list = []
    #target_string_list = []
    print '\n\n crawl.instrument_host Debug -------------'
    print '--Debug instrument_host_string_list ---------'    
    for instrument_host in instrument_host_string_list:
        print 'Instrument Host: {}'.format(instrument_host)

        # Clean data and make URL 
        instrument_host = instrument_host.upper()
        instrument_host = replace_all(instrument_host, '::', '_')
        instrument_host_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/instrument_host/Product/PDS4_host_{0}.xml'.format(instrument_host)

        # Starbase instrument host tree
        instrument_host_tree = etree.ElementTree(file=urllib2.urlopen(instrument_host_url))
        instrument_host_root = instrument_host_tree.getroot() 

        # Create InstrumentHost model
        h = InstrumentHostForm().save(commit=False)
        h.mission = Mission
        h.raw_data = instrument_host
        h.lid = instrument_host_root[0][0].text
        t = instrument_host_root[2][0].text
        h.title = t.title()  # Starbase error-Title needs to be in title case.
        h.type_of = instrument_host_root[2][1].text
        h.save()

        # Find Associated Instruments and Targets listed in instrument host tree
        for element in instrument_host_tree.findall(lidvid_reference):
            if element.text[21:31] == 'instrument':
                count_inst += 1
  
                # Clean data and make URL
                instrument = element.text[32:-5]
                instrument_cleaned = instrument.upper()
                instrument_cleaned = replace_all(instrument_cleaned, '.', '__')
                instrument_url = 'https://starbase.jpl.nasa.gov/pds4/context-pds4/instrument/Product/PDS4_inst_{0}.xml'.format(instrument_cleaned)
                print '{0}: {1}'.format(count_inst, instrument)

                # Starbase instrument tree
                instrument_tree = etree.ElementTree(file=urllib2.urlopen(instrument_url))
                instrument_root = instrument_tree.getroot()
                    
                # Create Instrument model
                i = InstrumentForm().save(commit=False)
                i.instrument_host = h
                i.raw_data = instrument
                i.lid = instrument_root[0][0].text
                i.title = instrument_root[2][0].text
                i.type_of = instrument_root[2][1].text
                i.save()
                                
            elif element.text[21:27] == 'target':
                count_targs += 1

                # Clean data and make URL
                target = element.text[28:]
                begin_index = target.index('.') + 1
                target_cleaned = target[begin_index:]
                target_cleaned = target_cleaned.upper()
                target_cleaned = replace_all(target_cleaned, '::', '_')               
                target_url = 'https://starbase.jpl.nasa.gov/pds4/1700/PDS4_context_bundle_20161220/target/Product/PDS4_target_{}.xml'.format(target_cleaned)
                print '{0}: {1}'.format(count_targs, target)
                
                # Starbase target tree
                target_tree = etree.ElementTree(file=urllib2.urlopen(target_url))
                target_root = target_tree.getroot()


                # Create Target model
                t = TargetForm().save(commit=False)
                t.instrument_host = h
                t.raw_data = target
                t.lid = target_root[0][0].text
                t.title = target_root[0][2].text
                t.type_of = target_root[1][1].text
                t.save()

        print '\n\nThere are {0} instruments and {1} targets in {2}.'.format(count_inst, count_targs, h.title)

        # Update List
        instrument_host_list.append(h)
    context_dict['instrument_host_list'] = instrument_host_list
    return context_dict
        


##################################################################################################
# Facility Crawl

# crawl.investigation is used to crawl the investigation products for a given mission's instrument 
# host(s).  A new entry, instrument_host_string_list is added to context_dict and then context_dict
# is returned
def facility(context_dict):

    # Dictionary Extractions
    facility = context_dict['facility']

    return context_dict

# NEED TO WORK ON THIS NEXT.  MAKING LIST IN IDEAS & INTENTIONS OF WHAT TO DO.
# I started this and realized I cannot just start here, there's a lot of prep work.


    

            

