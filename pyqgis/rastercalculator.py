"""Processing Script to demonstrate syntax for Raster Calculator

This script just returns the input raster as output
"""

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class RasterCalcProcessingAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
   
    def createInstance(self):
        return RasterCalcProcessingAlgorithm()

    def name(self):
        return 'rastercalctest'

    def displayName(self):
        return 'rastercalctest'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT, 'INPUT', defaultValue=None
                
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                  self.OUTPUT, 'OUTPUT'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        output = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '\"{}@1\"'.format(input.name()),
            'EXTENT': None,
            'LAYERS': [input],
            'OUTPUT':  parameters['OUTPUT'],
        }
        result = processing.run('qgis:rastercalculator', params, context=context)
        return {self.OUTPUT: result['OUTPUT']}

