

var tempCommentElement = null;

function CommentEdit(element)
{
    tempCommentElement = $(element.closest('.comment-wrapper'))
    var question_id = $('[label="label_question_id"]').val()
    var comment_id = $(element.closest('.comment-wrapper')).find('[label="label_comment_id"]').val()
    $.ajax({
        type: "POST",
        url: `${window.location.href}`,
        data: { 
            'question_id': parseInt(question_id), 
            'comment_id': parseInt(comment_id), 
            'post_type': 'comment_edit-read',
            'csrfmiddlewaretoken': window.CSRF_TOKEN },
            dataType: "json",
        success: function (response) 
        {
            contentErrorDiv = $("div[label='comment_content_edit_error']")
            if($('[label="comment_edit_dropzone_wrapper"]').children().length)
            {
                contentErrorDiv.removeClass('d-none')
                contentErrorDiv.find('span[label="error_content"]').text('Digər commenti editləmək üçün hazırda editlənən commenti ləğv edəsiniz. ')
                $('html,body').animate({scrollTop: contentErrorDiv.offset().top - 100},'slow');
                return;
            }
            else
            {
                contentErrorDiv.addClass('d-none');
                id_comment_content_edit.setData(response.content)
                $('[label="comment_edit_dropzone_wrapper"]').append('<div class="dropzone dz" id="commentEditDropzone"></div>')            
                $('[label="post_comment"]').addClass('d-none')
                $('[label="edit_comment"]').removeClass('d-none')   
                $('html,body').animate({scrollTop: $('[label="edit_comment"]').offset().top - 100},'slow');
                CommentEditDropzone(response, question_id, comment_id)
            }
        },
    }); // End of AJAX
} //End of Event listener


// Cancel The Editing
$('#comment_edit_cancel_btn').on('click', function(e){
    e.preventDefault()
    $('html,body').animate({scrollTop: tempCommentElement.offset().top - 100},'slow');
    $('[label="comment_edit_dropzone_wrapper"]').empty()
    $('[label="post_comment"]').removeClass('d-none')   
    $('[label="edit_comment"]').addClass('d-none') 
})//End of Event listener



function CommentEditDropzone(response, question_id, comment_id)
{

    Dropzone.autoDiscover = false;
    var isEnter = true;
    var commentEditDropzone = new Dropzone("#commentEditDropzone", {
        url: `${window.location.href}`,
        headers:{
            'X-CSRFToken' : window.CSRF_TOKEN 
        },
        autoProcessQueue: false,
        maxFiles : 2, // (Back-End : 2)
        maxFilesize : 2, //2 MB (Back-End : 2 MB)
        parallelUploads: 2,
        uploadMultiple : true,
        addRemoveLinks: true,
        autoProcessQueue: false, // Bununla biz submit etdikde filelar yuklenecek
        acceptedFiles: 'image/*', // (Back-End : only images)
        dictDefaultMessage: 'Əlavə şəkilləri bura yükləyin',
        dictFallbackMessage: 'Əlavə şəkilləri bura yükləyin',
        dictRemoveFile: 'Şəkli sil',
        dictFileTooBig: `Şəkilin tutumu böyüdür. Max şəkil tutumu: 2 MB`,
        dictInvalidFileType: 'Yalnız şəkil yükləyə bilərsiniz',
        dictMaxFilesExceeded: 'Maximum 2 şəkil yükləyə bilərsiniz',
        dictResponseError: "Server responded with {{statusCode}} code.",
        init: function() {
            dzClosure = this; // Makes sure that 'this' is understood inside the functions below.
    
            for (let i = 0; i < response.comment_image_info.length; i++) 
            {  
                this.options.addedfile.call(this, response.comment_image_info[i]);
                this.options.thumbnail.call(this, response.comment_image_info[i], response.comment_images_urls[i]);
                response.comment_image_info[i].previewElement.classList.add('dz-success');
                response.comment_image_info[i].previewElement.classList.add('dz-complete');      
            }  
            
             // for Dropzone to process the queue (instead of default form behavior):
            $('#comment_edit_submit_btn').on("click", function(e) {
                
                if (CheckCommentContent() & CheckImageLength())
                {
                    if (dzClosure.getQueuedFiles().length > 0) 
                    {
                        isEnter = true;                                
                        e.preventDefault();
                        e.stopPropagation();  
                        dzClosure.processQueue(); 
                        $('#comment_edit_submit_btn').addClass('disabled')
                        return false
                    } 
                    else 
                    {               
                        isEnter = true;                      
                        e.preventDefault();
                        var blob = new Blob(); //Back check is blob or not
                        blob.upload = { 'chunked': dzClosure.defaultOptions.chunking };
                        dzClosure.uploadFile(blob);
                        $('#comment_edit_submit_btn').addClass('disabled')
                    }    
                }
                else
                {
                    $('html,body').animate({scrollTop: $("div[label='comment_content_edit_error']").offset().top - 100},'slow');
                    e.preventDefault();
                    return false;
                }
            });

            //send all the form data along with the files:
            this.on("sendingmultiple", function(data, xhr, formData) 
            {
                formData.append("question_id", question_id);
                formData.append("comment_id", comment_id);
                formData.append("post_type", "comment_edit-update");
                formData.append("content", id_comment_content_edit.getData());
                formData.append("server_images", response.comment_images_urls);
            });
           
            function CheckCommentContent()
            {
                content = id_comment_content_edit.getData()
                contentErrorDiv = $("div[label='comment_content_edit_error']")
                if(!content) //Empty
                {
                    contentErrorDiv.removeClass('d-none')
                    contentErrorDiv.find('span[label="error_content"]').text('Mövzu doldurulmalıdır.')
                    return false;
                }
                else
                {   
                    contentErrorDiv.addClass('d-none');
                    return true;
                }
            };

            function CheckImageLength()
            {
                image_counter = response.comment_images_urls.length + dzClosure.getQueuedFiles().length;
                imageErrorDiv = $("div[label='comment_content_edit_error']")
                if(image_counter > 2) //Empty
                {
                    imageErrorDiv.removeClass('d-none')
                    imageErrorDiv.find('span[label="error_content"]').text('Maximum 2 şəkil yükləyə bilərsiz.')
                    //$('html,body').animate({scrollTop: imageErrorDiv.offset().top - 100},'slow');
                    return false;
                }
                else
                {   
                    imageErrorDiv.addClass('d-none');
                    return true;
                }

            };
        },

        success: function(file, response)
        {
            if(isEnter)
            {
                isEnter = false
                html = `
                            <input label='label_comment_id' type="hidden" value="${response.comment_id}">
                            <div class="tt-single-topic">
                                <div class="tt-item-header pt-noborder">
                                    <div class="tt-item-info info-top">
                                        <div class="tt-avatar-icon">
                                            <i class="tt-icon"><svg><use xlink:href="#icon-ava-t"></use></svg></i>
                                        </div>
                                        <div class="tt-avatar-title">
                                            <a href="#">${response.full_name}</a>
                                        </div>
                                        <a href="#" class="tt-info-time">
                                            <i class="tt-icon"><svg><use xlink:href="#icon-time"></use></svg></i>${response.created_date} (Dəyişdirildi)
                                        </a>
                                    </div>
                                    ${IsOwner(response.owner)}
                                </div>
                                <div class="tt-item-description">
                                    ${response.content}
                                    <div style="display: flex; justify-content: space-around;">
                                    ${GetImages(response.images)}
                                    </div>
                                </div>
    
                                <div class="tt-item-info info-bottom">
                                <!-- Upvote(like) -->
                                    <a href="#" class="tt-icon-btn" onclick="event.preventDefault(); actions(${response.question_id},'${$('#request_user').val()}', 'comment', 'like', 'comment_vote', ${response.comment_id});">                               
                                        <svg label='comment' class=" like_${response.comment_id}" style='fill:#666f74;' width="36" height="36" viewBox="0 0 36 36">
                                            <path d="M2 26h32L18 10 2 26z"></path>
                                        </svg>                               
                                    </a>
                                    <!-- Vote result: -->
                                    <span label='comment' style="color: #666f74; font-size: 20px; padding: 2px 20px 0px 20px;" class="vote_result_${response.comment_id}"> 0 </span>
                                    <!-- Downvote(dislike) -->
                                    <a href="#" class="tt-icon-btn" onclick="event.preventDefault(); actions(${response.question_id},'${$('#request_user').val()}', 'comment', 'dislike', 'comment_vote', ${response.comment_id});" >                             
                                        <svg label='comment' class=" dislike_${response.comment_id}" style='fill:#666f74;' width="36" height="36" viewBox="0 0 36 36">
                                            <path d="M2 10h32L18 26 2 10z"></path>
                                        </svg>                                
                                    </a>  
                                    <div class="col-separator"></div>
                                    <div class="tt-row-icon">
                                        <div class="tt-item">
                                            <!-- Edit -->
                                            <a label="comment_edit_btn" onclick="event.preventDefault(); CommentEdit(this)" href="#" class="tt-icon-btn tt-position-bottom">
                                                <i style="font-size: 22px; color: #666f74; cursor: pointer;" class="tt-icon fas fa-edit"></i>                                                              
                                            </a>                                                                                
                                        </div>   
                                        <div class="tt-item">
                                            <!-- Delete -->
                                            <a label="comment_delete_btn" onclick="event.preventDefault(); CommentDelete(this)" href="#" class="tt-icon-btn tt-position-bottom">
                                                <i style="font-size: 22px; color: red; cursor: pointer;" class="fas fa-trash-alt"></i>
                                            </a>                           
                                        </div>                                                                                                               
                                    </div>                         
                                </div>
                            </div>`
                tempCommentElement.empty()
                tempCommentElement.append(html)
    
                code = tempCommentElement.find('code')[0]
                if(code)
                {
                    hljs.highlightBlock(code)
                    tempCommentElement.find('code').addClass("hljs javascript");
                }
                $('html,body').animate({scrollTop: tempCommentElement.offset().top - 100},'slow');
    
                setTimeout(function(){ 
                    $('html,body').animate({scrollTop: tempCommentElement.offset().top - 100},'slow');
                    $('[label="comment_edit_dropzone_wrapper"]').empty()
                    $('[label="post_comment"]').removeClass('d-none')   
                    $('[label="edit_comment"]').addClass('d-none') 
                }, 2000); // 2 sec
    
    
                function IsOwner(argOwner)
                {
                    if(argOwner)
                    {
                        return ` <div class="tt-item-info info-top">                                
                                    <div class="tt-avatar-icon" style="padding-top: 60px;"> 
                                        <a href="#" onclick="event.preventDefault(); check_answer(${response.question_id}, ${response.comment_id});">
                                            <i class="tt-icon"><svg   width="36" height="36" viewBox="0 0 36 36"><path class="select_answer" style='fill:#aeb3b4;' d="M6 14l8 8L30 6v8L14 30l-8-8v-8z"></path></svg></i>
                                        </a> 
                                    </div>                                
                                </div>`
                    }
                    else
                    {
                        return ``
                    }
                }
    
                function GetImages(argImages)
                {
                    temp_html = ''
                    for (var i = 0; i < argImages.length; i++)
                    {
                        temp_html += `<div>
                                        <a href="${argImages[i]}" data-lightbox="comment_${response.comment_id}_imagegroup">
                                            <img style="width: auto; height:200px;"src="${argImages[i]}" alt="">
                                        </a>
                                    </div>`
                    }
                    return temp_html;
    
                }
            }        
        },
    
        
        removedfile: function(file) 
        {
            for (var i=0; i < response.comment_images_urls.length; i++)
            {
                if(response.comment_images_urls[i].split("/").pop() == file.name)
                {
                    response.comment_images_urls.splice(i, 1);
                }        
                file.previewElement.remove();    
            }    
        }

    })
} // End of function (CommentEditDropzone)


// Comment Delete

function CommentDelete(element){
    tempCommentElement = $(element.closest('.comment-wrapper')) 
    swal("Sualı sildikdən sonra geri qaytarmaq mümkün olmayacaq.", {
        icon: "warning",
        title: "Bu etmək istədiyindən əminsən?",
        text: "Commenti sildikdən sonra geri qaytarmaq mümkün olmayacaq.",
        buttons: {
            cancel: "Yox!",
            catch: {
            text: "Hə!",
            value: "remove",
            },
        },
    }) //End of swal
    .then((value) => {
        if(value == 'remove')
        {
            var question_id = $('[label="label_question_id"]').val()
            var comment_id = tempCommentElement.find('[label="label_comment_id"]').val()
            $.ajax({
                type: "POST",
                url: `${window.location.href}`,
                data: { 
                    'question_id': parseInt(question_id), 
                    'comment_id': parseInt(comment_id), 
                    'post_type': 'comment_delete',
                    'csrfmiddlewaretoken': window.CSRF_TOKEN },
                    dataType: "json",
                success: function (response) 
                {
                    if(response)
                    {
                        tempCommentElement.remove();
                        $('html,body').animate({scrollTop: $("div.question-wrapper").offset().top - 100},'slow');
                    }
                    else
                    {
                        alert('Sistemde problem var zehmet olmasa Discord Supporta bildirin.')          
                    }
                },
            }); // End of AJAX
        }        
    }); // End of then
}; // End of Event listener







