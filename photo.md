---
layout: page-full-width
title: Photos
fullscreen: false
full-width: true
addons: [comments, about]
#include:
#     js:
#         - /assets/gabryxx7/js/instafeed.min.js
#     css: 
#         - /assets/gabryxx7/css/gabry.css 

instagram: false
local_photos: true
---

> I am an amateur photographer who enjoys taking mostly landscape pictures. My current gear comprises:
> - Sony A7r III + Tamron 28-75mm f2.8
> - Mavic Air 2
> - Google Pixel 3 XL
{:.lead}
<!-- {:.message} -->
    

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
            template: {% raw %}"<article class='photo-card'> <div class='photo-card-img img'><img data-ignore src='{{image}}' loading='lazy'></img></div><a href='{{link}}' class='no-hover no-print-link photo-card-caption'><div class='img-title'>  </div> <div class='img-descr'> {{caption}} </div> </a></article>"{% endraw %},
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

{% if page.local_photos %}
    {% assign photolist = site.data.photos-list %}
    {% for photo in photolist.photos %}
        {% if photo.file %}
            {% if photo.highlight %}
                <article class='photo-card' style="flex: 0 1 auto;">
            {% else %}
                <article class='photo-card'>
            {% endif %}
                <div class='photo-card-img img'>
                    <img data-ignore src='{{ photolist.preview_folder }}{{ photo.file }}' loading='lazy'/>
                </div>
        {% else %}  
            <article class='photo-card multiple multi-{{ photo.files.size }}'>
                <div class='photo-card-img img'>
                {% for file in photo.files %}
                    <img data-ignore src='{{ photolist.preview_folder }}{{ file }}' loading='lazy'/>
                {% endfor %}    
                </div>
        {% endif %}
        <a href='{{ photo.url }}' class='no-hover no-print-link photo-card-caption'>
            {% if photo.title.size > 0 %}
                <div class='img-title'> <h3>{{ photo.title }}</h3></div>
            {% endif %}
            <div class='img-descr'> <p> {{ photo.caption }} </p> </div>
        </a>     
    {% if photo.location %}
        <div class="location"> <span class="icon-location2" style="font-size: 0.9rem;"> </span> {{ photo.location }}</div>
    {% endif %}
    </article>  
    {% endfor %}    
{% endif %}
    </div>
</div>
