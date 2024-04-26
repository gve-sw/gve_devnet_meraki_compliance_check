$(function() {
    /*Show corresponding network list as soon as organization is choosen in dropdown + reset child fields*/
    $('#organizations_select').bind('change', function() {
          $('.network-select').attr("hidden", true);
          $('.network-select .networks').val("0");
          $('.network-select .networks').attr("required", true);
          $('.camera-checkboxes').attr("hidden", true);
          var selectid = $( "#organizations_select option:selected" ).val();
          $('#' + selectid).attr("hidden",false);       
      });                            
  });  

  $(function(){
    $("#upload_link").on('click', function(e){
        e.preventDefault();
        $("#upload:hidden").trigger('click');
        document.getElementById("upload").value=""
    });

    $('#upload').on('change', function (e){
        let file = document.getElementById("upload").files[0];
    
        console.log("Uploading file...");
        const API_ENDPOINT = "/extract-input";
        const request = new XMLHttpRequest();
        const formData = new FormData();

        request.open("POST", API_ENDPOINT, true);
        
        request.onreadystatechange = () => {
        if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
            console.log(request.responseText);
        }
        };
        formData.append("file", file);

        request.send(formData);
        document.getElementById("upload").value=""
        document.getElementById("upload-check").hidden=false
    } );
});