'''
    This script removes the spheres from the collision tags of the links in a urdf and adds a collision_checking tag so
    that the urdf can be used with pinocchio. In pinocchio the collision_checking tag transforms cylinders as capsules.
    This way the links have only one collision object and not multiple ones.
'''

import os
import xml.etree.ElementTree as ET
import rospkg

# load URDF
rospack = rospkg.RosPack()
# pkgpath = rospack.get_path('ocs2_robotic_assets')
# urdfpath = os.path.join(pkgpath, 'resources/centauro/urdf', 'centauro_horizon.urdf')

pkgpath = rospack.get_path('centauro_urdf')
urdfpath = os.path.join(pkgpath, 'urdf', 'centauro_capsule.urdf')

urdf = open(urdfpath, 'r').read()
# print(urdf)

from urdf_parser_py import urdf as urdf_parser
robot = urdf_parser.Robot.from_xml_string(urdf)

# remove spheres from URDF
for link in robot.links:
    if link.collisions:
        spheres = []
        for coll in link.collisions:
            # check for sphere
            # TODO: check if sphere is the unique collision for this link and if yes remove it
            if isinstance(coll.geometry, urdf_parser.Sphere):
                spheres.append(coll)
                print('Will remove sphere for link ', link.name)
        for sphere in spheres:
            # link.collisions.remove(sphere)  # DOESN'T WORK!!!
            link.remove_aggregate(sphere)

for link in robot.links:
    if link.collisions:
        spheres = []
        for coll in link.collisions:
            if isinstance(coll.geometry, urdf_parser.Cylinder):     # if collision is cylinder
                # print("Link: ", link.name)
                # print("Collision: ", coll.name)
                if coll.name == None:
                    coll.name = link.name
                    # link.collision_checking = 0
                    print("added name to collision property of link ", link.name)

# print(urdf)

urdf = robot.to_xml_string()

# print(urdf)

# add collision_checking tag by modifying the xml
xml_root = ET.fromstring(urdf)
for link in xml_root.iter('link'):
    collision_exists = link.find("collision")
    if collision_exists != None:
        new_tag = ET.SubElement(link, "collision_checking")
        capsule_tag = ET.SubElement(new_tag, "capsule")
        capsule_tag.attrib = {'name': link.attrib['name']}
        # link.append(new_tag)
        print("added collision_checking tag to link ", link.attrib['name'])

print('The new urdf to be used by pinocchio is: ')
xml_string = ET.tostring(xml_root, encoding='unicode')
print(xml_string)

# save file

text_file = open(pkgpath + "/urdf/centauro_pinocchio_capsule.urdf", "w")

# write string to file
text_file.write('<?xml version="1.0" ?> \n' + xml_string)

# close file
text_file.close()
print("")