from typing import List, Optional, Any

# This is a stub file for the pxr.Usd module. It provides type hints and method signatures.

__all__ = [
    "Stage", "Prim", "Attribute", "VariantSet", "Layer", "SdfPath", "UsdGeomXform", 
    "XformOp", "UsdAttributeQuery", "UsdPrimRange", "UsdPrimRangeIterator", 
    "UsdStageCache", "UsdTimeCode", "UsdGeomMesh", "UsdGeomSphere", "UsdShadeShader", 
    "UsdShadeMaterial", "UsdGeomCamera", "UsdGeomCube", "UsdGeomCone", "UsdGeomCylinder", 
    "UsdGeomPoints", "UsdGeomBasisCurves", "UsdLuxDistantLight", "UsdLuxDiskLight", 
    "UsdPhysicsRigidBodyAPI", "UsdRenderSettings", "UsdGeomXformable", "UsdGeomGprim", 
    "UsdGeomPlane", "UsdGeomCapsule", "UsdShadeMaterialBindingAPI", "UsdShadeConnectableAPI", 
    "UsdCollectionAPI", "Relationship", "UsdReferences", "UsdPhysicsMeshCollisionAPI", 
    "UsdSkelAnimation", "UsdSkelSkeleton", "UsdSkelBindingAPI", "UsdSkelRoot", 
    "UsdSkelSkinningQuery", "UsdGeomScope", "UsdGeomTokens", "UsdLuxSphereLight", 
    "UsdLuxRectLight", "UsdPhysicsJointAPI", "UsdGeomSubset", "UsdShadeOutput", 
    "UsdShadeInput", "UsdUtils"
]


class Stage:
    @staticmethod
    def CreateNew(filePath: str) -> 'Stage':
        """Create a new USD stage at the specified file path."""
        pass

    @staticmethod
    def Open(filePath: str, load: str = None) -> 'Stage':
        """Open an existing USD stage from the specified file path."""
        pass

    @staticmethod
    def CreateInMemory(identifier: str = "") -> 'Stage':
        """Create a new in-memory USD stage."""
        pass
    
    def GetPrimAtPath(self, path: str) -> 'Prim':
        """Get the prim at the specified path."""
        pass

    def DefinePrim(self, path: str, typeName: Optional[str] = None) -> 'Prim':
        """Define a new prim at the specified path with an optional type name."""
        pass
    
    def GetDefaultPrim(self) -> 'Prim':
        """Get the default prim for the stage."""
        pass
    
    def SetDefaultPrim(self, prim: 'Prim') -> None:
        """Set the default prim for the stage."""
        pass
    
    def GetPseudoRoot(self) -> 'Prim':
        """Get the pseudo-root prim of the stage."""
        pass
    
    def GetRootLayer(self) -> 'Layer':
        """Get the root layer of the stage."""
        pass
    
    def GetLayerStack(self) -> List['Layer']:
        """Get the layer stack for this stage."""
        pass
    
    def GetStartTimeCode(self) -> float:
        """Get the start time code for the stage."""
        pass
    
    def GetEndTimeCode(self) -> float:
        """Get the end time code for the stage."""
        pass
    
    def SetStartTimeCode(self, startTime: float) -> None:
        """Set the start time code for the stage."""
        pass
    
    def SetEndTimeCode(self, endTime: float) -> None:
        """Set the end time code for the stage."""
        pass
    
    def GetTimeCodesPerSecond(self) -> float:
        """Get the time codes per second for the stage."""
        pass
    
    def SetTimeCodesPerSecond(self, timeCodesPerSecond: float) -> None:
        """Set the time codes per second for the stage."""
        pass
    
    def GetFramesPerSecond(self) -> float:
        """Get the frames per second for the stage."""
        pass
    
    def SetFramesPerSecond(self, framesPerSecond: float) -> None:
        """Set the frames per second for the stage."""
        pass
    
    def GetEditTarget(self) -> 'EditTarget':
        """Get the current edit target for the stage."""
        pass
    
    def SetEditTarget(self, editTarget: 'EditTarget') -> None:
        """Set the edit target for the stage."""
        pass
    
    def GetPathResolverContext(self) -> Any:
        """Get the path resolver context for the stage."""
        pass
    
    def GetObjectAtPath(self, path: str) -> Any:
        """Get an object at the specified path."""
        pass
    
    def Traverse(self) -> 'UsdPrimRange':
        """Traverse all prims on the stage."""
        pass
    
    def OverridePrim(self, path: str) -> 'Prim':
        """Create or return a prim at the specified path for overriding."""
        pass
    
    def RemovePrim(self, path: str) -> bool:
        """Remove the prim at the specified path."""
        pass
    
    def Save(self) -> bool:
        """Save the current stage to its file."""
        pass

    def SaveAs(self, filePath: str) -> bool:
        """Save the current stage to the specified file path."""
        pass
    
    def Reload(self) -> None:
        """Reload the stage from its file."""
        pass
    
    def Export(self, filePath: str, addSourceFileComment: bool = True) -> bool:
        """Export the stage to the specified file path."""
        pass
    
    def GetMetadata(self, key: str) -> Any:
        """Get stage metadata for the specified key."""
        pass
    
    def SetMetadata(self, key: str, value: Any) -> None:
        """Set stage metadata for the specified key."""
        pass
    
    def HasAuthoredMetadata(self, key: str) -> bool:
        """Check if the stage has authored metadata for the specified key."""
        pass
    
    def ClearMetadata(self, key: str) -> None:
        """Clear stage metadata for the specified key."""
        pass
    
    def GetInterpolationType(self) -> str:
        """Get the interpolation type for the stage."""
        pass
    
    def SetInterpolationType(self, interpolationType: str) -> None:
        """Set the interpolation type for the stage."""
        pass
    
    def GetMutedLayers(self) -> List[str]:
        """Get the muted layers for the stage."""
        pass
    
    def MuteLayer(self, layerIdentifier: str) -> bool:
        """Mute the specified layer."""
        pass
    
    def UnmuteLayer(self, layerIdentifier: str) -> bool:
        """Unmute the specified layer."""
        pass
    
    def IsLayerMuted(self, layerIdentifier: str) -> bool:
        """Check if the specified layer is muted."""
        pass




class Prim:
    def GetName(self) -> str:
        """Get the name of the prim."""
        pass

    def GetPath(self) -> 'SdfPath':
        """Get the path of the prim as an SdfPath."""
        pass

    def GetTypeName(self) -> str:
        """Get the type name of the prim."""
        pass

    def GetChildren(self) -> List['Prim']:
        """Get the children of the prim."""
        pass

    def GetParent(self) -> 'Prim':
        """Get the parent of the prim."""
        pass

    def GetStage(self) -> 'Stage':
        """Get the stage to which this prim belongs."""
        pass

    # Attribute methods
    def HasAttribute(self, attrName: str) -> bool:
        """Check if the prim has an attribute with the specified name."""
        pass

    def GetAttribute(self, attrName: str) -> 'Attribute':
        """Get the attribute with the specified name."""
        pass

    def CreateAttribute(self, attrName: str, typeName: str, custom: bool = True, variability: str = "Varying") -> 'Attribute':
        """Create a new attribute with the specified name and type."""
        pass

    def GetAttributes(self) -> List['Attribute']:
        """Get all attributes of the prim."""
        pass

    # Relationship methods
    def HasRelationship(self, relName: str) -> bool:
        """Check if the prim has a relationship with the specified name."""
        pass

    def GetRelationship(self, relName: str) -> 'Relationship':
        """Get the relationship with the specified name."""
        pass

    def CreateRelationship(self, relName: str, custom: bool = True) -> 'Relationship':
        """Create a new relationship with the specified name."""
        pass

    # Variant methods
    def GetVariantSets(self) -> List[str]:
        """Get the names of all variant sets on the prim."""
        pass

    def GetVariantSet(self, variantSetName: str) -> 'VariantSet':
        """Get the variant set with the specified name."""
        pass

    # References
    def GetReferences(self) -> 'UsdReferences':
        """Get the references object for this prim."""
        pass

    # Metadata methods
    def HasMetadata(self, key: str) -> bool:
        """Check if the prim has metadata for the specified key."""
        pass

    def GetMetadata(self, key: str) -> Any:
        """Get metadata for the specified key."""
        pass

    def SetMetadata(self, key: str, value: Any) -> None:
        """Set metadata for the specified key."""
        pass

    # Composition and validity
    def IsValid(self) -> bool:
        """Check if the prim is valid."""
        pass

    def IsDefined(self) -> bool:
        """Check if the prim is defined."""
        pass

    def IsActive(self) -> bool:
        """Check if the prim is active."""
        pass

    def SetActive(self, active: bool) -> None:
        """Set whether the prim is active."""
        pass

    def IsLoaded(self) -> bool:
        """Check if the prim is loaded."""
        pass

    def IsInstanceable(self) -> bool:
        """Check if the prim is instanceable."""
        pass

    def SetInstanceable(self, instanceable: bool) -> None:
        """Set whether the prim is instanceable."""
        pass

class Attribute:
    def GetName(self) -> str:
        """Get the name of the attribute."""
        pass

    def GetPath(self) -> 'SdfPath':
        """Get the path of the attribute."""
        pass

    def GetPrim(self) -> 'Prim':
        """Get the prim that owns this attribute."""
        pass

    def GetTypeName(self) -> str:
        """Get the type name of the attribute."""
        pass

    def Get(self, time: float = None) -> Any:
        """Get the value of the attribute at the specified time."""
        pass

    def Set(self, value: Any, time: float = None) -> bool:
        """Set the value of the attribute at the specified time."""
        pass

    def HasValue(self) -> bool:
        """Check if the attribute has an authored value."""
        pass

    def HasAuthoredValue(self) -> bool:
        """Check if the attribute has an authored value opinion."""
        pass

    def Clear(self) -> bool:
        """Clear the attribute's value."""
        pass

    def ClearAtTime(self, time: float) -> bool:
        """Clear the attribute's value at the specified time."""
        pass

    def SetMetadata(self, key: str, value: Any) -> bool:
        """Set metadata for the specified key."""
        pass

    def GetMetadata(self, key: str) -> Any:
        """Get metadata for the specified key."""
        pass

    def HasMetadata(self, key: str) -> bool:
        """Check if the attribute has metadata for the specified key."""
        pass

    def ClearMetadata(self, key: str) -> bool:
        """Clear metadata for the specified key."""
        pass

    def GetTimeSamples(self) -> List[float]:
        """Get all time samples for the attribute."""
        pass

    def GetNumTimeSamples(self) -> int:
        """Get the number of time samples for the attribute."""
        pass

    def GetConnectionPaths(self) -> List['SdfPath']:
        """Get the connection paths for the attribute."""
        pass

    def ConnectToSource(self, source: 'Attribute') -> bool:
        """Connect this attribute to a source attribute."""
        pass

    def DisconnectSource(self, source: 'Attribute' = None) -> bool:
        """Disconnect this attribute from a source attribute."""
        pass

    def HasDefault(self) -> bool:
        """Check if the attribute has a default value."""
        pass

    def GetDisplayName(self) -> str:
        """Get the display name of the attribute."""
        pass

    def SetDisplayName(self, name: str) -> bool:
        """Set the display name of the attribute."""
        pass

    def IsCustom(self) -> bool:
        """Check if the attribute is custom (not part of the schema)."""
        pass

    def IsAuthored(self) -> bool:
        """Check if the attribute has been authored."""
        pass

    def IsAuthoredAt(self, time: float) -> bool:
        """Check if the attribute has been authored at a specific time."""
        pass

    def Block(self) -> bool:
        """Block the attribute value."""
        pass

    def IsDefined(self) -> bool:
        """Check if the attribute is defined."""
        pass

    def CreateConnectionToSource(self, sourcePath: 'SdfPath') -> bool:
        """Create a connection to a source at the given path."""
        pass

    def BlockConnections(self) -> bool:
        """Block connections to this attribute."""
        pass


class VariantSet:
    def GetName(self) -> str:
        """Get the name of the variant set."""
        pass
    
    def GetVariantNames(self) -> List[str]:
        """Get the names of all variants in the set."""
        pass
    
    def SetVariantSelection(self, variantName: str) -> bool:
        """Set the active variant selection.
        
        Args:
            variantName: The name of the variant to select
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetVariantSelection(self) -> Optional[str]:
        """Get the active variant selection.
        
        Returns:
            Optional[str]: The name of the currently selected variant, or None if no variant is selected
        """
        pass
    
    def AddVariant(self, variantName: str) -> bool:
        """Add a new variant to the variant set.
        
        Args:
            variantName: The name of the variant to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def RemoveVariant(self, variantName: str) -> bool:
        """Remove a variant from the variant set.
        
        Args:
            variantName: The name of the variant to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def ClearVariantSelection(self) -> bool:
        """Clear the current variant selection.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def BlockVariantSelection(self) -> bool:
        """Block variant selection from resolving from weaker opinions.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetPrim(self) -> 'Prim':
        """Get the prim that owns this variant set.
        
        Returns:
            Prim: The prim that owns this variant set
        """
        pass
    
    def GetVariantEditContext(self, variantName: str) -> Any:
        """Get an edit context for editing the specified variant.
        
        Args:
            variantName: The name of the variant to edit
            
        Returns:
            Any: An edit context object
        """
        pass
    
    def HasAuthoredVariantSelection(self) -> bool:
        """Check if a variant selection has been authored.
        
        Returns:
            bool: True if a variant selection has been authored, False otherwise
        """
        pass
class Layer:
    @staticmethod
    def Find(filePath: str) -> Optional['Layer']:
        """Find an existing layer by file path."""
        pass
    
    @staticmethod
    def FindOrOpen(filePath: str) -> Optional['Layer']:
        """Find an existing layer or open it if not found."""
        pass
    
    @staticmethod
    def CreateNew(filePath: str, args: Optional[dict] = None) -> 'Layer':
        """Create a new layer at the specified file path."""
        pass
    
    @staticmethod
    def CreateAnonymous(identifier: str = "") -> 'Layer':
        """Create a new anonymous layer with an optional identifier."""
        pass
    
    def GetIdentifier(self) -> str:
        """Get the identifier of the layer."""
        pass
    
    def GetRealPath(self) -> str:
        """Get the real filesystem path of the layer."""
        pass
    
    def GetFileExtension(self) -> str:
        """Get the file extension of the layer."""
        pass
    
    def Export(self, filePath: str) -> bool:
        """Export the layer to the specified file path."""
        pass
    
    def ExportToString(self) -> str:
        """Export the layer to a string."""
        pass
    
    def ImportFromString(self, string: str) -> bool:
        """Import content from a string into the layer."""
        pass
    
    def Save(self, force: bool = False) -> bool:
        """Save the layer to its existing file path."""
        pass
    
    def Reload(self) -> bool:
        """Reload the layer from its file."""
        pass
    
    def Clear(self) -> None:
        """Clear the contents of the layer."""
        pass
    
    def TransferContent(self, source: 'Layer') -> None:
        """Transfer content from the source layer to this layer."""
        pass
    
    def GetDisplayName(self) -> str:
        """Get the display name of the layer."""
        pass
    
    def SetMuted(self, muted: bool) -> None:
        """Set whether this layer is muted."""
        pass
    
    def IsMuted(self) -> bool:
        """Check if this layer is muted."""
        pass
    
    def GetColorConfiguration(self) -> str:
        """Get the color configuration of the layer."""
        pass
    
    def SetColorConfiguration(self, colorConfig: str) -> None:
        """Set the color configuration of the layer."""
        pass
    
    def GetColorManagementSystem(self) -> str:
        """Get the color management system of the layer."""
        pass
    
    def SetColorManagementSystem(self, cms: str) -> None:
        """Set the color management system of the layer."""
        pass
    
    def GetTimeCodesPerSecond(self) -> float:
        """Get the time codes per second of the layer."""
        pass
    
    def SetTimeCodesPerSecond(self, timeCodesPerSecond: float) -> None:
        """Set the time codes per second of the layer."""
        pass
    
    def GetFramesPerSecond(self) -> float:
        """Get the frames per second of the layer."""
        pass
    
    def SetFramesPerSecond(self, framesPerSecond: float) -> None:
        """Set the frames per second of the layer."""
        pass
    
    def GetStartTimeCode(self) -> float:
        """Get the start time code of the layer."""
        pass
    
    def SetStartTimeCode(self, startTime: float) -> None:
        """Set the start time code of the layer."""
        pass
    
    def GetEndTimeCode(self) -> float:
        """Get the end time code of the layer."""
        pass
    
    def SetEndTimeCode(self, endTime: float) -> None:
        """Set the end time code of the layer."""
        pass
    
    def GetDefaultPrim(self) -> str:
        """Get the name of the default prim in the layer."""
        pass
    
    def SetDefaultPrim(self, primName: str) -> None:
        """Set the default prim in the layer."""
        pass
    
    def ClearDefaultPrim(self) -> None:
        """Clear the default prim in the layer."""
        pass
    
    def HasDefaultPrim(self) -> bool:
        """Check if the layer has a default prim."""
        pass
    
    def GetPrimAtPath(self, path: 'SdfPath') -> Any:
        """Get the prim at the specified path in the layer."""
        pass
    
    def GetPropertyAtPath(self, path: 'SdfPath') -> Any:
        """Get the property at the specified path in the layer."""
        pass
    
    def GetObjectAtPath(self, path: 'SdfPath') -> Any:
        """Get the object at the specified path in the layer."""
        pass
    
    def GetMetadata(self, key: str) -> Any:
        """Get metadata for the specified key."""
        pass
    
    def SetMetadata(self, key: str, value: Any) -> None:
        """Set metadata for the specified key."""
        pass
    
    def HasMetadata(self, key: str) -> bool:
        """Check if the layer has metadata for the specified key."""
        pass
    
    def ClearMetadata(self, key: str) -> None:
        """Clear metadata for the specified key."""
        pass
    
    def GetExternalReferences(self) -> List[str]:
        """Get all external references in the layer."""
        pass
    
    def IsAnonymous(self) -> bool:
        """Check if the layer is anonymous."""
        pass
    
    def IsDirty(self) -> bool:
        """Check if the layer has unsaved changes."""
        pass
class SdfPath:
    def __init__(self, path: str) -> None:
        """Initialize an SdfPath with the given path string.
        
        Args:
            path: The string representation of the path
        """
        pass
    
    def IsEmpty(self) -> bool:
        """Check if the path is empty.
        
        Returns:
            bool: True if the path is empty, False otherwise
        """
        pass
    
    def GetParentPath(self) -> 'SdfPath':
        """Get the parent path.
        
        Returns:
            SdfPath: The parent path
        """
        pass
    
    def AppendChild(self, childName: str) -> 'SdfPath':
        """Append a child name to the path.
        
        Args:
            childName: The name of the child to append
            
        Returns:
            SdfPath: A new path with the child appended
        """
        pass
    
    def GetString(self) -> str:
        """Get the string representation of the path.
        
        Returns:
            str: The string representation of the path
        """
        pass
    
    def AppendProperty(self, propertyName: str) -> 'SdfPath':
        """Append a property name to the path.
        
        Args:
            propertyName: The name of the property to append
            
        Returns:
            SdfPath: A new path with the property appended
        """
        pass
    
    def AppendElementString(self, element: str) -> 'SdfPath':
        """Append an element string to the path.
        
        Args:
            element: The element string to append
            
        Returns:
            SdfPath: A new path with the element appended
        """
        pass
    
    def AppendVariantSelection(self, variantSet: str, variant: str) -> 'SdfPath':
        """Append a variant selection to the path.
        
        Args:
            variantSet: The name of the variant set
            variant: The name of the variant
            
        Returns:
            SdfPath: A new path with the variant selection appended
        """
        pass
    
    def GetName(self) -> str:
        """Get the name component of the path.
        
        Returns:
            str: The name component of the path
        """
        pass
    
    def GetPrimPath(self) -> 'SdfPath':
        """Get the prim path (excluding any property component).
        
        Returns:
            SdfPath: The prim path
        """
        pass
    
    def GetPrimOrPrimVariantSelectionPath(self) -> 'SdfPath':
        """Get the prim path or prim variant selection path.
        
        Returns:
            SdfPath: The prim path or prim variant selection path
        """
        pass
    
    def IsAbsolutePath(self) -> bool:
        """Check if the path is an absolute path.
        
        Returns:
            bool: True if the path is absolute, False otherwise
        """
        pass
    
    def IsPropertyPath(self) -> bool:
        """Check if the path is a property path.
        
        Returns:
            bool: True if the path is a property path, False otherwise
        """
        pass
    
    def IsPrimPath(self) -> bool:
        """Check if the path is a prim path.
        
        Returns:
            bool: True if the path is a prim path, False otherwise
        """
        pass
    
    def HasPrefix(self, prefix: 'SdfPath') -> bool:
        """Check if the path has the specified prefix.
        
        Args:
            prefix: The prefix path to check
            
        Returns:
            bool: True if the path has the specified prefix, False otherwise
        """
        pass
    
    def MakeRelativePath(self, anchorPath: 'SdfPath') -> 'SdfPath':
        """Make a relative path using the specified anchor path.
        
        Args:
            anchorPath: The anchor path
            
        Returns:
            SdfPath: The relative path
        """
        pass
    
    @staticmethod
    def AbsoluteRootPath() -> 'SdfPath':
        """Get the absolute root path.
        
        Returns:
            SdfPath: The absolute root path
        """
        pass
    
    @staticmethod
    def EmptyPath() -> 'SdfPath':
        """Get an empty path.
        
        Returns:
            SdfPath: An empty path
        """
        pass

class UsdGeomXform:
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomXform':
        """Define a new transform prim at the specified path.
        
        Args:
            stage: The stage on which to define the transform
            path: The path at which to define the transform
            
        Returns:
            UsdGeomXform: The newly defined transform
        """
        pass
    
    def GetOrderedXformOps(self) -> List['XformOp']:
        """Get the ordered list of transform operations.
        
        Returns:
            List[XformOp]: The ordered list of transform operations
        """
        pass
    
    def AddXformOp(self, opType: str, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a new transform operation of the specified type.
        
        Args:
            opType: The type of transform operation
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added transform operation
        """
        pass
    
    def ClearXformOpOrder(self) -> None:
        """Clear the order of transform operations."""
        pass
    
    def SetResetXformStack(self, resetXformStack: bool) -> bool:
        """Set whether to reset the transform stack.
        
        Args:
            resetXformStack: Whether to reset the transform stack
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetResetXformStack(self) -> bool:
        """Check if the transform stack is reset.
        
        Returns:
            bool: True if the transform stack is reset, False otherwise
        """
        pass
    
    def SetXformOpOrder(self, ops: List['XformOp']) -> bool:
        """Set the order of transform operations.
        
        Args:
            ops: The ordered list of transform operations
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def AddTranslateOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a translate operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added translate operation
        """
        pass
    
    def AddScaleOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a scale operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added scale operation
        """
        pass
    
    def AddRotateXOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a rotate X operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added rotate X operation
        """
        pass
    
    def AddRotateYOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a rotate Y operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added rotate Y operation
        """
        pass
    
    def AddRotateZOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a rotate Z operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added rotate Z operation
        """
        pass
    
    def AddRotateXYZOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a rotate XYZ operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added rotate XYZ operation
        """
        pass
    
    def AddTransformOp(self, precision: str = "double", opSuffix: str = "") -> 'XformOp':
        """Add a transform operation.
        
        Args:
            precision: The precision of the operation
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added transform operation
        """
        pass

class XformOp:
    def GetOpType(self) -> str:
        """Get the type of the transform operation.
        
        Returns:
            str: The type of the transform operation
        """
        pass
    
    def Get(self, time: Any = None) -> Any:
        """Get the value of the transform operation at the specified time.
        
        Args:
            time: The time at which to get the value
            
        Returns:
            Any: The value of the transform operation
        """
        pass
    
    def Set(self, value: Any, time: Any = None) -> bool:
        """Set the value of the transform operation at the specified time.
        
        Args:
            value: The value to set
            time: The time at which to set the value
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetAttr(self) -> 'Attribute':
        """Get the attribute associated with this transform operation.
        
        Returns:
            Attribute: The attribute associated with this transform operation
        """
        pass
    
    def GetName(self) -> str:
        """Get the name of the transform operation.
        
        Returns:
            str: The name of the transform operation
        """
        pass
    
    def GetPrecision(self) -> str:
        """Get the precision of the transform operation.
        
        Returns:
            str: The precision of the transform operation
        """
        pass
    
    def IsInverseOp(self) -> bool:
        """Check if this is an inverse operation.
        
        Returns:
            bool: True if this is an inverse operation, False otherwise
        """
        pass

class UsdAttributeQuery:
    def __init__(self, attr: 'Attribute') -> None:
        """Initialize a UsdAttributeQuery for the given attribute.
        
        Args:
            attr: The attribute to query
        """
        pass
    
    def HasAuthoredValueOpinion(self) -> bool:
        """Check if the attribute has an authored value opinion.
        
        Returns:
            bool: True if the attribute has an authored value opinion, False otherwise
        """
        pass
    
    def Get(self, time: Any = None) -> Any:
        """Get the value of the attribute at the specified time.
        
        Args:
            time: The time at which to get the value
            
        Returns:
            Any: The value of the attribute
        """
        pass
    
    def GetAttribute(self) -> 'Attribute':
        """Get the attribute being queried.
        
        Returns:
            Attribute: The attribute being queried
        """
        pass
    
    def GetTimeSamples(self) -> List[float]:
        """Get all time samples for the attribute.
        
        Returns:
            List[float]: All time samples for the attribute
        """
        pass
    
    def GetTimeSamplesInInterval(self, interval: tuple) -> List[float]:
        """Get time samples in the specified interval.
        
        Args:
            interval: A tuple containing the start and end times
            
        Returns:
            List[float]: Time samples in the specified interval
        """
        pass
    
    def HasValue(self) -> bool:
        """Check if the attribute has a value.
        
        Returns:
            bool: True if the attribute has a value, False otherwise
        """
        pass
    
    def ValueMightBeTimeVarying(self) -> bool:
        """Check if the attribute's value might be time-varying.
        
        Returns:
            bool: True if the attribute's value might be time-varying, False otherwise
        """
        pass

class UsdPrimRange:
    def __init__(self, root: 'Prim') -> None:
        """Initialize a UsdPrimRange starting at the given root prim.
        
        Args:
            root: The root prim for the range
        """
        pass
    
    def __iter__(self) -> 'UsdPrimRangeIterator':
        """Return an iterator for the prim range.
        
        Returns:
            UsdPrimRangeIterator: An iterator for the prim range
        """
        pass
    
    @staticmethod
    def AllPrims(root: 'Prim') -> 'UsdPrimRange':
        """Create a range that includes all prims under the root.
        
        Args:
            root: The root prim
            
        Returns:
            UsdPrimRange: A range including all prims under the root
        """
        pass
    
    @staticmethod
    def PreAndPostVisit(root: 'Prim') -> 'UsdPrimRange':
        """Create a range that visits prims before and after their children.
        
        Args:
            root: The root prim
            
        Returns:
            UsdPrimRange: A range that visits prims before and after their children
        """
        pass
    
    @staticmethod
    def AllPrimsPreAndPostVisit(root: 'Prim') -> 'UsdPrimRange':
        """Create a range that includes all prims and visits them before and after their children.
        
        Args:
            root: The root prim
            
        Returns:
            UsdPrimRange: A range that includes all prims and visits them before and after their children
        """
        pass

class UsdPrimRangeIterator:
    def __next__(self) -> 'Prim':
        """Return the next prim in the range.
        
        Returns:
            Prim: The next prim in the range
            
        Raises:
            StopIteration: When there are no more prims in the range
        """
        pass
    
    def __iter__(self) -> 'UsdPrimRangeIterator':
        """Return the iterator itself.
        
        Returns:
            UsdPrimRangeIterator: The iterator itself
        """
        pass
    
    def IsPostVisit(self) -> bool:
        """Check if the current prim is being visited after its children.
        
        Returns:
            bool: True if the current prim is being visited after its children, False otherwise
        """
        pass
    
    def PruneChildren(self) -> None:
        """Skip the children of the current prim."""
        pass

class UsdStageCache:
    def __init__(self) -> None:
        """Initialize a new stage cache."""
        pass
    
    def Insert(self, stage: 'Stage') -> None:
        """Insert a stage into the cache.
        
        Args:
            stage: The stage to insert
        """
        pass
    
    def Find(self, identifier: str) -> Optional['Stage']:
        """Find a stage in the cache by its identifier.
        
        Args:
            identifier: The identifier of the stage to find
            
        Returns:
            Optional[Stage]: The found stage, or None if not found
        """
        pass
    
    def Erase(self, stage: 'Stage') -> None:
        """Erase a stage from the cache.
        
        Args:
            stage: The stage to erase
        """
        pass
    
    def Clear(self) -> None:
        """Clear all stages from the cache."""
        pass
    
    def GetAllStages(self) -> List['Stage']:
        """Get all stages in the cache.
        
        Returns:
            List[Stage]: All stages in the cache
        """
        pass
    
    def Size(self) -> int:
        """Get the number of stages in the cache.
        
        Returns:
            int: The number of stages in the cache
        """
        pass
    
    def IsEmpty(self) -> bool:
        """Check if the cache is empty.
        
        Returns:
            bool: True if the cache is empty, False otherwise
        """
        pass
    
    def Contains(self, stage: 'Stage') -> bool:
        """Check if the cache contains the specified stage.
        
        Args:
            stage: The stage to check for
            
        Returns:
            bool: True if the cache contains the stage, False otherwise
        """
        pass
    
    def FindOneMatching(self, predicate: callable) -> Optional['Stage']:
        """Find a stage in the cache that matches the specified predicate.
        
        Args:
            predicate: A function that takes a stage and returns a boolean
            
        Returns:
            Optional[Stage]: A matching stage, or None if none found
        """
        pass
    
    def FindAllMatching(self, predicate: callable) -> List['Stage']:
        """Find all stages in the cache that match the specified predicate.
        
        Args:
            predicate: A function that takes a stage and returns a boolean
            
        Returns:
            List[Stage]: All matching stages
        """
        pass

class UsdTimeCode:
    def __init__(self, time: float = 0.0) -> None:
        """Initialize a UsdTimeCode with the given time value.
        
        Args:
            time: The time value, defaults to 0.0
        """
        pass
    
    @staticmethod
    def Default() -> 'UsdTimeCode':
        """Return the default time code.
        
        Returns:
            UsdTimeCode: The default time code
        """
        pass
    
    @staticmethod
    def EarliestTime() -> 'UsdTimeCode':
        """Return the earliest possible time code.
        
        Returns:
            UsdTimeCode: The earliest possible time code
        """
        pass
    
    def GetValue(self) -> float:
        """Get the time value.
        
        Returns:
            float: The time value
        """
        pass
    
    def IsDefault(self) -> bool:
        """Check if this time code is the default time code.
        
        Returns:
            bool: True if this is the default time code, False otherwise
        """
        pass
    
    def __eq__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is equal to another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if the time codes are equal, False otherwise
        """
        pass
    
    def __ne__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is not equal to another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if the time codes are not equal, False otherwise
        """
        pass
    
    def __lt__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is less than another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if this time code is less than the other, False otherwise
        """
        pass
    
    def __gt__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is greater than another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if this time code is greater than the other, False otherwise
        """
        pass
    
    def __le__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is less than or equal to another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if this time code is less than or equal to the other, False otherwise
        """
        pass
    
    def __ge__(self, other: 'UsdTimeCode') -> bool:
        """Check if this time code is greater than or equal to another time code.
        
        Args:
            other: The other time code
            
        Returns:
            bool: True if this time code is greater than or equal to the other, False otherwise
        """
        pass
    
    @staticmethod
    def SafeStep(a: float, b: float, t: float) -> float:
        """Linearly interpolate between two time samples.
        
        Args:
            a: The first time sample
            b: The second time sample
            t: The interpolation parameter
            
        Returns:
            float: The interpolated time
        """
        pass


class UsdGeomMesh(UsdGeomGprim):
    """Represents a polygonal mesh in a USD stage.
    
    UsdGeomMesh is used to describe a 3D polygonal mesh with arbitrary topology.
    It supports features like points, normals, texture coordinates, and more.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomMesh':
        """Define a new mesh prim at the specified path.
        
        Args:
            stage: The stage in which to create the mesh
            path: The path at which to create the mesh
            
        Returns:
            UsdGeomMesh: The newly defined mesh
        """
        pass
    
    def GetPointsAttr(self) -> 'Attribute':
        """Get the points attribute.
        
        Returns:
            Attribute: The points attribute
        """
        pass
    
    def GetNormalsAttr(self) -> 'Attribute':
        """Get the normals attribute.
        
        Returns:
            Attribute: The normals attribute
        """
        pass
    
    def GetFaceVertexCountsAttr(self) -> 'Attribute':
        """Get the face vertex counts attribute.
        
        Returns:
            Attribute: The face vertex counts attribute
        """
        pass
    
    def GetFaceVertexIndicesAttr(self) -> 'Attribute':
        """Get the face vertex indices attribute.
        
        Returns:
            Attribute: The face vertex indices attribute
        """
        pass
    
    def GetSubdivisionSchemeAttr(self) -> 'Attribute':
        """Get the subdivision scheme attribute.
        
        Returns:
            Attribute: The subdivision scheme attribute
        """
        pass
    
    def GetTriangleSubdivisionRuleAttr(self) -> 'Attribute':
        """Get the triangle subdivision rule attribute.
        
        Returns:
            Attribute: The triangle subdivision rule attribute
        """
        pass
    
    def GetInterpolateBoundaryAttr(self) -> 'Attribute':
        """Get the interpolate boundary attribute.
        
        Returns:
            Attribute: The interpolate boundary attribute
        """
        pass
    
    def GetFaceVaryingLinearInterpolationAttr(self) -> 'Attribute':
        """Get the face varying linear interpolation attribute.
        
        Returns:
            Attribute: The face varying linear interpolation attribute
        """
        pass
    
    def GetHoleIndicesAttr(self) -> 'Attribute':
        """Get the hole indices attribute.
        
        Returns:
            Attribute: The hole indices attribute
        """
        pass
    
    def GetCornerIndicesAttr(self) -> 'Attribute':
        """Get the corner indices attribute.
        
        Returns:
            Attribute: The corner indices attribute
        """
        pass
    
    def GetCornerSharpnessesAttr(self) -> 'Attribute':
        """Get the corner sharpnesses attribute.
        
        Returns:
            Attribute: The corner sharpnesses attribute
        """
        pass
    
    def GetCreaseIndicesAttr(self) -> 'Attribute':
        """Get the crease indices attribute.
        
        Returns:
            Attribute: The crease indices attribute
        """
        pass
    
    def GetCreaseLengthsAttr(self) -> 'Attribute':
        """Get the crease lengths attribute.
        
        Returns:
            Attribute: The crease lengths attribute
        """
        pass
    
    def GetCreaseSharpnessesAttr(self) -> 'Attribute':
        """Get the crease sharpnesses attribute.
        
        Returns:
            Attribute: The crease sharpnesses attribute
        """
        pass
    
    def GetPrimvarsAPI(self) -> Any:
        """Get the primvars API for this mesh.
        
        Returns:
            Any: The primvars API
        """
        pass
    
    def CreatePointsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the points attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created points attribute
        """
        pass
    
    def CreateNormalsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the normals attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created normals attribute
        """
        pass

class UsdGeomSphere(UsdGeomGprim):
    """Represents a sphere primitive in a USD stage.
    
    UsdGeomSphere defines a simple sphere volume with a radius.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomSphere':
        """Define a new sphere prim at the specified path.
        
        Args:
            stage: The stage in which to create the sphere
            path: The path at which to create the sphere
            
        Returns:
            UsdGeomSphere: The newly defined sphere
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def CreateRadiusAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the radius attribute.
        
        Args:
            defaultValue: The default value for the radius
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created radius attribute
        """
        pass

class UsdShadeShader(UsdGeomXformable):
    """Represents a shader in a USD stage.
    
    UsdShadeShader represents a shader node in a shading network.
    It can have inputs, outputs, and a shader ID.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdShadeShader':
        """Define a new shader prim at the specified path.
        
        Args:
            stage: The stage in which to create the shader
            path: The path at which to create the shader
            
        Returns:
            UsdShadeShader: The newly defined shader
        """
        pass
    
    def GetIdAttr(self) -> 'Attribute':
        """Get the shader ID attribute.
        
        Returns:
            Attribute: The shader ID attribute
        """
        pass
    
    def CreateInput(self, name: str, typeName: str) -> 'Attribute':
        """Create a new input parameter for the shader.
        
        Args:
            name: The name of the input parameter
            typeName: The type of the input parameter
            
        Returns:
            Attribute: The created input parameter
        """
        pass
    
    def CreateOutput(self, name: str, typeName: str) -> 'Attribute':
        """Create a new output parameter for the shader.
        
        Args:
            name: The name of the output parameter
            typeName: The type of the output parameter
            
        Returns:
            Attribute: The created output parameter
        """
        pass
    
    def SetSourceAsset(self, identifier: str, resolvedPath: str = "", assetType: str = "") -> bool:
        """Set the source asset for the shader.
        
        Args:
            identifier: The asset identifier
            resolvedPath: The resolved path to the asset
            assetType: The type of the asset
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetSourceAsset(self, assetType: str = "") -> tuple:
        """Get the source asset for the shader.
        
        Args:
            assetType: The type of the asset
            
        Returns:
            tuple: A tuple containing the asset identifier and resolved path
        """
        pass
    
    def GetImplementationSourceAttr(self) -> 'Attribute':
        """Get the implementation source attribute.
        
        Returns:
            Attribute: The implementation source attribute
        """
        pass

class UsdShadeMaterial(UsdGeomXformable):
    """Represents a material in a USD stage.
    
    UsdShadeMaterial represents a material with shading networks for different
    rendering contexts such as surface, displacement, and volume.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdShadeMaterial':
        """Define a new material prim at the specified path.
        
        Args:
            stage: The stage in which to create the material
            path: The path at which to create the material
            
        Returns:
            UsdShadeMaterial: The newly defined material
        """
        pass
    
    def CreateSurfaceOutput(self) -> 'Attribute':
        """Create the surface output for the material.
        
        Returns:
            Attribute: The created surface output
        """
        pass
    
    def GetSurfaceOutput(self) -> 'Attribute':
        """Get the surface output attribute.
        
        Returns:
            Attribute: The surface output attribute
        """
        pass
    
    def CreateDisplacementOutput(self) -> 'Attribute':
        """Create the displacement output for the material.
        
        Returns:
            Attribute: The created displacement output
        """
        pass
    
    def GetDisplacementOutput(self) -> 'Attribute':
        """Get the displacement output attribute.
        
        Returns:
            Attribute: The displacement output attribute
        """
        pass
    
    def CreateVolumeOutput(self) -> 'Attribute':
        """Create the volume output for the material.
        
        Returns:
            Attribute: The created volume output
        """
        pass
    
    def GetVolumeOutput(self) -> 'Attribute':
        """Get the volume output attribute.
        
        Returns:
            Attribute: The volume output attribute
        """
        pass
    
    def ConnectSurfaceSource(self, surfaceShader: 'UsdShadeShader') -> bool:
        """Connect a surface shader to the surface output.
        
        Args:
            surfaceShader: The surface shader to connect
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def ConnectDisplacementSource(self, displacementShader: 'UsdShadeShader') -> bool:
        """Connect a displacement shader to the displacement output.
        
        Args:
            displacementShader: The displacement shader to connect
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def ConnectVolumeSource(self, volumeShader: 'UsdShadeShader') -> bool:
        """Connect a volume shader to the volume output.
        
        Args:
            volumeShader: The volume shader to connect
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass

class UsdGeomCamera(UsdGeomXformable):
    """Represents a camera in a USD stage.
    
    UsdGeomCamera defines camera properties like focal length, aperture,
    clipping range, projection, etc.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomCamera':
        """Define a new camera prim at the specified path.
        
        Args:
            stage: The stage in which to create the camera
            path: The path at which to create the camera
            
        Returns:
            UsdGeomCamera: The newly defined camera
        """
        pass
    
    def GetFocalLengthAttr(self) -> 'Attribute':
        """Get the focal length attribute.
        
        Returns:
            Attribute: The focal length attribute
        """
        pass
    
    def GetHorizontalApertureAttr(self) -> 'Attribute':
        """Get the horizontal aperture attribute.
        
        Returns:
            Attribute: The horizontal aperture attribute
        """
        pass
    
    def GetVerticalApertureAttr(self) -> 'Attribute':
        """Get the vertical aperture attribute.
        
        Returns:
            Attribute: The vertical aperture attribute
        """
        pass
    
    def GetClippingRangeAttr(self) -> 'Attribute':
        """Get the clipping range attribute.
        
        Returns:
            Attribute: The clipping range attribute
        """
        pass
    
    def GetProjectionAttr(self) -> 'Attribute':
        """Get the projection attribute.
        
        Returns:
            Attribute: The projection attribute
        """
        pass
    
    def GetFocusDistanceAttr(self) -> 'Attribute':
        """Get the focus distance attribute.
        
        Returns:
            Attribute: The focus distance attribute
        """
        pass
    
    def GetFStopAttr(self) -> 'Attribute':
        """Get the f-stop attribute.
        
        Returns:
            Attribute: The f-stop attribute
        """
        pass
    
    def CreateFocalLengthAttr(self, defaultValue=50.0, writeSparsely=False) -> 'Attribute':
        """Create the focal length attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created focal length attribute
        """
        pass
    
    def CreateHorizontalApertureAttr(self, defaultValue=36.0, writeSparsely=False) -> 'Attribute':
        """Create the horizontal aperture attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created horizontal aperture attribute
        """
        pass
    
    def CreateVerticalApertureAttr(self, defaultValue=24.0, writeSparsely=False) -> 'Attribute':
        """Create the vertical aperture attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created vertical aperture attribute
        """
        pass

class UsdGeomCube(UsdGeomGprim):
    """Represents a cube primitive in a USD stage.
    
    UsdGeomCube defines a cubic volume with a specified size.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomCube':
        """Define a new cube prim at the specified path.
        
        Args:
            stage: The stage in which to create the cube
            path: The path at which to create the cube
            
        Returns:
            UsdGeomCube: The newly defined cube
        """
        pass
    
    def GetSizeAttr(self) -> 'Attribute':
        """Get the size attribute.
        
        Returns:
            Attribute: The size attribute
        """
        pass
    
    def CreateSizeAttr(self, defaultValue=2.0, writeSparsely=False) -> 'Attribute':
        """Create the size attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created size attribute
        """
        pass

class UsdGeomCone(UsdGeomGprim):
    """Represents a cone primitive in a USD stage.
    
    UsdGeomCone defines a conical volume with a specified radius and height.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomCone':
        """Define a new cone prim at the specified path.
        
        Args:
            stage: The stage in which to create the cone
            path: The path at which to create the cone
            
        Returns:
            UsdGeomCone: The newly defined cone
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def GetHeightAttr(self) -> 'Attribute':
        """Get the height attribute.
        
        Returns:
            Attribute: The height attribute
        """
        pass
    
    def CreateRadiusAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the radius attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created radius attribute
        """
        pass
    
    def CreateHeightAttr(self, defaultValue=2.0, writeSparsely=False) -> 'Attribute':
        """Create the height attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created height attribute
        """
        pass

class UsdGeomCylinder(UsdGeomGprim):
    """Represents a cylinder primitive in a USD stage.
    
    UsdGeomCylinder defines a cylindrical volume with a specified radius and height.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomCylinder':
        """Define a new cylinder prim at the specified path.
        
        Args:
            stage: The stage in which to create the cylinder
            path: The path at which to create the cylinder
            
        Returns:
            UsdGeomCylinder: The newly defined cylinder
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def GetHeightAttr(self) -> 'Attribute':
        """Get the height attribute.
        
        Returns:
            Attribute: The height attribute
        """
        pass
    
    def GetAxisAttr(self) -> 'Attribute':
        """Get the axis attribute.
        
        Returns:
            Attribute: The axis attribute
        """
        pass
    
    def CreateRadiusAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the radius attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created radius attribute
        """
        pass
    
    def CreateHeightAttr(self, defaultValue=2.0, writeSparsely=False) -> 'Attribute':
        """Create the height attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created height attribute
        """
        pass

class UsdGeomPoints(UsdGeomGprim):
    """Represents a point cloud in a USD stage.
    
    UsdGeomPoints defines a set of 3D points with optional widths and IDs.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomPoints':
        """Define a new points prim at the specified path.
        
        Args:
            stage: The stage in which to create the points
            path: The path at which to create the points
            
        Returns:
            UsdGeomPoints: The newly defined points
        """
        pass
    
    def GetPointsAttr(self) -> 'Attribute':
        """Get the points attribute.
        
        Returns:
            Attribute: The points attribute
        """
        pass
    
    def GetWidthsAttr(self) -> 'Attribute':
        """Get the widths attribute.
        
        Returns:
            Attribute: The widths attribute
        """
        pass
    
    def GetIdsAttr(self) -> 'Attribute':
        """Get the ids attribute.
        
        Returns:
            Attribute: The ids attribute
        """
        pass
    
    def CreatePointsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the points attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created points attribute
        """
        pass
    
    def CreateWidthsAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the widths attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created widths attribute
        """
        pass
    
    def CreateIdsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the ids attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created ids attribute
        """
        pass

class UsdGeomBasisCurves(UsdGeomGprim):
    """Represents parametric curves in a USD stage.
    
    UsdGeomBasisCurves defines a set of parametric curves using control points.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomBasisCurves':
        """Define a new basis curves prim at the specified path.
        
        Args:
            stage: The stage in which to create the curves
            path: The path at which to create the curves
            
        Returns:
            UsdGeomBasisCurves: The newly defined curves
        """
        pass
    
    def GetPointsAttr(self) -> 'Attribute':
        """Get the points attribute.
        
        Returns:
            Attribute: The points attribute
        """
        pass
    
    def GetCurveVertexCountsAttr(self) -> 'Attribute':
        """Get the curve vertex counts attribute.
        
        Returns:
            Attribute: The curve vertex counts attribute
        """
        pass
    
    def GetWidthsAttr(self) -> 'Attribute':
        """Get the widths attribute.
        
        Returns:
            Attribute: The widths attribute
        """
        pass
    
    def GetBasisAttr(self) -> 'Attribute':
        """Get the basis attribute.
        
        Returns:
            Attribute: The basis attribute
        """
        pass
    
    def GetTypeAttr(self) -> 'Attribute':
        """Get the type attribute.
        
        Returns:
            Attribute: The type attribute
        """
        pass
    
    def GetWrapAttr(self) -> 'Attribute':
        """Get the wrap attribute.
        
        Returns:
            Attribute: The wrap attribute
        """
        pass
    
    def CreatePointsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the points attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created points attribute
        """
        pass
    
    def CreateCurveVertexCountsAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the curve vertex counts attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created curve vertex counts attribute
        """
        pass

class UsdLuxDistantLight(UsdGeomXformable):
    """Represents a distant light in a USD stage.
    
    UsdLuxDistantLight defines a distant light source that emits parallel light rays.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdLuxDistantLight':
        """Define a new distant light prim at the specified path.
        
        Args:
            stage: The stage in which to create the light
            path: The path at which to create the light
            
        Returns:
            UsdLuxDistantLight: The newly defined distant light
        """
        pass
    
    def GetAngleAttr(self) -> 'Attribute':
        """Get the angle attribute.
        
        Returns:
            Attribute: The angle attribute
        """
        pass
    
    def GetIntensityAttr(self) -> 'Attribute':
        """Get the intensity attribute.
        
        Returns:
            Attribute: The intensity attribute
        """
        pass
    
    def GetColorAttr(self) -> 'Attribute':
        """Get the color attribute.
        
        Returns:
            Attribute: The color attribute
        """
        pass
    
    def CreateAngleAttr(self, defaultValue=0.0, writeSparsely=False) -> 'Attribute':
        """Create the angle attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created angle attribute
        """
        pass
    
    def CreateIntensityAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the intensity attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created intensity attribute
        """
        pass
    
    def CreateColorAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the color attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created color attribute
        """
        pass

class UsdLuxDiskLight(UsdGeomXformable):
    """Represents a disk light in a USD stage.
    
    UsdLuxDiskLight defines a disk-shaped light source.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdLuxDiskLight':
        """Define a new disk light prim at the specified path.
        
        Args:
            stage: The stage in which to create the light
            path: The path at which to create the light
            
        Returns:
            UsdLuxDiskLight: The newly defined disk light
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def GetIntensityAttr(self) -> 'Attribute':
        """Get the intensity attribute.
        
        Returns:
            Attribute: The intensity attribute
        """
        pass
    
    def GetColorAttr(self) -> 'Attribute':
        """Get the color attribute.
        
        Returns:
            Attribute: The color attribute
        """
        pass
    
    def CreateRadiusAttr(self, defaultValue=0.5, writeSparsely=False) -> 'Attribute':
        """Create the radius attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created radius attribute
        """
        pass
    
    def CreateIntensityAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the intensity attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created intensity attribute
        """
        pass
    
    def CreateColorAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the color attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created color attribute
        """
        pass

class UsdPhysicsRigidBodyAPI:
    """API schema for representing rigid body physics on a prim.
    
    UsdPhysicsRigidBodyAPI provides attributes for configuring rigid body physics
    simulation, including mass, velocities, and other physical properties.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdPhysicsRigidBodyAPI':
        """Apply the rigid body API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdPhysicsRigidBodyAPI: The applied rigid body API
        """
        pass
    
    def GetMassAttr(self) -> 'Attribute':
        """Get the mass attribute.
        
        Returns:
            Attribute: The mass attribute
        """
        pass
    
    def GetVelocityAttr(self) -> 'Attribute':
        """Get the velocity attribute.
        
        Returns:
            Attribute: The velocity attribute
        """
        pass
    
    def GetAngularVelocityAttr(self) -> 'Attribute':
        """Get the angular velocity attribute.
        
        Returns:
            Attribute: The angular velocity attribute
        """
        pass
    
    def CreateMassAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the mass attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created mass attribute
        """
        pass
    
    def CreateVelocityAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the velocity attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created velocity attribute
        """
        pass
    
    def CreateAngularVelocityAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the angular velocity attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created angular velocity attribute
        """
        pass
    
    def GetRigidBodyEnabledAttr(self) -> 'Attribute':
        """Get the rigid body enabled attribute.
        
        Returns:
            Attribute: The rigid body enabled attribute
        """
        pass
    
    def GetKinematicEnabledAttr(self) -> 'Attribute':
        """Get the kinematic enabled attribute.
        
        Returns:
            Attribute: The kinematic enabled attribute
        """
        pass
    
    def GetStartsAsleepAttr(self) -> 'Attribute':
        """Get the starts asleep attribute.
        
        Returns:
            Attribute: The starts asleep attribute
        """
        pass

class UsdRenderSettings:
    """Represents render settings in a USD stage.
    
    UsdRenderSettings defines global render settings like resolution, aspect ratio,
    and other renderer-specific settings.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdRenderSettings':
        """Define a new render settings prim at the specified path.
        
        Args:
            stage: The stage in which to create the render settings
            path: The path at which to create the render settings
            
        Returns:
            UsdRenderSettings: The newly defined render settings
        """
        pass
    
    def GetResolutionAttr(self) -> 'Attribute':
        """Get the resolution attribute.
        
        Returns:
            Attribute: The resolution attribute
        """
        pass
    
    def GetPixelAspectRatioAttr(self) -> 'Attribute':
        """Get the pixel aspect ratio attribute.
        
        Returns:
            Attribute: The pixel aspect ratio attribute
        """
        pass
    
    def GetAspectRatioConformPolicyAttr(self) -> 'Attribute':
        """Get the aspect ratio conform policy attribute.
        
        Returns:
            Attribute: The aspect ratio conform policy attribute
        """
        pass
    
    def CreateResolutionAttr(self, defaultValue=None, writeSparsely=False) -> 'Attribute':
        """Create the resolution attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created resolution attribute
        """
        pass
    
    def CreatePixelAspectRatioAttr(self, defaultValue=1.0, writeSparsely=False) -> 'Attribute':
        """Create the pixel aspect ratio attribute.
        
        Args:
            defaultValue: The default value for the attribute
            writeSparsely: Whether to write sparsely
            
        Returns:
            Attribute: The created pixel aspect ratio attribute
        """
        pass
    
    def GetRenderProductsRel(self) -> 'Relationship':
        """Get the render products relationship.
        
        Returns:
            Relationship: The render products relationship
        """
        pass
    
    def GetProductsRel(self) -> 'Relationship':
        """Get the products relationship.
        
        Returns:
            Relationship: The products relationship
        """
        pass
    
    def GetActiveCamera(self) -> str:
        """Get the active camera path.
        
        Returns:
            str: The active camera path
        """
        pass
    
    def SetActiveCamera(self, path: str) -> bool:
        """Set the active camera path.
        
        Args:
            path: The active camera path
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
class UsdGeomXformable:
    """Base class for all transformable USD geometry types.
    
    UsdGeomXformable is an abstract base class for all USD prim types that can
    be positioned and oriented with a sequence of transformation operations.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomXformable':
        """Define a new xformable prim at the specified path.
        
        Args:
            stage: The stage in which to create the prim
            path: The path at which to create the prim
            
        Returns:
            UsdGeomXformable: The newly defined xformable prim
        """
        pass
    
    def GetXformOpOrderAttr(self) -> 'Attribute':
        """Get the xform operation order attribute.
        
        Returns:
            Attribute: The xform operation order attribute
        """
        pass
    
    def AddTranslateOp(self, opSuffix: str = '') -> 'XformOp':
        """Add a translate operation to the xformable.
        
        Args:
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added translate operation
        """
        pass
    
    def AddRotateXYZOp(self, opSuffix: str = '') -> 'XformOp':
        """Add a rotate XYZ operation to the xformable.
        
        Args:
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added rotate XYZ operation
        """
        pass
    
    def AddScaleOp(self, opSuffix: str = '') -> 'XformOp':
        """Add a scale operation to the xformable.
        
        Args:
            opSuffix: An optional suffix for the operation
            
        Returns:
            XformOp: The newly added scale operation
        """
        pass
class UsdGeomGprim(UsdGeomXformable):
    """Base class for all geometric primitives in USD.
    
    UsdGeomGprim is an abstract base class for all USD geometric primitives,
    providing common attributes like display color, opacity, and purpose.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomGprim':
        """Define a new geometric primitive at the specified path.
        
        Args:
            stage: The stage in which to create the prim
            path: The path at which to create the prim
            
        Returns:
            UsdGeomGprim: The newly defined geometric primitive
        """
        pass
    
    def GetDisplayColorAttr(self) -> 'Attribute':
        """Get the display color attribute.
        
        Returns:
            Attribute: The display color attribute
        """
        pass
    
    def GetDisplayOpacityAttr(self) -> 'Attribute':
        """Get the display opacity attribute.
        
        Returns:
            Attribute: The display opacity attribute
        """
        pass
    
    def GetPurposeAttr(self) -> 'Attribute':
        """Get the purpose attribute.
        
        Returns:
            Attribute: The purpose attribute
        """
        pass
class UsdGeomPlane(UsdGeomGprim):
    """Represents a plane primitive in a USD stage.
    
    UsdGeomPlane defines a plane with a specified size.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomPlane':
        """Define a new plane prim at the specified path.
        
        Args:
            stage: The stage in which to create the plane
            path: The path at which to create the plane
            
        Returns:
            UsdGeomPlane: The newly defined plane
        """
        pass
    
    def GetSizeAttr(self) -> 'Attribute':
        """Get the size attribute.
        
        Returns:
            Attribute: The size attribute
        """
        pass
class UsdGeomCapsule(UsdGeomGprim):
    """Represents a capsule primitive in a USD stage.
    
    UsdGeomCapsule defines a capsule with a specified radius and height.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomCapsule':
        """Define a new capsule prim at the specified path.
        
        Args:
            stage: The stage in which to create the capsule
            path: The path at which to create the capsule
            
        Returns:
            UsdGeomCapsule: The newly defined capsule
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def GetHeightAttr(self) -> 'Attribute':
        """Get the height attribute.
        
        Returns:
            Attribute: The height attribute
        """
        pass
class UsdShadeMaterialBindingAPI:
    """API for binding materials to prims.
    
    UsdShadeMaterialBindingAPI provides methods for binding materials to prims
    and querying those bindings.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdShadeMaterialBindingAPI':
        """Apply the material binding API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdShadeMaterialBindingAPI: The applied material binding API
        """
        pass
    
    def Bind(self, material: 'UsdShadeMaterial') -> bool:
        """Bind the prim to the specified material.
        
        Args:
            material: The material to bind to the prim
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetDirectBinding(self) -> 'UsdShadeMaterialBindingAPI.DirectBinding':
        """Get the direct binding for this prim.
        
        Returns:
            UsdShadeMaterialBindingAPI.DirectBinding: The direct binding
        """
        pass
    
    class DirectBinding:
        """Represents a direct material binding on a prim."""
        
        def GetMaterial(self) -> 'UsdShadeMaterial':
            """Get the bound material.
            
            Returns:
                UsdShadeMaterial: The bound material
            """
            pass
class UsdShadeConnectableAPI:
    """API for connecting shader inputs and outputs.
    
    UsdShadeConnectableAPI provides methods for connecting shader inputs
    to outputs and querying those connections.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdShadeConnectableAPI':
        """Apply the connectable API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdShadeConnectableAPI: The applied connectable API
        """
        pass
    
    def ConnectToSource(self, inputName: str, source: 'UsdShadeConnectableAPI', sourceName: str) -> bool:
        """Connect an input to a source.
        
        Args:
            inputName: The name of the input to connect
            source: The source connectable
            sourceName: The name of the source output
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetConnectedSource(self, inputName: str) -> tuple:
        """Get the connected source for the specified input.
        
        Args:
            inputName: The name of the input
            
        Returns:
            tuple: A tuple containing the source connectable, source name, and type name
        """
        pass
class UsdCollectionAPI:
    """API for working with collections of prims.
    
    UsdCollectionAPI provides methods for creating and managing collections
    of prims through includes and excludes relationships.
    """
    
    @staticmethod
    def Apply(prim: 'Prim', name: str) -> 'UsdCollectionAPI':
        """Apply the collection API to the specified prim with the given name.
        
        Args:
            prim: The prim to which to apply the API
            name: The name of the collection
            
        Returns:
            UsdCollectionAPI: The applied collection API
        """
        pass
    
    def IncludePath(self, path: 'SdfPath') -> bool:
        """Include a path in the collection.
        
        Args:
            path: The path to include
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def ExcludePath(self, path: 'SdfPath') -> bool:
        """Exclude a path from the collection.
        
        Args:
            path: The path to exclude
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def GetIncludesRel(self) -> 'Relationship':
        """Get the includes relationship.
        
        Returns:
            Relationship: The includes relationship
        """
        pass
class Relationship:
    """Represents a relationship between prims in a USD stage.
    
    Relationship defines a connection between prims through targets.
    """
    
    def GetName(self) -> str:
        """Get the name of the relationship.
        
        Returns:
            str: The name of the relationship
        """
        pass
    
    def GetTargets(self) -> List['SdfPath']:
        """Get the targets of the relationship.
        
        Returns:
            List[SdfPath]: The targets of the relationship
        """
        pass
    
    def AddTarget(self, path: 'SdfPath') -> None:
        """Add a target to the relationship.
        
        Args:
            path: The path to add as a target
        """
        pass
    
    def RemoveTarget(self, path: 'SdfPath') -> None:
        """Remove a target from the relationship.
        
        Args:
            path: The path to remove as a target
        """
        pass
class UsdReferences:
    """Handles references to external USD files or prims.
    
    UsdReferences provides methods for adding, removing, and managing
    references to external USD files or prims within a prim.
    """
    
    def __init__(self, prim: 'Prim') -> None:
        """Initialize with the given prim.
        
        Args:
            prim: The prim for which to manage references
        """
        pass
    
    def AddReference(self, filePath: str, primPath: str = '', layerOffset: Any = None) -> bool:
        """Add a reference to the prim.
        
        Args:
            filePath: The file path to reference
            primPath: The prim path within the referenced file
            layerOffset: An optional layer offset
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def RemoveReference(self, filePath: str, primPath: str = '') -> bool:
        """Remove a reference from the prim.
        
        Args:
            filePath: The file path of the reference to remove
            primPath: The prim path within the referenced file
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def ClearReferences(self) -> bool:
        """Clear all references from the prim.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
class UsdPhysicsMeshCollisionAPI:
    """API for configuring mesh collision properties.
    
    UsdPhysicsMeshCollisionAPI provides methods for configuring how a mesh
    should be used for collision detection in physics simulations.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdPhysicsMeshCollisionAPI':
        """Apply the mesh collision API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdPhysicsMeshCollisionAPI: The applied mesh collision API
        """
        pass
    
    def GetApproximationAttr(self) -> 'Attribute':
        """Get the approximation attribute.
        
        Returns:
            Attribute: The approximation attribute
        """
        pass
    
    def GetMeshSimplificationAttr(self) -> 'Attribute':
        """Get the mesh simplification attribute.
        
        Returns:
            Attribute: The mesh simplification attribute
        """
        pass
class UsdSkelAnimation:
    """Represents skeletal animation data in a USD stage.
    
    UsdSkelAnimation defines animation data for a skeleton, including
    joint transforms over time.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdSkelAnimation':
        """Define a new skeleton animation prim at the specified path.
        
        Args:
            stage: The stage in which to create the animation
            path: The path at which to create the animation
            
        Returns:
            UsdSkelAnimation: The newly defined skeleton animation
        """
        pass
    
    def GetJointsAttr(self) -> 'Attribute':
        """Get the joints attribute.
        
        Returns:
            Attribute: The joints attribute
        """
        pass
    
    def GetRotationsAttr(self) -> 'Attribute':
        """Get the rotations attribute.
        
        Returns:
            Attribute: The rotations attribute
        """
        pass
    
    def GetTranslationsAttr(self) -> 'Attribute':
        """Get the translations attribute.
        
        Returns:
            Attribute: The translations attribute
        """
        pass
    
    def GetScalesAttr(self) -> 'Attribute':
        """Get the scales attribute.
        
        Returns:
            Attribute: The scales attribute
        """
        pass
class UsdSkelSkeleton:
    """Represents a skeleton in a USD stage.
    
    UsdSkelSkeleton defines a hierarchy of joints for skeletal animation.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdSkelSkeleton':
        """Define a new skeleton prim at the specified path.
        
        Args:
            stage: The stage in which to create the skeleton
            path: The path at which to create the skeleton
            
        Returns:
            UsdSkelSkeleton: The newly defined skeleton
        """
        pass
    
    def GetJointsAttr(self) -> 'Attribute':
        """Get the joints attribute.
        
        Returns:
            Attribute: The joints attribute
        """
        pass
    
    def GetBindTransformsAttr(self) -> 'Attribute':
        """Get the bind transforms attribute.
        
        Returns:
            Attribute: The bind transforms attribute
        """
        pass
    
    def GetRestTransformsAttr(self) -> 'Attribute':
        """Get the rest transforms attribute.
        
        Returns:
            Attribute: The rest transforms attribute
        """
        pass
class UsdSkelBindingAPI:
    """API for binding geometry to skeletons.
    
    UsdSkelBindingAPI provides methods for binding geometry prims to skeletons
    for skeletal animation.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdSkelBindingAPI':
        """Apply the skeleton binding API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdSkelBindingAPI: The applied skeleton binding API
        """
        pass
    
    def GetAnimationSourceRel(self) -> 'Relationship':
        """Get the animation source relationship.
        
        Returns:
            Relationship: The animation source relationship
        """
        pass
    
    def GetSkeletonRel(self) -> 'Relationship':
        """Get the skeleton relationship.
        
        Returns:
            Relationship: The skeleton relationship
        """
        pass
    
    def GetJointsAttr(self) -> 'Attribute':
        """Get the joints attribute.
        
        Returns:
            Attribute: The joints attribute
        """
        pass
class UsdSkelRoot:
    """Represents a skeleton root in a USD stage.
    
    UsdSkelRoot defines a scope for skeletal animation data.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdSkelRoot':
        """Define a new skeleton root prim at the specified path.
        
        Args:
            stage: The stage in which to create the root
            path: The path at which to create the root
            
        Returns:
            UsdSkelRoot: The newly defined skeleton root
        """
        pass
class UsdSkelSkinningQuery:
    """Query object for skinning data.
    
    UsdSkelSkinningQuery provides methods for querying skinning data
    for a specific prim.
    """
    
    def __init__(self, skelQuery: Any, prim: 'Prim') -> None:
        """Initialize with the given skeleton query and prim.
        
        Args:
            skelQuery: The skeleton query
            prim: The prim to query
        """
        pass
    
    def GetJointIndices(self) -> List[int]:
        """Get the joint indices for skinning.
        
        Returns:
            List[int]: The joint indices
        """
        pass
    
    def GetJointWeights(self) -> List[float]:
        """Get the joint weights for skinning.
        
        Returns:
            List[float]: The joint weights
        """
        pass
    
    def ComputeJointSkinningTransforms(self, time: Any = None) -> List[Any]:
        """Compute the joint skinning transforms at the given time.
        
        Args:
            time: The time at which to compute the transforms
            
        Returns:
            List[Any]: The computed joint skinning transforms
        """
        pass
class UsdGeomScope(UsdGeomXformable):
    """Represents a scope in a USD stage.
    
    UsdGeomScope defines an organizational grouping of prims.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomScope':
        """Define a new scope prim at the specified path.
        
        Args:
            stage: The stage in which to create the scope
            path: The path at which to create the scope
            
        Returns:
            UsdGeomScope: The newly defined scope
        """
        pass
class UsdGeomTokens:
    """Provides access to common USD geometry tokens.
    
    UsdGeomTokens contains methods for accessing common tokens used
    in USD geometry schemas.
    """
    
    @staticmethod
    def GetSchemaAttributeNames() -> List[str]:
        """Get the schema attribute names.
        
        Returns:
            List[str]: The schema attribute names
        """
        pass
class UsdLuxSphereLight(UsdGeomXformable):
    """Represents a sphere light in a USD stage.
    
    UsdLuxSphereLight defines a spherical light source.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdLuxSphereLight':
        """Define a new sphere light prim at the specified path.
        
        Args:
            stage: The stage in which to create the light
            path: The path at which to create the light
            
        Returns:
            UsdLuxSphereLight: The newly defined sphere light
        """
        pass
    
    def GetRadiusAttr(self) -> 'Attribute':
        """Get the radius attribute.
        
        Returns:
            Attribute: The radius attribute
        """
        pass
    
    def GetIntensityAttr(self) -> 'Attribute':
        """Get the intensity attribute.
        
        Returns:
            Attribute: The intensity attribute
        """
        pass
    
    def GetColorAttr(self) -> 'Attribute':
        """Get the color attribute.
        
        Returns:
            Attribute: The color attribute
        """
        pass
class UsdLuxRectLight(UsdGeomXformable):
    """Represents a rectangular light in a USD stage.
    
    UsdLuxRectLight defines a rectangular light source.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdLuxRectLight':
        """Define a new rect light prim at the specified path.
        
        Args:
            stage: The stage in which to create the light
            path: The path at which to create the light
            
        Returns:
            UsdLuxRectLight: The newly defined rect light
        """
        pass
    
    def GetWidthAttr(self) -> 'Attribute':
        """Get the width attribute.
        
        Returns:
            Attribute: The width attribute
        """
        pass
    
    def GetHeightAttr(self) -> 'Attribute':
        """Get the height attribute.
        
        Returns:
            Attribute: The height attribute
        """
        pass
    
    def GetIntensityAttr(self) -> 'Attribute':
        """Get the intensity attribute.
        
        Returns:
            Attribute: The intensity attribute
        """
        pass
class UsdPhysicsJointAPI:
    """API for configuring physical joints between prims.
    
    UsdPhysicsJointAPI provides methods for configuring physical joints
    between prims for physics simulations.
    """
    
    @staticmethod
    def Apply(prim: 'Prim') -> 'UsdPhysicsJointAPI':
        """Apply the joint API to the specified prim.
        
        Args:
            prim: The prim to which to apply the API
            
        Returns:
            UsdPhysicsJointAPI: The applied joint API
        """
        pass
    
    def GetBody0Rel(self) -> 'Relationship':
        """Get the first body relationship.
        
        Returns:
            Relationship: The first body relationship
        """
        pass
    
    def GetBody1Rel(self) -> 'Relationship':
        """Get the second body relationship.
        
        Returns:
            Relationship: The second body relationship
        """
        pass
    
    def GetLocalPos0Attr(self) -> 'Attribute':
        """Get the local position for the first body.
        
        Returns:
            Attribute: The local position attribute for the first body
        """
        pass
class UsdGeomSubset:
    """Represents a subset of a geometry in a USD stage.
    
    UsdGeomSubset defines a subset of elements (faces, points, etc.) of a geometry.
    """
    
    @staticmethod
    def Define(stage: 'Stage', path: 'SdfPath') -> 'UsdGeomSubset':
        """Define a new geometry subset at the specified path.
        
        Args:
            stage: The stage in which to create the subset
            path: The path at which to create the subset
            
        Returns:
            UsdGeomSubset: The newly defined geometry subset
        """
        pass
    
    def GetIndicesAttr(self) -> 'Attribute':
        """Get the indices attribute.
        
        Returns:
            Attribute: The indices attribute
        """
        pass
    
    def GetElementTypeAttr(self) -> 'Attribute':
        """Get the element type attribute.
        
        Returns:
            Attribute: The element type attribute
        """
        pass
class UsdShadeOutput:
    """Represents an output parameter on a shader.
    
    UsdShadeOutput defines an output parameter for a shader node.
    """
    
    def __init__(self, attr: 'Attribute') -> None:
        """Initialize with the given attribute.
        
        Args:
            attr: The attribute representing the output
        """
        pass
    
    def GetTypeName(self) -> str:
        """Get the type name of the output.
        
        Returns:
            str: The type name of the output
        """
        pass
    
    def ConnectToSource(self, source: 'UsdShadeConnectableAPI', sourceName: str) -> bool:
        """Connect the output to a source.
        
        Args:
            source: The source connectable
            sourceName: The name of the source output
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
class UsdShadeInput:
    """Represents an input parameter on a shader.
    
    UsdShadeInput defines an input parameter for a shader node.
    """
    
    def __init__(self, attr: 'Attribute') -> None:
        """Initialize with the given attribute.
        
        Args:
            attr: The attribute representing the input
        """
        pass
    
    def GetTypeName(self) -> str:
        """Get the type name of the input.
        
        Returns:
            str: The type name of the input
        """
        pass
    
    def Get(self, time: Any = None) -> Any:
        """Get the value of the input at the specified time.
        
        Args:
            time: The time at which to get the value
            
        Returns:
            Any: The value of the input
        """
        pass
    
    def Set(self, value: Any, time: Any = None) -> bool:
        """Set the value of the input at the specified time.
        
        Args:
            value: The value to set
            time: The time at which to set the value
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
class UsdUtils:
    """Utility functions for working with USD files.
    
    UsdUtils provides utility functions for common USD operations.
    """
    
    @staticmethod
    def CreateNewUsdzPackage(usdzFilePath: str, contents: List[str]) -> bool:
        """Create a new USDZ package at the specified path with the given contents.
        
        Args:
            usdzFilePath: The path at which to create the USDZ package
            contents: A list of file paths to include in the package
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @staticmethod
    def ExtractUsdzContents(usdzFilePath: str, outDir: str) -> bool:
        """Extract the contents of a USDZ package to the specified directory.
        
        Args:
            usdzFilePath: The path of the USDZ package to extract
            outDir: The directory to which to extract the contents
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass