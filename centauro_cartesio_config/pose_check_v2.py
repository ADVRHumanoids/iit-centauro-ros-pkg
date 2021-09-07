#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from xbot_interface import xbot_interface as xbi
from xbot_interface import config_options as co
from cartesian_interface.pyci_all import *
import os
import math
import numpy as np
from urdf_parser_py.urdf import URDF


# Load good ole' Centavero
old_centauro_cfg_dir = '../../../configs/CentauroConfig/'
old_centauro_urdf_path = os.path.abspath(old_centauro_cfg_dir + 'urdf/centauro.urdf')
old_centauro_srdf_path = os.path.abspath(old_centauro_cfg_dir + 'srdf/centauro.srdf')

with open(old_centauro_urdf_path) as f:
    old_centauro_urdf = f.read()

with open(old_centauro_srdf_path) as f:
    old_centauro_srdf = f.read()

cfg = co.ConfigOptions()
cfg.set_urdf(old_centauro_urdf)
cfg.set_srdf(old_centauro_srdf)
cfg.generate_jidmap()
cfg.set_bool_parameter('is_model_floating_base', True)
cfg.set_string_parameter('model_type', 'RBDL')

old_model = xbi.ModelInterface(cfg)
old_urdfdom = URDF.from_xml_string(old_centauro_urdf)


# Load shiny new Centavero
centauro_cfg_dir = '../'
centauro_urdf_path = os.path.abspath(centauro_cfg_dir + 'centauro_urdf/urdf/centauro.urdf')
centauro_srdf_path = os.path.abspath(centauro_cfg_dir + 'centauro_srdf/srdf/centauro.srdf')

with open(centauro_urdf_path) as f:
    centauro_urdf = f.read()

with open(centauro_srdf_path) as f:
    centauro_srdf = f.read()

cfg = co.ConfigOptions()
cfg.set_urdf(centauro_urdf)
cfg.set_srdf(centauro_srdf)
cfg.generate_jidmap()
cfg.set_bool_parameter('is_model_floating_base', True)
cfg.set_string_parameter('model_type', 'RBDL')

new_model = xbi.ModelInterface(cfg)
new_urdfdom = URDF.from_xml_string(centauro_urdf)


# start tests
all_good = True


# check joint names
print('\nChecking joint names... ')
for jn in old_model.getEnabledJointNames():
    if jn not in new_model.getEnabledJointNames():
        print('Joint "{}" is present in old model and not in new'.format(jn))
        all_good = False

for jn in new_model.getEnabledJointNames():
    if jn not in old_model.getEnabledJointNames():
        print('Joint "{}" is present in new model and not in old'.format(jn))
        all_good = False

# check joint limits
print('\nChecking joint limits... ')
old_qmin, old_qmax = old_model.getJointLimits()
new_qmin, new_qmax = new_model.getJointLimits()
qlim_max_err = 0

for jn in new_model.getEnabledJointNames():
    old_idx = old_model.getDofIndex(jn)
    new_idx = new_model.getDofIndex(jn)

    if old_idx <= 0:
        continue

    err = math.fabs(old_qmax[old_idx] - new_qmax[new_idx])

    if err > 0:
        print('Joint "{}" qmax mismatch: error = {}'.format(
            jn, err
        ))
        qlim_max_err = max(qlim_max_err, err)
        all_good = False

    err =  math.fabs(old_qmin[old_idx] - new_qmin[new_idx])

    if err > 0:
        print('Joint "{}" qmin mismatch: error = {}'.format(
            jn, err
        ))
        qlim_max_err = max(qlim_max_err, err)
        all_good = False

print('Joint limits max error is {}'.format(qlim_max_err))


# check link names
print('\nChecking links... ')

for l in old_urdfdom.links:
    ln = l.name
    if not new_urdfdom.link_map.has_key(ln):
        print('Link "{}" missing in new model'.format(ln))


# check poses
print('\nChecking poses... ')

# random q for old model
old_q = np.random.uniform(old_qmin, old_qmax)
old_q[0:6] = np.random.uniform(-3, 3, 6)
old_qdot = np.ones(old_model.getJointNum())

# same q as old model, unless joint does not exist
new_q = np.zeros(new_model.getJointNum())
new_qdot = np.ones(new_model.getJointNum())

for jn in old_model.getEnabledJointNames():
    if jn in new_model.getEnabledJointNames():
        old_idx = old_model.getDofIndex(jn)
        new_idx = new_model.getDofIndex(jn)
        new_q[new_idx] = old_q[old_idx]

old_model.setJointPosition(old_q)
old_model.setJointVelocity(old_qdot)
old_model.update()
new_model.setJointPosition(new_q)
new_model.setJointVelocity(new_qdot)
new_model.update()

for l in old_urdfdom.links:
    ln = l.name

    if not new_urdfdom.link_map.has_key(ln):
        continue

    Told = old_model.getPose(ln, 'pelvis')
    Tnew = new_model.getPose(ln, 'pelvis')
    Terr = (Told.inverse() * Tnew).matrix()
    err = np.linalg.norm(Terr - np.eye(4))
    err_tr = np.linalg.norm(Told.translation - Tnew.translation)
    err_cos = (np.trace(Terr[0:3, 0:3]) - 1)/2.0
    err_cos = min(max(err_cos, -1.0), 1.0)
    err_rot = math.acos(err_cos) / math.pi * 180.

    def print_bold(str):
        print('\033[1m' + str + '\033[0m')

    if err > 1e-9:
        print_bold('\>\>\> Pose mismatch in link "{}": error {} m, {} deg'.format(ln, err_tr, err_rot))
        print('Old: \n{}'.format(Told))
        print('New: \n{}'.format(Tnew))

    vold = old_model.getJacobian(ln).dot(old_qdot)
    vnew = new_model.getJacobian(ln).dot(new_qdot)

    verr = np.linalg.norm(vold - vnew)
    if verr > 1e-9:
        print_bold('\>\>\> Twist mismatch in link "{}": error is {}'.format(ln, verr))
        print('Old: \n{}'.format(vold))
        print('New: \n{}'.format(vnew))
