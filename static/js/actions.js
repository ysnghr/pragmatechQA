function vote_actions(type, id, color, value){
  count = $(type + id + "_count").html();
  $(type + id + "_count").html(parseInt(count) + value);
  $(type + id).css("fill", color);
}

function actions(id, user, type, vote) {
  $.ajax({
    type: "POST",
    url: `${window.location.href}`,
    data: { action_type: vote, id: id, user: user, type: type, csrfmiddlewaretoken: window.CSRF_TOKEN },
    dataType: "json",
    success: function (response) {
      if (vote == "dislike") {
        if (response.disliked == "True") {
          vote_actions(".dislike_",id, "#666f74", - 1);
        } else {
          vote_actions(".dislike_",id, "#2c62a0", 1);
          if (response.liked == "True"){
            vote_actions(".like_",id, "#666f74", - 1);
          }
        }
      }
      else if (vote == "like"){
        if (response.liked == "True") {
          vote_actions(".like_",id, "#666f74", - 1);
        } else {
          vote_actions(".like_",id, "#2c62a0", 1);
          if (response.disliked == "True"){
            vote_actions(".dislike_",id, "#666f74", - 1);
          }
        }
      }
    },
  });
}
