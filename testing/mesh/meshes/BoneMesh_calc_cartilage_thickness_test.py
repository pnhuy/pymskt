import pytest
import pymskt as mskt
import SimpleITK as sitk

BONE_MESH = mskt.mesh.io.read_vtk('data/femur_mesh_10k_pts.vtk')
CARTILAGE_MESH = mskt.mesh.io.read_vtk('data/femur_cart_smoothed_binary_no_surface_resampling.vtk')
REF_MESH = mskt.mesh.io.read_vtk('data/femur_thickness_mm_regions_10k_pts.vtk')
SEG_IMAGE = sitk.ReadImage('data/right_knee_example.nrrd')

def test_cal_cartilage_thickness(
    bone_mesh=BONE_MESH,
    cartilage_mesh=CARTILAGE_MESH,
    ref_mesh=REF_MESH
):  
    cart_mesh = mskt.mesh.CartilageMesh(mesh=cartilage_mesh)

    mesh = mskt.mesh.BoneMesh(mesh=bone_mesh, list_cartilage_meshes=[cart_mesh])
    mesh.calc_cartilage_thickness()

    mskt.utils.testing.assert_mesh_scalars_same(mesh.mesh, ref_mesh, scalarname='thickness (mm)')

def test_exception_if_no_cartilage_mesh_and_no_cartilage_labels_provided(
    bone_mesh=BONE_MESH,
):  
    mesh = mskt.mesh.BoneMesh(mesh=bone_mesh)
    with pytest.raises(Exception):
        mesh.calc_cartilage_thickness()
    
def test_create_cartilage_meshes_if_not_created_yet(
    bone_mesh=BONE_MESH,
    seg_image=SEG_IMAGE,
    ref_mesh=REF_MESH,
    cart_mesh=CARTILAGE_MESH,
    cart_label=1
):  
    mesh = mskt.mesh.BoneMesh(mesh=bone_mesh, list_cartilage_labels=[cart_label,], seg_image=seg_image)
    mesh.assign_cartilage_regions()

    mskt.utils.assert_mesh_scalars_same(mesh.mesh, ref_mesh, scalarname='labels')
