"""Processing Script to demonstrate how to copy a raster layer.

A use case of this is detailed at https://gis.stackexchange.com/questions/416616/feed-an-existing-raster-to-qgis-raster-destination-parameter-in-qgis-processing
"""

from qgis.core import (QgsProcessing,
                       QgsRasterLayer,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class CopyRasterAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER = 'INPUT_RASTER'
    OUTPUT = 'OUTPUT'
    
    def createInstance(self):
        return CopyRasterAlgorithm()

    def name(self):
        return 'Copy Raster'

    def displayName(self):
        return 'copyraster'

    def initAlgorithm(self, config=None):
       
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                'Input raster layer',
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                  self.OUTPUT,
                  'OUTPUT'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputraster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
     
        params = {
            'INPUT':inputraster,
            'OUTPUT': parameters['OUTPUT']
        }
        result = processing.run("gdal:translate", params, context=context)
    
        return {self.OUTPUT: result['OUTPUT']}