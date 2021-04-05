import os
import re
import html

def main():
    
    entries = os.listdir('./')

    text_files = []
    nml_files = []

    text_files_wo_extension = []
    nml_files_wo_extension = []

    for entry in entries:
        if entry.endswith('.txt'):
            text_files.append(entry)
            text_files_wo_extension.append(entry[0:-4])
        elif entry.endswith('.nml'):
            nml_files.append(entry)
            nml_files_wo_extension.append(entry[0:-4])

         
    #print(text_files_wo_extension)
    #print(nml_files_wo_extension)

    for file in nml_files_wo_extension:
        if file not in text_files_wo_extension:
            create_txt(file)
        else:
            print(file + " already has txt playlist file.")


def create_txt(file):

    print("Creating text playlist file for " + file +".")

    with open(file + '.nml', 'r', encoding='utf-8') as f:
        lines = f.readlines()


    items = []
    playlist = []
    ordered_items = []
    
    #read entries
    for line in lines:
        title_result = re.match('.*<ENTRY.*TITLE="(.*?)".*', line)
        artist_result = re.match('.*<ENTRY.*ARTIST="(.*?)".*', line)
        file_result = re.match('.*<LOCATION.*FILE="(.*?)".*', line)
        
        #print(title_result)
        #print(artist_result)
        #print(file_result)

        #at least one is not None - matching happened - we are on a line of interest..
        if(title_result is not None or artist_result is not None or file_result is not None):
            if(title_result is None):
                title_result = "EMPTY TITLE"
                print("EMPTY TITLE")
            else:
                title = title_result.group(1)          

                
            if(artist_result is None):
                title_result = "EMPTY ARTIST"
                print("EMPTY ARTIST")
            else:
                artist = artist_result.group(1)

            filename = file_result.group(1)

            items.append((artist, title, filename))


    #print(items)
    
    #read playlist
    for line in lines:
        playlist_result = re.match('.*<PRIMARYKEY TYPE="TRACK" KEY="(.*?)".*', line)

        if(playlist_result is not None):
            key = playlist_result.group(1)
            delimiter_location = key.rfind(":")
            filename = key[delimiter_location + 1:]
            playlist.append(filename)
           

    
    #match playlist to items to order them
    for playlist_filename in playlist:
        result = [item for item in items if item[2] == playlist_filename].pop()
        ordered_items.append(result)



    #fix the html strings
    result_items = []

    for item in ordered_items:
        result_items.append((html.unescape(item[0]), html.unescape(item[1])))


    #write the results
    result_file = open(file + ".txt", 'w', encoding='utf-8')

    for item in tuple(result_items):
        result_file.write(item[0] + " - " + item[1] + "\n")
    
    result_file.close()
        

if __name__ == "__main__":
    main()



