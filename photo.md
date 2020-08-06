---
layout: photos
title: Photography
fullscreen: false
full-width: true
#include:
#     js:
#         - /assets/gabryxx7/js/instafeed.min.js
#     css: 
#         - /assets/gabryxx7/css/gabry.css 

instagram: false
photos: true
---

 <div class="columns">
    <div id="instafeed">
    <hy-img data-ignore>
        <span class="loading" slot="loading">
            <span class="icon-cog"></span>
        </span>
        <br/>
    </hy-img>


{% if page.instagram %}
    <script type="text/javascript">
        // $("#instafeed").attr("test","ciao");
        var feed = new Instafeed({
            target: 'instafeed',
            get: 'user',
            sortBy: 'most-recent',
            resolution: 'standard_resolution',
            userId: '{{ site.instagram.user_id }}',
            accessToken: '{{ site.instagram.access_token }}',
            clientId: '{{ site.instagram.client_id }}',
            limit: '100',
            template: {% raw %}"<article class='project-card'> <div class='project-card-img img'><img data-ignore src='{{image}}' loading='lazy'></img></div><a href='{{link}}' class='no-hover no-print-link project-card-caption'><div class='img-title'>  </div> <div class='img-descr'> {{caption}} </div> </a></article>"{% endraw %},
            success: function(response){
                $("#instafeed hy-img").remove();
                console.log("Instafeed.js response", response);
            }
        });
        feed.run();
    </script>
{% else %}
    <script type="text/javascript">
        $("#instafeed hy-img").remove();
    </script>
{% endif %}

{% if page.photos %}
    {% assign photolist = site.data.photos-list %}
    {% for photo in photolist.photos %}
        <article class='project-card'>
            <div class='project-card-img img'>
                <img data-ignore src='{{ photolist.preview_folder }}{{ photo.file }}' loading='lazy'/>
            </div>
            <a href='{{ photo.url }}' class='no-hover no-print-link project-card-caption'>
                <div class='img-title'> {{ photo.title }}</div>
                <div class='img-descr'> {{ photo.caption }} </div>
            </a>
        </article>        
    {% endfor %}    
{% endif %}
    </div>
</div>
