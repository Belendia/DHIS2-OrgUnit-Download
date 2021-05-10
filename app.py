from dhis2 import Api
import json

SERVER = 'https://et.dhis2.net/macepa/'
USERNAME = 'test'
PASSWORD = '#T0rn@d0;'

ORG_UNIT_FIELDS = 'id,name,shortName,featureType,coordinates,parent,openingDate'
ORG_UNIT_GROUP_FIELDS = 'id,name,shortName,organisationUnits'
PAGE_SIZE = 50


class DHIS2:
    def __init__(self):
        self.api = Api(SERVER, USERNAME, PASSWORD)
        self.org_units = {}
        self.org_unit_groups = {}
        self.__metadata_file_name = 'metadata/DHIS2_Metadata.json'

    def __download_org_units(self):
        print('Downloading org units...')
        for index, page in enumerate(
                self.api.get_paged('organisationUnits',
                                   params={'fields': ORG_UNIT_FIELDS},
                                   page_size=PAGE_SIZE)):
            if index == 0:
                self.org_units = page
            else:
                # merge the new org units with the previously downloaded org units
                self.org_units['organisationUnits'] += page['organisationUnits']
            print("Page {} of {}".format(index + 1, page['pager']['pageCount']))

    def __download_org_units_groups(self):
        print('Downloading org unit groups...')
        for index, page in enumerate(
                self.api.get_paged('organisationUnitGroups',
                                   params={'fields': ORG_UNIT_GROUP_FIELDS},
                                   page_size=PAGE_SIZE)):
            if index == 0:
                self.org_unit_groups = page
            else:
                # merge the new org units with the previously downloaded org units
                self.org_unit_groups['organisationUnitGroups'] += page['organisationUnitGroups']
            print("Page {} of {}".format(index + 1, page['pager']['pageCount']))

    def __save_metadata(self):
        print('Saving metadata to {} ... '.format(self.__metadata_file_name), end=" ")
        if 'pager' in self.org_units:
            del self.org_units['pager']
        if 'pager' in self.org_unit_groups:
            del self.org_unit_groups['pager']
        all_metadata = {'organisationUnitGroups': self.org_unit_groups['organisationUnitGroups'],
                        'organisationUnits': self.org_units['organisationUnits']}
        with open(self.__metadata_file_name, 'w') as f:
            json.dump(all_metadata, f)
        print('Done')

    def run(self):
        self.__download_org_units()
        self.__download_org_units_groups()
        self.__save_metadata()


if __name__ == "__main__":
    dhis2 = DHIS2()
    dhis2.run()
