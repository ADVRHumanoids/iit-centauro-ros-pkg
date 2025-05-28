import trimesh
import numpy as np
import os
import xml.etree.ElementTree as ET
 
def divide_mesh_into_cubes(mesh, N):
    bbox_min, bbox_max = mesh.bounds
    size = bbox_max - bbox_min
 
    num_per_axis = int(round(N ** (1/3)))
    cube_size = size / num_per_axis
 
    cubes = []
    for i in range(num_per_axis):
        for j in range(num_per_axis):
            for k in range(num_per_axis):
                min_corner = bbox_min + np.array([i, j, k]) * cube_size
                max_corner = min_corner + cube_size
 
                # Create a bounding box mesh
                box = trimesh.creation.box(extents=cube_size)
                box.apply_translation(min_corner + cube_size / 2)
 
                # Check intersection
                submesh = mesh.section_multiplane(plane_origin=min_corner,
                                                  plane_normal=[1, 0, 0],
                                                  heights=np.linspace(0, cube_size[0], 3))
 
                if submesh:
                    cubes.append((cube_size, min_corner + cube_size / 2))
 
    return cubes

def divide_mesh_into_cubes_voxel(mesh, N):
    # Estimate voxel size from desired number of cubes
    voxel_size = (mesh.bounds[1] - mesh.bounds[0]).max() / (N ** (1/3))
 
    # Voxelize the mesh
    voxelized = mesh.voxelized(pitch=voxel_size)
 
    # Get filled voxel indices
    filled = voxelized.sparse_indices
 
    # Get transform to convert voxel index -> world coordinates
    transform = voxelized.transform
 
    cubes = []
    for index in filled:
        # Convert voxel index to world position (homogeneous coordinates)
        index_hom = np.append(index, 1)  # [i, j, k, 1]
        position = transform @ index_hom  # world center of cube
        cubes.append((np.array([voxel_size]*3), position[:3]))
    
    return cubes

def generate_urdf(cubes, urdf_path):
    robot = ET.Element("robot", name="cube_robot")
 
    for i, (size, position) in enumerate(cubes):
        collision = ET.SubElement(robot, "collision")
        origin = ET.SubElement(collision, "origin", xyz=f"{position[0]*0.001} {position[1]*0.001} {position[2]*0.001}", rpy="0 0 0")
        geometry = ET.SubElement(collision, "geometry")
        box = ET.SubElement(geometry, "box", size=f"{size[0]*0.001} {size[1]*0.001} {size[2]*0.001}")
 
    indent_xml(robot)  # Use custom indent for pretty output
 
    tree = ET.ElementTree(robot)
    tree.write(urdf_path)
    print(f"URDF saved to {urdf_path}")

def indent_xml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def merge_voxels(filled, pitch, transform):
    import numpy as np
    from collections import defaultdict
 
    filled_set = set(map(tuple, filled))
    visited = set()
    merged_cubes = []
 
    dims = np.max(filled, axis=0) + 1  # rough grid size
 
    def can_expand(x, y, z):
        return (x, y, z) in filled_set and (x, y, z) not in visited
 
    for x, y, z in filled:
        if (x, y, z) in visited:
            continue
 
        # Try to expand as far as possible in x, then y, then z
        dx, dy, dz = 1, 1, 1
 
        # Expand in X
        while all(can_expand(x + i, y, z) for i in range(dx, dx + 1)):
            dx += 1
        # Expand in Y
        while all(can_expand(x + i, y + j, z) for i in range(dx) for j in range(dy, dy + 1)):
            dy += 1
        # Expand in Z
        while all(can_expand(x + i, y + j, z + k)
                  for i in range(dx) for j in range(dy) for k in range(dz, dz + 1)):
            dz += 1
 
        # Mark all these voxels as visited
        for i in range(dx):
            for j in range(dy):
                for k in range(dz):
                    visited.add((x + i, y + j, z + k))
 
        # Compute center and size
        min_index = np.array([x, y, z])
        size = np.array([dx, dy, dz]) * pitch
        center_index = min_index + np.array([dx, dy, dz]) / 2
        center_hom = np.append(center_index, 1)
        position = transform @ center_hom
 
        merged_cubes.append((size, position[:3]))
 
    return merged_cubes


def divide_mesh_into_merged_cubes(mesh, N):
    voxel_size = (mesh.bounds[1] - mesh.bounds[0]).max() / (N ** (1/3))
    voxelized = mesh.voxelized(pitch=voxel_size)
    filled = voxelized.sparse_indices
    transform = voxelized.transform
    return merge_voxels(filled, voxelized.pitch, transform)

def main():
    stl_path = "/home/tori/ws/src/robots/iit-centauro-ros-pkg/centauro_urdf/meshes/dg0001_simplified_v2.stl"  # replace with your STL file path
    urdf_output_path = "prova.urdf"
    N = 100000  # number of cubes
 
    mesh = trimesh.load_mesh(stl_path)
    #cubes = divide_mesh_into_cubes_voxel(mesh, N)
    cubes = divide_mesh_into_merged_cubes(mesh, N)
    generate_urdf(cubes, urdf_output_path)
 
if __name__ == "__main__":
    main()