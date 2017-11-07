#Downloading Module
import urllib.request
import shutil
import ElsevierScopus as e

#For all data sources, extract the download links
source=e.ElsevierScopus()
links=source.scrape()

print("Extracted links:")
print(links)

filename_counter=0
#Download
for url in links:
    filename='./elsevier'+str(filename_counter)+'.xlsx'
    print("Downloading "+filename)
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    filename_counter=filename_counter+1
