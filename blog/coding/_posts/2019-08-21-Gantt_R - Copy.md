---
layout: post
title: Gantt charts in R
excerpt_separator: <!--more-->
image: 
  path: /assets/gabryxx7/img/typing-window.png
  class: "wide-img"
  html: |-
    <div style='background-color: var(--body-bg);'><h2> DAMN </h2></div>
# categories: [coding]
# image: /assets/img/blog/hydejack-8.png
---
## Title test2

list:
- list1
- list 2
- list 3


The blog part is a WIP, this is a test
<!--more-->
{% comment %}
{% highlight R %}
{% endhighlight %}
{% endcomment %}
```R
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


Convallis aenean et tortor at risus viverra. Purus non enim praesent elementum. Quisque id diam vel quam. Id velit ut tortor pretium viverra suspendisse. Vitae nunc sed velit dignissim sodales ut eu sem. Nisl purus in mollis nunc sed. Congue eu consequat ac felis donec et odio. Accumsan tortor posuere ac ut consequat semper. Purus in massa tempor nec feugiat. Ac ut consequat semper viverra. Sit amet nisl purus in mollis nunc sed. Porta lorem mollis aliquam ut porttitor leo a. Et leo duis ut diam. Eget velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Faucibus purus in massa tempor nec feugiat nisl pretium fusce. Nibh nisl condimentum id venenatis a. Volutpat diam ut venenatis tellus in. Ac turpis egestas sed tempus urna et pharetra pharetra. Nisl tincidunt eget nullam non nisi.

Facilisi nullam vehicula ipsum a arcu cursus. Condimentum vitae sapien pellentesque habitant morbi tristique senectus et netus. Integer malesuada nunc vel risus commodo viverra maecenas. Vel risus commodo viverra maecenas accumsan lacus. Ullamcorper dignissim cras tincidunt lobortis feugiat. Et egestas quis ipsum suspendisse ultrices gravida dictum fusce ut. Ante metus dictum at tempor commodo ullamcorper. Porttitor massa id neque aliquam vestibulum morbi blandit cursus risus. Id leo in vitae turpis massa. Eget nunc scelerisque viverra mauris in. Risus viverra adipiscing at in tellus integer feugiat scelerisque. Risus nec feugiat in fermentum posuere. Ac turpis egestas maecenas pharetra convallis posuere.

Dignissim cras tincidunt lobortis feugiat. Nec dui nunc mattis enim. Dictum at tempor commodo ullamcorper. Maecenas sed enim ut sem viverra aliquet eget sit. Turpis egestas integer eget aliquet nibh praesent tristique magna. Sed velit dignissim sodales ut. Quis ipsum suspendisse ultrices gravida dictum fusce ut. Luctus accumsan tortor posuere ac ut consequat. Adipiscing elit duis tristique sollicitudin nibh sit amet. In hendrerit gravida rutrum quisque non tellus orci ac auctor. Placerat duis ultricies lacus sed turpis. Sagittis nisl rhoncus mattis rhoncus urna neque viverra justo nec. Tempor id eu nisl nunc mi. Felis bibendum ut tristique et egestas quis ipsum suspendisse ultrices.

Mauris augue neque gravida in. Odio ut sem nulla pharetra diam sit amet. Diam sit amet nisl suscipit adipiscing bibendum est ultricies. Tincidunt id aliquet risus feugiat in. Senectus et netus et malesuada fames ac turpis egestas. Placerat duis ultricies lacus sed turpis tincidunt id aliquet. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non. Est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque. Penatibus et magnis dis parturient montes nascetur. At varius vel pharetra vel turpis nunc eget. Ornare lectus sit amet est placerat in egestas erat. Urna et pharetra pharetra massa massa ultricies mi. Varius morbi enim nunc faucibus a pellentesque. Pulvinar neque laoreet suspendisse interdum.

Fringilla ut morbi tincidunt augue interdum. Vulputate ut pharetra sit amet. Tempus urna et pharetra pharetra massa. Tristique risus nec feugiat in fermentum posuere urna nec tincidunt. Sed lectus vestibulum mattis ullamcorper. Ipsum dolor sit amet consectetur. Lacus vel facilisis volutpat est velit egestas dui id ornare. Nulla facilisi etiam dignissim diam quis enim. Aliquet lectus proin nibh nisl condimentum id venenatis. Senectus et netus et malesuada fames.

Sollicitudin tempor id eu nisl nunc mi. Senectus et netus et malesuada fames ac turpis. Facilisis magna etiam tempor orci eu. Neque vitae tempus quam pellentesque nec. Sed lectus vestibulum mattis ullamcorper. In hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit. At varius vel pharetra vel turpis nunc eget. Malesuada bibendum arcu vitae elementum curabitur vitae nunc sed. Ultrices eros in cursus turpis massa tincidunt dui ut ornare. Purus sit amet luctus venenatis lectus. Congue eu consequat ac felis donec et odio pellentesque. Malesuada fames ac turpis egestas integer. Ut aliquam purus sit amet luctus venenatis lectus magna fringilla. In nisl nisi scelerisque eu ultrices vitae. Dictumst quisque sagittis purus sit amet volutpat consequat mauris. Sollicitudin nibh sit amet commodo nulla facilisi nullam. Dignissim suspendisse in est ante in nibh mauris. Sit amet nisl purus in mollis nunc sed id.

Hac habitasse platea dictumst quisque sagittis purus sit amet. Ut tellus elementum sagittis vitae et leo duis ut. Hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit. Platea dictumst vestibulum rhoncus est pellentesque elit. Nisi vitae suscipit tellus mauris a diam maecenas. Ut ornare lectus sit amet est. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Purus ut faucibus pulvinar elementum integer enim neque volutpat ac. Rhoncus est pellentesque elit ullamcorper dignissim cras. Penatibus et magnis dis parturient montes nascetur. Nisl purus in mollis nunc. Condimentum id venenatis a condimentum vitae sapien pellentesque habitant. Commodo quis imperdiet massa tincidunt nunc. Vitae tempus quam pellentesque nec nam aliquam sem et. Ullamcorper sit amet risus nullam eget felis eget nunc. Viverra suspendisse potenti nullam ac. Est velit egestas dui id ornare arcu odio ut.

Tincidunt praesent semper feugiat nibh sed pulvinar. Vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras tincidunt. Sapien eget mi proin sed libero enim sed faucibus. Et netus et malesuada fames ac. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Lorem ipsum dolor sit amet consectetur adipiscing. Lacus vestibulum sed arcu non odio euismod. Viverra mauris in aliquam sem fringilla ut morbi tincidunt augue. Mattis nunc sed blandit libero volutpat sed cras. Integer eget aliquet nibh praesent tristique. Urna condimentum mattis pellentesque id nibh. Faucibus scelerisque eleifend donec pretium vulputate. Pulvinar neque laoreet suspendisse interdum consectetur libero id faucibus. Commodo quis imperdiet massa tincidunt. Elit pellentesque habitant morbi tristique senectus.

Vel pretium lectus quam id leo in. Diam vel quam elementum pulvinar etiam non quam lacus suspendisse. Lectus sit amet est placerat. Et netus et malesuada fames ac turpis egestas. In massa tempor nec feugiat nisl pretium fusce. Consequat ac felis donec et. Sodales ut eu sem integer vitae justo. Est lorem ipsum dolor sit. At risus viverra adipiscing at in tellus integer feugiat. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper. Tincidunt eget nullam non nisi est. Amet est placerat in egestas erat. Et odio pellentesque diam volutpat commodo sed egestas. Sed ullamcorper morbi tincidunt ornare massa. Ut placerat orci nulla pellentesque dignissim enim sit amet.

Malesuada nunc vel risus commodo viverra maecenas. Ultrices sagittis orci a scelerisque. Quam vulputate dignissim suspendisse in est ante in nibh mauris. Feugiat sed lectus vestibulum mattis ullamcorper velit sed. Risus feugiat in ante metus dictum at tempor. Nascetur ridiculus mus mauris vitae ultricies leo integer malesuada. Eget mauris pharetra et ultrices neque ornare. Et sollicitudin ac orci phasellus. Tellus molestie nunc non blandit massa enim nec. Tellus integer feugiat scelerisque varius morbi enim nunc.

Posuere lorem ipsum dolor sit amet consectetur. Vulputate sapien nec sagittis aliquam malesuada bibendum arcu vitae elementum. Facilisis magna etiam tempor orci eu lobortis elementum. Blandit turpis cursus in hac habitasse platea dictumst quisque. Vitae aliquet nec ullamcorper sit amet risus nullam eget. Porta non pulvinar neque laoreet suspendisse interdum consectetur. Aliquam eleifend mi in nulla posuere. Vestibulum morbi blandit cursus risus at. Volutpat est velit egestas dui id. Aliquam ultrices sagittis orci a. Mi in nulla posuere sollicitudin aliquam ultrices sagittis.

In hendrerit gravida rutrum quisque non tellus orci. Scelerisque mauris pellentesque pulvinar pellentesque. Mauris augue neque gravida in fermentum et sollicitudin ac. Integer vitae justo eget magna fermentum iaculis eu non. Ac felis donec et odio pellentesque diam volutpat commodo sed. Vitae tortor condimentum lacinia quis vel eros donec ac odio. Suspendisse in est ante in nibh mauris cursus mattis molestie. Tellus in hac habitasse platea dictumst vestibulum rhoncus est. Ut aliquam purus sit amet luctus venenatis lectus magna fringilla. Integer quis auctor elit sed vulputate. Tempus iaculis urna id volutpat lacus laoreet. Neque ornare aenean euismod elementum nisi quis eleifend quam. Cursus risus at ultrices mi. Lectus arcu bibendum at varius vel pharetra. Orci ac auctor augue mauris. Tellus rutrum tellus pellentesque eu tincidunt tortor aliquam nulla facilisi.

Mi ipsum faucibus vitae aliquet. Tellus id interdum velit laoreet id donec ultrices. Neque viverra justo nec ultrices dui. Sed viverra ipsum nunc aliquet bibendum enim. Mauris augue neque gravida in fermentum et sollicitudin ac. Ut placerat orci nulla pellentesque dignissim enim sit amet. Aliquam vestibulum morbi blandit cursus risus at ultrices mi tempus. Ac orci phasellus egestas tellus rutrum. Mi tempus imperdiet nulla malesuada. Varius morbi enim nunc faucibus a pellentesque sit. Facilisi etiam dignissim diam quis enim lobortis. In aliquam sem fringilla ut morbi tincidunt augue interdum. Id leo in vitae turpis massa. Porta lorem mollis aliquam ut porttitor. Hendrerit dolor magna eget est lorem. Nunc aliquet bibendum enim facilisis gravida neque. Netus et malesuada fames ac turpis egestas sed. Sit amet volutpat consequat mauris nunc congue. Neque viverra justo nec ultrices dui sapien. Ut morbi tincidunt augue interdum velit.

Nulla at volutpat diam ut venenatis tellus in. Congue quisque egestas diam in arcu cursus euismod quis. Urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Elit scelerisque mauris pellentesque pulvinar pellentesque. Ut enim blandit volutpat maecenas volutpat blandit aliquam etiam. Id volutpat lacus laoreet non curabitur gravida arcu. Vitae ultricies leo integer malesuada nunc. Felis bibendum ut tristique et egestas quis ipsum suspendisse ultrices. Lacus viverra vitae congue eu consequat ac felis. Et tortor at risus viverra adipiscing at in. Risus pretium quam vulputate dignissim suspendisse. Turpis egestas integer eget aliquet nibh praesent tristique magna sit. Aenean et tortor at risus. Semper viverra nam libero justo laoreet sit amet cursus sit.