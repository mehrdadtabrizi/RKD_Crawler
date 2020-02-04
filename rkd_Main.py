#Web crawler for the Photo Archive RKD
#Written by Mehrdad Tabrizi, May 2019, Erlangen - Germany
#Contact: mehrdad.tabrizi1991@gmail.com 

import rkd
import rkd_Parameters as Parameters

def main():
    browser = rkd.browser_open()
    browser = rkd.browser_open_url(browser,Parameters.search_URL)
    browser = rkd.search_for_the_keyword(browser)
    first_item_url = ''.join((browser.current_url)[:-1])

    last_item = rkd.find_last_page(browser)
    PAGE_EXISTS = True
    rkd.create_csv_file(Parameters.CSV_File_PATH)
    item_dic = {

    }
    current_item = 159
    while (current_item <= last_item):
        #if (rkd.page_loaded_successfully(browser)):
        print('working on Item '+str(current_item)+ '...')
        browser.get(first_item_url + str(current_item-1))
        try:
            item_dic = rkd.extract_item_metadata(browser,current_item)
            rkd.append_metadata_to_CSV(item_dic)
        except:
            pass
            #PAGE_EXISTS = rkd.go_to_next_page(browser)
        current_item += 1

    rkd.browser_quit(browser)

if __name__ == '__main__':
    main()
