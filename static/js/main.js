$(document).ready(function(){
    $("#upload-btn").click(()=>{
        console.log("Hello clicked")
        $("#upload-field").click()
    })

    // Get the name of the uploaded file
    $("#upload-field").on('change',function(event){
        let filename=$("#upload-field").val().split('\\');
        // Set a standard size
        maxSizeInBytes = 10 * 1024 * 1024;
        // Get the size of the file the user is uploading
        file_detail=event.target.files[0]
        console.log(file_detail.size,"size of")
        if (file_detail.size < maxSizeInBytes){
            $("#file_name").text(filename[2])
            $(".merger-btn-holder").html(`<button >Merge</button>`)
        }else{
            $("#file_name").text('File too large !')
            $(".merger-btn-holder").html(`<button disabled>Merge</button>`)
            };
        
    })
    // Prvent form reload as the data is being processed
    $("#video-form").submit((e)=>{
        e.preventDefault();
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();
        var formData = new FormData($('#video-form')[0]);
        $(".message").html(
            `<div class="alert alert-success alert-dismissible fade show mt-3" role="alert">
            <small>Video merging. This will take a while to complete</smal>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`
        );
        $(".merger-btn-holder").html(`<button disabled>  
        <div class="spinner-border text-dark" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
        </button>`)
        // Get the form data and submit
        $.ajax({
            type: "post",
            url:"",
            data:formData,
            headers: {
                'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
              },
            processData: false,
            contentType: false,
            dataType: "json",
            success:function(resp){
                console.log(resp);
                $('#video-form')[0].reset()
                $(".message").html(
                    `<div class="alert alert-success alert-dismissible fade show mt-3" role="alert">
                    <small>${resp.details}</smal>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`
                );
                $("#file_name").text("");
                $(".merger-btn-holder").html(`<button>Merge</button>`)
                // Add download functionality to the button
                $("#download_btn").click(()=>{
                    var downloadLink = document.createElement('a');
                    downloadLink.href = `${resp.file_loc}`;
                    downloadLink.download = `${resp.file_name}`; 
                    // Trigger the download
                    downloadLink.click();
                })
                // Add share functionality
                $("#share_btn").click(()=>{
                    navigator.clipboard.writeText(`${resp.file_loc}`)
                    window.alert("Link copied !")
                })
            },
            error:function(err){
                console.log(err)
                $(".message").html(
                    `<div class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
                    <small>${err}</small>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`
                )
                $(".merger-btn-holder").html(`<button>Merge</button>`)
            }
        })

    });
})


