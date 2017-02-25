from jinja2 import Template

def render_map_with_dicts(dicts, map_name, template):
    """
    map_name is the output file
    dicts is a list of dicts, where every dict must have the following keys:
            Latitude
            Longitude
            Weight
    template is loaded below
    """
    with open('%s' % map_name, 'w+') as f:
        f.write(template.render(points=dicts))

def render_heatmap(df, map_name):
    # Provide a dataframe with Latitude, Longitude, and Weight column (or the latter will be created)
    if 'Weight' not in df.columns:
        df['Weight'] = 1.0
    dicts = df.T.to_dict().values()
    render_map_with_dicts(dicts, map_name, Template(heatmap_template))


heatmap_template = '''
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Marker Labels</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
      #panel {
        position: absolute;
        top: 5px;
        left: 50%;
        margin-left: -180px;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB_j6UQz4HVdHlJQl37Q7PKQ8WW0BV_BU8&libraries=visualization"></script>
    <script>
      var prev_infowindow = false;

      var heatmap;

      function initialize() {
        var detroit = { lat: 42.331427, lng: -83.045754 };
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 13,
          center: detroit
        });

        var heatMapData = [
          {% for point in points %}
              {
                location: new google.maps.LatLng({{point.Latitude}}, {{point.Longitude}}),
                weight: {{point.Weight}}
              },
          {% endfor %}
        ];

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: heatMapData
        });
        heatmap.setMap(map);
      }

      function changeRadius(r) {
            heatmap.set('radius', r * 1);
      }

      function changeOpacity(o) {
            heatmap.set('opacity', o * 1.0);
      }

      function toggleHeatmap() {
        if(heatmap.get())
        heatmap.setMap(heatmap.getMap() ? null : map);
      }

      function changeGradient() {
        var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
      }

      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>


  <body>
  <div id="panel">
    <button onclick="changeGradient()">Change gradient</button>

    Radius
    <input type="range" id="radiusSlider" onchange="changeRadius(radiusSlider.value)"  min="1" max="40" step="1" value="12">
    Opacity
    <input type="range" id="opacitySlider" onchange="changeOpacity(opacitySlider.value)"  min="0" max="1" step=".01" value=".6">

  </div>
  
  <div id="map"></div>
  </body>
</html>
'''
