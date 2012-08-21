'''
Created on Aug 21, 2012

@author: Luís de Sousa [luis.desousa@tudor.lu]

Contains a class that wraps spatial data sets stored in the disk.
PRovides method to retrieve useful information on the data set.

Issues:
. Only tested with vector GML files

'''

gdal=False
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except Exception,e:
    gdal=False

class DataSet:
	""" """

	dataSet=None
	dataType=None
	spatialReference=None

	def __init__(self, path):

		self.dataType = self.getDataSet(path)
		print self.dataType
		self.getSpatialReference()
		print self.getEPSG() 
		print self.getBBox()
		print self.getBBox()[0]

	def getDataSet(self, path):
		"""
		:param path: String
		:returns: "raster" or "vector"
		"""

		#logging.debug("Importing given output [%s] using gdal" % output.value)
		print "Importing given output [%s] using gdal" % path
		#If dataset is XML it will make an error like ERROR 4: `/var/www/html/wpsoutputs/vectorout-26317EUFxeb' not recognised as a supported file format.
		self.dataSet = gdal.Open(path)

		if self.dataSet:
			return "raster"

		if not self.dataSet:
			#logging.debug("Importing given output [%s] using ogr" % output.value)
			print "Importing given output [%s] using ogr" % path
			self.dataSet = ogr.Open(path)

		if self.dataSet:
			return "vector"
		else:
			return None

	def getSpatialReference(self):
		"""
		Loads the Spatial Reference System definition.
		"""

		sr = osr.SpatialReference()
		if self.dataType == "raster":
			wkt = self.dataSet.GetProjection()
			res = sr.ImportFromWkt(wkt)
			if res == 0:
				self.spatialReference = sr
		elif self.dataType == "vector":
			layer = self.dataSet.GetLayer()
			ref = layer.GetSpatialRef()
			if ref:
				self.spatialReference = ref

	def getEPSG(self):
		"""
		:return: Spatial Reference System EPSG code
		"""

		code=None
		if self.spatialReference.IsProjected():
			code = self.spatialReference.GetAuthorityCode("PROJCS")
		else:
			code = spatialReference.GetAuthorityCode("GEOGCS")
		return code

	def getBBox(self):
		"""
		:return: bounding box of the dataset
		"""

		if self.dataType == "raster":
			geotransform = self.dataSet.GetGeoTransform()
			height = self.dataSet.RasterYSize
			width = self.dataSet.RasterXSize
			return (geotransform[0],
				    geotransform[3]+geotransform[5]*self.dataSet.RasterYSize,
				    geotransform[0]+geotransform[1]*self.dataSet.RasterXSize,
				    geotransform[3])
		else:
			layer = self.dataSet.GetLayer()
			return layer.GetExtent()


# Testing

x = DataSet("/home/desousa/Tudor/MUSIC/Ludwigsburg/simpleLineLudwigsburgWithCRS.gml")









