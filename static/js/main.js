$(document).ready(function(){
    $("#upload-btn").click(()=>{
        console.log("Hello clicked")
        $("#upload-field").click()
    })

    // Get the name of the uploaded file
    $("#upload-field").on('change',function(){
        let filename=$("#upload-field").val().split('\\');
        $("#file_name").text(filename[2])
    })
        
})

