![womancleaningmold](https://github.com/darklysteamgear/moldBuilder/assets/61528531/26edc0ca-7fdc-4e9a-815d-e2153ce73834)
# IE MOLD BUILDER

This is a simple python script I created using OpenCV to help me automate creating molds through generating immersive engineering molds for my modpack. It generates new molds by first using openCV to "Cut" out molds for every 16x16 item texture inside of a designated folder. after it does this, it generates zenscript code based on the names of each item input to create code. this code is outputted to the console, and can be inserted into your craft tweaker script to add each mold into minecraft.

THIS WILL REQUIRE SOME EDITING TO GET THE SCRIPT TO WORK, SINCE IT WAS MADE FOR A SPECIFIC USE CASE. SEE LINE 104

### TO USE:
1.) Make sure you have python! this is a python script

2.) create a folder for minecraft 16x16 items you wish to create molds for, this will be your input folder.

3.) Designate or create an output folder for your molds. this is where your molds will be outputted to.

4.) create a mold builder class, or edit the one already bing used in molder.py and designate your input and output directories, as well as the mold_base and mold_nothing file provided.

5.) run and compile the python program, and get ready for mold!
