
    var stuff,
        map;

    /**
     * getUserCoordinates - use geolocation to grab the user's latitude and longitude
     * @callback - when all is done, callback(lat, lon) is called
     */
    function getUserCoordinates(callback) {
      navigator.geolocation.getCurrentPosition(function(location) {
        callback(location.coords.latitude, location.coords.longitude);
      });
    }

    function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
      var R = 6371; // Radius of the earth in km
      var dLat = deg2rad(lat2-lat1);  // deg2rad below
      var dLon = deg2rad(lon2-lon1);
      var a =
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
      Math.sin(dLon/2) * Math.sin(dLon/2);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      var d = R * c; // Distance in km
      return d;
    };

    function deg2rad(deg) {
      return deg * (Math.PI/180)
    };

    function getData(){
      var jData = $.ajax({
        dataType: "json",
        url: "/get_drinks_json",
        async: false
      });
      var rText = jData.responseText;
      return JSON.parse(rText)['json-data'];
    };

    function processData(deals){
      var googleData = [['Lat', 'Lon', 'Info']]
      for(var i = 0; i < deals.length; i++) {
        var deal = deals[i];
        var info = "";
        info += "bar_name: " + deal[4] + "\n";
        info += "drink_name: " + deal[2] + "\n";
        info += "price: " + deal[1] + "\n";
        info += "category: " + deal[3];
        googleData.push([deal[5], deal[6], info]);
      }
      return googleData;
    };

    function filter(address,spend,category,distance){
      /*Turn street address into lat and long*/
      var addressShit = $.ajax({
        url: 'http://maps.googleapis.com/maps/api/geocode/json',
        data: {
          sensor: false,
          address: address
        },
        async: false
      });

      var lat1 = JSON.parse(addressShit.responseText)['results'][0]['geometry']['location']['lat'];
      var lng1 = JSON.parse(addressShit.responseText)['results'][0]['geometry']['location']['lng'];

      /*filter list of shit*/
      shit = [];
      for(var i = 0; i < stuff.length; i++){
        var bar = stuff[i];
        if (getDistanceFromLatLonInKm(lat1,lng1,bar[5],bar[6]) < distance && category == bar[3] && spend >= bar[1]){
          shit.push(bar);
        }
      }
      console.log(shit);
    };

    function addLocator(lat, lon) {
      var pos = new google.maps.LatLng(lat, lon);
      var imgName = 'you.png';
      var marker = new google.maps.Marker({
        position: pos,
        map: map,
        icon: imgName,
        title: "You are here"
      })
    }

    function drawMap() {
      var data = google.visualization.arrayToDataTable(processData(stuff));
      map = new google.visualization.Map($('#map_div')[0]);
      map.draw(data, {showTip: true, mapType: 'normal'});
      getUserCoordinates(addLocator);
    };

    $(function(){
      $('form').submit(function(e){
        filter($('#address').val(),parseFloat($('#spend').val()),parseFloat($('#cat').val()),parseFloat($('#distance').val()));
        e.preventDefault();
      });
    });

    google.load("visualization", "1", {packages:["map"]});
    google.setOnLoadCallback(drawMap);
    var stuff = getData();