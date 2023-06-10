$(document).ready(function(){
    document.getElementById('root-div').addEventListener('click', function() {
        document.getElementById('upload-field').click();
    });
    
    // Get the name of the uploaded file
    $("#upload-field").on('change',function(event){
        let filename=$("#upload-field").val().split('\\');
        // Set a standard size
        maxSizeInBytes = 4 * 1024 * 1024;
        // Get the size of the file the user is uploading
        file_detail=event.target.files[0]
        console.log(file_detail.size,"size of")
        if (file_detail.size < maxSizeInBytes){
            $("#file_name").text(filename[2])
            $(".merger-btn-holder").html(`<button >Merge</button>`)
        }else{
            $("#file_name").text('File too large ! (max: 4mb)')
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
                'X-CSRFToken': csrftoken
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
                    $("#shorten_link").html(`
                    
                    <div class="mb-3 p-3 bg-dark text-white"><small>Visit: <a href="https://ft9javideomergeapp.pythonanywhere.com/ft9ja/${resp.short_url}" class="text-white">https://ft9javideomergeapp.pythonanywhere.com/ft9ja/${resp.short_url}</a></small></div>
                    `)
                    navigator.clipboard.writeText(`https://ft9javideomergeapp.pythonanywhere.com/ft9ja/${resp.short_url}`)
                    window.alert("Link copied !")
                })
                // Add the video for streamng
                $(".rectangle-bg").html(`
                    <div id="video-container">
                    <video controls autoplay>
                    <source src="${resp.file_loc}" type="video/mp4">
                    <source src="${resp.file_loc}" type="video/webm">
                    <source src="${resp.file_loc}" type="video/ogg">
                    <source src="${resp.file_loc}" type="video/mov">
                    <source src="${resp.file_loc}" type="video/avi">
                    <source src="${resp.file_loc}" type="video/wmv">
                    <source src="${resp.file_loc}" type="video/flv">
                    <source src="${resp.file_loc}" type="video/mkv">
                    <source src="${resp.file_loc}" type="video/mpeg">
                    <!-- Add more source tags for other video formats if needed -->
                    </video>
                
                    </div>
                `)
            },
            error:function(err){
                console.log(err)
                $(".message").html(
                    `<div class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
                    <small>An error occured !</small>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`
                )
                $(".merger-btn-holder").html(`<button>Merge</button>`)
            }
        })

    });
})


