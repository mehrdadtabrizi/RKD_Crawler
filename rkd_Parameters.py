#Web crawler for the Photo Archive RKD
#Written by Mehrdad Tabrizi, May 2019, Erlangen - Germany
#Contact: mehrdad.tabrizi1991@gmail.com 

Firefox_Driver_PATH = "C:\geckodriver.exe"
KEYWORD = "Adoration"
Iconography = "Adoration"
Header = [  'Branch',
            'File Name',
            'Image ID',
            'Artist',
            'Title',
            'Iconography',
            'Part',
            'Earliest Date',
            'Latest Date',
            'Margin Years',
            'Genre',
            'Material',
            'Medium',
            'Height of Image Field',
            'Width of Image Field',
            'Type of Object',
            'Height of Object',
            'Width of Object',
            'Diameter of Object',
            'Position of Depiction on Object',
            'Current Location',
            'Repository Number',
            'Original Location',
            'Original Place',
            'Original Position',
            'Context',
            'Place of Discovery',
            'Place of Manufacture',
            'Associated Scenes',
            'Related Works of Art',
            'Type of Similarity',
            'Inscription',
            'Text Source',
            'Bibliography',
            'Photo Archive',
            'Image Credits',
            'Details URL',
            'Additional Information']

CSV_File_PATH = 'RKD_Metadaten (' + KEYWORD + ').csv'
base_url = 'https://rkd.nl/en/'

search_URL = 'https://rkd.nl/en/explore/images'


Images_PATH = 'D:\_DATA\HiWiDateien\Crawler\Downloaded Images\_Anbetung, Adoration\RKD\ '

Images_are_already_downloaded = False