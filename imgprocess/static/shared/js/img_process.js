function showPreview(objFileInput,html_element) {
    if (objFileInput.files[0]) {
        var fileReader = new FileReader();
        fileReader.onload = function (e) {
            $(html_element).html('<img src="'+e.target.result+'" width="100%" height="100%" class="upload-preview" />');
        }
		fileReader.readAsDataURL(objFileInput.files[0]);
    }
}


$(function(e){
    $("#form_upload_image").submit(function(r){
        form_data=new FormData(this)
        $.ajax({
            url:$(this).attr("action"),
            data:form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method:"POST",
            success:function(result){
                console.log(result);
                $("#result-box").html("<img src='/static/imageprocess/images/result/"+result["saved_name"]+"' width='100%' height='100%' />");
            },
            error:function(result){
                console.log("error");
            }
        });
        return false;
    });


    $("#form_equalize").submit(function(){
        
        form_data=new FormData(this)
        $.ajax({
            url:$(this).attr("action"),
            data:form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method:"POST",
            success:function(result){
                console.log(result);
                $("#result-box").html("<img src='/static/imageprocess/images/result/"+result["saved_name"]+"' width='100%' height='100%' />");
                $("#hist-preview").html("<img src='/static/imageprocess/images/hist/"+result["preview_hist"]+"' width='100%' height='100%' />");
                $("#hist-result-box").html("<img src='/static/imageprocess/images/histresult/"+result["new_hist"]+"' width='100%' height='100%' />");
            },
            error:function(result){
                console.log("error");
            }
        });
        return false;
    })
});