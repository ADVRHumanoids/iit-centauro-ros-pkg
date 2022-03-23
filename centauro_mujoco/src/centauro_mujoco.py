#!/usr/bin/env python3

from ast import arg
import subprocess
import os 
import shutil
import argparse
import rospkg
from lxml import etree
from copy import deepcopy
import sys
import rospy

rospy.init_node('mujoco_sim')

descr = """
A wrapper aroung mujoco_simulator that assembles a set of separate files
that describe the simulation into a sigle XML file that mujoco can understand.
These files are:
 - the robot urdf
 - a simulation option file (e.g. step size, disabled collisions, ...)
 - a world description (e.g. a ground plane, lights, ...)
 - a configuration file for the decentralized controllers (e.g., default gains)
"""
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('--urdf', help='The path to the robot urdf file')
parser.add_argument('--simopt', help='The path to an XML file containing simulator options')
parser.add_argument('--world', help='The path to an XML file containing the world description')
parser.add_argument('--ctrlcfg', help='The path to a YAML file containing decentralized control configuration')
parser.add_argument('--sites', help='The path to an XML file containing additional sites for the model')
parser.add_argument('--name', help='Unique robot name')
args, _ = parser.parse_known_args()

# handle to rospack system
rospack = rospkg.RosPack()

# utils
def remove_comments(XML):
    tree = etree.fromstring(XML)
    etree.strip_tags(tree, etree.Comment)
    robot = tree.xpath('/robot')[0]
    mujoco = etree.Element("mujoco")
    compiler = etree.Element("compiler")
    compiler.attrib['fusestatic'] = 'false'
    mujoco.append(compiler)
    robot.append(mujoco)
    return etree.tostring(tree)


def treeMerge(a, b):

    def inner(aparent, bparent):
        print(f'processing {aparent.tag} vs {bparent.tag}')
        for bchild in bparent:
            print(f'..processing {bchild.tag}')
            achild = aparent.xpath('./' + bchild.tag)
            if achild and bchild.getchildren():
                inner(achild[0], bchild)
            else:
                aparent.append(bchild)


    res = deepcopy(a)
    inner(res, b)
    return res


# useful paths
urdf_path = args.urdf
mj_xml_dir = f'/tmp/{args.name}_mujoco'
mj_urdf_path = os.path.join(mj_xml_dir, f'{args.name}.urdf')
mj_xml_path = os.path.join(mj_xml_dir, f'{args.name}.xml')
mj_xml_path_orig = os.path.join(mj_xml_dir, f'{args.name}.orig.xml')

# create directory
shutil.rmtree(mj_xml_dir)
os.makedirs(mj_xml_dir, exist_ok=True)

# pre-process urdf to 
#  1) turn package:// directives into absolute paths
#  2) create a different symlink for each mesh to circumvent mjc's bug
with open(urdf_path, 'r') as file:
    urdf = file.read()

seq_id = 0
urdf = remove_comments(urdf.encode()).decode()
urdf_processed = str()
last_pos = 0
pos = urdf.find('filename="')    
while pos != -1:
    uri_start = pos + len('filename="')
    uri_end = urdf.find('"', uri_start)
    uri = urdf[uri_start:uri_end]

    if uri.startswith('package://'):
        pkg_start = len('package://')
        pkg_end = uri.find('/', pkg_start)
        pkg_name = uri[pkg_start:pkg_end]
        uri = rospack.get_path(pkg_name) + uri[pkg_end:] 
    
    filename = os.path.basename(uri)
    dst_file = os.path.join(mj_xml_dir, str(seq_id) + '_' + filename)
    seq_id += 1
    if not os.path.exists(dst_file):
        try: 
            os.remove(dst_file)
        except: pass
        
        os.symlink(uri, dst_file)

    urdf_processed = urdf_processed + urdf[last_pos:uri_start] + dst_file
    last_pos = uri_end
    pos = urdf.find('filename="', uri_end)    

urdf_processed = urdf_processed + urdf[last_pos:]

# write pre-processed urdf
open(mj_urdf_path, 'w').write(urdf_processed)

# produce mujoco's xml
cmd = f'mujoco_compile {mj_urdf_path} {mj_xml_path_orig}'
subprocess.run(cmd.split())

# add options and world
with open(mj_xml_path_orig, 'r') as file:
    mj_xml = file.read()
    mj_xml_tree = etree.fromstring(mj_xml)

with open(args.simopt, 'r') as file:
    mj_opt = file.read()
    mj_opt_tree = etree.fromstring(mj_opt)

with open(args.world, 'r') as file:
    mj_world = file.read()
    mj_world_tree = etree.fromstring(mj_world)

with open(args.sites, 'r') as file:
    mj_sites = file.read()
    mj_sites_tree = etree.fromstring(mj_sites)


mj_xml_tree.remove(mj_xml_tree.xpath('./compiler')[0])
mj_xml_tree.remove(mj_xml_tree.xpath('./size')[0])

xml_merged = treeMerge(mj_xml_tree, mj_opt_tree)
xml_merged = treeMerge(xml_merged, mj_world_tree)

# add sites
site_bodies = mj_sites_tree.xpath('./body')
for sb in site_bodies:
    sname = sb.get('name')
    body = xml_merged.findall(f".//body[@name='{sname}']")[0]
    site = etree.Element('site')
    site.attrib['name'] = sb.xpath('./site')[0].get('name')
    body.append(site)

open(mj_xml_path, 'w').write(etree.tostring(xml_merged, pretty_print=True).decode())
subprocess.run(['mujoco_simulator', mj_xml_path, args.ctrlcfg])

print('bye')