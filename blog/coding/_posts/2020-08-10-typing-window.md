---
layout: post
title: How I made the blog's terminal animation
excerpt_separator: <!--more-->
# categories: [coding]
image: 
  path: /assets/gabryxx7/img/typing-window.png
  class: "wide-img"
  html: |-
    <div class='typing-window post' style='margin: 2rem;'>
    <div class='typing-toolbar'>
    <div class="typing-toolbar-btn min">—</div>
    <div class="typing-toolbar-btn size">☐</div>
    <div class="typing-toolbar-btn close disabled">✕</div>
    </div>
    <div class="typing-area">▌</div>
    </div>
description: >
  I made a gif of me mashing  the keyboard on hackertyper and it got me the idea of using this terminal as a welcoming animation!
---

<script>
var postTyperStarted = false;

var startPostTyper = function(typingWindow){
  postTyperStarted = true;
  var typingWindow = document.getElementsByClassName('typing-window post')[0];  

  if(!typingWindow){
    return;
  };
  
  var app = typingWindow.getElementsByClassName('typing-area')[0];
  var terminalStarter = "> <span style='color: #5cd400;'> gabryxx7@blog:</span><span style='color: #1c39c7;'>~</span>$ ";
  var typewriter = new Typewriter(app, {
    loop: false,
    delay: 'natural',
    cursor: '▌'
  });
  console.log("Starting post typer!");
  typewriter
  .changeDelay(90)
  .pasteString("<br /> " +terminalStarter)
  .pauseFor(1200)
  .typeString("Hey!")
  .pauseFor(1500)
  .pasteString("<br /> " +terminalStarter)
  .pauseFor(1200)
  .typeString("So you're wondering how I did this?")
  .pauseFor(800)
  .pasteString("<br /> " +terminalStarter)
  .pauseFor(1500)
  .typeString("Wonder <strong>NO MORE</strong>")
  .pauseFor(1000)
  .pasteString("<br /> " + terminalStarter)
  .pauseFor(500)
  .typeString("Here is a tutorial!")
  .start();
};
document.getElementById('_pushState').addEventListener('hy-push-state-load', function() {
    if(!postTyperStarted) startPostTyper();
});
document.addEventListener('DOMContentLoaded', function(){ 
  if(!postTyperStarted) startPostTyper();
}, false);
</script>


So I wanted to give my blog a cool vibe while also looking good. I did not want it to be too overwhelming with effects, sliding animations and such.
So I opted for something simple, it's just text after all! But it's also quite catchy and fun to watch.

So here is how I have achieved this effect, it's nothing crazy hard really but I love playing with CSS and Javascript and so I did.

<!--more-->

- Table of Contents
{:toc .large-only}

I started by looking for Javascript libraries that implemented the typewriter effect. I would rather go for pure javsacript than JQuery, even better if it's a lightweight specific library that only includes that effect.

So I found [Typewriter.js](https://github.com/tameemsafi/typewriterjs), which does exactly what I needed!

The challenge was of course to make sure it looked nice and smooth!

# Creating the terminal typewriter
## The basic HTML
The `html` is really simple, nothing to explain here. I just added a pipe `▌` character as default in the typing area so it does not look empty when the user loads the page and Typewriter has not started typing yet.

{% highlight html %}
  <div class='typing-window'>
    <div class="typing-area">▌</div>
  </div>
{% endhighlight %}


```html
  <div class='typing-window'>
    <div class="typing-area">▌</div>
  </div>
```

Now that we have our `html` structure we can start styling it and adding the actual typewriter to it!

## Styling the terminal
I wanted to give it a terminal look, but also not a `DOS` look, something a bit more fancy and modern. So I started with a simple rounded rectangle with a nice dark gray background:

{% highlight css %}
.typing-window {
  transition: opacity 0.5s, max-height 0.5s;
  max-height: 9000px;
  font-size: 1.6rem;
  line-height: 1.2;
  font-weight: 400;
  font-family: var(--code-font-family);
  background-color: #1f1f21;
  border-radius: 0.5rem;
  padding: 0;
  color: #ccc;
  margin-bottom: 2rem;
  box-shadow: 0 1px 1px rgba(0,0,0,0.12), 0 2px 2px rgba(0,0,0,0.12), 0 4px 4px rgba(0,0,0,0.12), 0 8px 8px rgba(0,0,0,0.12), 0 16px 16px rgba(0,0,0,0.12);
  
  strong {
    font-weight: 700;
  }

  .typing-area{
    padding: 1.5rem 1.5rem 1.5rem 1rem;
  }
}
{% endhighlight %}

<div class='typing-window'>
  <div class="typing-area">Terminal Example! The font is <strong><a href="https://github.com/tonsky/FiraCode">FiraCode</a></strong> <br/>
   <- -> != !== ==> |= ▌</div>
  </div>

(I LOVE this font, it's amazing and it has some cool ligatures!)
A few CSS tricks I learnt over the years:
- `transition`: It animates any change to the specified property, in this case I am aimating `opacity` and `max-height` so whenever they change, their value is animated in `0.5s`
- `font-family`: I am using the CSS variable that Hydejack uses for the code blocks font family, just to be consistent with the rest of the website
- `box-shadow`: This is a layered, high quality shadow generated with https://brumm.af/shadows

## Start typing!
This is the best part of the project!

Now that we have everything set up we can start typing in text into the terminal. Let's start by retreiving the container where the text will go

Ok so now that we have our container, we need to look for the typing area. It's also a good idea to only start typing if the container exists, and do nothing otherwise.
{% highlight javascript %}
var typerStarted = false;
var startTyper = function() {   
  typerStarted = true;
  var typingWindow = document.getElementsByClassName('typing-window')[0];  
  if(!typingWindow){
    return;
  };
  var app = typingWindow.getElementsByClassName('typing-area')[0];
  var typewriter = new Typewriter(app, {
    loop: true,
    delay: 'natural',
    cursor: '▌'
  });
  typewriter
  .pasteString("Hey, I'm alive!)
  .pauseFor(1200)
  .typeString("<br/> Yup, still alive!")
  .pauseFor(2000)
  .deleteChars(17)
  .typeString(" Noooo don't delete mee!")
  .pauseFor(1000)
  .start();
};
{% endhighlight %}

We also need to make sure that the typing only starts when the page content is loaded. In the case of Hydejack (the Jekyll theme I am using), we need to account for dynamic page loading so:

{% highlight javascript %}
document.addEventListener('DOMContentLoaded', function(){ 
  if(!typerStarted) startTyper();
}, false);
document.getElementById('_pushState').addEventListener('hy-push-state-load', function() {
  if(!typerStarted) startTyper();
});
{% endhighlight %}

Alright so let's test it out, shall we?


<div class='typing-window test'>
  <div class="typing-area"></div>
  </div>

<script>
var typerStarted = false;
var startTestTyper = function() {   
  typerStarted = true;
  console.log("Starting test typer");
  var typingWindow = document.getElementsByClassName('typing-window test')[0];  
  if(!typingWindow){
    return;
  };
  var app = typingWindow.getElementsByClassName('typing-area')[0];
  var typewriter = new Typewriter(app, {
    loop: true,
    delay: 'natural',
    cursor: '▌'
  });
  typewriter
  .pasteString("Hey, I'm alive!")
  .pauseFor(1200)
  .typeString("<br/> Yup, still alive!")
  .pauseFor(2000)
  .deleteChars(17)
  .typeString(" Noooo don't delete mee!")
  .pauseFor(1000)
  .start();
};

document.addEventListener('DOMContentLoaded', function(){ 
  if(!typerStarted) startTestTyper();
}, false);
document.getElementById('_pushState').addEventListener('hy-push-state-load', function() {
  if(!typerStarted) startTestTyper();
});

</script>

## Adding a status bar
Let's try and give it more of a terminal look now by adding a Ubuntu-styled status bar. Let's add a few `div`s for the bar and its buttons

{% highlight html %}
  <div class='typing-window'>
    <div class='typing-toolbar'>
      <div class="typing-toolbar-btn min">—</div>
      <div class="typing-toolbar-btn size">☐</div>
      <div class="typing-toolbar-btn close disabled">✕</div>
    </div>
    <div class="typing-area">▌</div>
  </div>
{% endhighlight %}

Let's style it up a little bit now. We want to use an `inset` shadow, and give a different color to the buttons.
The only clickable button should be the closing button so let's change it's `:hover:` CSS and also add a `disabled` state.


{% highlight css %}
.typing-toolbar {
  display: flex;
  justify-content: flex-end;
  height: 1.6rem;
  padding: 0.1rem 0.1rem 0.2rem 0.2rem;
  background-color: var(--border-color);
  border-radius: 0.5rem 0.5rem 0rem 0rem;
  box-shadow: inset -6px 3px 10px 0px rgba(0,0,0,0.11);

  .typing-toolbar-btn {
    transition: background-color 250ms;
    display: inline-block;
    height: 1.1rem;
    width: 1.1rem;
    margin-top: 0.1rem;
    margin-right: 0.7rem;
    position: relative;
    z-index: 2;
    border-radius: 100%;
    margin-bottom: 0.2rem;
    text-align: center;
    font-size: 0.8rem;
    padding-top: 0.1rem;
    color: #848282;
    font-weight: 700;
  }
  .typing-toolbar-btn.close {
    background-color: #e01e1e;
  }
  .typing-toolbar-btn.close.disabled {
    background-color: #693737;
    color: #8e8e8e;
  }
  
  .typing-toolbar-btn.min {
    background-color: var(--body-bg);
  }
  .typing-toolbar-btn.size {
    background-color: var(--body-bg);
  }
  .typing-toolbar-btn.close:not(.disabled):hover,
  .typing-toolbar-btn.close:not(.disabled):focus,
  .typing-toolbar-btn.close:not(.disabled):active {
    transition: background-color 250ms;
    background-color: #f94b29;
    cursor: pointer;
  }
}
{% endhighlight %}

<div class='typing-window test-close_noaction'>
  <div class='typing-toolbar'>
    <div class="typing-toolbar-btn min">—</div>
    <div class="typing-toolbar-btn size">☐</div>
    <div class="typing-toolbar-btn close">✕</div>
  </div>
  <div class="typing-area">▌</div>
</div>

Now for the final touch, let's make it so that the close button actually closes the terminal, but we'll enable the button after 10 seconds so there is time for some text to be typed in the terminal!

{% highlight javascript %}
var startTestTyper = function() {   
  typerStarted = true;
  var typingWindow = document.getElementsByClassName('typing-window test')[0];  
  if(!typingWindow){
    return;
  };

  //Let's retreive the close button, remember that getElementsByClassName returns an array
  //of elements but we only need the first one
  var closeBtn =  typingWindow.getElementsByClassName('typing-toolbar-btn close')[0];
  setTimeout (function() {
    closeBtn.classList.toggle('disabled');
    closeBtn.onclick = function() {
          typewriter.stop();
          typingWindow.style.opacity = 0.01;
      };
  }, 10000);

  
  //Let's listen for the end of the CSS transition (remember how opacity and max-height are animated in css?)
  typingWindow.addEventListener('transitionend', function(event) {
    //We don't want this to run for all the children, just this specific target
    //Events propagate through the DOM tree
    if(event.target !== event.currentTarget)
      return;
      // Javascript returns max-height as a string "0px" so we need to check it it's "0px" before removing the element
    if (event.propertyName === "max-height" && typingWindow.style.maxHeight === "0px"){
      typingWindow.remove();
    }else if(event.propertyName === "opacity" && typingWindow.style.opacity < 0.1){
      //We FIRST change the opacity to make it invisible and only THEN we scale it down to slide the other content up
      typingWindow.style.maxHeight = 0;
    };
 });
  ...
};
{% endhighlight %}

<div class='typing-window test-close'>
  <div class='typing-toolbar'>
    <div class="typing-toolbar-btn min">—</div>
    <div class="typing-toolbar-btn size">☐</div>
    <div class="typing-toolbar-btn close disabled">✕</div>
  </div>
  <div class="typing-area">▌</div>
</div>

<script>
var closeTyperStarted = false;
var startTestCloseTyper = function() {   
  closeTyperStarted = true;
  var typingWindow = document.getElementsByClassName('typing-window test-close')[0];  
  if(!typingWindow){
    return;
  };
  
  var closeBtn =  typingWindow.getElementsByClassName('typing-toolbar-btn close')[0];
  setTimeout (function() {
    closeBtn.classList.toggle('disabled');
    closeBtn.onclick = function() {
          typewriter.stop();
          typingWindow.style.opacity = 0.01;
      };
  }, 10000);
  
  typingWindow.addEventListener('transitionend', function(event) {
    if(event.target !== event.currentTarget)
      return;
      /* Javascript returns max-height as a string "0px" */
    if (event.propertyName === "max-height" && typingWindow.style.maxHeight === "0px"){
      typingWindow.remove();
    }else if(event.propertyName === "opacity" && typingWindow.style.opacity < 0.1){
      typingWindow.style.maxHeight = 0;
    };
 });

  var app = typingWindow.getElementsByClassName('typing-area')[0];
  var typewriter = new Typewriter(app, {
    loop: true,
    delay: 'natural',
    cursor: '▌'
  });
  typewriter
  .pasteString("Hey, I'm alive!")
  .pauseFor(1200)
  .typeString("<br/> Yup, still alive!")
  .pauseFor(2000)
  .deleteChars(17)
  .typeString(" Noooo don't delete mee!")
  .pauseFor(1000)
  .start();
};

document.addEventListener('DOMContentLoaded', function(){ 
  if(!closeTyperStarted) startTestCloseTyper();
}, false);
document.getElementById('_pushState').addEventListener('hy-push-state-load', function() {
  if(!closeTyperStarted) startTestCloseTyper();
});

</script>

**Heads up**: Reload the page if you don't see the terminal or if you closed it already!
{:.message}
The code is fairly simple:
1. Retreive the close button
2. Add an event listener to its click
3. Add an event listener to the `typingWindow` `transitionend`
3. When It gets clicked, set the opacity of the window to 0
4. CSS will start the animation, when it's over it will trigger the event `transitionend`
5. On the event handler we check if the opacity is below a certain threshold, if it is then the element is invisible and we can scale it down by
  setting its `max-height` to 0
5. When the `transitionend` is triggered again we'll check if `max-height` is equal to `0px` and if its we can remove the whole `typingWindow` from the DOM

## Extras (looping, list of words, emojis)
Alright so here are a few extra tricks I implemented to save some time. I am also writing it down for me to remember.
The way `Typewriter.js` works is by adding events to a queue. Calling `pasteString()` `deleteChars()` or `pauseFor()` will add those events to the queue, and they will be executed in order whenever `start()` is called. After that, we won't be able to add any new event to the queue, we'll only be able to `stop()` the typewriter.

I wanted my typewriter to keep changing the last few words in loop so I implemented a little trick without having to rewrite the library:

{% highlight javascript %}
function appendLeadingZeroes(n){
  if(n <= 9){
    return "0" + n;
  };
  return n;
};

function strip(html){
  var doc = new DOMParser().parseFromString(html, 'text/html');
  return doc.body.textContent || "";
};

var randomDelay = function(){
  return Math.random() * (pause[1] - pause[0] + pause[0]);
};

  var totalLoops = 20;
  var wordList = ["<em>PhD Student</em> 📚", "Programmer 💻", "Photographer 📷", "Pizza Lover 🍕", "Gamer 👾", "Swimmer 🏊", "Traveller 🌏"];
  var pause = [1000, 4500];
  var terminalStarter = "> <span style='color: #5cd400;'> gabryxx7@blog:</span><span style='color: #1c39c7;'>~</span>$ ";
  var current_datetime = new Date();
  var formatted_date = current_datetime.getFullYear() + "-" + appendLeadingZeroes(current_datetime.getMonth() + 1) + "-" + appendLeadingZeroes(current_datetime.getDate()) + " " + appendLeadingZeroes(current_datetime.getHours()) + ":" + appendLeadingZeroes(current_datetime.getMinutes()) + ":" + appendLeadingZeroes(current_datetime.getSeconds());

  var typewriter = new Typewriter(app, {
    loop: false,
    delay: 'natural',
    cursor: '▌'
  });
  typewriter
  .pasteString(terminalStarter +"["+formatted_date+"]")
  .pauseFor(1000);
  .changeDelay(90)
  .pasteString("<br /> " +terminalStarter)
  .pauseFor(1200)
  .typeString("Hey!")
  .pauseFor(800)
  .typeString(" I'm <strong>Gabriele</strong>")
  .pauseFor(1000)
  .pasteString("<br /> " + terminalStarter)
  .typeString(" I'm a...");

  for(var k = 0; k < totalLoops; k++){ 
    for(var i=0; i < wordList.length; i++){
      typewriter
      .typeString(wordList[i])
      .pauseFor(randomDelay())
      .deleteChars(strip(wordList[i]).length);
    };
  };
  typewriter.start();
{% endhighlight %}
So the main idea is to have a list of words that keep being written and deleted, but I did not want to manually enter the char to delete every time.
So by using a list I can delete the length of the previous word and type in the new one:

- Create a list of words
- Type the first part of the text (non looped)
- Add a loop which types in and deletes each word from the list (including pauses)
- 
- Loop the previous loop for how many times you want. If you have 10 words with a delay of 2 seconds between each word, 100 loops will take ~2000 seconds, around half an hour.

**TIP:** You can use `html` to format your text, but don't forget that `deleteChars()` of Typewriter expects the number of chars without counting html, so a simple `string.length` in javascript won't work. You need to strip the string of the html and that's where `strip()` comes in
{:.message}
**Heads up:** I tried with 100 loops and I noticed it would take a few seconds for the Typewriter to start, slowing down the page loading, so I use 20 loops
{:.message}


# Adding a terminal typewriter to your page or post

## Adding content to the blog page

So first thing I did was to allow for the Hydejack's blog page layout to include content besides the list of post, so I copied the blog layout from hydejack and create a new layout file `_layouts/blog__custom.html` based on the `base` layout:

**TIP:** You can avoid Jekyll capturing liquid code by wrapping it in `\{\% raw \%\} \{\% endraw \%\}`
{:.message}

{% highlight liquid %}
{% raw %}
---
layout: base
---

{{ content | markdownify }}
{% assign plugins = site.plugins | default:site.gems %}

{% if plugins contains 'jekyll-paginate' %}
  {% assign posts = paginator.posts %}
{% else %}
  {% assign posts = site.categories[page.slug] | default:site.tags[page.slug] | default:site.posts %}
{% endif %}
  
{% for post in posts %}
  {% include_cached components/post.html post=post no_link_title=page.no_link_title no_excerpt=page.no_excerpt hide_image=page.hide_image %}
{% endfor %}

{% if plugins contains 'jekyll-paginate' %}
  {% include components/pagination.html %}
{% endif %}

{% endraw %}
{% endhighlight %}

So you can see how I added {% raw %}`{{ content | markdownify }}`{% endraw %} to the top to add whatever content I'll write to any page using `blog-custom` as a layout.

Now that we can add content to the top of the blog page we can start creating our structure for the typewriter window:

## Allowing for custom featured images in posts

I made a few changes to the Hydejack theme so that I could:
- Display wide images as a post feature image
- Display divs and javascript content as a featured post content (as you can see for this post)

For the first point I simply added custom classes for posts, I added a `class` property to the post `image` (aside from `path`).
In order to use this new property I edited the `_incudes/component/hy-img.html` as below:

{% highlight liquid %}
{% raw %}
{% assign img_class = include.img.class | default:"" %}
{% assign include_class = include.class | default:"" %}
{% classes = include_class | concat: img_class %}
<img
  {{ sources }}
  {% if include.alt %}alt="{{ include.alt }}"{% endif %}
  {% if classes != '' %}class="{{ classes }}"
  {% if include.property %}property="{{ include.property }}"{% endif %}
  {% if include.width %}width="{{ include.width }}"{% endif %}
  {% if include.height %}height="{{ include.height }}"{% endif %}
  {% if include.width and include.height %}loading="lazy"{% endif %}
/>
{% endraw %}
{% endhighlight %}
I simply always add classes to the `img` tag which are empty by default, in this way I am sure this will work with the pre-existing configuration. If I always added `include.img.class` when it did not exist I could have incurred into issues later, and I definitely wouldn't want to remove `include.class` as it might be used in otehr cases. Furthermore, I did not want to add any `style` tag simply because I noticed the `hy-img` always end up with `style="opacity: 0;` in the final `html` page and I am not sure if that's needed or not so I did not want to overwrite that.

Let's not forget to add the `CSS` for dealing with wide featured images:

{% highlight css %}
.content .aspect-ratio img.wide-img {
  margin: auto;
  width: 100%;
  /* height: 100%; */
  /* object-fit: scale-down; */
  object-position: center;
  background-color: var(--gray-bg);
  vertical-align: middle;
  object-fit: scale-down !important;
}
{% endhighlight %}

For the second point of displaying divss into post featured images, it was actually fairly simple. Sasme as before I added a new post image property called `html`, I then edited the file `_includes/component/post.html` so that if `image.html` is definied it will use the html instead of the image path. so I changed this :

{% highlight liquid %}
{% raw %}
<div class="lead aspect-ratio sixteen-nine flip-project-img">
  {% include_cached components/hy-img.html img=post.image alt=post.title width=864 height=486 %}
</div>
{% endraw %}
{% endhighlight %}

To this:

{% highlight liquid %}
{% raw %}
  {% if post.image.html %}
    <div class="lead aspect-ratio sixteen-nine flip-project-html">
      {{ post.image.html }}
    </div>
  {% else %}
    <div class="lead aspect-ratio sixteen-nine flip-project-img">
      {% include_cached components/hy-img.html img=post.image alt=post.title width=864 height=486 %}
    {% endif %}
{% endraw %}
{% endhighlight %}

Last touch, I added the console effect `html` to the post property which now looks something like this:

{% highlight yaml %}
---
layout: post
title: How I made the blog's terminal animation
excerpt_separator: <!--more-->
# categories: [coding]
image: 
  path: /assets/gabryxx7/img/typing-window.png
  class: "wide-img"
  html: |-
    <div class='typing-window post' id='typing-window'>
    <div class='typing-toolbar'>
    <div class="typing-toolbar-btn min">—</div>
    <div class="typing-toolbar-btn size">☐</div>
    <div class="typing-toolbar-btn close disabled" id="typing-close-btn">✕</div>
    </div>
    <div class="typing-area">▌</div>
    </div>
description: >
  I made a gif of me mashing  the keyboard on hackertyper and it got me the idea of using this terminal as a welcoming animation!
---
{% endhighlight %}

Beware that this only works in the post page or in the post preview, it will NOT work in the post card when showed as related post (you'd have to edit `_includes/component/post-card.html` for that). I would not recommend it as it makes everything more complicated and messy with loading randomg javascript all the time. For this reason I would suggest to have an image to display as a fallback option

## Adding the javascript
When it comes to the post terminal I can simply add the javascript shown above in between the `<script></script>` tags. For the page, I added the javascript to the `_includes/my-scripts.html`. The event listeners will try to load the terminal at every page but the function returns if there is no element with classes `typing-window blog`.

**IMPORTANT**: When deploying jekyll with the command `JEKYLL_ENV=production bundle exec jekyll build` (to enable the search function) make sure that your javascript is **PERFECT** as in, add a `;` to EVERY statement. Otherwise then it gets minified, something like 
{% highlight javascript %}
var test = 1
var test = 3
{% endhighlight %}
Becomes:
{% highlight javascript %}
var test = 1var test = 3
{% endhighlight %}
Generating an error and making your whole javascript code crash


An important note, if you end up using IDs instead of classes, multiple terminials on the same page might not work. The reason is that when Javascript calls `getElementById()` it always retreives one only element with that id. That's the purpose of IDs, right? Uniquely identifying elements. If we want it to work for ANY html element with the class `typing-window` we need to use `getElementByClass()` as shown above.

## Adding a description to your page terminal
You will notice I also added a little description to the typing window to link to this post, I simply wrapped the whole window in another div like this:

{% highlight html %}
<div class="typing-window-wrapper">
  <p class="note-sm">
    Do you want to make one yourself for your website? Check this post out:
    <strong><a href="/blog/blog/coding/2020-08-10-typing-window/" class="flip-title">How I made the blog's terminal animation</a></strong>
  </p>
  <div class='typing-window blog'>
    <div class='typing-toolbar'>
      <div class="typing-toolbar-btn min">—</div>
      <div class="typing-toolbar-btn size">☐</div>
      <div class="typing-toolbar-btn close disabled">✕</div>
    </div>
    <div class="typing-area">▌</div>
  </div>
</div>
{% endhighlight %}

I then added some extra `CSS` to `_sass/my-style.scss`

{% highlight css %}
.typing-window-wrapper .note-sm{
  position: absolute;
  right: 23rem;
  width: 21rem;
  padding: 0.5rem 1rem 0 1rem;
}
{% endhighlight %}