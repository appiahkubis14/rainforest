 loader()
 $.get("/reportres/",function(data){

 	$("#reportgrpres").html(data)
     unload()
 })


 $.get("/groupreport/",function(data){

 	$("#adam").html(data)
 })

