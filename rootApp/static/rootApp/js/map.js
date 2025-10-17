   var map = L.map('mapid', {
       maxBounds: L.latLngBounds([6.712, -3.426], [5.738, -1.956]),
       minZoom: 10,
       // zoomControl: false,



   }).setView([6.3, -2.7], 11);

   // setView([9.099, -1.000], 7);


   googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
       maxZoom: 20,

       subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
   }).addTo(map);




   function mapdisbled(map) {
       map.touchZoom.disable();
       map.doubleClickZoom.disable();
       // map.scrollWheelZoom.disable();
       //map.dragging.disable();
       map.keyboard.disable();
       if (map.tap) map.tap.disable();
   }




   L.control.mousePosition().addTo(map);


   $('#zoomin').on('click', function() {

       mapdisbled(map);
       map.zoomIn(1);
   })


   $('#zoomout').on('click', function() {

       mapdisbled(map);
       map.zoomOut(1);
   })



   function autoquick1(code, ftype) {
       getextent('/extent/' + code + '/' + ftype + '/', map);
       // selectmap('/highlight/' + code  + '/' + ftype + '/',map,'',selectstyle)
   }



   function getextent(url, map) {
       $.get(url, function(data) {
           map.fitBounds([
               [data[1], data[0]],
               [data[3], data[2]]
           ])
       })
   }

   //Highlightmap style
   function highlightstyle() {
       return {
           fillColor: 'transparent',
           weight: 4,
           opacity: 1,
           color: 'cyan',
           dashArray: '',
           fillOpacity: '1'
       };

   }

   //selecymap style
   function selectstyle() {
       return {
           fillColor: 'transparent',
           weight: 4,
           opacity: 1,
           color: '#f00',
           dashArray: '',
           fillOpacity: '1'
       };

   }




   var selectfeaturezone;

   function selectmap(url, map, typem, mnh) {
       $.get(url, function(data) {
           if (selectfeaturezone != undefined) {
               map.removeLayer(selectfeaturezone)
           }
           if (typem == 'point') {
               selectfeaturezone = new L.GeoJSON(data, { pointToLayer: mnh }).addTo(map).bringToFront();
           } else {
               selectfeaturezone = new L.GeoJSON(data, { style: mnh }).addTo(map).bringToBack();
           }
       }).done(function() {}).fail(function() {});
   }








   //Autocomplete function
   var options = {
       url: function(phrase) {
           return "/autocompleteview/?phrase=" + phrase;
       },
       placeholder: "Search by region,district,plantation",
       template: {
           type: "description",
           fields: {
               description: "type"
           },
       },
       getValue: "name",
       requestDelay: 500,
       list: {
           match: {
               enabled: true
           },
           maxNumberOfElements: 10,
           showAnimation: {
               type: "slide",
               time: 300
           },
           hideAnimation: {
               type: "slide",
               time: 300
           },
           onSelectItemEvent: function() {
               var code = $("#inputsearch").getSelectedItemData().code;
               var ftype = $("#inputsearch").getSelectedItemData().type;
               autoquick1(code, ftype)
           },
           onChooseEvent: function() {
               var code = $("#inputsearch").getSelectedItemData().code;
               var ftype = $("#inputsearch").getSelectedItemData().type;
               autoquick1(code, ftype)

           },
           onKeyEnterEvent: function() {
               var code = $("#inputsearch").getSelectedItemData().code;
               var ftype = $("#inputsearch").getSelectedItemData().type;
               autoquick1(code, ftype)
           },
           onShowListEvent: function() {
               $(".circlemainsmallsearch").addClass("hidden");
           },
           onLoadEvent: function() {
               $(".circlemainsmallsearch").removeClass("hidden");
           }
       },
       theme: "blue-light",
       //theme: "round"
   };






   $("#layerbtn").click(function() {
       // alert("goop")
       $("#basemap").slideToggle("slow");
   });

   var options = {
       position: 'topleft', // Leaflet control position option
       circleMarker: { // Leaflet circle marker options for points used in this plugin
           color: 'red',
           radius: 2
       },
       lineStyle: { // Leaflet polyline options for lines used in this plugin
           color: 'red',
           dashArray: '1,6'
       },
       lengthUnit: { // You can use custom length units. Default unit is kilometers.
           display: 'km', // This is the display value will be shown on the screen. Example: 'meters'
           decimal: 2, // Distance result will be fixed to this value. 
           factor: null, // This value will be used to convert from kilometers. Example: 1000 (from kilometers to meters)  
           label: 'Distance:'
       },
       angleUnit: {
           display: '&deg;', // This is the display value will be shown on the screen. Example: 'Gradian'
           decimal: 2, // Bearing result will be fixed to this value.
           factor: null, // This option is required to customize angle unit. Specify solid angle value for angle unit. Example: 400 (for gradian).
           label: 'Bearing:'
       }
   }

   L.control.scale().addTo(map);



   L.control.browserPrint({

       printModes: ["Portrait", "Landscape", "Auto", "Custom"],
       manualMode: true // use true if it's debug and/or default button is okay for you, otherwise false.
   }).addTo(map);

   document.querySelector("#custom_print_button").addEventListener("click", function() {
       var modeToUse = L.control.browserPrint.mode.auto();
       map.printControl.print(modeToUse);

       // alert( $("#mapotitle").val())

       var titt = $("#mapotitle").val()

       $(".grid-print-container").append("<h2 id='tittop'>" + titt + "</h2>");


   });









   // var style = {
   //     color: 'red',
   //     opacity: 1.0,
   //     fillOpacity: 0,
   //     weight: 2,
   //     clickable: false
   // };
   // L.Control.FileLayerLoad.LABEL = '<img class="icon" src="/static/rootApp/leaflet/folder.svg" alt="file icon"/>';
   // control = L.Control.fileLayerLoad({
   //     fitBounds: true,
   //     layerOptions: {
   //         style: style,
   //         pointToLayer: function(data, latlng) {
   //             return L.circleMarker(
   //                 latlng, { style: style }
   //             );
   //         }
   //     }
   // });
   // control.addTo(map);
   // control.loader.on('data:loaded', function(e) {
   //     var layer = e.layer;
   //     console.log(layer);
   // });



   function getColor(d) {
       return d > 1000 ? '#800026' :
           d > 500 ? '#BD0026' :
           d > 200 ? '#E31A1C' :
           d > 100 ? '#FC4E2A' :
           d > 50 ? '#FD8D3C' :
           d > 20 ? '#FEB24C' :
           d > 10 ? '#FED976' :
           '#FFEDA0';
   }



   L.LegendControl = L.Control.extend({
       onAdd: function(map) {
           var labels = [];
           var div = L.DomUtil.create('div', 'info legend');

           html = (' <img src="/static/rootApp/img/ledgend.png" style="width:60% ;">')
          


           labels.push(html);
           // }

           div.innerHTML = labels.join('');
           return div;
       }
   });



   L.legendControl = function(options) {
       return new L.LegendControl(options);
   };







   var optionmeasure = {
       position: 'topleft',
       primaryAreaUnit: 'hectares',
   }

   var measureControl = new L.Control.Measure(optionmeasure);
   measureControl.addTo(map);






   map.on("browser-print-start", function(e) {
       /*on print start we already have a print map and we can create new control and add it to the print map to be able to print custom information */
       L.legendControl({ position: 'bottomright' }).addTo(e.printMap);

       // L.legendControl({ position: 'bottomleft' }).addTo(e.printMap);

   });


    loader();
   var querylayer
   $.get("/lulc/asd/", function(res) {
       querylayer = L.tileLayer(res["mapid"]);
       map.addLayer(querylayer);
        unload();
   });



   var querylayer
   $("#filter").click(function() {
       var start = $("#start").val()

       var end = $("#end").val()

       if (start && end) {
           // if (querylayer) {
           //     map.removeLayer(querylayer);
           // }


           $("#changedetection").dialog("open");
           // $("#overlay").removeClass("hidden");

           // $.get("/asd/?start=" + start + '&end=' + end, function(res) {

           //    if (res.mapid == "error"){

           //       alert(res.mapid)
           //       $("#overlay").addClass("hidden");

           //    }else{


           //     querylayer = L.tileLayer(res["mapid"]);

           //     map.addLayer(querylayer);
           //     $("#overlay").addClass("hidden");

           //    }

           // });




           $("#overlay_chart").show();
           $.get("/lulc/analysis/?start=" + start + '&end=' + end, function(data) {



               if (data.chart == "error") {

                   $("#overlay_chart").hide();
                   alert("An error occurred")
               } else {

                   $("#analysis_contain_parent").html(data)

                   $("#overlay_chart").hide();
               }


           });



       } else {


           alert("soop")

       }




   })






   // $('#rangecheck').on('click', function() {
     $("body").on("click", "#rangecheck ", function() {
       
        $("#timeseries").dialog("open");


   })



   let coords;
   var drawnItems = new L.geoJson().addTo(map);
   drawnItems.bringToFront();
   var layer;

   map.on(L.Draw.Event.CREATED, function(event) {
       drawnItems.removeLayer(layer);
       layer = event.layer;

       // $("#dialog").dialog("open");
       drawnItems.addLayer(layer);

       let type = event.layerType;

       // if (type === 'rectangle' | ) {
       // layer.on("mouseover", function() {
       coords = layer.getLatLngs();

       var start = $("#start").val()

       var end = $("#end").val()









       if (start && end) {

           $("#changedetection").dialog("open");

           $("#overlay_chart").show();


           $.get("/lulc/analysis/?start=" + start + '&end=' + end + '&coords=' + coords, function(res) {

               $("#analysis_contain_parent").html(res)

               $("#overlay_chart").hide();



           });




       } else {


           alert("Please Provide the Start and End Date ")



       }

       // });
       // }
   });

   L.EditToolbar.Delete.include({
       removeAllLayers: false,
   });

   new L.Control.Draw({
       edit: {
           featureGroup: drawnItems,
       },
       draw: {
           polygon: true,
           rectangle: true,
           circlemarker: false,
           marker: false,
           polyline: false,
           circle: false,
       },
   }).addTo(map);


   // map.on('click', function(e) {

   //     var popLocation = e.latlng;
   //     $.get("/getdist/?coord=" + popLocation, function(res) {

   //         console.log(res)
   //         var popup = L.popup({ maxWidth: 560 })
   //             .setLatLng(popLocation)
   //             .setContent('<div class="row"  style="width:20vw"><h4 style="text-align: center;">' + res["status"] + '</h4><div id="distinfo"> <button id=' + res["distcode"] + '  class="btn btn-success analyse" style=" margin-left: 35%;"> Analyse </button> </div></div>')
   //             .openOn(map);

   //         // $("#distinfo").html(res)



   //     });


   // });



   function distyle() {
       return {
           fillColor: 'transparent',
           color: 'white',
           weight: '3',
           dashArray: '5,10',
           opacity: '1',
           fillOpacity: '0',
       };
   }


   function onEachFeatureasd(feature, layer) {
       // layer.bindPopup(html, {offset: L.point(0,0),})

       console.log(feature.getLatLngs())

   }




   var dismapo, coordz
   $("body").on("click", ".analyse ", function() {


       $.get("/lulc/district/" + $(this).attr("id"), function(data) {

           if (dismapo) {
               map.removeLayer(dismapo)
           }
           dismapo = new L.GeoJSON(data, {
                   style: distyle,
                   onEachFeature: onEachFeatureasd
               })
               .addTo(map).bringToFront();

           map.fitBounds(dismapo.getBounds());
           // map.flyTo(dismapo.getBounds(), 14, {
           // animate: true,
           // duration: 1.5
           // });
           // coordz = dismapo.getLatLngs();

           // coords.push(feature.geometry.coordinates);

           console.log(dismapo.geometry.coordinates)

       });


       var start = $("#start").val()

       var end = $("#end").val()


       if (start && end) {

           $("#changedetection").dialog("open");

           $("#overlay_map_analysis").removeClass("hidden");


           $.get("/analysis/?start=" + start + '&end=' + end + '&coords=' + coordz, function(res) {

               $("#analysis_cont_map").html(res)
               $("#overlay_map_analysis").addClass("hidden");



           });




       } else {


           alert("Please Provide the Start and End Date ")



       }





   })










   // map.on('click', function(e) {        
   //      var popLocation= e.latlng;

   // $.get("/getdist/?coord=" + popLocation , function(res) {

   // });
   //      var popup = L.popup()
   //      .setLatLng(popLocation)

   // html = ('<p> '+res+' </p>')
   // html+= ('<button class"btn btn-success">Analyze</button>')
   //      // html += ('<table id="customers"> ')

   //      // html += ('<tr> <th>Name of plantation </th> <td>' + feature.properties['name']+ '</td></tr>')

   //      // html += ('<tr> <th>Area</th> <td>' + feature.properties['area']+ '</td></tr>')
   //      // html += ('<tr> <th>Year of Establishment</th> <td>N/A</td></tr>')
   //      // html += ('<tr> <th>Area reported planted</th> <td>N/A</td></tr>')
   //      // html += ('<tr> <th>Area verified planted</th> <td>N/A</td></tr>')
   //      // html += ('<tr> <th>Percentage survival</th> <td>70%</td></tr>')
   //      .setContent(html)
   //      .openOn(map);        
   //  });