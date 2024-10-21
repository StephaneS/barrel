#Cycle Render
#E:/E/Blend/Python/barrel.py
#open in the same scite this file
#E:\E\Unity\ssreadme_unity_blender.c

#ToRead: C:\TEMP\test_python.txt is where I am dumping the result of API
#http://www.blendernation.com/category/blender/python-scripts/
#generated blender file E:\E\Blend\barril_final_fs.blend
#https://www.youtube.com/watch?v=RHFX8OWzpUQ
import bpy
import bmesh
import sys
import os
#import ss   #stephane sintes fonctions
from ss_new import *
from ss_blender_lib import *
####################   START CODING        #################### 

#20240827if is_debug:
#20240827   list_system_path()

def mesh_understanding_good():
	bpy.ops.object.mode_set(mode='OBJECT')  #object mode
	obj = bpy.context.active_object
	print('obj name = ',obj.name)  #obj that is currently under edit mode
	current_mesh = obj.data   #we access to the current mesh
	vertices_collection =  current_mesh.vertices
	edges_collection =  current_mesh.edges
	faces_collection =  current_mesh.polygons  #there is no face but polygon
	print(vertices_collection[0])
	for current_vertice in vertices_collection:
	  print('vertice index =',current_vertice.index, end=" ")
	  print('select =',current_vertice.select)  # current_vertice.select is the selection status true or false
	for current_edge in edges_collection:
	  print('edge index =',current_edge.index, end=" ")
	  print('select =',current_edge.select)
	for current_face in faces_collection:
	  print('face index =',current_face.index, end=" ")
	  print('select =',current_face.select)

'''
mesh_understanding_bad has an issue, if I want to modify the face.select it does not work
this is fixed by using mesh_understanding that fix the issue by changing the select in obj mode
'''
def mesh_understanding_bad():
 bpy.ops.object.mode_set(mode='EDIT')  #Edit mode
 obj = bpy.context.edit_object   #you need to be in edit mode
 print('obj name = ',obj.name)  #obj that is currently under edit mode
 current_mesh = obj.data   #we access to the current mesh
 print(type(current_mesh.vertices))   #vertices is a collection:  <class 'bpy_prop_collection'>
 vertices_collection =  current_mesh.vertices
 edges_collection =  current_mesh.edges
 faces_collection =  current_mesh.polygons  #there is no face but polygon
 print(vertices_collection[0])		#<bpy_struct, MeshVertex at 0x0000022F04923BA8>
 for current_vertice in vertices_collection:
  print('vertice index =',current_vertice.index, end=" ")
  print('select =',current_vertice.select)
 for current_edge in edges_collection:
  print('edge index =',current_edge.index, end=" ")
  print('select =',current_edge.select)
 for current_face in faces_collection:
  print('face index =',current_face.index, end=" ")
  print('select =',current_face.select)
  current_face.select = False  #this will have no impact
 return(current_vertice)


#work in node editor
def nodeSelect():
	print("bpy.context.area.type = ",bpy.context.area.type) 
	for window in bpy.context.window_manager.windows:
		screen = window.screen
	for area in bpy.context.screen.areas:
		area.type
		#print("area.type = ",area.type)
        #to find the NODE_EDITOR you must have a NODE_EDITOR window open
		if area.type == "NODE_EDITOR":
			for region in area.regions:
				#print("region.type = ",region.type) 
				override = {'window': window, 'screen': screen, 'area': area,'region' : region}
			#override = bpy.context.copy()
			#override['area'] = area
				try:
					bpy.ops.node.select_all(override,action='DESELECT')
				except:
					print('error detectected  bpy.ops.node.select_all')
					pass
				try:
					bpy.ops.node.delete(override)
				except:
					print('error detectected bpy.ops.node.delete(')
					pass


#pour redresser les trais dans uv    scale  shift - x - 0
#pour selectionner des vertices alt - bouton droit
def uv_line():
        # UV data is accessible only in object mode
        prev_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Update vertex selection properties, in case the script wasn't run in  object mode
        bpy.context.object.update_from_editmode()
        # Active object assumed to be a mesh and already have a UV map
        mesh = bpy.context.object.data   #<class 'bpy_types.Mesh'>
        #super_dir(mesh,'mesh')
        uv_map = mesh.uv_layers.active
        selected_loops = []
        pt_uv = set()   # A set is an unordered collection with no duplicate elements
        my_uv = Vector()	# my_uv is a vector
        for index, uv_loop in enumerate(uv_map.data):   #enumerate return the couter and the data
                if(uv_loop.select):
                        selected_loops.append(index)
                        print("index=",index,"uv_loop=",uv_loop)
                        print("uv_loop.uv=",uv_loop.uv)
                        #if(uv_loop.uv.x == my_uv.x):
                        my_uv = uv_loop.uv
                        my_uv.x
                        my_uv.y
                        pt_uv.add ((my_uv.x,my_uv.y))  #add the point to the list; several point have the same mapping, I guess this is due to the symetrie of the barrel that create the same mapping
        for my_uv in pt_uv:
         my_uv

	#we take only the last 2 points because lot of duplication
        #we define 2 vectors my_uv1 and my_uv2
        my_uv1 = Vector()
        my_uv2 = Vector()
        #we restaure the last 2 points
        my_uv1 = pt_uv.pop()
        my_uv2 = pt_uv.pop()
        #I have 2 point I compute the vector between the 2 points
        x = (my_uv2[0]-my_uv1[0])
        y = (my_uv2[1]-my_uv1[1])
        vectA =  Vector(( abs(x), abs(y), 0))
        vectB =  Vector(( 0, 1, 0))
        angle = vectA.angle(vectB)  #compute the angle between current uv vector and vertical vector
        angled = degrees(angle)    #convert the angle in degree
        print('angle degree',angled)
        # Restore whatever mode the object is in previously
        bpy.ops.object.mode_set(mode=prev_mode)
        return angled








bpy.context.selected_objects
print(bpy.data.scenes.keys())



#bpy.ops.wm.read_factory_settings()
def which_points_selected():
    obj = bpy.context.edit_object
    me = obj.data
    counter = 0
    for pt in me.points:
      #print(pt.select)
      if pt.select == True:  # 
        print(counter)
      counter = counter+1
    return counter

#loop for all contexts
def loop_context():
 for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
      print('VIEW_3D')
    elif  area.type == 'PROPERTIES':
     print('PROPERTIES');
    elif  area.type == 'CONSOLE':
     print('CONSOLE');
    elif  area.type == 'OUTLINER':
     print('OUTLINER');
 return	


def face_separate_and_rename(new_name):
	#here the list of objects before
	objListBefore = set(bpy.data.objects[:])
	bpy.ops.mesh.separate();  #separate the face
	#when you separate the faces, the new obj created is not the new one
	#here the list of objects after
	objListAfter = set(bpy.data.objects[:])
	#make the difference between the 2 list
	new_objects = objListBefore ^ objListAfter
	for o in new_objects:
	 print(o.name)
	 o.name =  new_name
	return



####################   START CODING        #################### 
version=4.2
layer1 = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
origin = (0,0,0)



delete_obj_by_name('Cube')


space_view_3d = get_SpaceView3D()
if(version >= 2.8):
      space_view_3d.overlay.show_floor = True   #enleve/met le floor
else:
      space_view_3d.show_floor = True #enleve/met le floor
      space_view_3d.show_all_objects_origin #false

super_dir(space_view_3d,"space_view_3d")

space_region_view_3d = get_RegionView3D()

#add 3 planes and one cylinder

if(version >= 2.8):
    bpy.ops.mesh.primitive_plane_add(size =5, location=(0, 0, -20))
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -20))
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -20))
    obj = bpy.context.active_object
    obj.name = "Plane_Wine"
    plane_wine_obj = obj
else:
    bpy.ops.mesh.primitive_plane_add(radius =5, location=(0, 0, -20))
    bpy.ops.mesh.primitive_plane_add(radius=5, location=(0, 0, -20))
#add cylinder with 12 vertices
bpy.ops.mesh.primitive_cylinder_add(vertices=12, location=origin)


#add modifier SUBSURF in the cylinder =>allow to subdivide the faces
bpy.ops.object.modifier_add(type='SUBSURF')

if(version >= 2.8):
	bpy.context.object.modifiers["Subdivision"].levels = 2
else:
	bpy.context.object.modifiers["Subsurf"].levels = 2
    
#smooth the result
bpy.ops.object.shade_smooth()

#Edit mode
bpy.ops.object.mode_set(mode='EDIT')



#get region  area
region, region_view_3d, space_view_3d, area_view_3d = view3d_find(True)
super_dir(area_view_3d, "area_view_3d")

#define the override
override = {'scene' : bpy.context.scene,'region' : region,'area'   : area_view_3d,'space'  : space_view_3d}



obj = bpy.context.edit_object   #you need to be in edit mode
print('obj name = ',obj.name)  #obj that is currently under edit mode:  obj name =  Cylinder

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190814_123634.jpg

print("we are ok same picture")



me = obj.data   #we access to the current mesh of cylinder
bm = bmesh.from_edit_mesh(me)  #we use the  bmesh module, accessing the current edit mode mesh.
current_vertice = mesh_understanding_bad()
current_vertice = mesh_understanding_good()

obj = bpy.context.active_object
super_dir(obj,'obj')

'''
bmesh module is documented here https://www.blender.org/api/blender_python_api_2_64_9/bmesh.html

Mesh Access
There are 2 ways to access BMesh data, 
you can create a new BMesh by converting a mesh from bpy.types.BlendData.meshes or 
by accessing the current edit mode mesh. see: bmesh.types.BMesh.from_mesh and bmesh.from_edit_mesh respectively.

When explicitly converting from mesh data python owns the data, that is to say - that the mesh only exists while python holds a reference to it, 
and the script is responsible for putting it back 
into a mesh data-block when the edits are done.
Note that unlike bpy, a BMesh does not necessarily correspond to data in the currently open blend file, a BMesh can be created, edited and freed without the user ever seeing or having access to it. 
Unlike edit mode, the bmesh module can use multiple BMesh instances at once.
Take care when dealing with multiple BMesh instances since the mesh data can use a lot of memory, 
while a mesh that python owns will be freed in when the script holds no references to it, 
its good practice to call bmesh.types.BMesh.free which will remove all the mesh data immediately and disable further acce

bmesh.from_edit_mesh(mesh)
Return a BMesh from this mesh, currently the mesh must already be in editmode

'''
#Edit mode
bpy.ops.object.mode_set(mode='EDIT')
#at this level we have from 0 to 35 edge for the cylinder so a total of 36 edges
# 12 vertical
# 2x 12 horizontal  C:/D/SSPublic/Public_ImageNote/2016/07_020_int003173_20160906_125017.jpg


'''
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":2, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":12, "mesh_select_mode_init":(True, False, False)}, TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})


'''
#add 2 edge loop
#for this we use the loopcut_slide and the first parameter is the override allowing to have a correct context
#Hotkey: Ctrl-R

nb_cut=2
edge_index=30
if(version >= 2.8):
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":2, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":12, "mesh_select_mode_init":(True, False, False)}, TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})
    
	#add_loopcut_slide_28(edge_index, nb_cut)
else:
	add_loopcut_slide(override,edge_index,nb_cut)
	
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190814_130754.jpg


#en reality quand du rajoute un surface diviser a un cylindre ca cree un structure complexe, avec les cotes en forme de ciseaux
# c est normal car le nombre de face est multiplier par 10 -- face equi surface  c est pour ca que ca forme un boule
#C:/D/SSPublic/Public_ImageNote/2017/RN006562_capture_20171105_173356.jpg
# et si regarde la  top face  est constituee de multi face comme des parts de gateau
# en rajoutant un edge loupe en haut et en bas , ca t'annule ce cisaillement et redonne la forme du cylinder

#we want to place those 2 edge loop on top and bottom, so the way is to  scale z
#le fait de les scaler en z les separent en z et les place en haut et en bas, ca permet de re-avoit un cyclindre


if(version >= 2.8):
    bpy.ops.transform.resize(value=(1, 1, 3), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
else:
	bpy.ops.transform.resize(override,value=(0, 0, 3), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)


#C:/D/SSPublic/Public_ImageNote/2016/int003266_capture_20160911_153833.jpg



###########		VIEWS       #####################
#set the front view
set_top_view_in_view_3d('FRONT')
bpy.ops.object.mode_set(mode='OBJECT')


##################  background image   ##################
#On met le tonneau en image de fond pour pouvoir le dessiner par-dessus comme un calque
#on voit la  background image uniquement en front view
bpy.ops.object.mode_set(mode='OBJECT')

'''
20240829
sur blender j'ai recréé le tonneau il y a plusieurs API qui ne sont plus supportés.
 Par exemple la gestion de mettre des images en background ne se fait plus de la même façon lorsque j'exécute une commande je fais planter blender donc il faut que je reprenne ça en main
J'ai finalement isolé le problème qui vient du fait de mettre background =True 
finalement quand je vais pas j'obtiens à peu près la même image donc j'ai pas besoin de l’utiliser 

l'instruction suivante plante
bpy.ops.object.empty_image_add(filepath="C:\\E\\Blend\\barril_pic.jpg", relative_path=True, align='VIEW', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), background=True)
mais sans le background ca fontionne
'''


if(version >= 4.2):
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    result = bpy.ops.object.empty_image_add(filepath=r"C:/E/Blend/barril_pic.jpg", relative_path=True, align='VIEW', location=(0, 0, 0), rotation=(1.5708, 0, 0), scale=(4, 4, 4))
    print('result', result) # result {'FINISHED'}
    
elif(version >= 2.8):
    bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.object.empty_add(override,type='IMAGE', radius=1, align='VIEW', location=(0, 0, 0), rotation=(1.10871, 0.0132652, 1.14827))
    bpy.ops.object.load_background_image(filepath=os.environ['FOLDER_E']+'/E/Blend/barril_pic.jpg')
    bpy.context.object.rotation_euler[0] = 1.5708
    obj = bpy.data.objects["Cylinder"]
else:    
    background_image(os.environ['FOLDER_E']+'/E/Blend/barril_pic.jpg')

obj = bpy.data.objects["Cylinder"]
bpy.context.view_layer.objects.active = obj  # we select the Cylinder  object
obj.select_set(True)

#C:/D/SSPublic/Public_ImageNote/2020/RN006562_capture_20200615_080329.jpg


#adapt the cylinder to the cylinder picture
#Edit mode
bpy.ops.object.mode_set(mode='EDIT')
#Select all
bpy.ops.mesh.select_all(action='SELECT')
#scale x y z
factor = 3.12847


if(version >= 2.8):
    bpy.ops.transform.resize(value=(factor, factor, factor), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
    #scale z  C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190814_133400.jpg
    bpy.ops.transform.resize(value=(1, 1, 1.49343), constraint_axis=(False, False, True), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
    #scale shift-z    on scale la circonference  en x et y  - il garde sa hauteur
    bpy.ops.transform.resize(value=(0.900938, 0.900938, 1), constraint_axis=(True, True, False), mirror=False,proportional_edit_falloff='SMOOTH', proportional_size=1)
else:
    bpy.ops.transform.resize(value=(factor, factor, factor), constraint_axis=(False, False, False), mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    #scale z  C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190814_133400.jpg
    bpy.ops.transform.resize(value=(0, 0, 1.49343), constraint_axis=(False, False, True), mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    #scale shift-z    on scale la circonference  en x et y  - il garde sa hauteur
    bpy.ops.transform.resize(value=(0.900938, 0.900938, 0), constraint_axis=(True, True, False), mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)




#let incline the view the barrel
if(version >= 4.2):   
        area_type = 'VIEW_3D'
        areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen
        ):
            bpy.ops.view3d.view_orbit( type = 'ORBITUP')
else:
    #let incline the view the barrel
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            bpy.ops.view3d.view_orbit(override, type = 'ORBITUP')
            break



result  = bpy.ops.mesh.select_all(action='DESELECT')  #AKey : deselect all mesh


#the next step is drawing the top of the barrel
#let s select the top face - the id is 10

#C:/D/SSPublic/Public_ImageNote/2016/int003267_capture_20160911_155457.jpg

select_faces(10)  #we select the top face, the top barrel disk face


#I developped a function that allow to provide the id of the face selected
#which face is selected?
nbFaceSelected,faceSelected = which_face_selected()
print("nb of face selected =" + str(nbFaceSelected) + "  id face selected " + str(faceSelected))
#nb of face selected=1  nb total faces [10]

len(me.vertices)
len(me.edges)
len(me.polygons) # faces
len(me.polygons[10].vertices)

face = me.polygons[10]
face_normal=face.normal
face_normal.z		#   =1   le cyndre hauteur est sur axe z 




for i in list(me.polygons):
	print("index="+str(i.index))
	face = me.polygons[i.index]
	face_normal=face.normal
	face_normal.z		#   =1   le cyndre hauteur est sur axe z 


#Exclude the top face
'''
when we exclude a face this is not adding one face but several face connected to the vertices
because we exclude the face 10 does not exist anymore
'''
bpy.ops.mesh.extrude_region_move()



#scale x and y
bpy.ops.transform.resize(value=(0.978341, 0.978341, 1), constraint_axis=(True, True, False), mirror=False,proportional_edit_falloff='SMOOTH', proportional_size=1)

#Exclude
bpy.ops.mesh.extrude_region_move()
#scale x and y    en vue du dessu or fait l interieur du tonneau plus petit
bpy.ops.transform.resize(value=(0.864725, 0.864725, 1), constraint_axis=(True, True, False), mirror=False,proportional_edit_falloff='SMOOTH', proportional_size=1)

#C:/D/SSPublic/Public_ImageNote/20240829_120201.jpg




#Exclude profondeur en descendant on z
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.799307), "constraint_axis":(False, False, True), "mirror":False,  "proportional_edit_falloff":'SMOOTH'})
#C:/D/SSPublic/Public_ImageNote/2016/07_020_int003269_20160911_160236.jpg
#Exclude


bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(0.983494, 0.983494, 0), constraint_axis=(True, True, False), mirror=False,proportional_edit_falloff='SMOOTH', proportional_size=1)
#C:/D/SSPublic/Public_ImageNote/2016/int003270_capture_20160911_160307.jpg


bpy.ops.object.mode_set(mode='EDIT')

#AKey : select all
#bpy.ops.mesh.select_all(action='SELECT')

if(version >= 2.8):

    space_view_3d.shading.type = 'WIREFRAME'
    space_view_3d.shading.type = 'MATERIAL'
    space_view_3d.shading.type = 'SOLID'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.shading.type = 'SOLID'
            break

else:
    space_view_3d.viewport_shade = 'WIREFRAME'
    space_view_3d.viewport_shade = 'MATERIAL'
    space_view_3d.viewport_shade = 'SOLID'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.viewport_shade = 'SOLID'
            break



#we need to be in edit mode solid

bpy.ops.mesh.select_all(action='DESELECT')

select_faces(45)
#even if very thin face 45 is a face :C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_184535.jpg
#face 45 is a face on x y plan  // au convercle du tonneau

if(version >= 4.2):

    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":5, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":39, "mesh_select_mode_init":(False, False, True)}, TRANSFORM_OT_edge_slide={"value":-0.253485, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "correct_uv":False, "release_confirm":False, "use_accurate":False})

elif(version >= 2.8):
    bpy.ops.mesh.loopcut_slide(override,MESH_OT_loopcut={"number_cuts":5, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":39, "mesh_select_mode_init":(False, False, True)}, TRANSFORM_OT_edge_slide={"value":-0.253485, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":False, "release_confirm":False, "use_accurate":False})
else:
    
    #add 5 lookup at the center  therefore parallel on the barrel lid
    add_loopcut_slide(override,45,5)

#C:/D/SSPublic/Public_ImageNote/20240829_133201.jpg
#C:/D/SSPublic/Public_ImageNote/2016/int003271_capture_20160911_161138.jpg



#AKey : deselect all
bpy.ops.mesh.select_all(action='DESELECT')


###		Delete the second part of the barrel

#we select the bottom face of the barrel
select_faces(13)

#et on remote en selectionant les face adjacentes pour avoir la moitie partie du bas du tonneau selectiones

bpy.ops.mesh.select_more()  # select +vertice
bpy.ops.mesh.select_more()  # select first line of face
bpy.ops.mesh.select_more()
bpy.ops.mesh.select_more()
#C:/D/SSPublic/Public_ImageNote/2016/int003272_capture_20160911_162420.jpg


bpy.ops.mesh.delete(type='FACE')  #delete faces  => on a coupe le tonneau en 2 pour faire une symetrie



###		Make a symetry

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_185811.jpg

#set the front view

if(version >= 4.2):
    set_top_view_in_view_3d('FRONT')
elif(version >= 2.8):
    bpy.ops.view3d.view_axis(override, type = 'FRONT')
else:
    bpy.ops.view3d.viewnumpad(override, type = 'FRONT')



#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_185833.jpg

#select   vertice
bpy.ops.mesh.select_mode(type="VERT")
#bpy.ops.mesh.select_mode(type="EDGE")
#bpy.ops.mesh.select_mode(type="FACE")

select_Vertices(83)
#C:/D/SSPublic/Public_ImageNote/2016/int003279_capture_20160913_135339.jpg




bpy.ops.mesh.loop_multi_select(ring=False)



#move the cursor to selected obj
if(version >= 4.2):
    area_type = 'VIEW_3D'
    areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]
    with bpy.context.temp_override(
        window=bpy.context.window,
        area=areas[0],
        region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
        screen=bpy.context.window.screen
    ):
        bpy.ops.view3d.snap_cursor_to_selected()
else:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            bpy.ops.view3d.snap_cursor_to_selected(override)
            break

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_190308.jpg

#OBJECT mode
bpy.ops.object.mode_set(mode='OBJECT')

#changing the object origin to cursor
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_190426.jpg


#add mirror for the cylinder on z direction
bpy.ops.object.modifier_add(type='MIRROR')
if(version >= 2.8):
    bpy.context.object.modifiers["Mirror"].use_axis[0] = False
    bpy.context.object.modifiers["Mirror"].use_axis[1] = False
    bpy.context.object.modifiers["Mirror"].use_axis[2] = True
else:
    bpy.context.object.modifiers["Mirror"].use_x = False
    bpy.context.object.modifiers["Mirror"].use_z = True
#C:/D/SSPublic/Public_ImageNote/2016/int003280_capture_20160913_135903.jpg file not detected





#### ADD a Lattice object and its associated modifier


# a lattice is an object composed only of vertice - a lattice object has no Face
#add lattice modifier
bpy.ops.object.modifier_add(type='LATTICE')


#add lattice object
if(version >= 2.8):
    bpy.ops.object.add(radius=1, type='LATTICE', enter_editmode=False, location=(0, 0, 0))
else:
    bpy.ops.object.add(radius=1, type='LATTICE', view_align=False, enter_editmode=False, location=(0, 0, 0), layers=layer1)





#identify the cylinder
obj = bpy.data.objects["Cylinder"]
#get the dimension of the cylinder
(x,y,z) = obj.dimensions

obj = bpy.context.active_object
print('obj name = ',obj.name)
#scale the lattice to have the same dimention as the barrel a little bit bigger
bigger = 0.2;

if(version >= 2.8):
   bpy.ops.transform.resize(value=(x+bigger, y+bigger, z+bigger), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
else:
    bpy.ops.transform.resize(value=(x+bigger, y+bigger, z+bigger), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_191052.jpg



obj = bpy.data.objects["Cylinder"]
if(version >= 2.8):
    obj.select_set(True)
else:
    obj.select = True
bpy.ops.object.mode_set(mode='EDIT') #Edit mode
#Affect the lattice object to lattice modifer
obj.modifiers["Lattice"].object = bpy.data.objects["Lattice"]

#add more points to the lattice  .. so 7 points means 7x4=28 vertices
bpy.data.lattices["Lattice"].points_w = 7



#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_203724.jpg
obj = bpy.data.objects["Lattice"]
list(obj.data.points)


counter = which_points_selected()
print(counter)



#we need to be in edit mode
#Edit mode
bpy.ops.object.mode_set(mode='EDIT')

#get the Lattice object
obj = bpy.data.objects["Lattice"]

#select 4 pts of the Lattice
for x in range(20,24): #
    print("x=",x)
    obj.data.points[x].select = True

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_204501.jpg
if(version >= 2.8):
    bpy.ops.transform.resize(value=(1.1519, 1.1519, 1.1519), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
else:
    bpy.ops.transform.resize(value=(1.1519, 1.1519, 1.1519), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
#C:/D/SSPublic/Public_ImageNote/2016/int003485_capture_20160915_153308.jpg
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_204552.jpg

def deselect_lattice_vertice():
	for x in range(0,28): #
		obj.data.points[x].select = False


#deselect the previous lattice  points
deselect_lattice_vertice()

for x in range(16,20): #
    obj.data.points[x].select = True

def resize_lattice(x,y,z):
    if(version >= 2.8):
        bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
    else:
        bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

resize_lattice (1.423, 1.423, 1.423)


#deselect the previous 4 points
deselect_lattice_vertice()

for x in range(12,16): #
    obj.data.points[x].select = True

resize_lattice (1.5, 1.5, 1.5)


#deselect the previous 4 points
deselect_lattice_vertice()

for x in range(8,12): #
    obj.data.points[x].select = True

resize_lattice (1.423, 1.423, 1.423)

#deselect the previous 4 points
deselect_lattice_vertice()



for x in range(4,8): #
    obj.data.points[x].select = True

resize_lattice (1.1519, 1.1519, 1.1519)

#deselect the previous 4 points
deselect_lattice_vertice()




# deselect the Lattice ans select the cylinder
deselect_all_object()
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_204905.jpg

obj = bpy.data.objects["Cylinder"]
if(version >= 2.8):
    obj.select_set(True)
else:
    obj.select = True


#OBJECT mode
bpy.ops.object.mode_set(mode='OBJECT')
#Duplicate the cylinder need to be in  OBJECT mode
bpy.ops.object.duplicate_move() # "Cylinder.001" is created
#deselect cylinder

if(version >= 2.8):
    bpy.data.objects["Cylinder"].select_set(False)
    bpy.data.objects["Cylinder.001"].select_set(True)
else:
    bpy.data.objects["Cylinder"].select = False
    bpy.data.objects["Cylinder.001"].select = True


#select cylinder.001 and deselect the Cylinder


def get_OUTLINER():
 for area in bpy.context.window.screen.areas:
  print("area.type = ", area.type)
  if area.type == 'OUTLINER':
    return(area.spaces[0])
#r area.type =  INFO
#r area.type =  PROPERTIES
#r area.type =  CONSOLE
#r area.type =  OUTLINER
#r area.type =  VIEW_3D 
 return
 
outliner = get_OUTLINER()


if(version >= 2.8):

    bpy.ops.collection.create(name  = "RingCollection") #create collection
    bpy.context.scene.collection.children.link(bpy.data.collections["RingCollection"]) #make it visible in outliner
    cylinder_ring_collection = bpy.data.collections["RingCollection"]
    scene = bpy.context.scene
    #super_dir(bpy.context.scene,'bpy.context.scene')
    collection = bpy.context.scene.collection
    #super_dir(bpy.ops.collection,'bpy.ops.collection')
    #super_dir(bpy.context.scene.collection,'bpy.context.scene.collection')
    #super_dir(bpy.context,'bpy.context')
    #super_dir(bpy.data,'bpy.data')        
       
    cylinder_d  = bpy.data.objects["Cylinder.001"]
    cylinder_collection = find_collection(bpy.context, cylinder_d)
    #cylinder_ring_collection =  make_collection("RingCollection", cylinder_collection)
    cylinder_collection.objects.unlink(cylinder_d)  # remove it from the old collection
    #cylinder_ring_collection.objects.link(cylinder_d)  # put the cube in the new collection

    bpy.data.collections['RingCollection'].hide_viewport = False
    bpy.data.collections[cylinder_collection.name].hide_viewport = True 
    view_layer = bpy.context.view_layer

    #super_dir(view_layer.active_layer_collection,'view_layer.active_layer_collection')        
    #super_dir(cylinder_ring_collection,'cylinder_ring_collection')        

    #view_layer.active_layer_collection= cylinder_ring_collection
    #collection = bpy.data.collections.new('My Collection')
    #bpy.context.scene.collection.children.link(collection)
    # NOTE the use of 'collection.name' to account for potential automatic renaming
    #layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
    #bpy.context.view_layer.active_layer_collection = layer_collection
    #layer_collection.hide_viewport = True
else:
    bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    #move "Cylinder.001" the new layer (layer 2)
    #change active layer 
    bpy.context.scene.layers[1] = True
    bpy.context.scene.layers[0] = False




context = bpy.context
scene = context.scene
context.selected_objects[0]

#super_dir(bpy.context.scene.objects,'bpy.context.scene.objects')       
#super_dir(bpy.data.objects["Cylinder.001"],'obj_Cylinder')
#apply modifiers Subsurf and Lattice that I used previously 
#we apply only in Layer1 with the duplicate cylinder



if(version >= 4.2):
    bpy.context.view_layer.objects.active = bpy.data.objects['Cylinder.001']
    bpy.context.object.modifiers["Subdivision"].show_only_control_edges = False
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    bpy.ops.object.modifier_apply(modifier="Mirror")
    bpy.ops.object.modifier_apply( modifier="Lattice")
elif(version >= 2.8):
    bpy.context.view_layer.objects.active = bpy.data.objects['Cylinder.001']
    bpy.context.object.modifiers["Subdivision"].show_only_control_edges = False 
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")
else:
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
    


if(version >= 2.8):
    space_view_3d.shading.type = 'WIREFRAME'
else:
    #r bpy.data.objects['Lattice']
    scene.objects.active
    scene.objects.active = context.selected_objects[0]
    context.selected_objects[0]
    #r bpy.data.objects['Cylinder.001']

    #C:/D/SSPublic/Public_ImageNote/2016/int003503_capture_20160915_153641.jpg
    #set WIREFRAME mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.viewport_shade = 'WIREFRAME'
            break
           

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_210343.jpg
#the issue is that the Lattice is selected in the outliner , while I need to select the Cylinder001
#sol

#we need to be in edit mode solid
if(version >= 2.8):
    bpy.ops.object.mode_set(mode='EDIT')  #Edit mode
    space_view_3d.shading.type = 'SOLID'
    bpy.ops.mesh.select_mode(type="FACE")       #FACE Mode
    #en FACE mode - tu click avec ALT un edge de la FACE et ca te selectione tout le loop
    #which_face_selected()  257
    #select_faces(296)
else:
    #set SOLID  mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.viewport_shade = 'SOLID'
            break

#C:/D/SSPublic/Public_ImageNote/20240829_173300.jpg



obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)	#bmesh is a module : This module provides access to blenders bmesh data structures.
#from_edit_mesh Return a BMesh from this mesh, currently the mesh must already be in editmode.
#https://www.blender.org/api/blender_python_api_2_64_9/bmesh.types.html#module-bmesh.types
bm.faces.ensure_lookup_table()
if(version >= 2.8):
    faceSelectedR1 = [0, 2, 5, 12, 16, 18, 21, 28, 32, 34, 37, 44, 48, 50, 53, 60, 64, 66, 69, 76, 80, 82, 85, 92, 96, 98, 101, 108, 112, 114, 117, 124, 128, 130, 133, 140, 144, 146, 149, 156, 176, 178, 181, 188, 192, 194, 197, 204]
    for faceIndex in faceSelectedR1:
        #print(faceIndex)
        bm.faces[faceIndex].select = True
    faceSelectedR2 = [209, 211, 214, 219, 225, 227, 230, 235, 241, 243, 246, 251, 257, 259, 262, 267, 273, 275, 278, 283, 289, 291, 294, 299, 305, 307, 310, 315, 321, 323, 326, 331, 337, 339, 342, 347, 353, 355, 358, 363, 369, 371, 374, 379, 385, 387, 390, 395]
    for faceIndex in faceSelectedR2:
        #print(faceIndex)
        bm.faces[faceIndex].select = True
    #select all faces of Ring3
    faceSelectedR3 = [212, 221, 222, 223, 228, 237, 238, 239, 244, 253, 254, 255, 260, 269, 270, 271, 276, 285, 286, 287, 292, 301, 302, 303, 308, 317, 318, 319, 324, 333, 334, 335, 340, 349, 350, 351, 356, 365, 366, 367, 372, 381, 382, 383, 388, 397, 398, 399]
    for faceIndex in faceSelectedR3:
        #print(faceIndex)
        bm.faces[faceIndex].select = True
else:
    #select all faces of Ring1
    faceSelectedR1 = [1221, 1223, 1226, 1227, 1253, 1255, 1258, 1259, 1285, 1287, 1290, 1291, 1317, 1319, 1322, 1323, 1349, 1351, 1354, 1355, 1381, 1383, 1386, 1387, 1413, 1415, 1418, 1419, 1445, 1447, 1450, 1451, 1477, 1479, 1482, 1483, 1509, 1511, 1514, 1515, 1541, 1543, 1546, 1547, 1573, 1575, 1578, 1579]
    for faceIndex in faceSelectedR1:
     #print(faceIndex)
     bm.faces[faceIndex].select = True
    #select all faces of Ring2
    faceSelectedR2 =[208, 209, 220, 222, 224, 225, 236, 238, 240, 241, 252, 254, 256, 257, 268, 270, 272, 273, 284, 286, 288, 289, 300, 302, 304, 305, 316, 318, 320, 321, 332, 334, 336, 337, 348, 350, 352, 353, 364, 366, 368, 369, 380, 382, 384, 385, 396, 398]
    for faceIndex in faceSelectedR2:
     #print(faceIndex)
     bm.faces[faceIndex].select = True
    #select all faces of Ring3
    faceSelectedR3 =[0, 1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19, 28, 29, 30, 31, 32, 33, 34, 35, 44, 45, 46, 47, 48, 49, 50, 51, 60, 61, 62, 63, 64, 65, 66, 67, 76, 77, 78, 79, 80, 81, 82, 83, 92, 93, 94, 95, 96, 97, 98, 99, 108, 109, 110, 111, 112, 113, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 140, 141, 142, 143, 144, 145, 146, 147, 156, 157, 158, 159, 176, 177, 178, 179, 188, 189, 190, 191, 192, 193, 194, 195, 204, 205, 206, 207]
    for faceIndex in faceSelectedR3:
     #print(faceIndex)
     bm.faces[faceIndex].select = True

bmesh.update_edit_mesh(me, loop_triangles=True, destructive=True)


#Duplicate the 3 Rings
bpy.ops.mesh.duplicate_move()

#we scale now the 3 rings, to  make them bigger w.r.t to barrel
#scale shift-z on veut pas les agrandir en hauteur

if(version >= 2.8):
    bpy.ops.transform.resize(value=(1.05, 1.05, 1.05), constraint_axis=(True, True, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)
else:
    bpy.ops.transform.resize(value=(1.05, 1.05, 1.05), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    
#we need to have epaisseur of the ring

#separate  the 3 rings are separated and  put in Cylinder.002 just created
bpy.ops.mesh.separate();
list_all_mesh()


if(version >= 2.8):
    bpy.data.objects["Cylinder.002"].name= "Rings"
    bpy.data.objects["Cylinder.001"].select_set(False)
    bpy.data.objects["Rings"].select_set(True)
    bpy.context.scene.objects['Rings'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings']
else:
    #Rename cylinder.002 Rings
    bpy.data.objects["Cylinder.002"].name= "Rings"
    bpy.data.objects["Cylinder.001"].select= False
    bpy.data.objects["Rings"].select= True
    #select Rings in the outliner
    bpy.context.scene.objects['Cylinder.001'].select = False
    bpy.context.scene.objects['Rings'].select = True
    
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_211956.jpg
bpy.context.scene.objects['Rings'].type
#MESH
#display the object name in the 3D windows 
bpy.context.scene.objects['Rings'].show_name = True


#C:/D/SSPublic/Public_ImageNote/2016/int003521_capture_20160915_155614.jpg

bpy.ops.object.mode_set(mode='OBJECT')

if(version >= 2.8):
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings']
else:
    #active the object *** it will be selected in white in the outliner
    bpy.context.scene.objects.active = bpy.data.objects["Rings"]
    #C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_212130.jpg
    #ca me fait passer en object mode alors que j'etais en dot


#Edit mode
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
#Select all #AKey 
bpy.ops.mesh.select_all(action='SELECT')


#exclude and scale - 
#on donne une epaisseur au Rings

if(version >= 2.8):
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, True), "mirror":False,  "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
    scale_direction_x_and_y = (True, True, False)
    bpy.ops.transform.resize(value=(0.947585, 0.947585, 0.947585), constraint_axis=scale_direction_x_and_y, mirror=False,proportional_edit_falloff='SMOOTH', proportional_size=1)
else:
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False,  "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
    scale_direction_x_and_y = (True, True, False)
    bpy.ops.transform.resize(value=(0.947585, 0.947585, 0.947585), constraint_axis=scale_direction_x_and_y, constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


#Deselect all #AKey 
bpy.ops.mesh.select_all(action='DESELECT')
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_212303.jpg


#maintenant il faut separer les 3 rings video 17mn15

#on selectionne une face du ring et on appluie sur la touche L

obj = bpy.context.edit_object
mesh = obj.data
bm = bmesh.from_edit_mesh(mesh)	#bmesh is a module : This module provides access to blenders bmesh data structures.
bm.faces.ensure_lookup_table()

select_faces(faceSelectedR1[0])

#get the number of elements (face) of the rings
nbRingsCount = len(bm.faces)
print("number of face of the ring=",nbRingsCount)
#loop for all faces
for faceIndex in bm.faces:
 print(faceIndex)
#allow to simulate the L Key, but you have to select a face before
bpy.ops.mesh.select_linked()
#C:/D/SSPublic/Public_ImageNote/2016/int003563_capture_20160917_143458.jpg
#separate P_Key
bpy.ops.mesh.separate(type='SELECTED')   #ring 1 is created
#C:/D/SSPublic/Public_ImageNote/2016/int003572_capture_20160917_143524.jpg


#which face is selected?
counter,faceSelected = which_face_selected()
print("number of faces selected:",counter,faceSelected)
bm.faces.ensure_lookup_table()

#deselect the ring 1
bpy.ops.mesh.select_all(action='DESELECT')

#list of all object
list_all_object()

select_faces(faceSelectedR2[0])
#select ring 2
bpy.ops.mesh.select_linked()
bpy.ops.mesh.separate(type='SELECTED')  #ring 2 is created
#deselect the ring 2
bpy.ops.mesh.select_all(action='DESELECT')


bm.faces.ensure_lookup_table()

#select ring 3
select_faces(0)
bpy.ops.mesh.select_linked()
bpy.ops.mesh.separate(type='SELECTED')  #ring 3 is created
#deselect the ring 2
bpy.ops.mesh.select_all(action='DESELECT') 


if(version >= 2.8):
    bpy.data.collections['RingCollection'].hide_viewport = True
    bpy.data.collections[cylinder_collection.name].hide_viewport =  False
    bpy.context.view_layer.objects.active = bpy.data.objects['Cylinder']
    bpy.data.objects["Cylinder"].select_set(True)
else:
    #I suppress now the rings, since there is nothing more inside
    bpy.data.objects['Rings'].select = True
    #delete()#Delete the lattice
    #change layer come back to layer 0
    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = False
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = bpy.data.objects["Cylinder"]


#to apply modifier you need to be in object mode
#Select first cylinder and apply lattice then apply mirror
if(version >= 4.2):
    cmd_result = bpy.ops.object.modifier_apply( modifier="Lattice")
    cmd_result  = bpy.ops.object.modifier_apply( modifier="Mirror")
else:
    cmd_result = bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")
    cmd_result  = bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
print("cmd_result = %s\n" % (cmd_result))


#Delete the lattice object
deselect_all_object()
delete_obj_by_name('Lattice')



bpy.ops.object.mode_set(mode='EDIT')#Edit mode
#we separate the top face and the bottom face of the barrel and we  rename it
#we need first to deselect
bpy.ops.mesh.select_all(action='DESELECT')  #deselect all mesh
select_faces(61)  #top face
face_separate_and_rename("TopFace")
bpy.ops.mesh.select_all(action='DESELECT')  #deselect all mesh
select_faces(157)  #bottom face
face_separate_and_rename("BottomFace")



#decoupe le tonneau utile pour le uv projection
bpy.data.objects["Cylinder"].select_set(True)
bpy.ops.object.mode_set(mode='EDIT')#Edit mode
select_edges(164)  #un edge vertical
#which edge is selected?
(counter,edgeIndex,total_edges_count) = which_edge_selected()


#edge loop select
bpy.ops.mesh.loop_multi_select(ring=False)
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_213050.jpg

#control-E  -> we mark the stream in red (the privious vertical line of edge become red
bpy.ops.mesh.mark_seam()
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_213125.jpg

activeObj = get_active_obj() #get active  object 
activeObj.name
#r 'Cylinder'
#Donc pour faire la projection je crée 2  fenêtres
#Donc je découpe en deux verticalement mes fenêtres
split_area('VERTICAL','IMAGE_EDITOR','UV')

bpy.ops.mesh.select_all(action='DESELECT')  #deselect all mesh



def set_scene_active_obj(obj_name):
    if(version >= 2.8):
        bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    else:
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]


set_scene_active_obj('Cylinder')

bpy.ops.object.mode_set(mode='OBJECT')
if(version >= 2.8):
    bpy.context.scene.objects['Cylinder'].select_set(True)
    bpy.context.scene.objects['TopFace'].select_set(True)
    bpy.context.scene.objects['BottomFace'].select_set(True)
else:
    bpy.context.scene.objects['Cylinder'].select = True
    bpy.context.scene.objects['TopFace'].select = True
    bpy.context.scene.objects['BottomFace'].select = True

bpy.ops.object.join()

obj_cylinder =  bpy.context.scene.objects['Cylinder']
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')


#highlighted the full scene this is a tip this allow to not use lamp
#AttributeError: 'WorldLighting' object has no attribute 'use_ambient_occlusion'
if(version >= 4.2):
    world = bpy.context.scene.world
    # Désactiver l'occlusion ambiante
    world.cycles.ao_factor = 0
else:
    bpy.context.scene.world.light_settings.use_ambient_occlusion = False

'''
j utilise bien le render engine cycle
bpy.context.scene.render.engine
'CYCLES'
world = bpy.context.scene.world

# Désactiver l'occlusion ambiante
world.cycles.ao_factor = 0
'''

#show cursor  location
if(version >= 2.8):
    cursor = bpy.context.scene.cursor.location
else:
    cursor = bpy.context.scene.cursor_location

cursor
#r Vector((0.0, 0.0, 0.0))
#######################   Cylinder MATERIAL   ###########################

#Load a Texture image

filepath = os.environ['FOLDER_E']+"/E/Blend/TexturesCom_WoodPlanksClean0068_1_seamless_S.jpg"
img = bpy.data.images.load(filepath)
#use Cycle render
bpy.context.scene.render.engine = 'CYCLES'

#material creation
#we add a material named Earth2  C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_214745.jpg
mat_barrel_obj = add_material("mat_cylinder")


obj = bpy.context.object



#add a texture node
#http://blender.stackexchange.com/questions/5413/how-to-connect-nodes-to-node-group-inputs-and-outputs-in-python

#get the contect of NODE_EDITOR
for area in bpy.context.screen.areas:
    if area.type == "NODE_EDITOR":
        override = {'screen': bpy.context.screen, 'area': area}
#bpy.ops.node.select_all(override, action='DESELECT')

tree = obj_cylinder.active_material.node_tree
nodes = tree.nodes
links = tree.links
list(nodes)
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_215011.jpg
nodeTexture = nodes.new(type='ShaderNodeTexImage') 
nodeTexture.location = (100,0)
node_add = nodeTexture
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_215034.jpg
#C:/D/SSPublic/Public_ImageNote/2016/int003617_capture_20160918_183524.jpg
#nodeDiffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
#nodeDiffuse.location = (200,0)

 

#nodeMatOutput = nodes.new(type='ShaderNodeOutputMaterial')
#nodeMatOutput.location = (400,0)
#nodeMatOutput.name = 'MatMainOutput'
for node in nodes:
   print(node.name)
   
if(version >= 2.8):
    for node in nodes:
       if node.name == 'Principled BSDF':
          nodeDiffuse = node
else:
    for node in nodes:
       if node.name == 'Diffuse BSDF':
          nodeDiffuse = node

links.new(nodeTexture.outputs[0], nodeDiffuse.inputs[0])

#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_215155.jpg

#links.new(nodeDiffuse.outputs[0], nodeMatOutput.inputs[0])
#links.new(nodeTexture.outputs[0], nodeDiffuse.inputs[0])

nodeTexture.image = bpy.data.images['TexturesCom_WoodPlanksClean0068_1_seamless_S.jpg']
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_215322.jpg

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.unwrap(method='ANGLE_BASED',fill_holes=True, correct_aspect=True, use_subsurf_data=True, margin=0.001)


#C:/D/SSPublic/Public_ImageNote/2016/int003581_capture_20160917_150720.jpg
#C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190816_094140.jpg   not good projection
#bpy.ops.transform.rotate(value=-1.56876, axis=(-0, -0, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)



def rotate_uv(angle):
    screen = get_active_screen()
    window = get_active_window()
    for area in screen.areas:
      print(area.type)	 
      if area.type == 'IMAGE_EDITOR': 
        override = {'window': window, 'screen': screen, 'area': area}
        bpy.ops.uv.select_all(override,action='SELECT')
        bpy.ops.transform.rotate(override,value=radians(angle), orient_axis='Z', orient_type='VIEW', orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        

    

def get_active_screen():
    return bpy.context.window.screen
def get_active_window():
    return bpy.context.window
def rotate_uv3(angle):
    # Obtenez l'écran et la fenêtre actifs
    screen = get_active_screen()  #bpy.context.window.screen
    window = get_active_window()
    # Trouver l'IMAGE_EDITOR
    area_type = 'IMAGE_EDITOR'
    areas = [area for area in screen.areas if area.type == area_type]
    if not areas:
        print(f"Erreur : Aucun éditeur d'image trouvé dans l'écran actif.")
        return
    area = areas[0]
    # Trouver la région WINDOW dans l'IMAGE_EDITOR
    region = next((region for region in area.regions if region.type == 'WINDOW'), None)
    if not region:
        print(f"Erreur : Aucune région 'WINDOW' trouvée dans l'éditeur d'image.")
        return
    # Utiliser temp_override pour créer un contexte temporaire
    with bpy.context.temp_override(window=window, area=area, region=region):
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.transform.rotate(value=radians(angle))



if(version >= 4.2):
    rotate_uv3(90)
else:    
    rotate_uv(90)





bpy.ops.uv.select_all(action='DESELECT')
bpy.context.scene.tool_settings.uv_select_mode = 'EDGE'
#C:/D/SSPublic/Public_ImageNote/20240830_183354.jpg

def special(x,y):
    print(x)
    bpy.ops.uv.select(extend=False, location=(x,y))
    angle = uv_line()
    bpy.ops.uv.select_loop(extend=False, location=(x,y))
    if(angle > 60):
     bpy.ops.uv.align(axis='ALIGN_Y')
     print('ALIGN_Y')
    else:
     bpy.ops.uv.align(axis='ALIGN_X')
     print('ALIGN_X')

import numpy
if(version >= 4.2):
    pass
elif(version >= 2.8):
    for y in numpy.arange(0.0, 0.685, 0.01):
        special(0.058,y)
            
    for x in numpy.arange(0.0, 1.0, 0.01):
        special(x,0.346)        

    for y in numpy.arange(0.0, 0.685, 0.01):
        special(0.058,y)
            
    for x in numpy.arange(0.0, 1.0, 0.01):
        special(x,0.346)        
else:
    #I separated the barrel in 3 part : top,body,and bottom, but I canno't project uv for the 3 part, 
    #I can only do it for one object
    #so how to select several objects?
    #bpy.ops.uv.export_layout(filepath="E:\\E\\Blend\\Python\\barrel.png", size=(1024, 1024))
    bpy.ops.uv.select_all(action='DESELECT')
    #Loop Select  in uv  - alt + mouse  right click
    bpy.ops.uv.select_loop(extend=False, location=(0.03, 0.36))
    #C:/D/SSPublic/Public_ImageNote/2016/int003590_capture_20160917_150824.jpg
    #so you need to give the mouse position in normalised format, to get the position on the vertex, you can 
    #change the cursor position Left click
    #bpy.ops.utnv.cursor_set(location=(0.0116882, 0.010138))
    #the bottom left corner is the coor (0;0)   top right corner is (1;1)
    #to get the cursor position: n to open the info window; check la case Normalised
    #C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_213954.jpg
    #in uv alt-clik to select several vertice, then align them horizontaly
    #C:/D/SSPublic/Public_ImageNote/2016/int003599_capture_20160917_150946.jpg
    bpy.context.scene.tool_settings.uv_select_mode = 'EDGE'
    #C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190815_214304.jpg
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.113, 0.172))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.086, 0.264))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.066, 0.447))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.102,0.549))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.145,0.627))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.474,0.646))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.5,0.606))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.473,0.565))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.550))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.548))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.155))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.177))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.118))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.177))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.118))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.171))
    bpy.ops.uv.align(axis='ALIGN_Y')

    bpy.ops.uv.select_loop(extend=False, location=(0.475,0.121))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.197,0.022))
    bpy.ops.uv.align(axis='ALIGN_Y')
    bpy.ops.uv.select_loop(extend=False, location=(0.005,0.398))
    bpy.ops.uv.align(axis='ALIGN_X')
    bpy.ops.uv.select_loop(extend=False, location=(0.119,0.398))
    bpy.ops.uv.align(axis='ALIGN_X')
    bpy.ops.uv.select_loop(extend=False, location=(0.217,0.398))
    bpy.ops.uv.align(axis='ALIGN_X')
    bpy.ops.uv.select_loop(extend=False, location=(0.296,0.398))
    bpy.ops.uv.align(axis='ALIGN_X')

    bpy.ops.uv.select_loop(extend=False, location=(0.365,0.398))
    bpy.ops.uv.align(axis='ALIGN_X')

    bpy.ops.uv.select(extend=False, location=(0.365/20,0.398))
    angle = uv_line()

    for x in range(1, 15, 1): 
        print(x)
        bpy.ops.uv.select(extend=False, location=(0.365+x/20,0.398))
        angle = uv_line()
        bpy.ops.uv.select_loop(extend=False, location=(0.365+x/20,0.398))
        if(angle > 60):
         bpy.ops.uv.align(axis='ALIGN_Y')
         print('ALIGN_Y')
        else:
         bpy.ops.uv.align(axis='ALIGN_X')
         print('ALIGN_X')
    
#C:/D/SSPublic/Public_ImageNote/2016/int003608_capture_20160918_183139.jpg

if(version >= 2.8):
    space_view_3d.shading.type = 'WIREFRAME'
    space_view_3d.shading.type = 'MATERIAL'
    space_view_3d.shading.type = 'SOLID'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.shading.type = 'MATERIAL'
            break
else:
    #set TEXTURED mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            space_data.viewport_shade
            space_data.viewport_shade = 'TEXTURED'
            break
#replace IMAGE_EDITOR window by  NODE_EDITOR window
for window in bpy.context.window_manager.windows:
 screen = window.screen
for area in screen.areas:
  if area.type == 'IMAGE_EDITOR':
    area.type = "NODE_EDITOR"


#code not really used 
if(version < 2.8):
    nodeSelect() #does not work from file but works from cmd line!!!!
    #desactive the link
    #nodes[0].inputs[0].links[0].is_valid = False
    for node in nodes:
     node.name
     node.type
     node.select

    for node in nodes:
     node.select = False
     if node.type == 'OUTPUT_MATERIAL':
       if node.name == 'Material Output':
        node.select = True
    print('override',override)

    try:
        bpy.ops.node.delete(override)  #this functio does not work from file but from console still do not understand why
    except:
        print('bpy.ops.node.delete(override) to be executed by hand')
        pass

#change active layer 
if(version >= 2.8):   
    bpy.data.collections['RingCollection'].hide_viewport = False
    bpy.data.collections[cylinder_collection.name].hide_viewport =  True
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
    bpy.data.objects["Rings.001"].select_set(True)
else:
    bpy.context.scene.layers[1] = True
    bpy.context.scene.layers[0] = False
    bpy.ops.object.mode_set(mode='OBJECT')
    
## collection cylinder_ring_collection
    
if(version >= 2.8):
    bpy.context.scene.objects['Rings.002'].select_set(True)
    bpy.context.scene.objects['Rings.003'].select_set(True)
    bpy.context.scene.objects['Rings.001'].select_set(True)
    bpy.ops.object.join()
    bpy.data.objects['Cylinder'].select_set(False)
    bpy.context.scene.objects['Cylinder'].select_set(False)
    bpy.context.scene.objects['Rings.001'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
    #move "Rings" to Main collection
    ring_obj  = bpy.data.objects["Rings.001"]
    cylinder_ring_collection =  make_collection("RingCollection", ring_obj)
    cylinder_ring_collection.objects.unlink(ring_obj)  # put the cube in the new collection
    cylinder_collection.objects.link(ring_obj)  # remove it from the old collection
    #Acticve main collectiob
    bpy.data.collections['RingCollection'].hide_viewport = True
    bpy.data.collections[cylinder_collection.name].hide_viewport =  False
    bpy.context.scene.objects['Rings.001'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
else:
    bpy.data.objects['Rings.001'].select = True
    #move "Rings" to layer 1
    bpy.ops.object.move_to_layer(layers=layer1)
    #change active layer => Back to main layer
    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = False
    bpy.ops.object.mode_set(mode='OBJECT')
    #deselect all obj of the scene
    for obj in bpy.context.scene.objects:
     obj.name
     bpy.context.scene.objects[obj.name].select = False
     bpy.data.objects[obj.name].select = False  
    #Join the 3 rings in Rings.001
    bpy.context.scene.objects['Rings.002'].select = True
    bpy.context.scene.objects['Rings.003'].select = True
    bpy.context.scene.objects['Rings.001'].select = True
    bpy.data.objects['Rings.002'].select = True
    bpy.data.objects['Rings.003'].select = True
    bpy.data.objects['Rings.001'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Rings.001']
    bpy.ops.object.join()
    bpy.data.objects['Cylinder'].select = False
    bpy.context.scene.objects['Cylinder'].select = False
    bpy.context.scene.objects['Rings.001'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Rings.001']

#######################   RING MATERIAL   ###########################

obj = bpy.context.object
print(obj.name)
mat = bpy.data.materials.new("MatRings")
mat.use_nodes = True
obj.data.materials.append(mat)

tree = bpy.context.object.active_material.node_tree
nodes = tree.nodes
links = tree.links
list(nodes)

nodeTexture = nodes.new(type='ShaderNodeTexImage')
nodeTexture.location = (100,0)


for node in nodes:
   print(node.name)
   
if(version >= 2.8):
    for node in nodes:
       if node.name == 'Principled BSDF':
          nodeDiffuse = node
else:
    for node in nodes:
       if node.name == 'Diffuse BSDF':
          nodeDiffuse = node
links.new(nodeTexture.outputs[0], nodeDiffuse.inputs[0])


#Load a background image

filepath = os.environ['FOLDER_E']+"/E/Blend/texture_metal.jpg"
img = bpy.data.images.load(filepath)
super_dir(img,'img')

nodeTexture.image = bpy.data.images['texture_metal.jpg']



#######################   CAMERA   ###########################
camera_obj  = get_obj_by_name('Camera')
show_obj_position_rotation_scale(camera_obj)
current_obj = camera_obj
current_obj.location= Vector((46.38999938964844,-4.260000228881836,27.420000076293945))
current_obj.rotation_euler  =Euler ((1.1110643148422241,-0.04154288023710251,1.3769240379333496))

if False:
    #place the camera at the right location
    for obj in bpy.data.objects:
      print(obj.name)
      #print(obj.location)
      if obj.name == 'Camera':
       print(obj.location)
       obj.location.y =  -4.9200
       obj.location.x = 27.5500   
       obj.location.z = 15.0900
       obj.rotation_euler=Euler((1.0988470315933228, 0.023034295067191124, 1.396122694015503), 'XYZ')


#deselect all obj of the scene and delete the Rings
if(version >= 2.8):
    deselect_all_object()
    for obj in bpy.context.scene.objects:
     obj.name
     bpy.context.scene.objects[obj.name].select_set(False)
     
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings']
    bpy.context.scene.objects['Rings'].select_set(True)
    delete()	 #delete  object selected
else:
    for obj in bpy.context.scene.objects:
     obj.name
     bpy.context.scene.objects[obj.name].select = False  
    bpy.context.scene.objects.active = bpy.data.objects['Rings']
    bpy.context.scene.objects['Rings'].select = True
    delete()	 #delete  object selected


#replace NODE_EDITOR  window by  IMAGE_EDITOR window
for window in bpy.context.window_manager.windows:
 screen = window.screen
 
for area in screen.areas:
  if area.type == 'NODE_EDITOR':
    area.type = "IMAGE_EDITOR"



if(version >= 2.8):
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
    bpy.context.scene.objects['Rings.001'].select_set(True)
    bpy.context.scene.objects['Cylinder'].select_set(False)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')    
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=1.0, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)
else:
    bpy.context.scene.objects.active = bpy.data.objects['Rings.001']
    bpy.context.scene.objects['Rings.001'].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=1.0, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)


def resize(valuei):
    # Obtenez l'écran et la fenêtre actifs
    screen = get_active_screen()  #bpy.context.window.screen
    window = get_active_window()
    # Trouver l'IMAGE_EDITOR
    area_type = 'IMAGE_EDITOR'
    areas = [area for area in screen.areas if area.type == area_type]
    if not areas:
        print(f"Erreur : Aucun éditeur d'image trouvé dans l'écran actif.")
        return
    area = areas[0]
    # Trouver la région WINDOW dans l'IMAGE_EDITOR
    region = next((region for region in area.regions if region.type == 'WINDOW'), None)
    if not region:
        print(f"Erreur : Aucune région 'WINDOW' trouvée dans l'éditeur d'image.")
        return
    # Utiliser temp_override pour créer un contexte temporaire
    with bpy.context.temp_override(window=window, area=area, region=region):
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.transform.resize(value=valuei, proportional_edit_falloff='SMOOTH', proportional_size=1)
        
if(version >= 4.2):
    resize((0.765252, 0.765252, 0.765252))

elif(version >= 2.8):
    for window in bpy.context.window_manager.windows:
     screen = window.screen
    print("execute B")   
    for area in screen.areas:
      print(area.type)	 
      if area.type == 'IMAGE_EDITOR': 
        override = {'window': window, 'screen': screen, 'area': area}
        bpy.ops.uv.select_all(override,action='SELECT')
        bpy.ops.transform.resize(override,value=(0.765252, 0.765252, 0.765252), proportional_edit_falloff='SMOOTH', proportional_size=1)




#Add the loaded image in the VIEW_3D context
for area in bpy.context.screen.areas:
 if area.type == 'VIEW_3D':
  bpy.ops.mesh.select_all(action='DESELECT')  #AKey : deselect all
  break
#Tu dois effacer la collection  non d'utilisee

super_dir(cylinder_ring_collection,'cylinder_ring_collection')
super_dir(bpy.data.collections,'bpy.data.collections',is_debug = False)
#delete collection ring
r = bpy.data.collections.remove(cylinder_ring_collection)
print(r)
#result = r.pop()
#if result != 'FINISHED':
#    print("error")



### Preparation du Sol
#


deselect_all_object()
switch_to_3d_view()
plane_obj  =get_obj_by_name('Plane')
show_obj_position_rotation_scale(plane_obj)
bpy.context.scene.objects['Plane'].select_set(True)
bpy.ops.object.mode_set(mode='OBJECT')

if(version >= 4.2):
       bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
 
else:
    (override_VIEW_3D,override_OUTLINER) = get_override()
    bpy.ops.object.origin_set(override_VIEW_3D,type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')


for window in bpy.context.window_manager.windows:
    screen = window.screen
    print("screen: %s" % (screen.name))   #Layout
    
for screen in bpy.data.screens:
    print("split_area screen",screen.name)

#allow to remove the collection by using info
is_info = False
if is_info:
    (override_VIEW_3D,override_OUTLINER) = get_override()#
    bpy.ops.outliner.collection_delete(override_OUTLINER,hierarchy=False) #False enleve la collection mais met les objects dans la collection principale

if(version >= 2.8):
    bpy.context.scene.objects['Rings.001'].select_set(False)
    bpy.context.scene.objects['Plane'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Plane']
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False),  mirror=False,  proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.translate(value=(-16, 0, 0), constraint_axis=(True, False, False),  mirror=False,  proportional_edit_falloff='SMOOTH', proportional_size=1)

else:
    bpy.context.scene.objects['Rings.001'].select = False
    bpy.context.scene.objects['Plane'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Plane']
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.translate(value=(-16, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

def move_obj_z(obj_name,z,is_debug = False):
    for obj in bpy.data.objects:
      if is_debug:print(obj.name)
      if obj.name == obj_name:
        if is_debug:print(obj.location)
        obj.location.z = z

#place the Plane  at the right location
move_obj_z('Plane',-4.68)

print(GL.is_debug)



obj = bpy.context.object
print(obj.name)
mat = bpy.data.materials.new("MatRings")
mat.use_nodes = True
obj.data.materials.append(mat)

tree = bpy.context.object.active_material.node_tree
nodes = tree.nodes
links = tree.links
list(nodes)

nodeTexture = nodes.new(type='ShaderNodeTexImage')
nodeTexture.location = (100,0)


for node in nodes:
   print(node.name)
   
if(version >= 2.8):
    for node in nodes:
       if node.name == 'Principled BSDF':
          nodeDiffuse = node
else:
    for node in nodes:
       if node.name == 'Diffuse BSDF':
          nodeDiffuse = node
links.new(nodeTexture.outputs[0], nodeDiffuse.inputs[0])


#Load  pave_de_paris  image
filepath = os.environ['FOLDER_E']+"/E/Blend/Texture/pave_de_paris.jpg"
img = bpy.data.images.load(filepath)

nodeTexture.image = bpy.data.images['pave_de_paris.jpg']
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.cube_project(cube_size=1.0, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)

bpy.ops.object.mode_set(mode='OBJECT')

if(version >= 4.2):
    for obj in bpy.context.scene.objects:
         obj.name
         bpy.context.scene.objects[obj.name].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
    bpy.data.objects["Rings.001"].select_set(True)    
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["Mirror"].use_axis[0] = False
    bpy.context.object.modifiers["Mirror"].use_axis[1] = False
    bpy.context.object.modifiers["Mirror"].use_axis[2] = True
    bpy.ops.object.modifier_apply( modifier="Mirror")
    bpy.ops.object.mode_set(mode='OBJECT')    
    bpy.context.view_layer.objects.active = bpy.data.objects['Cylinder']
    bpy.data.objects["Cylinder"].select_set(True)
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    bpy.data.objects["Rings.001"].select_set(True)    
    bpy.ops.object.join()
elif(version >= 2.8):
    for obj in bpy.context.scene.objects:
         obj.name
         bpy.context.scene.objects[obj.name].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects['Rings.001']
    bpy.data.objects["Rings.001"].select_set(True)    
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["Mirror"].use_axis[0] = False
    bpy.context.object.modifiers["Mirror"].use_axis[1] = False
    bpy.context.object.modifiers["Mirror"].use_axis[2] = True
    bpy.ops.object.modifier_apply( modifier="Mirror")
    bpy.ops.object.mode_set(mode='OBJECT')    
    bpy.context.view_layer.objects.active = bpy.data.objects['Cylinder']
    bpy.data.objects["Cylinder"].select_set(True)
    bpy.ops.object.modifier_apply( modifier="Subsurf")
    bpy.data.objects["Rings.001"].select_set(True)    
    bpy.ops.object.join()
else:    
    #deselect all obj of the scene and delete the Rings
    for obj in bpy.context.scene.objects:
     obj.name
     bpy.context.scene.objects[obj.name].select = False  
    #change active layer 
    bpy.context.scene.layers[0] = False
    bpy.context.scene.layers[1] = True
    for obj in bpy.context.scene.objects:
     obj.name
     bpy.context.scene.objects[obj.name].select = False  

    bpy.context.scene.objects.active = bpy.data.objects['Cylinder.001']
    bpy.context.scene.objects['Cylinder'].select = True
    delete() #delete  object selected

    #change active layer 
    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = False
    bpy.context.scene.objects.active = bpy.data.objects['Rings.001']
    bpy.context.scene.objects['Rings.001'].select = True
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
    bpy.context.scene.objects['Rings.001'].select = False
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects['Cylinder'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Cylinder']
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
    bpy.context.scene.objects['Rings.001'].select = True
    bpy.ops.object.join()

if(version >= 4.2):
       bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
else:
    bpy.ops.object.origin_set(override_VIEW_3D,type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(-10, 0, 0)}) # "Cylinder.001" is created
bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(-10, 10, 0)}) # "Cylinder.002" is created
bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(-10, -10, 0)}) # "Cylinder.003" is created
bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(-5, -5, 0)}) # "Cylinder.004" is created


#place the barrels at the right location
for obj in bpy.data.objects:
  print(obj.name)
  #print(obj.location)
  if obj.name == 'Cylinder':
   print(obj.location)
   obj.location.x = 0
   obj.location.y =  0
   obj.location.z = 0
   obj.rotation_euler=Euler((0,0,0), 'XYZ')
  if obj.name == 'Cylinder.001':
   print(obj.location)
   obj.location.x = -10.0
   obj.location.y =  0
   obj.location.z = 0
   obj.rotation_euler=Euler((0,0,0), 'XYZ')
  if obj.name == 'Cylinder.002':
   print(obj.location)
   obj.location = (-18.9856, 12.9712, -1.0077)
   obj.rotation_euler=Euler((1.5040, -0.5984, 0.0963), 'XYZ')
  if obj.name == 'Cylinder.003':
   print(obj.location)
   obj.location =  (1.9410, 13.0066, 0.0000)
   obj.rotation_euler=Euler((0.0000, 0.0000, 0.0000), 'XYZ')
  if obj.name == 'Cylinder.004':
   print(obj.location)
   obj.location =  (-2.5880, -11.2192, 0.0000)
   obj.rotation_euler=Euler((0.0000, 0.0000, 0.0000), 'XYZ')

if(version >= 2.8):
    for obj in bpy.context.scene.objects:
         obj.name
         bpy.context.scene.objects[obj.name].select_set(False)
    #plane for Pave et on le decoupe en 25 per 25 face
    bpy.context.scene.objects['Plane'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Plane']
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=25)
else:
    #plane for Pave et on le decoupe en 25 per 25 face
    bpy.context.scene.objects['Plane'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Plane']
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=25)
    #C:/D/SSPublic/Public_ImageNote/2019/RN006562_capture_20190816_112125.jpg

#add modifier SUBSURF =>allows to subdivide the faces

bpy.ops.object.modifier_add(type='SUBSURF')

if(version >= 2.8):
    bpy.context.object.modifiers["Subdivision"].levels = 2
    bpy.context.object.modifiers["Subdivision"].render_levels = 4

else:
	bpy.context.object.modifiers["Subsurf"].levels = 3


##########################  STOPPED HERE  = you can render   ########################## 


#ensuite tu dois faire les paves avec de la hauteur .... a finir
################    DISPLACE   ############
bpy.ops.object.modifier_add(type='DISPLACE')
displace_obj  = bpy.context.object.modifiers["Displace"]
super_dir(displace_obj,"displace_obj")

bpy.context.object.modifiers["Displace"].strength = 0.4
bpy.data.objects['Plane'].modifiers["Displace"]
bpy.ops.texture.new()
bpy.ops.texture.new()
bpy.data.objects['Plane'].modifiers["Displace"].texture = bpy.data.textures['Texture.001']
bpy.data.textures["Texture.001"].type = 'IMAGE'
texture_obj =  bpy.data.textures['Texture.001']
texture_obj.image = bpy.data.images['pave_de_paris.jpg']
super_dir(texture_obj,"texture_obj")


mat_wine = add_material("Wine2",plane_wine_obj)
tree = plane_wine_obj.active_material.node_tree
nodes = tree.nodes
links = tree.links
nodeGlossy = nodes.new(type='ShaderNodeBsdfGlossy') 
nodeGlossy.location = (100,0)
nodeGlossy.inputs['Roughness'].default_value = 0.228
nodeGlossy.distribution  = 'BECKMANN'
nodeGlossy.inputs['Color'].default_value = (0.8000000715255737, 0.0088645713403821, 0.025358285754919052, 1.0)
for node in nodes:
   print(node.name)
   if node.name == 'Material Output':
      nodeDiffuse = node
links.new(nodeGlossy.outputs[0], nodeDiffuse.inputs[0])


#place the plane_wine_obj  at the right location
plane_wine_obj.location.z = -4.68
plane_wine_obj.location= Vector((-18.795475006103516,8.64976978302002,-4.665816307067871))
plane_wine_obj.rotation_euler  =Euler ((0.0,0.0,0.0))
plane_wine_obj.scale= Vector((1.0,1.0,1.0))




if(version >= 2.8):
    bpy.context.scene.objects['Plane'].select_set(False)
    bpy.context.scene.objects['Plane.001'].select_set(True)
    plane_water_object = bpy.data.objects['Plane.001']
    plane_water_object.name = 'Plane_Water'
    bpy.context.view_layer.objects.active = plane_water_object
    obj = bpy.context.object
    print(obj.name)
    mat = bpy.data.materials.new("Wine")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    tree = bpy.context.object.active_material.node_tree
    nodes = tree.nodes
    links = tree.links
    nodeGlossy = nodes.new(type='ShaderNodeBsdfGlossy') 
    nodeGlossy.location = (100,0)
    nodeGlossy.inputs['Roughness'].default_value = 0.228
    nodeGlossy.distribution  = 'BECKMANN'
    nodeGlossy.inputs['Color'].default_value = (0.8000000715255737, 0.0088645713403821, 0.025358285754919052, 1.0)
    node_add = nodeGlossy
    for node in nodes:
       print(node.name)
       if node.name == 'Material Output':
          nodeDiffuse = node
    links.new(nodeGlossy.outputs[0], nodeDiffuse.inputs[0])
    
else:
    bpy.context.scene.objects['Plane'].select = False
    bpy.context.scene.objects['Plane_Water'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Plane_Water']
    obj = bpy.context.object
    print(obj.name)
    mat = bpy.data.materials.new("Wine")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    tree = bpy.context.object.active_material.node_tree
    nodes = tree.nodes
    links = tree.links
    nodeGlossy = nodes.new(type='ShaderNodeBsdfGlossy') 
    nodeGlossy.location = (100,0)
    nodeGlossy.inputs['Roughness'].default_value = 0.228
    nodeGlossy.distribution  = 'BECKMANN'
    nodeGlossy.inputs['Color'].default_value = (0.8000000715255737, 0.0088645713403821, 0.025358285754919052, 1.0)
    node_add = nodeGlossy
    for node in nodes:
       print(node.name)
       if node.name == 'Material Output':
          nodeDiffuse = node
    links.new(nodeGlossy.outputs[0], nodeDiffuse.inputs[0])



bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.scene.objects['Plane'].select_set(True)
bpy.context.scene.objects['Plane_Water'].select_set(False)
bpy.context.view_layer.objects.active = bpy.data.objects['Plane']
bpy.ops.object.mode_set(mode='OBJECT')
if(version >= 4.2):
       bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
else:
    bpy.ops.object.origin_set(override_VIEW_3D,type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')



bpy.ops.transform.resize(value=(1.75484, 1.75484, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
if(version >= 4.2):
       bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
       set_top_view_in_view_3d('FRONT')
else:
    bpy.ops.object.origin_set(override_VIEW_3D,type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    #set the front view
    bpy.ops.view3d.view_camera(override_VIEW_3D)





#light 
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 4.2

obj_wine = bpy.data.materials['Wine']
super_dir(obj_wine,"obj_wine")
bpy.data.materials["Wine"].node_tree.nodes["Glossy BSDF"].inputs[1].default_value = 0.25
bpy.data.materials["Wine"].node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (0.0051008, 0.568621, 0.8, 1)

show_obj_position_rotation_scale(plane_water_object)
current_obj  = plane_water_object
current_obj.location= Vector((-14.290985107421875,-2.0672423488576896e-06,-4.733720302581787))
current_obj.rotation_euler  =Euler ((0.0,0.0,0.0))
current_obj.scale= Vector((8.057737350463867,8.057737350463867,1.1677768230438232))
deselect_all_object()
set_active_obj(plane_wine_obj)
plane_wine_obj.select_set(True)



bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0, 0, 1)}) # "Cylinder.001" is created
#Exclude profondeur en descendant on z

bpy.ops.object.mode_set(mode='EDIT')  #Edit mode
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.3), "constraint_axis":(False, False, True), "mirror":False,  "proportional_edit_falloff":'SMOOTH'})
obj = bpy.context.active_object
obj.name = "Triangle_Wine"
triangle_wine_obj = obj

mesh_data = triangle_wine_obj.data
vertices = mesh_data.vertices
list(vertices)


def add_plane(plane_name, my_size = 10, my_location = (0, 0, 0)):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_plane_add(size = my_size, location= my_location)
    obj = bpy.context.active_object
    obj.name = plane_name
    return(obj)

#Triangle creation
plane_test_obj  =add_plane("test_plane")

deselect_all_object()
set_active_obj(plane_test_obj)
bpy.ops.object.mode_set(mode='EDIT')  #Edit mode
mesh_data = plane_test_obj.data
vertices = mesh_data.vertices
edges = mesh_data.edges
list(vertices)
len(vertices)  #4
bpy.ops.mesh.select_all(action='DESELECT')
select_edges(0)
bpy.ops.mesh.merge(type='CENTER')




dddd
exec(compile(open( "C:\E\Blend\Python\ss_launch2.py").read(), "C:\E\Blend\Python\ss_launch2.py", 'exec'))
exec(compile(open( r"C:\E\Blend\Python\barrel.py").read(), r"C:\E\Blend\Python\barrel.py", 'exec'))

'''
C:/D/SSPublic/Public_ImageNote/20240830_210900.jpg
a partir d ici je fais render de l image ce qui prend 5mn
voici le resultat du render
'''
for i in range(1,3):
    print(i)
    select_Vertices(i)



##########################  STOPPED HERE    ########################## 


#list all materials
list(bpy.data.materials)
#[bpy.data.materials['Dots Stroke'], bpy.data.materials['mat_cylinder'], bpy.data.materials['Material'], bpy.data.materials['MatRings'], bpy.data.materials['MatRings.001'], bpy.data.materials['Wine'], bpy.data.materials['Wine2']]
for mat in bpy.data.materials:
 print(mat.name)

'''

[bpy.data.materials['Dots Stroke'], bpy.data.materials['mat_cylinder'], bpy.data.materials['Material'], bpy.data.materials['MatRings'], bpy.data.materials['MatRings.001'], bpy.data.materials['Wine'], bpy.data.materials['Wine2']]

Dots Stroke
mat_cylinder
Material
MatRings
MatRings.001
Wine
Wine2

'''
'''
for mat in bpy.data.materials:
 print(mat.name)
 print(mat.type)

'''
super_dir('mat')
#bpy.ops.view3d.viewnumpad(override, type = 'FRONT')





#for the object selected, list all node of the active material
tree = bpy.context.object.active_material.node_tree
nodes = tree.nodes
links = tree.links
list(nodes)


for node in nodes:
 node.name
 node.type
 node.select

super_dir(node,'node')


r = node.inputs['Roughness']
print(r.default_value)

r = node.inputs['Color'].default_value
list(r)

#r[0.8000000715255737, 0.0088645713403821, 0.025358285754919052, 1.0]
red = r[0]
g = r[1]
b = r[2]

for obj in bpy.data.objects:
  print(obj.name)
  print(obj.location)
  print(obj.rotation_euler)



for node in nodes:
 node
 node.name
 list(node.inputs)
 print('links=',node.inputs[0].links)
# links.remove(node.inputs[0].links)



#get the contect of NODE_EDITOR
for area in bpy.context.screen.areas:
    if area.type == "NODE_EDITOR":
        override = {'screen': bpy.context.screen, 'area': area}
bpy.ops.node.add_node(override,type="ShaderNodeTexImage", use_transform=True)

dddd
root_folder = 'C:/E/Blend/'
is_debug = False
filename = root_folder+'/Python/barrel.py'
exec(compile(open(filename).read(), filename, 'exec'))

#save the context
context_save = bpy.context.area.type

#change context 
bpy.context.area.type = "NODE_EDITOR"
bpy.ops.node.add_node(type="ShaderNodeTexImage", use_transform=True)

#restore the context
bpy.context.area.type = context_save


#save the context
context_save = bpy.context.area.type

#change context 
bpy.context.area.type = "VIEW_3D"
bpy.context.area.type = "CONSOLE"
bpy.context.area.type = "IMAGE_EDITOR"
bpy.context.area.type = "NODE_EDITOR"
bpy.context.area.type = "SEQUENCE_EDITOR"

for area in bpy.context.screen.areas:
 print(area.type)

#restore the context
bpy.context.area.type = context_save




#pointer de fonction
cube_obj = bpy.ops.mesh.primitive_cube_add
x=0
y=0
z=0
cube_obj(location=(x,y,z))


for area in bpy.context.screen.areas:
 print(area.type)
 if area.type == 'VIEW_3D':
  print('VIEW_3D')
 elif  area.type == 'PROPERTIES':
  print('PROPERTIES');
  space_data = area.spaces.active
  xx = space_data.context = 'MATERIAL'
  bpy.ops.material.new()
  dir(space_data)



bpy.ops.material.new()
bpy.ops.objects["Cylinder"].active_material_index

list(bpy.ops.objects)
bpy.data.node_groups["Shader Nodetree"].nodes["Diffuse BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
bpy.ops.object.material_slot_assign()
bpy.ops.object.editmode_toggle()
bpy.context.space_data.viewport_shade = 'TEXTURED'

bpy.data.materials['Material.001'].name
bpy.data.materials['Material.001'].active_node_material

#list all materials
list(bpy.data.materials)
#r bpy.data.materials['Earth'], bpy.data.materials['Earth.001'], bpy.data.materials['Earth2'], bpy.data.materials['Material']]

#accés au material par son nom
mat = bpy.data.materials['Earth2']

#si un object a plusieurs materials, on seltection le material grace a l'index
object = bpy.context.object
object.active_material_index 
object.active_material_index = 1

#access au material actif
active_material = object.active_material

#list all textures
list(bpy.data.textures)

bpy.data.meshes['Cylinder']



bpy.ops.object.particle_system_add()

##downloaded Texture tonneau woodplanksbare0138   http://www.textures.com/download/woodplanksbare0138/34735

#bpy.ops.mesh.mark_seam()
#bpy.context.object.data.type = 'SUN'


#To delete an object you have to select it first and to run the delete command but you can fail if there are dependency

is_enabled = False

if is_enabled:
 bpy.data.objects['Cylinder'].select = True
 bpy.data.objects['Cylinder.001'].select = True
 bpy.data.objects['Lattice'].select = True
 bpy.data.objects['Rings'].select = True
 delete()	 #delete  object selected

#outliner
bpy.ops.outliner.show_active()
#=> got error message context is not active


for area in bpy.context.screen.areas:
    if  area.type == 'OUTLINER':
     print('OUTLINER');
     print(area)
     my_area = area
     bpy.ops.outliner.object_operation(type='DELETE');
#access object in outliner:
list(bpy.context.scene.objects)

bpy.context.scene.objects['Lattice'].select = True
bpy.ops.outliner.object_operation(type='DELETE');


#get the parent of an object
bpy.data.objects["Cube"].parent


#if there is dependency, the delete does not work
for obj in bpy.data.objects:
  print(obj.name)
  if(obj.name == "Lattice"):
   obj.select = True
   bpy.ops.object.delete(use_global=True)
   

#list scene object
scene_current = bpy.data.scenes[0]
list(scene_current.objects)
for obj in scene_current.objects:
 print(obj.name)

obj_Lamp = scene_current.objects['Lamp']


list_all_object()

#list all mesh object
for item in bpy.data.objects:
 if item.type == "MESH":
     print(item.name)


#rename mesh
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
     print(obj.name)



#list all mesh 
for item in bpy.data.meshes:
     print(item.name)
obj= bpy.data.meshes['Cylinder']

#active the object Lamp and put SUN for the lamp ***
bpy.context.scene.objects.active = bpy.data.objects["Lamp"]
bpy.context.object.data.type  = 'SUN'



#list all windows area
for area in bpy.context.screen.areas:
    print(area.type)


#work set the 3D window in full

def scale_uv():
 print("execute A")
 for window in bpy.context.window_manager.windows:
    screen = window.screen
 print("execute B")   
 for area in screen.areas:
  print(area.type)	 
  if area.type == 'IMAGE_EDITOR': 
    override = {'window': window, 'screen': screen, 'area': area}
    #bpy.ops.screen.screen_full_area(override)
    bpy.ops.mesh.loop_multi_select(override,ring=False)
    #bpy.ops.uv.select_linked()
    print("execute C")
    #bpy.ops.transform.resize(override,value=(1.32406, 1.32406, 1.32406), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
 return
 
scale_uv()
 
bpy.context.scene.tool_settings.proportional_edit_falloff = 'LINEAR'

#in uv alt-click to select several vertice, then align them horizontaly
bpy.ops.uv.align(axis='ALIGN_Y')
#in uv alt-clik to select several vertice, then align them verticaly
bpy.ops.uv.align(axis='ALIGN_X')


for loop_index in selected_loops:
    selected_vertices.add(mesh.loops[loop_index].vertex_index)

for vertex_index in selected_vertices:
    print(mesh.vertices[vertex_index].co)

print('*' * 20)

# Restore whatever mode the object is in previously
bpy.ops.object.mode_set(mode=prev_mode)


prev_mode = bpy.context.object.mode
bpy.ops.object.mode_set(mode='OBJECT')
for index, uv_loop in enumerate(uv_map.data):
    uv_loop.select = True
bpy.ops.object.mode_set(mode=prev_mode)

for loop in bpy.data.loops :
    uv_coords = bpy.data.uv_layers.active.data[loop.index].uv
    print(uv_coords)

dddd
exec(compile(open( "C:\E\Blend\Python\ss_launch2.py").read(), "C:\E\Blend\Python\ss_launch2.py", 'exec'))
exec(compile(open( r"C:\E\Blend\Python\barrel.py").read(), r"C:\E\Blend\Python\barrel.py", 'exec'))
dddd
root_folder = 'C:/E/Blend/'
is_debug = False
filename = root_folder+'/Python/barrel.py'
exec(compile(open(filename).read(), filename, 'exec'))


##########################  STOPPED HERE    ########################## 
dddd
exec(compile(open( "C:\E\Blend\Python\ss_launch2.py").read(), "C:\E\Blend\Python\ss_launch2.py", 'exec'))
exec(compile(open( r"C:\E\Blend\Python\barrel.py").read(), r"C:\E\Blend\Python\barrel.py", 'exec'))


'''
# create a list with potential path
root_folders = []
root_folders.append('C:/Users/ssintes/Downloads/archive/ADAS')
root_folders.append('/nfs/nc/home/ssintes/ADAS/')
root_folders.append('E:/E/Blend/')
root_folders.append('E:/E/Blend/Projects/')
root_folders.append('/home/ssintes/E/Blender/')
root_folders.append('C:/E/Blend/')

#open blender 'C:/Users/1/Downloads/blender-2.79b-windows64/blender-2.79b-windows64/blender.exe'

#Launch blender file script from blender python console:
import os, imp
ss = imp.load_source('ss', os.environ['FOLDER_E'] + '/E/Blend/Python/py')
set_version(2.79)	#set the version I wanto use in the py lib module
version=get_version()  #use the same version in the current python  blender script
root_folder = os.environ['FOLDER_E']+'/E/Blend/'
set_debug(False)	#set the debug mode
filename = root_folder+'/Python/barrel.py'
exec(compile(open(filename).read(), filename, 'exec'))
'''
