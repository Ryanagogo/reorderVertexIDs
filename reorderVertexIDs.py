import maya.cmds as cmds
import maya.api.OpenMaya as om

def startUI():
		windowName = 'reorderVertexIDsUI'

		if cmds.window( windowName, exists=True ):
			cmds.deleteUI( windowName, wnd=True )

		#create window
		window = cmds.window( windowName, title='Reorder Vertex IDs - v1.1 : Ryan Roberts', mb=True, mbv=True )

		#layout
		mainFormLayout = cmds.formLayout( parent=window )

		#controls
		sourceMeshTitle = cmds.text( label='Source Mesh', parent=mainFormLayout )
		sourceMeshTextField = cmds.textField( 'sourceMeshTextField', height=30, placeholderText='Source Mesh Name', parent=mainFormLayout )
		getSourceMeshButton = cmds.button( label='Get Source Mesh', height=30, c=getSourceMesh, parent=mainFormLayout )

		attachPositionData = [
			[sourceMeshTitle,'top',5,0],
			[sourceMeshTitle,'left',5,0],
			[sourceMeshTitle,'right',2,50],

			[sourceMeshTextField,'left',5,0],
			[sourceMeshTextField,'right',2,50],

			[getSourceMeshButton,'left',5,0],
			[getSourceMeshButton,'right',2,50]
		]

		attachControlData = [
			[sourceMeshTextField,'top',5,sourceMeshTitle],
			[getSourceMeshButton,'top',5,sourceMeshTextField]
		]

		cmds.formLayout( mainFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		destinationMeshTitle = cmds.text( label='Destination Mesh', parent=mainFormLayout )
		destinationMeshTextField = cmds.textField( 'destinationMeshTextField', height=30, placeholderText='Destination Mesh Name', parent=mainFormLayout )
		getDestinationMeshButton = cmds.button( label='Get Destination Mesh', height=30, c=getDestinationMesh, parent=mainFormLayout )

		attachPositionData = [
			[destinationMeshTitle,'top',5,0],
			[destinationMeshTitle,'left',2,50],
			[destinationMeshTitle,'right',5,100],

			[destinationMeshTextField,'left',2,50],
			[destinationMeshTextField,'right',5,100],

			[getDestinationMeshButton,'left',2,50],
			[getDestinationMeshButton,'right',5,100]
		]

		attachControlData = [
			[destinationMeshTextField,'top',5,destinationMeshTitle],
			[getDestinationMeshButton,'top',5,destinationMeshTextField]
		]

		cmds.formLayout( mainFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		switchMeshesButton = cmds.button( label='Switch Meshes', height=30, c=switchMeshes, parent=mainFormLayout )

		attachPositionData = [
			[switchMeshesButton,'left',5,0],
			[switchMeshesButton,'right',5,100]
		]

		attachControlData = [
			[switchMeshesButton,'top',5,getSourceMeshButton]
		]
		
		cmds.formLayout( mainFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		reorderPointsButton = cmds.button( label='Reorder Vertex IDs', height=60, c=reorderDoIt, parent=mainFormLayout )

		attachPositionData = [
			[reorderPointsButton,'left',5,0],
			[reorderPointsButton,'right',5,100]
		]

		attachControlData = [
			[reorderPointsButton,'top',15,switchMeshesButton]
		]
		
		cmds.formLayout( mainFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		cmds.showWindow( windowName )

def getSourceMesh(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		cmds.textField( 'sourceMeshTextField', edit=True, text=selected[0] )

def getDestinationMesh(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		cmds.textField( 'destinationMeshTextField', edit=True, text=selected[0] )

def switchMeshes(*args):
	sourceMeshText = cmds.textField( 'sourceMeshTextField', query=True, text=True )
	destinationMeshText = cmds.textField( 'destinationMeshTextField', query=True, text=True )

	cmds.textField( 'sourceMeshTextField', edit=True, text=destinationMeshText )
	cmds.textField( 'destinationMeshTextField', edit=True, text=sourceMeshText )

def reorderDoIt(*args):
	meshes = []
	sourceMeshText = cmds.textField( 'sourceMeshTextField', query=True, text=True )

	if sourceMeshText == '':
		cmds.error('source mesh textfield is empty')

	if cmds.objExists(sourceMeshText) == False:
		cmds.error('the source mesh ( '+sourceMeshText+' ) does not exist')

	if cmds.nodeType(sourceMeshText) != 'mesh':
		shapes = cmds.listRelatives( sourceMeshText, shapes=True )

		if shapes is None or len(shapes) < 1 or cmds.nodeType(shapes[0]) != 'mesh':
			cmds.error('source ( '+sourceMeshText+' ) is not a mesh')

	meshes.append( sourceMeshText )

	destinationMeshText = cmds.textField( 'destinationMeshTextField', query=True, text=True )
	
	if destinationMeshText == '':
		cmds.error('destination mesh textfield is empty')

	if cmds.objExists(destinationMeshText) == False:
		cmds.error('the destination mesh ( '+destinationMeshText+' ) does not exist')

	if cmds.nodeType(destinationMeshText) != 'mesh':
		shapes = cmds.listRelatives( destinationMeshText, shapes=True )

		if shapes is None or len(shapes) < 1 or cmds.nodeType(shapes[0]) != 'mesh':
			cmds.error('destination ( '+destinationMeshText+' ) is not a mesh')

	meshes.append( destinationMeshText )

	reorder( meshes=meshes )

def reorder(**kwargs):
	meshes = kwargs.get('meshes',[])

	################################################################
	#
	# do some error checking
	#
	################################################################

	if len(meshes) < 2:
		cmds.error('please select 2 meshes')
		
	fromMesh = meshes[0]
	toMesh = meshes[1]

	if cmds.nodeType(fromMesh) != 'mesh':
		shapes = cmds.listRelatives( fromMesh, shapes=True)

		if shapes is not None and len(shapes) > 0 and cmds.nodeType(shapes[0]) == 'mesh':
			fromMesh = shapes[0]
		else:
			cmds.error('source mesh was not found')

	if cmds.nodeType(toMesh) != 'mesh':
		shapes = cmds.listRelatives( toMesh, shapes=True)

		if shapes is not None and len(shapes) > 0 and cmds.nodeType(shapes[0]) == 'mesh':
			toMesh = shapes[0]
		else:
			cmds.error('destination mesh was not found')

	if len( cmds.listHistory( toMesh ) ) > 1:
		cmds.error('destination mesh ( '+toMesh+' ) has history, please delete history')

	################################################################
	#
	# use api to get the mesh data from
	# the source and destination meshes
	#
	################################################################
	
	selectionList = om.MSelectionList()
	selectionList.add( fromMesh )
	selectionList.add( toMesh )
	
	fromDagPath = selectionList.getDagPath(0)
	toDagPath = selectionList.getDagPath(1)
	fromMeshFn = om.MFnMesh( fromDagPath )
	toMeshFn = om.MFnMesh( toDagPath )
	fromPoints = fromMeshFn.getPoints()
	toPoints = toMeshFn.getPoints()
	fromDagNodeFn = om.MFnDagNode(fromDagPath)
	toDagNodeFn = om.MFnDagNode(toDagPath)
	fromBoundingBox = fromDagNodeFn.boundingBox
	toBoundingBox = toDagNodeFn.boundingBox

	################################################################
	#
	# More error checking!
	# make sure source mesh doesn't have
	# more points than the destination mesh
	#
	################################################################

	if len(fromPoints) > len(toPoints):
		cmds.error('source mesh ( '+fromMesh+' ) has more points than destination mesh ( '+toMesh+' ). Source mesh must have the same number of points or less points than the destination mesh')

	################################################################
	#
	# build lookup tables for points and faces
	#
	################################################################

	fromVertices = fromMeshFn.getVertices()
	toVertices = toMeshFn.getVertices()

	fromVertPolyTable = [None]*len(fromPoints)
	fromPolyVertTable = []
	index = 0

	for faceID,numberOfVerts in enumerate(fromVertices[0]):
		fromPolyVertTable.append([])

		for x in range(numberOfVerts):
			vertID = fromVertices[1][index]
			fromPolyVertTable[faceID].append(vertID)

			if fromVertPolyTable[vertID] is None:
				fromVertPolyTable[vertID] = [faceID]
			else:
				fromVertPolyTable[vertID].append(faceID)

			index = index+1

	toVertPolyTable = [None]*len(toPoints)
	toPolyVertTable = []
	index = 0

	for faceID,numberOfVerts in enumerate(toVertices[0]):
		toPolyVertTable.append([])

		for x in range(numberOfVerts):
			vertID = toVertices[1][index]
			toPolyVertTable[faceID].append(vertID)
			
			if toVertPolyTable[vertID] is None:
				toVertPolyTable[vertID] = [faceID]
			else:
				toVertPolyTable[vertID].append(faceID)

			index = index+1

	################################################################
	#
	# create a list of destination points that
	# are in the bounding box of the source
	# mesh and have a matching point
	#
	################################################################

	toSearchPoints = {}
	toMatchingPoints = {}
	for index,point in enumerate(toPoints):
		if fromBoundingBox.contains(point):
			matchingPoint = findMatchingPoint(point=point, meshFn=fromMeshFn, meshPoints=fromPoints)

			if matchingPoint != None:
				#print(index,matchingPoint)
				toSearchPoints[index] = None
				toMatchingPoints[index] = matchingPoint

	################################################################
	#
	# create a list of destination faceIds
	# associated with bounding box points
	#
	################################################################

	toMatchingPolys = {}
	toBorderingPolys = {}

	for toIndex in toSearchPoints:
		toPolyIds = toVertPolyTable[toIndex]

		for toPolyId in toPolyIds:
			toVerts = toPolyVertTable[toPolyId]

			for toVert in toVerts:
				found = toSearchPoints.get(toVert,False)
				#toUsePoints[toVert] = False

				if found == False:
					toBorderingPolys[toPolyId] = True
				else:
					toMatchingPolys[toPolyId] = True

	# just a double check to make sure the matching
	# polys list doesn't contain any connecting polys items
	for toPolyId in toBorderingPolys:
		toMatchingPolys.pop(toPolyId,False)

	################################################################
	#
	# Find any matching points, from the connecting polys,
	# between the source and destination meshes
	#
	################################################################

	toPointsConvert = {}

	for toPolyId in toBorderingPolys:
		toPolyVerts = toMeshFn.getPolygonVertices( toPolyId )
		
		for toPolyVert in toPolyVerts:
			matchingPoint = toMatchingPoints.get(toPolyVert,None)

			if matchingPoint != None:
				toPointsConvert[toPolyVert] = matchingPoint


	################################################################
	#
	# create points conversion table for the destination mesh
	#
	################################################################
	
	newIndex = len(fromPoints)
	for toIndex,toPoint in enumerate(toPoints):
		matchingPointFound = toMatchingPoints.get(toIndex,None)

		if matchingPointFound == None:
			toPointsConvert[toIndex] = newIndex
			newIndex = newIndex+1

	################################################################
	#
	# new points, poly and polyconnects lists
	#
	################################################################

	newPoints = om.MPointArray()
	newPoints.setLength( len(toPoints) )
	newPolys = []
	newPolyConnects = []

	################################################################
	#
	# get info from the source mesh (the from mesh)
	#
	################################################################

	for index,fromPoint in enumerate(fromPoints):
		newPoints[index] = fromPoint

	for fromPolyVerts in fromPolyVertTable:
		newPolys.append(len(fromPolyVerts))

		for fromPolyVert in fromPolyVerts:
			newPolyConnects.append(fromPolyVert)

	################################################################
	#
	# get data from the destination mesh (the to mesh)
	#
	################################################################
	
	for toPointId,toPointConvertId in toPointsConvert.iteritems():
		newPoints[toPointConvertId] = toPoints[toPointId]

	for toPolyId,toPolyVerts in enumerate(toPolyVertTable):
		isMatchingPoly = toMatchingPolys.get(toPolyId,None)

		if isMatchingPoly == None:
			newPolys.append(len(toPolyVerts))

			for toPolyVert in toPolyVerts:
				newPolyConnects.append(toPointsConvert[toPolyVert])

	################################################################
	#
	# create a new mesh with the vertex IDs reordered
	#
	################################################################

	reorderedMesh = om.MFnMesh()
	reorderedMesh.create( newPoints, newPolys, newPolyConnects )
	meshShape = reorderedMesh.partialPathName()
	meshTransform = cmds.listRelatives(meshShape,parent=True)[0]
	cmds.select(meshTransform)
	cmds.hyperShade(assign='initialShadingGroup')
	cmds.polySoftEdge(meshTransform, angle=0, ch=False)

	toMeshTransform = cmds.listRelatives(toMesh,parent=True)[0]
	newMeshName = cmds.rename(meshTransform,toMeshTransform+'_reordered')
	cmds.select(newMeshName)

	print('Finished Reordering Vertex IDs')

def findMatchingPoint(**kwargs):
	tol = kwargs.get('tolerance',0.000001)
	meshFn = kwargs.get('meshFn',None)
	meshPoints = kwargs.get('meshPoints',None)
	point = kwargs.get('point',None)
	
	closestPointData = meshFn.getClosestPoint( point, om.MSpace.kWorld )
	closestPoint = closestPointData[0]
	polyId = closestPointData[1]
	polyVerts = meshFn.getPolygonVertices( polyId )

	for polyVert in polyVerts:
		meshPoint = meshPoints[polyVert]

		if (point[0] < meshPoint[0]+tol) and (point[1] < meshPoint[1]+tol) and (point[2] < meshPoint[2]+tol):
			if (point[0] > meshPoint[0]-tol) and (point[1] > meshPoint[1]-tol) and (point[2] > meshPoint[2]-tol):
				return polyVert
				break

	return None
	
