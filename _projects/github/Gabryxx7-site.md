---
layout: project
title: Gabryxx7-site
icon: icon-github
caption: Just a personal blog made with Jekyll and a heavily customised version of
  Hydejack free
date: 2019-08-11 09:47:36
image:
  path: /assets/gabryxx7/img/GitHub/Gabryxx7-site/matrix_coding.gif
description: Just a personal blog made with Jekyll and a heavily customised version
  of Hydejack free
links:
- title: Source
  url: https://github.com/Gabryxx7/Gabryxx7-site

---

---
layout: home
cover: true
# image: /assets/img/blog/hydejack-9.jpg
image: /assets/gabryxx7/img/matrix_coding.gif
description: >
  Hydejack is a boutique Jekyll theme for hackers, nerds, and academics,
  with a focus on personal sites that are meant to impress.
hide_description: true
selected_projects:
  - _projects/nick-engmann.md
  - /showcase/shawn-yeager/
projects_page: showcase.md
selected_posts:
  - hydejack/_posts/2020-07-03-introducing-hydejack-9.md
  - /blog/hydejack/2018-09-01-introducing-dark-mode/
  - hydejack/_posts/2018-06-30-introducing-hydejack-8.md
  - hydejack/_posts/2018-06-01-example-content-iii.md
posts_page: /posts/
no_third_column: true
title: Gabriele Marini
---

# [Gabryxx7 Personal Blog](http://gmarini.com/)
![Screenshot](/assets/gabryxx7/img/GitHub/Gabryxx7-site/matrix_coding.gif){:.lead width="1920" height="1080" loading="lazy"}

~~~r

library(tidyverse)
library(lubridate)
library(scales)
library(Cairo)
library(data.table)
library(reshape2)
library(Cairo)

generateGantt <- function(tasks, hlines, vlines=NULL, plotTitle="Timeline", fontFamily="Open Sans"){
  # Custom theme for making a clean Gantt chart
  theme_gantt <- function(base_size=11, base_family=fontFamily) {
    ret <- theme_bw(base_size, base_family) %+replace%
      theme(panel.background = element_rect(fill="#ffffff", colour=NA),
            axis.title.x=element_text(vjust=-0.2), axis.title.y=element_text(vjust=1.5),
            title=element_text(vjust=1.2, family=fontFamily),
            panel.border = element_blank(),
            axis.line=element_blank(),
            panel.grid.minor.x=element_line(size=0.2, colour="grey90"),
            panel.grid.major.x = element_line(size=0.4, colour="grey85"),
            panel.grid.major.y = element_blank(),
            panel.grid.minor.y = element_blank(),
            axis.ticks=element_blank(),
            legend.position="none", 
            axis.title=element_text(size=rel(0.8), family=fontFamily),
            strip.text=element_text(size=rel(1), family=fontFamily),
            strip.background=element_rect(fill="#ffffff", colour=NA),
            panel.spacing.y=unit(1.5, "lines"),
            legend.key = element_blank())
    ret
  }

~~~

```r
library(tidyverse)
library(lubridate)
library(scales)
library(Cairo)
library(data.table)
library(reshape2)
library(Cairo)

generateGantt <- function(tasks, hlines, vlines=NULL, plotTitle="Timeline", fontFamily="Open Sans"){
  # Custom theme for making a clean Gantt chart
  theme_gantt <- function(base_size=11, base_family=fontFamily) {
    ret <- theme_bw(base_size, base_family) %+replace%
      theme(panel.background = element_rect(fill="#ffffff", colour=NA),
            axis.title.x=element_text(vjust=-0.2), axis.title.y=element_text(vjust=1.5),
            title=element_text(vjust=1.2, family=fontFamily),
            panel.border = element_blank(),
            axis.line=element_blank(),
            panel.grid.minor.x=element_line(size=0.2, colour="grey90"),
            panel.grid.major.x = element_line(size=0.4, colour="grey85"),
            panel.grid.major.y = element_blank(),
            panel.grid.minor.y = element_blank(),
            axis.ticks=element_blank(),
            legend.position="none", 
            axis.title=element_text(size=rel(0.8), family=fontFamily),
            strip.text=element_text(size=rel(1), family=fontFamily),
            strip.background=element_rect(fill="#ffffff", colour=NA),
            panel.spacing.y=unit(1.5, "lines"),
            legend.key = element_blank())
    ret
  }
  
  if(!grepl("ndex", colnames(tasks)))
    tasks$Index <- seq(nrow(tasks),1,-1)
  tasks$Start <- as.POSIXct(tasks$Start, origin="1970-01-01")
  tasks$End <- as.POSIXct(tasks$End, origin="1970-01-01")
  breaks <- tasks$Task
  labels <- breaks
  
  
  markers <- tasks[grep("marker", tasks$Type),]
  markers$Task <- ""
  markers$Project <- ""
  
  if(!("MarkerSize" %in% colnames(markers))){
    #markers <- transform(markers, MarkerSize = as.numeric(MarkerSize))
    markers$MarkerSize <-9
  }
  
  if(!("MarkerShape" %in% colnames(markers))){
    #markers <- transform(markers, MarkerShape = as.numeric(MarkerShape))
    markers$MarkerShape <-18
  }
  
  if(!("MarkerColor" %in% colnames(markers))){
    markers$MarkerColor <- as.factor("#E8E8E8")
    #markers <- transform(markers, MarkerColor = as.character(MarkerColor))
  }
  
  if(!("MarkerOffset" %in% colnames(markers))){
    #markers <- transform(markers, MarkerOffset = as.numeric(MarkerOffset))
    markers$MarkerOffset <-0
  }
  
  if(!("MarkerXPos" %in% colnames(markers))){
    #markers <- transform(markers, MarkerXPos = as.character(MarkerXPos))
    markers$MarkerXPos <- "center"
  }
  
  markers[markers$MarkerXPos == ""] <- "center"
  
  markers$PosY <- markers$Index - markers$MarkerOffsetY
  markersStart <- markers[grep("tart", markers$MarkerXPos),]
  markersStart$PosX <- difftime(markersStart$End , markersStart$Start, units="secs")*0.9 + markersStart$Start
  
  markersEnd <- markers[grep("nd", markers$MarkerXPos),]
  markersEnd$PosX <- difftime(markersEnd$End , markersEnd$Start, units="secs")*0.1 + markersEnd$Start
  
  markersCenter <- markers[grep("enter", markers$MarkerXPos),]
  markersCenter$PosX <- difftime(markersCenter$End , markersCenter$Start, units="secs")*0.5 + markersCenter$Start
  
  allDates <- melt(tasks[,c("Start", "End")])$value
  yearsVlines <- data.frame("date"=as.POSIXct(lubridate::ymd(unique(lubridate::year(allDates)), truncated=2L)))
  hour(yearsVlines$date) <- 0
  
  bars <- tasks[grep("bar", tasks$Type),]
  
  if(!("BarColor" %in% colnames(bars))){
   # bars <- transform(bars, BarColor = as.character(BarColor))
    bars$BarColor <- "#E8E8E8"
  }
  
  if(!("BarSize" %in% colnames(bars))){
    #bars <- transform(bars, BarSize = as.character(BarSize))
    bars$BarSize <- "#E8E8E8"
  }
  
  # Build plot
  timeline <- ggplot()
  
  if(!is.null(vlines)){
    vlines$Date <- as.POSIXct(vlines$Date, origin="1970-01-01")
    timeline <- timeline + geom_vline(data=vlines, aes(xintercept=Date, color=Color, linetype=LineType, size=Size))
  }
  
  if(!is.null(hlines))
    timeline <- timeline + geom_hline(data=hlines,aes(yintercept=Index, color=Color, linetype=LineType, size=Size))
  
  tasks$LabelFace[tasks$LabelFace == ""] <- "plain"
  
  
  if(!("LabelFace" %in% colnames(tasks))){
    #tasks <- transform(tasks, LabelFace = as.character(LabelFace))
    tasks$LabelFace <- "#E8E8E8"
  }
  if(!("LabelColor" %in% colnames(tasks))){
    #tasks <- transform(tasks, LabelColor = as.character(LabelColor))
    tasks$LabelColor <- "#E8E8E8"
  }
  if(!("LabelSize" %in% colnames(tasks))){
    #tasks <- transform(tasks, LabelSize = as.character(LabelSize))
    tasks$LabelSize <- "#E8E8E8"
  }
  
  
  timeline <- timeline +
    geom_vline(data=yearsVlines,aes(xintercept=date, color="grey70", linetype="solid", size=0.65)) +
    geom_segment(data=bars, aes(x=Start, xend=End, y=Index, yend=Index, color=BarColor, size=BarSize)) + 
    geom_point(data=markersStart, mapping=aes(x=PosX, y=PosY, size=MarkerSize-0.5, color=MarkerColor, shape=MarkerShape)) +
    geom_point(data=markersEnd, mapping=aes(x=PosX, y=PosY, size=MarkerSize-0.5, color=MarkerColor, shape=MarkerShape)) +
    geom_point(data=markersCenter, mapping=aes(x=PosX, y=PosY, size=MarkerSize-0.5, color=MarkerColor, shape=MarkerShape)) +
    scale_color_identity() +
    scale_shape_identity() +
    scale_linetype_identity() +
    scale_size_identity() +
    scale_y_continuous(breaks=tasks$Index, labels=labels, trans='reverse') +
    scale_x_datetime(date_labels = "%b '%y", date_breaks="1 month", expand = expand_scale(mult = c(.015, .015))) +
    guides(colour=guide_legend(title=NULL)) +
    labs(x=NULL, y=NULL) +
    theme_gantt() +
    ggtitle(label = plotTitle) +
    theme(axis.text.x=element_text(angle=0, hjust=0.5, size=7), axis.text.y=element_text(color=tasks$LabelColor, face=tasks$LabelFace, size=tasks$LabelSize))
  
  return(list("timeline"=timeline))
}
```

[gmarini.com](http://gmarini.com/)

Developded with [Jekyll](https://jekyllrb.com/) and [Hydejack](https://hydejack.com/).

I heavily customised the free version of Hydejack with some new layouts, a custom resume, custom dark mode, a gallery, some code highlighting and so on...

There are still some fixed I need to do but it's looking good so far, might want to automate the instagram feed gallery pull

# Hydejack

A boutique Jekyll theme for hackers, nerds, and academics.  
{:.lead}

1. this list will be replaced by the toc
{:toc .large-only}

![Screenshot](/assets/gabryxx7/img/GitHub/Gabryxx7-site/hydejack-9.jpg){:.lead width="1920" height="1080" loading="lazy"}

Hydejack's cover page on a variety of screen sizes.
{:.figcaption}


**Hydejack** is a boutique Jekyll theme for hackers, nerds, and academics, with a focus on personal sites that are meant to impress. 

It includes a blog that is suitable for both prose and technical documentation, a portfolio to showcase your projects, and a resume template that looks amazing on the web and in print.

> Your complete presence on the web — A [blog], [portfolio], and [resume].
{:.lead}


## A Personal Site That Won't Disappear

**Hydejack** is 100% built on Open Source software, and is Open Source itself, save for parts of the PRO version. The PRO version is a one-time payment that gives you the right to use it forever.

Hydejack is all static sites. _HTML_. All you need is a web server --- any web server --- to have a professional web presence that lasts a lifetime.


## A Free Blogging Theme
**Hydejack** started out as a free blogging theme for Jekyll — and continues to be so.

<!--posts-->


## An Impressive Portfolio
A portfolio that's guaranteed to be impressive — no matter what you put into it.

<!--projects-->


## A Printable Resume
Get a resume that's consistent across the board — whether it's on the web, mobile, print, or [PDF](assets/Resume.pdf).

[![Resume PDF](/assets/gabryxx7/img/GitHub/Gabryxx7-site/resume.png){:.lead width="884" height="632" loading="lazy"}][resume]{:.no-hover}

Front and center page of a print resume generated by Hydejack.
{:.figcaption}


## Just Markdown
Write all content with Markdown. __Hydejack__ gives you [additional CSS classes](docs/writing.md) to stylize your content, without losing compatibility with other Jekyll themes.


## Just Markup
**Hydejack** boasts a plethora of modern JavaScript, but make no mistake: It's still a _plain old web page_ at its core. It works without JavaScript and you can even view it in a text-based browser like `w3m`:

![w3m Screenshot](/assets/gabryxx7/img/GitHub/Gabryxx7-site/w3m.png){:width="1920" height="1260" loading="lazy"}

The Hydejack blog, as seen by the text browser `w3m`.
{:.figcaption}


## Syntax Highlighting
**Hydejack** features syntax highlighting, powered by [Rouge].

```js
// file: `example.js`
document.querySelector("hy-push-state").addEventListener("hy-push-state-load", () => {
  const supportsCodeHighlights = false; // TBD!!
});
```

Code blocks can have a filename and a caption.
{:.figcaption}


## Beautiful Math
They say math is beautiful — and with **Hydejack**'s [math support][math] it's guaranteed to also look beautiful:

$$
\begin{aligned}
  \phi(x,y) &= \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right) \\[2em]
            &= \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j)            \\[2em]
            &= (x_1, \ldots, x_n)
               \left(\begin{array}{ccc}
                 \phi(e_1, e_1)  & \cdots & \phi(e_1, e_n) \\
                 \vdots          & \ddots & \vdots         \\
                 \phi(e_n, e_1)  & \cdots & \phi(e_n, e_n)
               \end{array}\right)
               \left(\begin{array}{c}
                 y_1    \\
                 \vdots \\
                 y_n
               \end{array}\right)
\end{aligned}
$$

Hydejack uses KaTeX to efficiently render math.
{:.figcaption}


## Build an Audience
The PRO version has built-in support for customizable [Tinyletter] newsletter subscription boxes.

If you are using a different service like MailChimp, you can build a custom newsletter subscription box using [Custom Forms][forms].

{% include pro/newsletter.html %}


## Features

{% include features.md %}


## Download

{% include table.md %}


## Get It Now

Use the the form below to purchase Hydejack PRO:

<div class="gumroad-product-embed" data-gumroad-product-id="nuOluY"><a href="https://gumroad.com/l/nuOluY">Loading…</a></div>


[blog]: /blog/
[portfolio]: showcase.md
[resume]: resume.md
[download]: download.md
[welcome]: README.md
[forms]: forms-by-example.md

[features]: #features
[news]: README.md#build-an-audience
[syntax]: README.md#syntax-highlighting
[latex]: #beautiful-math
[dark]: hydejack/_posts/2018-09-01-introducing-dark-mode.md
[search]: #_search-input
[grid]: _featured_categories/hydejack.md

[lic]: LICENSE.md
[pro]: licenses/PRO.md
[docs]: docs/README.md
[ofln]: docs/advanced.md#enabling-offline-support
[math]: docs/writing.md#adding-math

[kit]: https://github.com/hydecorp/hydejack-starter-kit/releases
[src]: https://github.com/hydecorp/hydejack
[gem]: https://rubygems.org/gems/jekyll-theme-hydejack
[buy]: https://gum.co/nuOluY

[gpss]: https://developers.google.com/speed/pagespeed/insights/?url=https%3A%2F%2Fhydejack.com%2Fdocs%2F
[rouge]: http://rouge.jneen.net
[katex]: https://khan.github.io/KaTeX/
[mathjax]: https://www.mathjax.org/
[tinyletter]: https://tinyletter.com/
