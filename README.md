# LEGO IMAGE BUILDER, CIS 381

This code is intended to be run on a raspberry pi connected to a fanuc robot via a logic level converter

 - To generate low resolution image:
 
    `python2 legoimage.py <image_file>`
    
 - To initiate robot sending procedure:
 
    `python2 send_image_to_robot.py <low_res_image_file>`