var dataset
var trueColor
var trueColorVis

function loadimage(path){
  dataset = ee.Image(path)
  trueColor = dataset.select(['R', 'G', 'B']);
  trueColorVis = {
    min: 0.0,
    max: 255.0,
  };
}

function loadcollection(){
  dataset = ee.ImageCollection('USDA/NAIP/DOQQ')
    .filter(ee.Filter.date('2017-01-01', '2018-12-31'))
  trueColor = dataset.select(['R', 'G', 'B']);
  trueColorVis = {
    min: 0.0,
    max: 255.0,
  };
}

//loadcollection();
loadimage('USDA/NAIP/DOQQ/m_4407137_nw_19_060_20181205_20190326');
Map.setCenter(-71.48031110099911,44.44075976024589, 15);
Map.addLayer(trueColor, trueColorVis, 'True Color');

Export.image.toDrive({image: dataset, description: 'snowNH', scale: 1});