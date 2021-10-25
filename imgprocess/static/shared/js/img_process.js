function showPreview(objFileInput, html_element) {
    if (objFileInput.files[0]) {
        var fileReader = new FileReader();
        fileReader.onload = function (e) {
            $(html_element).html('<img src="' + e.target.result + '" width="100%" height="100%" class="upload-preview" />');
        }
        fileReader.readAsDataURL(objFileInput.files[0]);
    }
}


$(function (e) {
    //on va forcer le telechargement des fichiers pgm
    $("#download-pgm-result").click(function(){
        var dname=$(this).attr("data-download")
        $.get($(this).attr("data-url"),{download_name:dname},function(e){
            
        });
    });

    $("#image-viewver").hide();
    $("#image-viewver").click(function () {
        $(this).fadeOut(1000)
    });
    $(document).on("click", "img:not(.viewver)", function () {
        $("#image-viewver .content").html("<img src='" + $(this).attr("src") + "' class='viewver' />");
        $("#image-viewver").fadeIn(1000)
    });

//exemple de requete ajax
    $("#form_upload_image").submit(function (r) {
        form_data = new FormData(this)
        $.ajax({
            url: $(this).attr("action"),
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method: "POST",
            success: function (result) {
                console.log(result);
                $("#result-box").html("<img src='/static/imageprocess/images/result/" + result["saved_name"] + "' width='100%' height='100%' />");
                $("#download-pgm-result").attr("data-download",result["pgm_name"])
            },
            error: function (result) {
                console.log("error");
            }
        });
        return false;
    });


    $("#form_equalize").submit(function () {

        form_data = new FormData(this)
        $.ajax({
            url: $(this).attr("action"),
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method: "POST",
            success: function (result) {
                console.log(result);
                $("#result-box").html("<img src='/static/imageprocess/images/result/" + result["saved_name"] + "' width='100%' height='100%' />");
                $("#hist-preview").html("<img src='/static/imageprocess/images/hist/" + result["preview_hist"] + "' width='100%' height='100%' />");
                $("#hist-result-box").html("<img src='/static/imageprocess/images/histresult/" + result["new_hist"] + "' width='100%' height='100%' />");
            },
            error: function (result) {
                console.log("error");
            }
        });
        return false;
    });


    $("#form_make_operation").submit(function () {
        form_data = new FormData(this)
        $.ajax({
            url: $(this).attr("action"),
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method: "POST",
            success: function (result) {
                $("#result-box").html("<img src='/static/imageprocess/images/result/" + result["saved_name"] + "' width='100%' height='100%' />");
            },
            error: function (result) {
                console.log("error");
            }
        });
        return false;
    });
   
    $("#form_make_convolution").submit(function () {
        form_data = new FormData(this)
        $.ajax({
            url: $(this).attr("action"),
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            method: "POST",
            success: function (result) {
                $("#result-box").html("<img src='/static/imageprocess/images/" + result["saved_name"] + "' width='100%' height='100%' />");
            },
            error: function (result) {
                console.log("error");
            }
        });
        return false;
    });

    $(".sober-horizontal").click(function(){
        $("#kernel").val("-1 -2 -1\n0 0 0\n1 2 1")
    });
    $(".sober-vertical").click(function(){
        $("#kernel").val("-1 0 1\n-2 0 2\n-1 0 1")
    });
    $(".filtre-moyenneur").click(function(){
        $("#kernel").val("0.1111 0.1111 0.1111\n0.1111 0.1111 0.1111\n0.1111 0.1111 0.1111")
    });

    $(".filtre-laplacien").click(function(){
        $("#kernel").val("0 1 0\n1 -4 1\n0 1 0")
    });

    $(".filtre-prewit-x").click(function(){
        $("#kernel").val("-1 0 1\n-1 0 1\n-1 0 1")
    });

    $(".filtre-prewit-y").click(function(){
        $("#kernel").val("-1 -1 -1\n0 0 0\n1 1 1")
    });
    $(".filtre-constrate").click(function(){
        $("#kernel").val("0 -1 0\n-1 5 -1\n0 -1 1")
    });
    $(".filtre-repoussage").click(function(){
        $("#kernel").val("-2 1 0\n-1 1 1\n0 1 2")
    });

    $(".filtre-flou").click(function(){
        $("#kernel").val("1 1 1\n1 1 1\n1 1 1")
    });

    $(".filtre-gaussien").click(function(){
        $("#kernel").val("0.0625 0.125 0.0625\n0.125 0.25 0.125\n0.0625 0.125 0.0625")
    });



});


