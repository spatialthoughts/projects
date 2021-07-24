"""Processing Script to Apply a Filter to a Vector Layer

Example of how to write a processing scirpt that doesn't 
return a new layer but applies a filter/selection on 
input.
"""

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterVectorLayer)
from qgis import processing


class FilterLayerAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    COUNTRY = 'COUNTRY'
    COUNTRIES = ['United States of America', 'CANADA', 'MEXICO']
    
    def createInstance(self):
        return FilterLayerAlgorithm()

    def name(self):
        return 'filterlayer'

    def displayName(self):
        return 'Filter Layer'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                'Input layer',
                types=[QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(self.COUNTRY,
                'Select a Country',
                self.COUNTRIES,
                defaultValue='United States of America'
            )
        )
                

    def processAlgorithm(self, parameters, context, feedback):
        input = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        country = self.COUNTRIES[self.parameterAsEnum(parameters, self.COUNTRY, context)]

        expression = '\"NAME\" = \'{}\''.format(country)
        input.setSubsetString(expression)
        return {self.OUTPUT: parameters[self.INPUT]}

