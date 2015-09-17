import maya.cmds as cmds
import maya.api.OpenMaya as om

#from sets import Set

sourceComponents = {'face':'','vertex1':'','vertex2':''}
destinationComponents = {'face':'','vertex1':'','vertex2':''}

def startUI():
		windowName = 'reorderVertexIDsUI'

		if cmds.window( windowName, exists=True ):
			cmds.deleteUI( windowName, wnd=True )

		#create window
		window = cmds.window( windowName, title='Reorder Vertex IDs - v1.2 : Ryan Roberts', mb=True, mbv=True )

		#layout
		mainTabLayout = cmds.tabLayout( parent=window )

		traverseFormLayout = cmds.formLayout( parent=mainTabLayout )
		positionFormLayout = cmds.formLayout( parent=mainTabLayout )
		helpFormLayout = cmds.formLayout( parent=mainTabLayout )

		tabLabels = [
			[traverseFormLayout, 'By Traversing'],
			[positionFormLayout, 'By Position'],
			[helpFormLayout, 'Help']
		]

		cmds.tabLayout( mainTabLayout, edit=True, tabLabel=tabLabels )

		#####################################################################
		#####################################################################
		##
		## by position controls
		##
		#####################################################################
		#####################################################################

		#####################################################################
		#
		# source mesh controls
		#
		#####################################################################

		positionSourceMeshTitle = cmds.text( label='Source Mesh', parent=positionFormLayout )
		positionSourceMeshTextField = cmds.textField( 'positionSourceMeshTextField', height=30, placeholderText='Source Mesh Name', parent=positionFormLayout )
		positionGetSourceMeshButton = cmds.button( label='Get Source Mesh', height=30, c=getSourceMesh, parent=positionFormLayout )

		attachPositionData = [
			[positionSourceMeshTitle,'top',5,0],
			[positionSourceMeshTitle,'left',5,0],
			[positionSourceMeshTitle,'right',2,50],

			[positionSourceMeshTextField,'left',5,0],
			[positionSourceMeshTextField,'right',2,50],

			[positionGetSourceMeshButton,'left',5,0],
			[positionGetSourceMeshButton,'right',2,50]
		]

		attachControlData = [
			[positionSourceMeshTextField,'top',5,positionSourceMeshTitle],
			[positionGetSourceMeshButton,'top',5,positionSourceMeshTextField]
		]

		cmds.formLayout( positionFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# destination mesh controls
		#
		#####################################################################

		positionDestinationMeshTitle = cmds.text( label='Destination Mesh', parent=positionFormLayout )
		positionDestinationMeshTextField = cmds.textField( 'positionDestinationMeshTextField', height=30, placeholderText='Destination Mesh Name', parent=positionFormLayout )
		positionGetDestinationMeshButton = cmds.button( label='Get Destination Mesh', height=30, c=getDestinationMesh, parent=positionFormLayout )

		attachPositionData = [
			[positionDestinationMeshTitle,'top',5,0],
			[positionDestinationMeshTitle,'left',2,50],
			[positionDestinationMeshTitle,'right',5,100],

			[positionDestinationMeshTextField,'left',2,50],
			[positionDestinationMeshTextField,'right',5,100],

			[positionGetDestinationMeshButton,'left',2,50],
			[positionGetDestinationMeshButton,'right',5,100]
		]

		attachControlData = [
			[positionDestinationMeshTextField,'top',5,positionDestinationMeshTitle],
			[positionGetDestinationMeshButton,'top',5,positionDestinationMeshTextField]
		]

		cmds.formLayout( positionFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# switch mesh controls
		#
		#####################################################################

		positionSwitchMeshesButton = cmds.button( label='Switch Meshes', height=30, c=switchMeshes, parent=positionFormLayout )

		attachPositionData = [
			[positionSwitchMeshesButton,'left',5,0],
			[positionSwitchMeshesButton,'right',5,100]
		]

		attachControlData = [
			[positionSwitchMeshesButton,'top',5,positionGetSourceMeshButton]
		]
		
		cmds.formLayout( positionFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# position reorder controls
		#
		#####################################################################

		positionReorderPointsButton = cmds.button( label='Reorder Vertex IDs', height=60, c=positionReorderDoIt, parent=positionFormLayout )

		attachPositionData = [
			[positionReorderPointsButton,'left',5,0],
			[positionReorderPointsButton,'right',5,100]
		]

		attachControlData = [
			[positionReorderPointsButton,'top',15,positionSwitchMeshesButton]
		]
		
		cmds.formLayout( positionFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#####################################################################
		##
		## by traverse controls
		##
		#####################################################################
		#####################################################################

		#####################################################################
		#
		# source components controls
		#
		#####################################################################

		traverseSourceComponentsTitle = cmds.text( label='Source Components', parent=traverseFormLayout )
		traverseGetSourceFaceButton = cmds.button( label='Get Face', c=getSourceFace, parent=traverseFormLayout )
		traverseGetSourceVertex1Button = cmds.button( label='Get Vtx 1', c=getSourceVertex1, parent=traverseFormLayout )
		traverseGetSourceVertex2Button = cmds.button( label='Get Vtx 2', c=getSourceVertex2, parent=traverseFormLayout )
		traverseSourceTextScrollList = cmds.textScrollList( 'traverseSourceTextScrollList', nr=3, ams=True, sc=traverseSelectItems, parent=traverseFormLayout )
		traverseClearSourceButton = cmds.button( label='Clear', c=clearSourceComponents, parent=traverseFormLayout )

		attachPositionData = [
			[traverseSourceComponentsTitle,'top',5,0],
			[traverseSourceComponentsTitle,'left',5,0],
			[traverseSourceComponentsTitle,'right',2,50],

			[traverseGetSourceFaceButton,'left',5,0],
			[traverseGetSourceFaceButton,'right',0,17],

			[traverseGetSourceVertex1Button,'left',0,17],
			[traverseGetSourceVertex1Button,'right',0,33],

			[traverseGetSourceVertex2Button,'left',0,33],
			[traverseGetSourceVertex2Button,'right',5,50],

			[traverseSourceTextScrollList,'left',5,0],
			[traverseSourceTextScrollList,'right',2,50],

			[traverseClearSourceButton,'left',5,0],
			[traverseClearSourceButton,'right',2,50]
		]

		attachControlData = [
			[traverseGetSourceFaceButton,'top',5,traverseSourceComponentsTitle],
			[traverseGetSourceVertex1Button,'top',5,traverseSourceComponentsTitle],
			[traverseGetSourceVertex2Button,'top',5,traverseSourceComponentsTitle],
			[traverseSourceTextScrollList,'top',5,traverseGetSourceFaceButton],
			[traverseClearSourceButton,'top',5,traverseSourceTextScrollList]
		]

		cmds.formLayout( traverseFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# destination components controls
		#
		#####################################################################

		traverseDestinationComponentsTitle = cmds.text( label='Destination Components', parent=traverseFormLayout )
		traverseGetDestinationFaceButton = cmds.button( label='Get Face', c=getDestinationFace, parent=traverseFormLayout )
		traverseGetDestinationVertex1Button = cmds.button( label='Get Vtx 1', c=getDestinationVertex1, parent=traverseFormLayout )
		traverseGetDestinationVertex2Button = cmds.button( label='Get Vtx 2', c=getDestinationVertex2, parent=traverseFormLayout )
		traverseDestinationTextScrollList = cmds.textScrollList( 'traverseDestinationTextScrollList', nr=3, ams=True, sc=traverseSelectItems, parent=traverseFormLayout )
		traverseClearDestinationButton = cmds.button( label='Clear', c=clearDestinationComponents, parent=traverseFormLayout )

		attachPositionData = [
			[traverseDestinationComponentsTitle,'top',5,0],
			[traverseDestinationComponentsTitle,'left',2,50],
			[traverseDestinationComponentsTitle,'right',5,100],

			[traverseGetDestinationFaceButton,'left',5,50],
			[traverseGetDestinationFaceButton,'right',0,67],

			[traverseGetDestinationVertex1Button,'left',0,67],
			[traverseGetDestinationVertex1Button,'right',0,83],

			[traverseGetDestinationVertex2Button,'left',0,83],
			[traverseGetDestinationVertex2Button,'right',5,100],

			[traverseDestinationTextScrollList,'left',2,50],
			[traverseDestinationTextScrollList,'right',5,100],

			[traverseClearDestinationButton,'left',2,50],
			[traverseClearDestinationButton,'right',5,100]
		]

		attachControlData = [
			[traverseGetDestinationFaceButton,'top',5,traverseDestinationComponentsTitle],
			[traverseGetDestinationVertex1Button,'top',5,traverseDestinationComponentsTitle],
			[traverseGetDestinationVertex2Button,'top',5,traverseDestinationComponentsTitle],
			[traverseDestinationTextScrollList,'top',5,traverseGetDestinationFaceButton],
			[traverseClearDestinationButton,'top',5,traverseDestinationTextScrollList]
		]

		cmds.formLayout( traverseFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# switch components controls
		#
		#####################################################################

		traverseSwitchComponentsButton = cmds.button( label='Switch Components', height=30, c=switchComponents, parent=traverseFormLayout )

		attachPositionData = [
			[traverseSwitchComponentsButton,'left',5,0],
			[traverseSwitchComponentsButton,'right',5,100]
		]

		attachControlData = [
			[traverseSwitchComponentsButton,'top',5,traverseClearSourceButton]
		]
		
		cmds.formLayout( traverseFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# traverse reorder controls
		#
		#####################################################################

		traverseReorderPointsButton = cmds.button( label='Reorder Vertex IDs', height=60, c=traverseReorderDoIt, parent=traverseFormLayout )

		attachPositionData = [
			[traverseReorderPointsButton,'left',5,0],
			[traverseReorderPointsButton,'right',5,100],
			[traverseReorderPointsButton,'bottom',5,100]
		]

		#attachControlData = [
		#	[traverseReorderPointsButton,'top',15,traverseSwitchComponentsButton]
		#]
		
		cmds.formLayout( traverseFormLayout, edit=True, ap=attachPositionData )

		#####################################################################
		#
		# traverse target list controls
		#
		#####################################################################

		traverseTargetListTitle = cmds.text( label='Target List', parent=traverseFormLayout )
		traverseTargetTextScrollList = cmds.textScrollList( 'traverseTargetTextScrollList', sc=traverseSelectTargets, parent=traverseFormLayout )
		traverseTargetGetButton = cmds.button( label='Get Mesh Targets', height=30, c=traverseGetTargetList, parent=traverseFormLayout )
		traverseTargetClearButton = cmds.button( label='Clear Target List', height=30, c=traverseClearTargetList, parent=traverseFormLayout )

		attachPositionData = [
			[traverseTargetListTitle,'left',5,0],
			[traverseTargetListTitle,'right',5,100],

			[traverseTargetTextScrollList,'left',5,0],
			[traverseTargetTextScrollList,'right',5,100],

			[traverseTargetGetButton,'left',5,0],
			[traverseTargetGetButton,'right',2,50],

			[traverseTargetClearButton,'left',2,50],
			[traverseTargetClearButton,'right',5,100]
		]

		attachControlData = [
			[traverseTargetListTitle,'top',15,traverseSwitchComponentsButton],

			[traverseTargetTextScrollList,'top',5,traverseTargetListTitle],
			[traverseTargetTextScrollList,'bottom',5,traverseTargetGetButton],

			[traverseTargetGetButton,'bottom',15,traverseReorderPointsButton],
			[traverseTargetClearButton,'bottom',15,traverseReorderPointsButton]
		]

		cmds.formLayout( traverseFormLayout, edit=True, ap=attachPositionData, ac=attachControlData )

		#####################################################################
		#
		# show window
		#
		#####################################################################

		cmds.showWindow( windowName )

def traverseSelectItems(*args):
	sourceSelectedItems = cmds.textScrollList( 'traverseSourceTextScrollList', query=True, si=True )
	destinationSelectedItems = cmds.textScrollList( 'traverseDestinationTextScrollList', query=True, si=True )
	
	if sourceSelectedItems == None:
		sourceSelectedItems = []

	if destinationSelectedItems == None:
		destinationSelectedItems = []

	allSelectedItems = sourceSelectedItems+destinationSelectedItems
	cmds.select( allSelectedItems )

def traverseSelectTargets(*args):
	targetItems = cmds.textScrollList( 'traverseTargetTextScrollList', query=True, si=True )

	if targetItems == None:
		targetItems = []

	cmds.select( targetItems )

def traverseUpdateSourceItems(*args):
	cmds.textScrollList( 'traverseSourceTextScrollList', edit=True, ra=True )
	cmds.textScrollList( 'traverseSourceTextScrollList', edit=True, a=sourceComponents['face'] )
	cmds.textScrollList( 'traverseSourceTextScrollList', edit=True, a=sourceComponents['vertex1'] )
	cmds.textScrollList( 'traverseSourceTextScrollList', edit=True, a=sourceComponents['vertex2'] )

def traverseUpdateDestinationItems(*args):
	cmds.textScrollList( 'traverseDestinationTextScrollList', edit=True, ra=True )
	cmds.textScrollList( 'traverseDestinationTextScrollList', edit=True, a=destinationComponents['face'] )
	cmds.textScrollList( 'traverseDestinationTextScrollList', edit=True, a=destinationComponents['vertex1'] )
	cmds.textScrollList( 'traverseDestinationTextScrollList', edit=True, a=destinationComponents['vertex2'] )

def clearSourceComponents(*args):
	sourceComponents['face'] = ''
	sourceComponents['vertex1'] = ''
	sourceComponents['vertex2'] = ''
	traverseUpdateSourceItems()

def clearDestinationComponents(*args):
	destinationComponents['face'] = ''
	destinationComponents['vertex1'] = ''
	destinationComponents['vertex2'] = ''
	traverseUpdateDestinationItems()

def traverseGetTargetList(*args):
	selected = cmds.ls(sl=True)
	cmds.textScrollList( 'traverseTargetTextScrollList', edit=True, ra=True )

	for item in selected:
		cmds.textScrollList( 'traverseTargetTextScrollList', edit=True, a=item )

def traverseClearTargetList(*args):
	cmds.textScrollList( 'traverseTargetTextScrollList', edit=True, ra=True )

def getSourceFace(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		sourceComponents['face'] = selected[0]
		traverseUpdateSourceItems()

def getDestinationFace(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		destinationComponents['face'] = selected[0]
		traverseUpdateDestinationItems()
	
def getSourceVertex1(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		sourceComponents['vertex1'] = selected[0]
		traverseUpdateSourceItems()

def getDestinationVertex1(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		destinationComponents['vertex1'] = selected[0]
		traverseUpdateDestinationItems()
	
def getSourceVertex2(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		sourceComponents['vertex2'] = selected[0]
		traverseUpdateSourceItems()

def getDestinationVertex2(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		destinationComponents['vertex2'] = selected[0]
		traverseUpdateDestinationItems()
	
def getSourceMesh(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		cmds.textField( 'positionSourceMeshTextField', edit=True, text=selected[0] )

def getDestinationMesh(*args):
	selected = cmds.ls(sl=True)

	if selected is not None and len(selected) > 0:
		cmds.textField( 'positionDestinationMeshTextField', edit=True, text=selected[0] )

def switchMeshes(*args):
	sourceMeshText = cmds.textField( 'positionSourceMeshTextField', query=True, text=True )
	destinationMeshText = cmds.textField( 'positionDestinationMeshTextField', query=True, text=True )

	cmds.textField( 'positionSourceMeshTextField', edit=True, text=destinationMeshText )
	cmds.textField( 'positionDestinationMeshTextField', edit=True, text=sourceMeshText )

def switchComponents(*args):
	sourceFace    = sourceComponents['face']
	sourceVertex1 = sourceComponents['vertex1']
	sourceVertex2 = sourceComponents['vertex2']
	destinationFace    = destinationComponents['face']
	destinationVertex1 = destinationComponents['vertex1']
	destinationVertex2 = destinationComponents['vertex2']

	sourceComponents['face']    = destinationFace
	sourceComponents['vertex1'] = destinationVertex1
	sourceComponents['vertex2'] = destinationVertex2
	destinationComponents['face']    = sourceFace
	destinationComponents['vertex1'] = sourceVertex1
	destinationComponents['vertex2'] = sourceVertex2

	traverseUpdateSourceItems()
	traverseUpdateDestinationItems()

def traverseReorderDoIt(*args):
	faces = [sourceComponents['face'], destinationComponents['face']]
	vertex1s = [sourceComponents['vertex1'], destinationComponents['vertex1']]
	vertex2s = [sourceComponents['vertex2'], destinationComponents['vertex2']]

	definedError = False
	if sourceComponents['face'] == '':
		cmds.warning('source face has not been defined')
		definedError = True
	if sourceComponents['vertex1'] == '':
		cmds.warning('source vertex1 has not been defined')
		definedError = True
	if sourceComponents['vertex2'] == '':
		cmds.warning('source vertex2 has not been defined')
		definedError = True

	if destinationComponents['face'] == '':
		cmds.warning('destination face has not been defined')
		definedError = True
	if destinationComponents['vertex1'] == '':
		cmds.warning('destination vertex1 has not been defined')
		definedError = True
	if destinationComponents['vertex2'] == '':
		cmds.warning('destination vertex2 has not been defined')
		definedError = True

	if definedError:
		cmds.error('not all components have not been defined')

	sourcePointsList = cmds.polyListComponentConversion( sourceComponents['face'], ff=True, tv=True )
	sourcePoints = cmds.ls(sourcePointsList,fl=True)

	destinationPointsList = cmds.polyListComponentConversion( destinationComponents['face'], ff=True, tv=True )
	destinationPoints = cmds.ls(destinationPointsList,fl=True)

	#####################################################################
	#
	# make sure the faces contain the same number of points
	#
	#####################################################################

	if len(sourcePoints) != len(destinationPoints):
		cmds.error('faces have different number of points, faces need to have the same number of points')

	#####################################################################
	#
	# make sure the points are part of the same face
	#
	#####################################################################

	pointsError = False

	pointsFound = False
	pointsList = cmds.polyListComponentConversion( sourceComponents['face'], ff=True, tv=True )
	points = cmds.ls(pointsList, fl=True)
	if sourceComponents['vertex1'] in points and sourceComponents['vertex2'] in points:
		pointsFound = True

	if not pointsFound:
		cmds.warning('source points need to be part of the same face')
		pointsError = True

	pointsFound = False
	pointsList = cmds.polyListComponentConversion( destinationComponents['face'], ff=True, tv=True )
	points = cmds.ls(pointsList, fl=True)
	if destinationComponents['vertex1'] in points and destinationComponents['vertex2'] in points:
		pointsFound = True

	if not pointsFound:
		cmds.warning('destination points need to be part of the same face')
		pointsError = True

	if pointsError:
		cmds.error( 'points need to be part of the same face' )

	#####################################################################
	#
	# make sure the points are part of the same edge
	#
	#####################################################################

	sourceEdgesList = cmds.polyListComponentConversion( sourceComponents['face'], ff=True, te=True )
	sourceEdges = cmds.ls(sourceEdgesList, fl=True)

	destinationEdgesList = cmds.polyListComponentConversion( destinationComponents['face'], ff=True, te=True )
	destinationEdges = cmds.ls(destinationEdgesList, fl=True)

	edgeError = False

	edgeFound = False
	for edge in sourceEdges:
		pointsList = cmds.polyListComponentConversion( edge, fe=True, tv=True )
		points = cmds.ls(pointsList,fl=True)
		if sourceComponents['vertex1'] in points and sourceComponents['vertex2'] in points:
			edgeFound = True

	if not edgeFound:
		cmds.warning('source points need to be part of the same edge')
		edgeError = True

	edgeFound = False
	for edge in destinationEdges:
		pointsList = cmds.polyListComponentConversion( edge, fe=True, tv=True )
		points = cmds.ls(pointsList,fl=True)
		if destinationComponents['vertex1'] in points and destinationComponents['vertex2'] in points:
			edgeFound = True

	if not edgeFound:
		cmds.warning('destination points need to be part of the same edge')
		edgeError = True

	if edgeError:
		cmds.error( 'points need to be part of the same edge' )

	#####################################################################
	#
	# make sure destination mesh and target
	# meshes have the same number of points
	#
	#####################################################################

	destMesh = cmds.listRelatives( destinationComponents['face'], parent=True )[0]
	destMeshTransform = cmds.listRelatives( destMesh, parent=True )[0]
	destPoints = cmds.ls( destMeshTransform+'.vts[*]', fl=True )

	targetList = cmds.textScrollList( 'traverseTargetTextScrollList', query=True, ai=True )

	if targetList == None:
		targetList = []

	wrongNumberOfPointFound = False
	for target in targetList:
		targetPoints = cmds.ls( target+'.vts[*]', fl=True )
		if (len(targetPoints) != len(destPoints)):
			cmds.warning(target+' has a different number of points')
			wrongNumberOfPointFound = True

	if wrongNumberOfPointFound:
		cmds.error( 'all target meshes must have the same number of points as the destination mesh' )

	traverseReorder( faces=faces, vertex1s=vertex1s, vertex2s=vertex2s, targetList=targetList )

def traverseReorder(**kwargs):
	faces = kwargs.get('faces',[])
	vertex1s = kwargs.get('vertex1s',[])
	vertex2s = kwargs.get('vertex2s',[])
	targetList = kwargs.get('targetList',[])

	fromMesh = cmds.listRelatives(faces[0],parent=True)[0]
	toMesh = cmds.listRelatives(faces[1],parent=True)[0]

	fromFaceId = extractIndex(faces[0])
	fromVertex1Id = extractIndex(vertex1s[0])
	fromVertex2Id = extractIndex(vertex2s[0])

	toFaceId = extractIndex(faces[1])
	toVertex1Id = extractIndex(vertex1s[1])
	toVertex2Id = extractIndex(vertex2s[1])

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

	################################################################
	#
	# start creation of poly and point convert tables
	#
	################################################################

	toPointConvert = [None]*len(toPoints)
	toPointConvert[toVertex1Id] = fromVertex1Id
	toPointConvert[toVertex2Id] = fromVertex2Id

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

	fromPolyId = fromFaceId
	toPolyId = toFaceId
	fromStartVertexId = fromVertex1Id
	fromEndVertexId = fromVertex2Id
	toStartVertexId = toVertex1Id
	toEndVertexId = toVertex2Id

	fromPolyData = traversePoly( fromPolyId, fromStartVertexId, fromEndVertexId, fromPolyVertTable[fromPolyId] )
	toPolyData = traversePoly( toPolyId, toStartVertexId, toEndVertexId, toPolyVertTable[toPolyId] )

	fromCheckPolys = [fromPolyData]
	toCheckPolys = [toPolyData]

	fromPolysFound = [False]*len(fromVertices[0])
	toPolysFound = [False]*len(toVertices[0])

	for count in range( len(fromPolyVertTable) ):
		newFromCheckPolys = []
		newToCheckPolys = []
		newFromCheckPolyIDs = []
		newToCheckPolyIDs = []

		for checkIndex,checkItem in enumerate(fromCheckPolys):
			fromPolyId = fromCheckPolys[checkIndex]['id']
			toPolyId = toCheckPolys[checkIndex]['id']
			fromPolyEdges = fromCheckPolys[checkIndex]['edges']
			toPolyEdges = toCheckPolys[checkIndex]['edges']

			fromPolysFound[fromPolyId] = True
			toPolysFound[toPolyId] = True
			
			for edgeIndex,edgeItem in enumerate(fromPolyEdges):
				fromStartVertexId = fromPolyEdges[edgeIndex][0]
				fromEndVertexId = fromPolyEdges[edgeIndex][1]
				toStartVertexId = toPolyEdges[edgeIndex][0]
				toEndVertexId = toPolyEdges[edgeIndex][1]

				fromConnectingPolyId = getConnectingPoly( fromPolyId, set(fromVertPolyTable[fromStartVertexId]), set(fromVertPolyTable[fromEndVertexId]) )
				toConnectingPolyId = getConnectingPoly( toPolyId, set(toVertPolyTable[toStartVertexId]), set(toVertPolyTable[toEndVertexId]) )

				if fromConnectingPolyId != None and toConnectingPolyId != None:
					fromPolyData = traversePoly( fromConnectingPolyId, fromStartVertexId, fromEndVertexId, fromPolyVertTable[fromConnectingPolyId] )
					toPolyData = traversePoly( toConnectingPolyId, toStartVertexId, toEndVertexId, toPolyVertTable[toConnectingPolyId] )

					fromPolyPoints = fromPolyData['polyPoints']
					toPolyPoints = toPolyData['polyPoints']

					for fromPolyPointIndex,fromPolyPoint in enumerate(fromPolyPoints):
						fromPolyPointId = fromPolyPoints[fromPolyPointIndex]
						toPolyPointId = toPolyPoints[fromPolyPointIndex]
						toPointConvert[toPolyPointId] = fromPolyPointId

					if not fromPolysFound[fromPolyData['id']] and fromPolyData['id'] not in newFromCheckPolyIDs:
						newFromCheckPolyIDs.append( fromPolyData['id'] )
						newFromCheckPolys.append( fromPolyData )
						newToCheckPolys.append( toPolyData )

		fromCheckPolys = list(newFromCheckPolys)
		toCheckPolys = list(newToCheckPolys)

	newToPointConvert = [None]*len(toPoints)

	newPolys = []
	newPolyConnects = []

	newIndex = len(fromPoints)
	for toId,fromId in enumerate(toPointConvert):
		if fromId == None:
			newToPointConvert[toId] = newIndex
			newIndex = newIndex+1
		else:
			newToPointConvert[toId] = fromId

	index = 0
	for faceID,numberOfVerts in enumerate(toVertices[0]):
		newPolys.append(numberOfVerts)

		for x in range(numberOfVerts):
			vertID = toVertices[1][index]
			newPolyConnects.append( newToPointConvert[vertID] )

			index = index+1

	################################################################
	#
	# create a new mesh with the vertex IDs reordered
	#
	################################################################

	if len(targetList) > 0:
		for target in targetList:

			################################################################
			#
			# use api to get the target mesh points list
			#
			################################################################

			targetMesh = cmds.listRelatives( target, shapes=True )[0]
			
			targetSelectionList = om.MSelectionList()
			targetSelectionList.add( targetMesh )
			
			targetDagPath = targetSelectionList.getDagPath(0)
			targetMeshFn = om.MFnMesh( targetDagPath )
			targetPoints = targetMeshFn.getPoints()

			newTargetPoints = om.MPointArray()
			newTargetPoints.setLength( len(targetPoints) )

			for toId,fromId in enumerate(newToPointConvert):
				newTargetPoints[fromId] = targetPoints[toId]

			reorderedMesh = om.MFnMesh()
			reorderedMesh.create( newTargetPoints, newPolys, newPolyConnects )
			meshShape = reorderedMesh.partialPathName()
			meshTransform = cmds.listRelatives(meshShape,parent=True)[0]
			cmds.select(meshTransform)
			cmds.hyperShade(assign='initialShadingGroup')
			cmds.polySoftEdge(meshTransform, angle=0, ch=False)

			#toMeshTransform = cmds.listRelatives(toMesh,parent=True)[0]
			newMeshTransform = cmds.rename(meshTransform,target+'_reordered')

			# copy and paste transform attributes
			t = cmds.getAttr(target+'.translate')[0]
			r = cmds.getAttr(target+'.rotate')[0]
			s = cmds.getAttr(target+'.scale')[0]

			cmds.setAttr( newMeshTransform+'.translate', t[0], t[1], t[2] )
			cmds.setAttr( newMeshTransform+'.rotate', r[0], r[1], r[2] )
			cmds.setAttr( newMeshTransform+'.scale', s[0], s[1], s[2] )

			cmds.select(newMeshTransform)

	else:
		newPoints = om.MPointArray()
		newPoints.setLength( len(toPoints) )

		for toId,fromId in enumerate(newToPointConvert):
			newPoints[fromId] = toPoints[toId]

		reorderedMesh = om.MFnMesh()
		reorderedMesh.create( newPoints, newPolys, newPolyConnects )
		meshShape = reorderedMesh.partialPathName()
		meshTransform = cmds.listRelatives(meshShape,parent=True)[0]
		cmds.select(meshTransform)
		cmds.hyperShade(assign='initialShadingGroup')
		cmds.polySoftEdge(meshTransform, angle=0, ch=False)

		toMeshTransform = cmds.listRelatives(toMesh,parent=True)[0]
		newMeshTransform = cmds.rename(meshTransform,toMeshTransform+'_reordered')

		# copy and paste transform attributes
		t = cmds.getAttr(toMeshTransform+'.translate')[0]
		r = cmds.getAttr(toMeshTransform+'.rotate')[0]
		s = cmds.getAttr(toMeshTransform+'.scale')[0]

		cmds.setAttr( newMeshTransform+'.translate', t[0], t[1], t[2] )
		cmds.setAttr( newMeshTransform+'.rotate', r[0], r[1], r[2] )
		cmds.setAttr( newMeshTransform+'.scale', s[0], s[1], s[2] )

		cmds.select(newMeshTransform)

	print('Finished Reordering Vertex IDs')


def traversePoly( polyId, startVertexId, endVertexId, polyVerts ):
	edges = []
	polyPoints = []

	edgeStartVertexId = startVertexId
	endEndVertexId = endVertexId

	for edgeIndex in range(len(polyVerts)):
		polyPoints.append( edgeStartVertexId )
		edges.append( [edgeStartVertexId, endEndVertexId] )
		nextVertexId = getNextVertex( polyId, edgeStartVertexId, endEndVertexId, polyVerts )
		edgeStartVertexId = endEndVertexId
		endEndVertexId = nextVertexId

	return { 'id':polyId,'edges':edges,'polyPoints':polyPoints }

def getConnectingPoly( polyId, startVertPolySet, endVertPolySet ):
	commonPolysSet = startVertPolySet & endVertPolySet

	if polyId in commonPolysSet:
		commonPolysSet.remove(polyId)

	commonPolysList = list(commonPolysSet)
	if len(commonPolysList) == 1:
		return commonPolysList[0]
	
	return None

def getNextVertex( polyId, startVertexId, endVertexId, polyVerts ):
	numberOfVerts = len(polyVerts)
	vertIndex = {}
	for index,vertId in enumerate(polyVerts):
		vertIndex[vertId] = index

	startIndex = vertIndex[startVertexId]
	endIndex = vertIndex[endVertexId]

	if startIndex == 0 and endIndex == numberOfVerts-1:
		return polyVerts[endIndex-1]

	elif startIndex == numberOfVerts-1 and endIndex == 0:
		return polyVerts[endIndex+1]

	elif startIndex < endIndex:
		nextIndex = endIndex+1
		if nextIndex > numberOfVerts-1:
			nextIndex = 0
		return polyVerts[nextIndex]

	elif startIndex > endIndex:
		nextIndex = endIndex-1
		if nextIndex < 0:
			nextIndex = numberOfVerts-1
		return polyVerts[nextIndex]

	return None

def extractIndex(component):
	tokens = component.split('.')
	number = tokens[len(tokens)-1].replace('f[','').replace('vtx[','').replace(']','')
	return int( number )

def positionReorderDoIt(*args):
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

	positionReorder( meshes=meshes )

def positionReorder(**kwargs):
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
	
