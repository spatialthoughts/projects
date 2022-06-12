"""Algorithm to calculate Zonal Statistics using GEE API

This script uses CHIRPS data.
"""
import ee
ee.Initialize()

import json
from PyQt5.QtCore import QCoreApplication, QVariant

from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, 
    QgsProcessingParameterFeatureSource, QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,QgsFields, QgsField, QgsWkbTypes,
    QgsFeatureSink, QgsProcessingUtils)


class AnnualPrecipitation(QgsProcessingAlgorithm):
    """Calculates annual rainfall using GEE API for each input features"""
    INPUT = 'INPUT'
    YEAR = 'YEAR'
    OUTPUT = 'OUTPUT'

    
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT',
                self.tr('Input Layer'),
                types=[QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                'YEAR',
                self.tr('Year'),
                QgsProcessingParameterNumber.Integer,
                2021, False, 1
            )
        )
        
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Annual_Precipitation',
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source= self.parameterAsSource(parameters, self.INPUT, context)
        year = self.parameterAsInt(parameters, self.YEAR, context)
        
        outputFields = source.fields()
        newFields = QgsFields()
        newFields.append(QgsField('year', QVariant.Int))
        newFields.append(QgsField('precipitation', QVariant.Int))

        outputFields = QgsProcessingUtils.combineFields(outputFields, newFields)
        sink, dest_id = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outputFields,
            source.wkbType(),
            source.sourceCrs()
            )
        feedback.pushInfo(self.tr( "Processing Input"))
        
        
        chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD')
        startDate = ee.Date.fromYMD(year, 1, 1)
        endDate = startDate.advance(1, 'year')
        filtered = chirps.filter(ee.Filter.date(startDate, endDate))
        total_precipitation = filtered.sum()
        
        #features = [f for f in source.getFeatures()]
        
        total_features = 100.0 / source.featureCount() if source.featureCount() else 0

        for current, out_f in enumerate(source.getFeatures()):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
                  
            geometry = out_f.geometry()
            json_geometry = json.loads(geometry.asJson())['coordinates']
            polygon = ee.Geometry.MultiPolygon(json_geometry)
            stats = total_precipitation.reduceRegion(**{
              'reducer': ee.Reducer.mean(),
              'geometry': polygon,
              'scale': 5000,
              })
            precipitation = stats.getNumber('precipitation').getInfo()
            feedback.pushInfo(str(precipitation))
            attributes = out_f.attributes()

            attributes.append(year)
            attributes.append(precipitation)

            out_f.setAttributes(attributes)
            sink.addFeature(out_f, QgsFeatureSink.FastInsert)
            feedback.setProgress(int(current * total_features))

        return {self.OUTPUT: sink} 

    def name(self):
        return 'annual_precipitation_gee'

    def displayName(self):
        return self.tr('Annual Precipitation GEE')
        
    def shortHelpString(self):
        return self.tr('Annual Precipitation Calculated using CHIRPS data via GEE API')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AnnualPrecipitation()
