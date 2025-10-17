var mymap = L.map('mapid',{maxBounds: L.latLngBounds([6.674, -3.2249], [5.891, -2.298]),}).setView([6.088, -2.063], 9);

initialbasemap= L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var legendToggle = 'no';

$("#legendbtn").click(function() {
  if (legendToggle == 'no') {
    $('#resultBox').css("display", "none");
    legendToggle = 'yes';
  }else {    
    $('#resultBox').css("display", "block"); 
    legendToggle = 'no';
  }
});





  $("#filtermap").click(function() {
       $(".slidebox1").animate({ width: "toggle" });
       //  if (boxToggle == 'off') {
       //   $(".box2").animate({width: "toggle"});
       //   boxToggle = 'on';
       // }else if (boxToggle == 'on') {   
       //   boxToggle = 'on';
       // }
   });

$("#berryClose1").click(function() {
    $(".slidebox1").animate({ width: "toggle" });
    boxToggle = 'off';
});



$("#berryClose").click(function() {
    $(".slidebox").animate({ width: "toggle" });
    boxToggle = 'off';
});

   //end of autocomplete  
   var basemapCont = 'off';
   var legendCont = 'off';

   function shutall() {
       $(".legendCont").css('display', 'none');
       $(".legendcet").css('display', 'none');
       $(".basemapCont").css('display', 'none');
       $(".basemapcet").css('display', 'none');
       basemapCont = 'off';
       legendCont = 'off';

   }

   function toggleLegend() {
       $(".legendCont").animate({
           width: "toggle"
       });
       $(".legendcet").animate({
           width: "toggle"
       });
   }


   function toggleBasemap() {
       $(".basemapCont").animate({
           width: "toggle"
       });
       $(".basemapcet").animate({
           width: "toggle"
       });
   }

   $('#legBox').click(function() {

       if (legendCont == 'off') {
           shutall();
           toggleLegend();

           legendCont = 'on';
           basemapCont = 'off';
       } else {
           shutall();
           legendCont = 'off';
           basemapCont = 'off';
       }
   });
   $('#baseMap').click(function() {
       if (basemapCont == 'off') {
           shutall();
           toggleBasemap();
           basemapCont = 'on';
           legendCont = 'off';
       } else {
           shutall();
           basemapCont = 'off';
           legendCont = 'off';
       }
   });



   $('#basemap10').css('border-color', '#f00')
   $('.tileDiv').click(function(e) {

       mymap.removeLayer(initialbasemap)
       $('#basemap > img').css('border-color', '#3e5766')
       var toolname = $(this).attr('id');
       if (toolname == 'no_basemap') {
           initialbasemap = L.tileLayer('').addTo(mymap);;

       } else if (toolname == 'basemap1') {

           initialbasemap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
               maxZoom: 19,
               attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'
           }).addTo(mymap);

       } else if (toolname == 'basemap2') {

           initialbasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
               maxZoom: 20,
               subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
           }).addTo(mymap);

       } else if (toolname == 'basemap3') {

           initialbasemap = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
               maxZoom: 19,
               attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'
           }).addTo(mymap);
       } else if (toolname == 'basemap4') {
           initialbasemap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
               maxZoom: 17,
               attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
           }).addTo(mymap);

       } else if (toolname == 'basemap5') {
           initialbasemap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
               maxZoom: 17,
               attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
           }).addTo(mymap);

       } else if (toolname == 'basemap6') {
           initialbasemap = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
               attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
           }).addTo(mymap);
       } else if (toolname == 'basemap7') {
           initialbasemap = L.tileLayer('https://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png', {
               maxZoom: 18,
               attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
           }).addTo(mymap)


       } else if (toolname == 'basemap8') {
           initialbasemap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
               maxZoom: 19,
               attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
           }).addTo(mymap);


       } else if (toolname == 'basemap9') {
           initialbasemap = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}', {
               attribution: 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
           }).addTo(map);


       } else if (toolname == 'basemap10') {
           initialbasemap = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.{ext}', {
               attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
               subdomains: 'abcd',
               minZoom: 0,
               maxZoom: 20,
               ext: 'png'
           }).addTo(map);


       }
   })



















// function farmstyle() {
//     return {
//         fillColor: "transparent",
//         weight: 2,
//         opacity: 1,
//         color: "black",
//         dashArray: "3",
//         fillOpacity: 0.7,
//     };
// }

function farmresetHighlight(e) {
    geodata.resetStyle(e.target);
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

// function farmonEachFeature(feature, layer) {
//     layer.on({
//         mouseover: highlightFeature,
//         mouseout: farmresetHighlight,
//         click: zoomToFeature,
//     });
// }

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7,
        fillColor: 'transparent',
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

   function onEachtreepoints(feature, layer) {
       layer.on({ click: zoomToFeaturerpoint,
        });

       layer.bindTooltip('</b>Species:<b>' + feature.properties.ptn_species, {
            direction: 'auto'
        })
        // labeltoshow = '<table class="table table-bordered">'
        // labeltoshow += "<tbody><tr><td> <b> Image </b></td><td> <a class='example-image-link' href='/media/" + feature.properties.image + "'  data-lightbox='example-2' data-title='Optional caption.'> <img class='example-image' src='/media/" + feature.properties.image + "'  alt='image-1'/></a> </td></tr>"
        // labeltoshow += "<thead><tr style='background-color:#4aa;color:white;'><th colspan='2' > <b><center> BIN"+ feature.properties.binid + "</center></b></th><tr></thead>"
        // labeltoshow += "<tbody><tr><td> <b> Bin Type  </b></td><td> Communal Bin </td></tr>"
        // labeltoshow += "<tbody><tr><td> <b> Region </b></td><td> " + feature.properties.region + " </td></tr>"
        // labeltoshow += "<tbody><tr><td> <b> District </b></td><td> " + feature.properties.district + " </td></tr>"
        // labeltoshow += "<tbody><tr><td> <b> Location </b></td><td> " + feature.properties.location + " </td></tr>"
        // labeltoshow += "<tbody><tr><td> <b> Comments </b></td><td> " + feature.properties.comments + " </td></tr>"

      //  if (feature.properties.status == "bag" || feature.properties.wastetype == "bin"  &&  feature.properties.refusetype == "Community" ){
      //   labeltoshow += "<tr><td> <b> Status </b></td><td> Not Full </td></tr>"

      // }  else if(feature.properties.wastetype == "van" &&  feature.properties.refusetype == "Community" ) {
      //    labeltoshow += "<tr><td> <b> Status </b></td><td> Overflowing </td></tr>"
      // }else if(feature.properties.wastetype == "bin" &&  feature.properties.refusetype == "Household" ){
      //   labeltoshow += "<tr><td> <b> Status </b></td><td> Not Full </td></tr>"
      // } else if(feature.properties.wastetype == "van" &&  feature.properties.refusetype == "Household" ){
      //   labeltoshow += "<tr><td> <b> Status </b></td><td>  Full </td></tr>"
      // }else{

      //   labeltoshow += "<tr><td> <b> Status </b></td><td>  Full </td></tr>"
      // }
        // labeltoshow += "<tr><td> <b> Latest Updated </b></td><td> " + feature.properties.entrydate + " </td></tr>"
        // labeltoshow += "</tbody></table>"
       // layer.bindPopup(labeltoshow,{Width: "auto"});
   };
 function zoomToFeaturerpoint(e) {

   var latLngs = [e.target.getLatLng()];
       // var markerBounds = L.latLngBounds(latLngs);
       mymap.fitBounds(latLngs);
  }


// //////////////////////////////////////////////////
///////// MAP TOOLS  ////////////////////////
// ////////////////////////////////////////////////////
            var ghanabounds;

            
            ghanabounds = L.latLngBounds([3.7388, -4.262], [12.1748, 2.200]);
            



         function mapdisbled(mymap) {
            mymap.touchZoom.disable();
            mymap.doubleClickZoom.disable();
            mymap.scrollWheelZoom.disable();
            //map.dragging.disable();
            mymap.keyboard.disable();
            if (mymap.tap) mymap.tap.disable();
        }
        //enabled map
        function mapenabled(mymap) {
            mymap.touchZoom.enable();
            mymap.doubleClickZoom.enable();
            mymap.scrollWheelZoom.enable();
            //map.dragging.enable();
            mymap.keyboard.enable();
            if (mymap.tap) mymap.tap.enable();

        } //

        $('#reload').on('click', function() {
            location.reload();
        })

        $('#zoomin').on('click', function() {
            mapdisbled(mymap);
            mymap.zoomIn(1);
        })


        $('#zoomout').on('click', function() {

            mapdisbled(mymap);
            mymap.zoomOut(1);
        })



        $('#zoomex').on('click', function() {
            mymap.fitBounds(ghanabounds);
            mymap.panTo(new L.LatLng(8.099, -1.125));;
        })


        var zoomextpre = 0;
        $('#previousebtn').click(function() {
            if (zoomextpre == 1) {
                mymap.setZoom(currentzoom1);
                zoomextpre = 0;
            }
        });

        mymap.on('zoomstart', function(e) {
            currentzoom1 = mymap.getZoom();
            zoomextpre = 1;

        })

        //$('.comlabel').prop('disabled', true)
        //$('.houselabel').prop('disabled', true)
        mymap.on('zoomend', function(e) {
            currentzoom = mymap.getZoom();
            if (currentzoom >= 9) {
                //$('.comlabel').prop('disabled', false)
            } else {
                //$('.comlabel').prop('disabled', true).prop('checked', false).trigger('change')
            }
            if (currentzoom >= 11) {
                //$('.houselabel').prop('disabled', false)
            } else {
                //$('.houselabel').prop('disabled', true).prop('checked', false).trigger('change')
            }
        })


           $('#zoomtabfil').on('click', function() {
       location.reload();
   })



// //////////////////////////////////////////////////
///////// MAP TOOLS  ////////////////////////
// ////////////////////////////////////////////////////

    function loaderbar(loadbar, valeu) {
        if (valeu == true) {
            $(loadbar).removeClass('hidden')
        } else if (valeu == false) {
            $(loadbar).addClass('hidden')
        }
    }
    function newdistrict() {
        return {
            fillColor: 'transparent',
            color: '#2df',
            weight: '3.5',
            dashArray: '',
            opacity: '0.8',
            fillopacity: '0',
        };

    }

     function newfarm() {
        return {
            fillColor: 'rgb(55,61,86,0.5)',
            color: 'rgb(55,61,86)',
            weight: '3.5',
            dashArray: '',
            opacity: '0.8',
            fillopacity: '0',
        };

    }


    districtnmap('/districtboundaryapi/', newdistrict, district_onEachFeature)


    var farmmap
    farmMap('/farmboundarylayer/', newfarm, farm_onEachFeature,farmmap)





  
    function farmMap(url, mnh, oneach , farm) {
        // removela(map, regmap)
        loaderbar('#loadbar', true)
        $.get(url, function(data) {
            farmmap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            .addTo(map);
            // removelaturn(regmap, true)
        }).done(function() {
            $('#farmcheck').prop('disabled', false)

             $('#farmload').hide()

            loaderbar('#loadbar', false)
            // districtmapdrawn('/map/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }





    function districtnmap(url, mnh, oneach) {
        // removela(map, regmap)
        loaderbar('#loadbar', true)
        $.get(url, function(data) {
            dismap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            // .addTo(map);
            // removelaturn(regmap, true)
        }).done(function() {
            $('#districtcheck').prop('disabled', false)
            loaderbar('#loadbar', false)
            // districtmapdrawn('/map/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }


    var customOptions = {'maxWidth': '900','className' : 'custom'}

    function district_onEachFeature(feature, layer) {
        layer.bindTooltip('</b>District Name:<b>' + feature.properties.district, {
            direction: 'auto'
        })

        labeltoshow = '<div id="regdetails" class="row"> </div>'
                  
        layer.bindPopup(labeltoshow ,customOptions );


        layer.on({
            mouseover: highlightFeature,
            mouseout: district_resetHighlight,
            click: zoomToFeature
            
        });
    }



     function farm_onEachFeature(feature, layer) {
        layer.bindTooltip('</b>Beneficiary Name:<b>' + feature.properties.beneficiary, {
            direction: 'auto'
        })

        labeltoshow = '<table class="table table-bordered">'
        labeltoshow += "<thead><tr style='background-color:#4aa;color:white;'><th colspan='2' > <b><center> "+ feature.properties.beneficiary + "</center></b></th><tr></thead>"
        labeltoshow += "<tbody><tr><td></td> <td> <img style='width:60%' src=/media/" + feature.properties.image+ " > <td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Beneficiary Type </b></td><td> " + feature.properties.type_beneficiary + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Gender </b></td><td> " + feature.properties.indvi_gender + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Date of Birth </b></td><td> " + feature.properties.indvi_dob + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Contact </b></td><td> " + feature.properties.indvi_phone_no + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Farm Size (HA) </b></td><td> " + feature.properties.area + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Establishment Type </b></td><td> " + feature.properties.establishment_type + "</td></tr>"
        labeltoshow += "<tbody><tr><td> <b>Total trees </b></td><td> " + feature.properties.total_tree + " </td></tr>"
        labeltoshow += "<tbody><tr><td> <b> Tree Species </b></td><td> " + feature.properties.treespecies + " </td></tr>"
        labeltoshow += "</tbody></table>"

         layer.bindPopup(labeltoshow, {
            direction: 'auto'
        })



        layer.on({
            mouseover: highlightFeature,
            mouseout: district_resetHighlight,
            click: zoomToFeature
            
        });
    }











    function highlightFeature(e) {
        var layer = e.target;
        layer.setStyle({
            weight: 5,
            color: '#203F73',
            dashArray: '',
            fillOpacity: 0,
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }




    function district_resetHighlight(e) {
        dismap.resetStyle(e.target);
    }



$('#distcheck').on('change', function() {
    var man = $('#distcheck').is(':checked');
    // if (dismap == undefined) {
    //     districtmapdrawn('/mapApp/districtboundary/NONE/', newdistrict, onEachFeaturedis)
    // }
    if (man == true) {
        if (dismap) {
            mymap.addLayer(dismap);

        }
    } else {
        mymap.removeLayer(dismap);
    }
})

$('#farmcheck').on('change', function() {
    var man = $('#farmcheck').is(':checked');
    // if (dismap == undefined) {
    //     districtmapdrawn('/mapApp/districtboundary/NONE/', newdistrict, onEachFeaturedis)
    // }
    if (man == true) {

        if (farmmap) {
         
            mymap.addLayer(farmmap);

        }
    } else {
        mymap.removeLayer(farmmap);
    }
})


var geojsonMarkerOptions = {
    radius: 6,
    fillColor: "green",
    color: "white",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

var tree

$.get("/treelayer/",function(data){

    tree = L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                // baseballIcon = L.icon({iconUrl:'/static/app/img/tree.png' ,iconSize: [40,20]});
                //  return L.marker(latlng, {icon: baseballIcon});
                return L.circleMarker(latlng,geojsonMarkerOptions);

            },
            onEachFeature: onEachtreepoints

        });


    // mymap.addLayer(tree)

     $("#treeload").hide()

   $(".overlay1").hide()

})


$('#treeloadcheck').on('change', function() {
    var man = $('#treeloadcheck').is(':checked');
    // if (dismap == undefined) {
    //     districtmapdrawn('/mapApp/districtboundary/NONE/', newdistrict, onEachFeaturedis)
    // }
    if (man == true) {
        if (tree) {
            mymap.addLayer(tree);

        }
    } else {
        mymap.removeLayer(tree);
    }
})









var optionmeasure = {
  position: 'topleft' ,
  primaryAreaUnit: 'hectares',
}

var measureControl = new L.Control.Measure(optionmeasure);
measureControl.addTo(mymap);


