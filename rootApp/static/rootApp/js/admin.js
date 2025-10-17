$(document).ready(function() {


/////////////////////////////////////////////////////////////////////////////////////////
    // forest('/district/', newforest, onEachFeatureforest)

    function forest(url, mnh, oneach) {
        // removela(map, regmap)
        loaderbar('#oveli', true)
        $.get(url, function(data) {
            dismap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            .addTo(map).bringToFront();
            // removelaturn(regmap, true)
        }).done(function() {
            $('#forestcheck').prop('disabled', false)
            loaderbar('#oveli', false)
            // districtmapdrawn('/mapApp/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }

    function onEachFeatureforest(feature, layer) {
         html = ('<h2 style="text-align: center;"><strong>Attribute</strong> </h2>')
       html+= ('<div class="row" style="padding:5px; "> ')
        html += ('<table id="customers"> ')

        html += ('<tr> <th>Name of plantation </th> <td>' + feature.properties['name']+ '</td></tr>')

        html += ('<tr> <th>Area</th> <td>' + feature.properties['area']+ '</td></tr>')
        html += ('<tr> <th>Year of Establishment</th> <td>N/A</td></tr>')
        html += ('<tr> <th>Area reported planted</th> <td>N/A</td></tr>')
        html += ('<tr> <th>Area verified planted</th> <td>N/A</td></tr>')
         html += ('<tr> <th>Percentage survival</th> <td>70%</td></tr>')
         // html += ('<tr> <th>Percentage survival</th> <td>80%</td></tr>')


        html += ('</table>')
        html += ('</div >')



        layer.bindPopup(html, {offset: L.point(0,0),})
        layer.on({
            mouseover: highlightFeature,
            mouseout: forest_resetHighlight,
            click: zoomToFeature
        });
    }




    $('#plantationcheck').on('change', function() {
        var man = $('#plantationcheck').is(':checked');
        if (man == true) {
            if (dismap) {
                map.addLayer(dismap).bringToFront();
                // map.addLayer(regioncapital);
                removelaturn(dismap, true)
            }
        } else {
            map.removeLayer(dismap);
            // map.removeLayer(regioncapital);
        }
    })


  

////////////////////////////////////////////////////////////////////////////////////////



































/////////////////////////////////////////////////////////////////////////////////////////
    protectedArea('/lulc/proarea/', newprotect, onEachFeatureprotect)

    function protectedArea(url, mnh, oneach) {
        // removela(map, regmap)
        loaderbar('#oveli', true)
        $.get(url, function(data) {
            protectedareamap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            // .addTo(map).bringToFront();
            // removelaturn(regmap, true)
        }).done(function() {
            $('#protectcheck').prop('disabled', false)
            loaderbar('#oveli', false)
            // districtmapdrawn('/mapApp/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }

    function onEachFeatureprotect(feature, layer) {
        // maplabel(layer, feature.properties['region_name'] + ' REGION');
        // layer.on({
        //     click: zoomToFeaturer
        // });

         layer.bindTooltip('</b> Protected Area  Name:<b>' + feature.properties.reserve_na, {
            direction: 'auto'
        })
        layer.on({
            mouseover: highlightFeature,
            mouseout: protectarea_resetHighlight,
            click: zoomToFeature
        });
    }




    $('#protectcheck').on('change', function() {
        var man = $('#protectcheck').is(':checked');
        if (man == true) {
            if (regmap) {
                map.addLayer(protectedareamap).bringToFront();
                // map.addLayer(regioncapital);
                removelaturn(protectedareamap, true)
            }
        } else {
            map.removeLayer(protectedareamap);
            // map.removeLayer(regioncapital);
        }
    })


      $('#querycheck').on('change', function() {
        var man = $('#querycheck').is(':checked');
        if (man == true) {
            if (querylayer) {
                map.addLayer(querylayer).bringToFront();
                // map.addLayer(regioncapital);
                removelaturn(querylayer, true)
            }
        } else {
            map.removeLayer(querylayer);
            // map.removeLayer(regioncapital);
        }
    })


////////////////////////////////////////////////////////////////////////////////////////

    regionmap('/lulc/studyarea/', newregion, onEachFeaturereg)

    function regionmap(url, mnh, oneach) {
        // removela(map, regmap)
        loaderbar('#oveli', true)
        $.get(url, function(data) {
            regmap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            .addTo(map).bringToBack();
            // removelaturn(regmap, true)
        }).done(function() {
            $('#regcheck').prop('disabled', false)
            loaderbar('#oveli', false)
            // districtmapdrawn('/mapApp/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }

    function onEachFeaturereg(feature, layer) {
        // maplabel(layer, feature.properties['region_name'] + ' REGION');
        layer.on({
            click: zoomToFeaturer
        });
    }




    $('#regcheck').on('change', function() {
        var man = $('#regcheck').is(':checked');
        if (man == true) {
            if (regmap) {
                map.addLayer(regmap);
                // map.addLayer(regioncapital);
                removelaturn(regmap, true)
            }
        } else {
            map.removeLayer(regmap);
            // map.removeLayer(regioncapital);
        }
    })



    $('#districtcheck').on('change', function() {
        var man = $('#districtcheck').is(':checked');
        // if (dismap == undefined){
        //   districtmapdrawn('/mapApp/districtboundary/NONE/',newdistrict,onEachFeaturedis)
        // }
        if (man == true) {
            if (dismap) {
                map.addLayer(dismap);
                // map.addLayer(districtcapital);
                // removelaturn(dismap, true)
                // removelaturn(regmap, true)

            }

        } else {
            map.removeLayer(dismap);
            // map.removeLayer(districtcapital);
        }
    })



    function removelaturn(dat, tru) {
        if (dat != undefined) {
            if (tru == true) {
                dat.bringToBack()
            } else {
                dat.bringToFront()
            }
        }
    }



    function newprotect() {
        return {
            fillColor: 'transparent',
            color: '#aea',
            weight: '2',
            dashArray: '5,10',
            opacity: '1',
            fillOpacity: '0',
        };
    }

    function newforest() {
        return {
            fillColor: 'transparent',
            color: '#be6',
            weight: '3',
            dashArray: '5,10',
            opacity: '1',
            fillOpacity: '0',
        };
    }



    function newregion() {
        return {
            fillColor: 'transparent',
            color: 'red',
            weight: '3',
            dashArray: '',
            opacity: '1',
            fillOpacity: '0',
        };
    }


    function zoomToFeaturer(e) {
        map.fitBounds(e.target.getBounds());
        // selectpolygon(e.target.feature.id);
        // stateofhousehold = true;
        // stateofcom = false;
        // $('#inputcodecode').val(e.target.feature.id)
        // $('.overallhh').addClass('hidden');
        // $('.overallcom').removeClass('hidden');
    }

    function newdistrict() {
        return {
            fillColor: 'transparent',
            color: 'black',
            weight: '3',
            dashArray: '',
            // opacity: '0.7',
            fillopacity: '0',
        };

    }


    function loaderbar(loadbar, valeu) {
        if (valeu == true) {
            $(loadbar).removeClass('hidden')
        } else if (valeu == false) {
            $(loadbar).addClass('hidden')
        }
    }




    districtnmap('/lulc/district/', newdistrict, district_onEachFeature)
    var dismap
    function districtnmap(url, mnh, oneach) {
        // removela(map, regmap)
        loaderbar('#oveli', true)
        $.get(url, function(data) {
            dismap = new L.GeoJSON(data, {
                style: mnh,
                onEachFeature: oneach
            })
            // .addTo(map);
            // removelaturn(regmap, true)
        }).done(function() {
            $('#districtcheck').prop('disabled', false)
            loaderbar('#oveli', false)
            // districtmapdrawn('/mapApp/districtboundary/NONE/',newdistrict,onEachFeaturedis)

        }).fail(function() {
            // loaderbar('.regc.circlemainsmall',false)
        });
    }

    function onEachFeaturereg(feature, layer) {
        // maplabel(layer, feature.properties['region_name'] + ' REGION');
        layer.on({
            click: zoomToFeaturer
        });
    }





    function district_onEachFeature(feature, layer) {
        layer.bindTooltip('</b>District Name:<b>' + feature.properties.district, {
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

   function protectarea_resetHighlight(e) {
        protectedareamap.resetStyle(e.target);
    }


    function forest_resetHighlight(e) {
        dismap.resetStyle(e.target);
    }


    function zoomToFeature(e) {
        map.fitBounds(e.target.getBounds());
    }


    function totitlefunction(txt) {
        var currVal = txt;
        // currVal = currVal.toLowerCase().replace(/\b[a-z]/g, function(txtVal) {
        //     return txtVal.toUpperCase();
        // });
        return currVal;
    }









    // var kop
    // setInterval(function() {
    //     $("#checkpoint").val(7)
    //     $.get("/galamsey/pointcheck/", function(data) {

    //         console.log(data)
    //             // alert("done")
    //             // console.log(dat)
    //         if (data > $("#checkpoint").val()) {

    //             signage('/galamsey/incidentreportspoint/');
    //             // var sod = $("#checkpoint").val(data)
    //             document.getElementById("checkpoint").value = data;
    //             // alert($("#checkpoint").val())
    //             alert("root")
    //         } else {
    //             console.log("done")
    //                 // var sod = $("#checkpoint").val(data)
    //                 // signage('/galamsey/incidentreportspoint/');

    //         }


    //     })
    // }, 3000);



















    // function zoomToFeaturerproject(e) {
    //     map.fitBounds(e.target.getBounds());
    // }

    function zoomToFeaturerproject(e) {
        var latLngs = [e.target.getLatLng()];
        var markerBounds = L.latLngBounds(latLngs);
        map.fitBounds(markerBounds);
    }








    function showNotification(msg, from, align, type) {
        //type = ['','info','success','warning','danger'];
        //color = Math.floor((Math.random() * 4) + 1);

        $.notify({
            icon: "ti-info",
            message: msg

        }, {
            //type: type[color],
            type: type,
            timer: 300000,
            placement: {
                from: from,
                align: align
            }
        });
    }

    var redIcon = L.icon({
        iconUrl: '/static/img/point.gif',
        //shadowUrl: 'leaf-shadow.png',

        iconSize: [38, 40], // size of the icon
        //shadowSize:   [50, 64], // size of the shadow
        iconAnchor: [38, 40], // point of the icon which will correspond to marker's location
        //shadowAnchor: [4, 62],  // the same for the shadow
        popupAnchor: [-18, -30] // point from which the popup should open relative to the iconAnchor
    });






    function getMarkerLayer(obj, layer) {
        html = ('<div class="row" style="padding:5px; margin-top:25px;"> ')
        html += ('<table id="customers"> ')
        if (obj.image) {

            html += ('<tr> <th><b> Description </b></th> <td>' + obj.Description + '</td><td rowspan="3"><a class="fancybox fancybox1" rel="ligthbox" href="/media/' + obj.image + '" title="' + obj.project_community + '"><img src="/media/' + obj.image + '" alt="" style="width:100px; height:100px;" /></a></p> </td></tr>')

        } else {

            html += ('<tr> <th><b> Description </b></th> <td>' + obj.Description + '</td><td rowspan="3"><a class="fancybox fancybox1" rel="ligthbox" href="/media/img/no-image.png" title="' + obj.project_community + '"><img src="/media/img/no-image.png" alt="" style="width:100px; height:100px;" /></a></p> </td></tr>')

        }

        html += ('<tr> <th>Status</th> <td>' + obj.status + '</td></tr>')

        if (obj.voice) {

            html += ('<tr> <th>Voice Message  </th> <td><audio src="/media/' + obj.voice + '" type="audio/mpeg" controls>      </audio> </td></tr>')

        }

        html += ('</table>')
        html += ('</div >')




        var marker = L.marker([parseFloat(obj.lat), parseFloat(obj.lng)], { icon: redIcon }).bindPopup(html, {
            maxWidth: "auto"
        });

        return marker;
    }














$( "body" ).on( "click", ".galamsey ", function() {
  getextent($(this).attr("id"))
});















});




    // $(".galamsey ").click(function() {
    //     // alert("helloo")
    //     getextent($(this).attr("id"))
    // })




