import urllib.request
import requests
import PIL
from PIL import Image

class Item():
    def __init__(self, url):
        self.urlChunk = url;
        self.chunkPrefix = "";
        self.chunkSuffix = "";
        self.baseURL = "https://github.com/msikma/pokesprite/tree/master/items";
        self.name = self.getName();
        self.url = self.getURL(self.urlChunk);

    def downloadSprite(self):
        print("Getting Sprite: " + self.url);
        im = Image.open(requests.get(self.url, stream=True).raw);
        im = self.autocrop_image(im);
        im.save(self.name + ".png");

    def autocrop_image(self, image, border = 0):
        # Get the bounding box
        bbox = image.getbbox()

        # Crop the image to the contents of the bounding box
        image = image.crop(bbox)

        # Determine the width and height of the cropped image
        (width, height) = image.size

        # Add border
        width += border * 2
        height += border * 2
        
        # Create a new image object for the output image
        cropped_image = Image.new("RGBA", (width, height), (0,0,0,0))

        # Paste the cropped image onto the new image
        cropped_image.paste(image, (border, border))

        # Done!
        return cropped_image
        
    def getName(self):
        name = self.urlChunk;
        name = name.replace("--held","");
        name = name.replace("-"," ").title();
        unspacedName = name;
        name = name.replace(" ","");
        nameChunks = name.split("/");
        unspacedNameChunks = unspacedName.split("/")
        self.chunkPrefix = nameChunks[0];
        self.chunkSuffix = nameChunks[1];
        #print(nameChunks)
        
        name = self.chunkSuffix;

        #Suffix before Prefix
        if self.chunkPrefix in ["Apricorn","Berry","Ball",
                             "Hm","Tm","Tr","Fossil","Mint",
                             "Flute","Scarf","Memory",
                             "Plate","Shard","Incense",
                                "Petal","Gem","Mulch",
                                "PokeCandy"]:
            if self.chunkPrefix in ["Hm","Tm","Tr"]:
                self.chunkPrefix = self.chunkPrefix.upper();
            
            name = self.chunkSuffix + self.chunkPrefix;

        #Prefix before Suffix
        if self.chunkPrefix in ["ExpCandy","Roto"]:

            if self.chunkPrefix in ["ExpCandy"]:
                self.chunkSuffix = self.chunkSuffix.upper();

            name = self.chunkPrefix + self.chunkSuffix;

        #Unique Candy Case
        if self.chunkPrefix == "AvCandy":
            newChunks = unspacedNameChunks;
            newChunkPre = newChunks[0].split(" ");
            newChunkSuf = newChunks[1].split(" ");

            if len(newChunkSuf) == 1:
                name = self.chunkSuffix + "Candy";

            else:
                name = newChunkSuf[0] + "Candy" + newChunkSuf[1].upper();           
        
        return name;
        
    def getURL(self, thisURL):
        return self.baseURL.replace("github.com","raw.githubusercontent.com").replace("/tree","/") + "/" + thisURL + ".png";

def cutName(s):
    spaceInd = s.index(" ")
    name = s[spaceInd+1:].replace('"',"").replace(",","")
    return name

#Item Extractor
jsonURL = "https://raw.githubusercontent.com/msikma/pokesprite/master/data/item-map.json"
jsonFile = urllib.request.urlopen(jsonURL)
jsonTXT = []

for line in jsonFile:
    jsonTXT.append(line.decode("utf-8"))
    
jsonTXT = jsonTXT[1:-1]
trimTXT = []

for i in range(len(jsonTXT)):
    
    trim = cutName(jsonTXT[i].strip());

    if trim not in trimTXT:    
        trimTXT.append(trim);
        #print("Item " + str(i) + ": " + trim);

#Create List of Item Objects
itemList = []
for i in range(len(trimTXT)):
    itemList.append(Item(trimTXT[i]));
    #print(itemList[i].name);

#Download Sprites
for item in itemList:
    item.downloadSprite();
