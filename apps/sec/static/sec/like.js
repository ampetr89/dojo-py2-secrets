
$(document).ready(function(){
    LIKE_URL = "{% url 'users:add_like' 1 %}"
    $('.like').click(function(e){
        
        controls = $(this).parent().parent().parent();
        secret_id = controls.attr('secid');
        n_likes = controls.find('.n_likes');
        
        likeword = controls.find('.likeword');
        $.ajax({
            url: LIKE_URL.replace('1', secret_id),
            success: function(res){
                
                n_likes.text(parseInt(n_likes.text())+1);
                if(n_likes.text()==1){
                    likeword.text('Like');
                }else{
                    likeword.text('Likes');
                }
                
            },
            method: 'GET'
        })
        e.preventDefault();
        
    })
})
