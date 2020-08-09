---
layout: photo-feed
title: Photos
addons: [comments, about]
---

> I am an amateur photographer who enjoys taking mostly landscape pictures. My current gear comprises:
> - Sony A7r III + Tamron 28-75mm f2.8
> - Mavic Air 2
> - Google Pixel 3 XL
{:.lead}
<!-- {:.message} -->
    
<div class="photo-feed">
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
</div>
