import cv2
import os
import numpy as np
import matplotlib

#this will use opencv to overlay and build a mold of any given 16x16 item asset from minecraft
#mold nothing file is a 20x20 file to aid in the masking process. The code will not work without a white 20x20 file.
#Please note that all outputted mold textures are 16x16
class MoldBuilder():
    def __init__(self, inputDirectory, outputDirectory, moldFile, moldNothingFile):
        self.inputD = inputDirectory
        self.outputD = outputDirectory
        self.moldF = moldFile
        self.moldNothingF = moldNothingFile
        self.inputFiles = {
            "names": [],
            "directories": []
        }
        self.outputString = ""
        self.populate_input_files()
        self.mainProgramStr = ""
        self.moldProgramStr = ""

    #populates the class with the appropriate directories that were given
    def populate_input_files(self):
        self.inputFiles = {
            "names": [],
            "directories": []
        }
        for filename in os.listdir(self.inputD):
            f = self.inputD + "/" + filename
            # checking if it is a file
            if os.path.isfile(f):
                self.outputString += f + " added to input directories \n"
                self.inputFiles["directories"].append(str(f))
                self.inputFiles['names'].append(str(filename[6:-4]))

#THis forms the molds by centering the item you wish to create a mold of, creating some masks with opencv, and then saving the result in a designated folder.
    def form_mold(self, mold, item, name):
        print("creating mold for item " + item)
        #voodoo script for using a completely empty mask to make the mold look a litle better
        nothing = cv2.imread(self.moldNothingF)
        image1 = cv2.imread(item)
        image2 = cv2.imread(mold)
        x_offset = y_offset = 2
        nothing[y_offset:y_offset + image1.shape[0], x_offset:x_offset + image1.shape[1]] = image1
        image1 = nothing
        img2gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
        #opencv nonsense to get a cool mold
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([15, 15, 15])
        lower_white = np.array([240, 240, 240])
        upper_white = np.array([254, 254, 254])
        ret, mask= cv2.threshold(img2gray, 254, 50, cv2.THRESH_BINARY)
        mask2 = cv2.inRange(hsv, lower_black, upper_black)
        mask3 = cv2.inRange(hsv, lower_white, upper_white)
        result = cv2.bitwise_and(image2, image2, mask=mask)
        result[mask2>0] = (54,54,54)

        #result = cv2.add(result,result2)
        #some more trash code
        # Convert image to image gray
        tmp = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Applying thresholding technique
        _, alpha = cv2.threshold(tmp, 10, 250, cv2.THRESH_BINARY)

        # Using cv2.split() to split channels
        # of coloured image
        b, g, r = cv2.split(result)

        # Making list of Red, Green, Blue
        # Channels and alpha
        rgba = [b, g, r, alpha]

        # Using cv2.merge() to merge rgba
        # into a coloured/multi-channeled image
        dst = cv2.merge(rgba, 4)

        sub = cv2.add(image2, image1)
        #cv2.imshow("Masked", result)
        dst = cv2.resize(dst, (16,16), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(self.outputD +"/"+ name + "_mold.png", dst)

    #creates all of the molds by running the form mold class for each item in the given directory
    def create_molds(self):
        i = 0
        for item in self.inputFiles["directories"]:
            self.form_mold(self.moldF, item, self.inputFiles["names"][i])
            self.outputString += "Mold created for item " + item +  "\n"
            i=i+1
 #outputs the log
    def print_output_log(self):
        print(self.outputString)

    #So far just prints everything you need to paste within a contained script for craft tweaker to get your molds to work.
    def program_mold(self, mname):
        self.moldProgramStr +=("var " +mname + "_mold = VanillaFactory.createItem(\"" + mname + "_mold\");\n")
        self.moldProgramStr += (mname + "_mold.maxStackSize = 1;\n")
        self.moldProgramStr += (mname + "_mold.register();\n")
        self.outputString += "Mold " + mname + " programmed into mold script\n"

   #prints everything you need to paste inside of your main craft tweaker script to get your molds to work. please reconfigure as needed, as currently this method was only configured for my use case
    #which was generating molds for modular warfare items.
    def integrate_with_ie(self,mname):
        self.mainProgramStr += "<contenttweaker:" + mname + "_mold>.displayName = \"" + mname[:-4].capitalize() + " Magazine Mold\";\n"
        self.mainProgramStr +="mods.immersiveengineering.MetalPress.addRecipe(<modularwarfare:block."+ mname + ">, <ore:ingotSteel>,<contenttweaker:" + mname + "_mold>, 5000, 16);\n"
        self.outputString += "Mold " + mname + " integrated with IE\n"

    #this runs all of the methods to generate everything you need to paste into your script folders to get your molds to work.
    def integrate_molds(self):
        i = 0
        for dir in self.inputFiles["directories"]:
            self.program_mold(self.inputFiles["names"][i])
            self.integrate_with_ie(self.inputFiles["names"][i])
            i+= 1
        print(self.moldProgramStr)
        print(self.mainProgramStr)

#main name == main method. I may add some more features to this little script later, but feel free to do whatever as long as you give me some credit
if __name__ == "__main__":
    molds = MoldBuilder("C://Users/.../PycharmProjects/moldBuilder/moldinput", "C://Users/.../PycharmProjects/moldBuilder/moldoutput", "C://Users/.../PycharmProjects/moldBuilder/Molds/mold_base.png","C://Users/.../PycharmProjects/moldBuilder/Molds/mold_nothing.png")
    molds.create_molds()
    print(molds.inputFiles["names"])
    molds.integrate_molds()
    molds.print_output_log()


