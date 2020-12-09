function vote_actions(type, id, color, value, label){
  count = $(type + id + "_count" + '[label=\''+ label + '\']').html();
  $(type + id + "_count" + '[label=\''+ label + '\']').html(parseInt(count) + value);
  $(type + id + '[label=\''+ label + '\']').css("fill", color);
}

function actions(id, user, type, vote, post_type, comment_id = null) {

  if(comment_id == null)
  {
    $.ajax({
      type: "POST",
      url: `${window.location.href}`,
      data: { 
        'post_type': post_type,
        'action_type': vote, 
        'id': id, 
        'user': user, 
        'type': type, 
        'csrfmiddlewaretoken': window.CSRF_TOKEN },
      dataType: "json",
      success: function (response) {
        if (vote == "dislike") {
          if (response.disliked == "True") 
          {
            vote_actions(".dislike_",id, "#666f74", - 1, 'question');
          } 
          else 
          {
            vote_actions(".dislike_",id, "#2c62a0", 1, 'question');
            if (response.liked == "True")
            {
              vote_actions(".like_",id, "#666f74", - 1, 'question');
            }
          }
        }
        else if (vote == "like")
        {
          if (response.liked == "True") 
          {
            vote_actions(".like_",id, "#666f74", - 1, 'question');
          } 
          else 
          {
            vote_actions(".like_",id, "#2c62a0", 1, 'question');
            if (response.disliked == "True"){
              vote_actions(".dislike_",id, "#666f74", - 1, 'question');
            }
          }
        }
      },
    });
  }
  else
  {
    $.ajax({
      type: "POST",
      url: `${window.location.href}`,
      data: { 
        'post_type': post_type,
        'action_type': vote, 
        'id': id, 
        'comment_id' : comment_id,
        'user': user, 
        'type': type, 
        'csrfmiddlewaretoken': window.CSRF_TOKEN },
      dataType: "json",
      success: function (response) {
        if (vote == "dislike") 
        {
          if(response.liked == "False" &&  response.disliked == "False" )
          {
            $(`.dislike_${comment_id}`).css("fill", "#2c62a0");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) - 1
            $(`.vote_result_${comment_id}`).html(vote_result)
          }
          else if (response.liked == "True" &&  response.disliked == "False")
          {
            $(`.dislike_${comment_id}`).css("fill", "#2c62a0");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) - 2
            $(`.vote_result_${comment_id}`).html(vote_result)
            $(`.like_${comment_id}`).css("fill", "#666f74");
          }
          else if (response.liked == "False" &&  response.disliked == "True")
          {
            $(`.dislike_${comment_id}`).css("fill", "#666f74");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) + 1
            $(`.vote_result_${comment_id}`).html(vote_result)
          }
          
        }
        else if (vote == "like")
        {
          if(response.liked == "False" &&  response.disliked == "False" )
          {
            $(`.like_${comment_id}`).css("fill", "#2c62a0");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) + 1
            $(`.vote_result_${comment_id}`).html(vote_result)
          }
          else if (response.liked == "True" &&  response.disliked == "False")
          {
            $(`.like_${comment_id}`).css("fill", "#666f74");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) - 1
            $(`.vote_result_${comment_id}`).html(vote_result)
          }
          else if (response.liked == "False" &&  response.disliked == "True")
          {
            $(`.like_${comment_id}`).css("fill", "#2c62a0");
            vote_result = parseInt($(`.vote_result_${comment_id}`).html()) + 2
            $(`.vote_result_${comment_id}`).html(vote_result)
            $(`.dislike_${comment_id}`).css("fill", "#666f74");
          }



          // if (response.liked == "True") 
          // {
          //   $(`.like_${comment_id}`).css("fill", "#666f74");
          //   vote_result = parseInt($(`.vote_result_${comment_id}`).html()) - 1
          //   $(`.vote_result_${comment_id}`).html(vote_result)
          // } 
          // else 
          // {
          //   vote_actions(".like_",comment_id, "#2c62a0", 1, 'comment');
          //   if (response.disliked == "True")
          //   {
          //     vote_actions(".dislike_",comment_id, "#666f74", - 1, 'comment');
          //   }
          // }
        }
      },
    });
  }

}


function check_answer(question_id, comment_id) 
{
    $.ajax({
      type: "POST",
      url: `${window.location.href}`,
      data: { 
        'question_id': parseInt(question_id), 
        'comment_id': parseInt(comment_id), 
        'post_type': 'select_answer',
        'csrfmiddlewaretoken': window.CSRF_TOKEN },

      dataType: "json",
      success: function (response) 
      {
        myList = document.querySelectorAll('[label="label_comment_id"]')
        
        for(var i = 0; i < myList.length;  i++)
        {
            if($(myList[i]).val() == comment_id)
            {
              if(response.fill_green)
              {
                $(myList[i]).closest('.tt-item').find('.select_answer').css('fill','#48A868')
                $(myList[i]).closest('.tt-item').addClass('tt-wrapper-success')

              }              
              else
              {
                $(myList[i]).closest('.tt-item').find('.select_answer').css('fill','#aeb3b4')
                $(myList[i]).closest('.tt-item').removeClass('tt-wrapper-success')
              }
            }
            else
            {
              $(myList[i]).closest('.tt-item').find('.select_answer').css('fill','#aeb3b4')
              $(myList[i]).closest('.tt-item').removeClass('tt-wrapper-success')

            }

        }
        
        
      },
    });
  
}



