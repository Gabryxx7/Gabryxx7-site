---
layout: project
title: Miscellaneous
caption: A collection of Javascript/WebGL fun tests
description: >
  A collection of Javascript/WebGL tests
image: 
  path: /assets/gabryxx7/img/miscellaneous.PNG
  #  srcset:
  #    1920w: /assets/gabryxx7/img/level0.PNG
  #    960w:  /assets/gabryxx7/img/level0@0,5x.PNG
  #    480w:  /assets/gabryxx7/img/level0.PNG@0,25x.PNG
date: 01 Aug 2020
#  accent_image: "https://austinhuang.me/assets/sidebar-bg.jpg"
accent_image: 
  background: "linear-gradient(202deg, rgb(0 11 121) 13%, rgb(255 255 255) 87%)"
# links:
#   - title: Link
#     url: https://github.com/Gabryxx7/TheTower
# accent_color: 'rgb(76,195,85)'
# theme_color: '#bada55'
---
# Miscellaneous

## [[R/Plotly]  3D Waves point distribution and animation](/assets/gabryxx7/html/r_plotly_wave.html)

<img src='/assets/gabryxx7/img/r_wave_screenshot.PNG'  width='300' height='200' />


~~~R 
library(plotly)

spacing <- 0.15
sideLength <- 10
fps <- 30
seconds <- 2
frames <- fps*seconds
pointRow <- seq(0,sideLength, spacing)
nPoints <- length(pointRow)
x <- rep(pointRow,nPoints)
y <- sort(rep(pointRow, nPoints))
frame <- sort(rep(seq(1,frames), nPoints*nPoints))
x <- rep(x, frames)
y <- rep(y, frames)
z <- matrix(0, nrow = nPoints, ncol = nPoints)

data <- data.frame("x"=as.numeric(x), "y"=as.numeric(y), "frame"=as.numeric(frame))
data$z <- sin(data$x+data$frame*0.2)*0.15 + cos(data$y +data$frame*0.05)*0.35
yRange <- c(min(data$z), max(data$z))
data$alpha <- data$y
data$color <- data$y + yRange[1]

p <- plot_ly(data, x = ~x, y = ~y, z = ~z, color = ~z, opacity = ~z, frame=~frame, marker = list(size = 1.4)) %>%
   add_markers() %>%
   layout(scene = 
             list(
                xaxis = list(range = c(0,gridSize)),
                yaxis = list(range = c(0,gridSize)),
                zaxis = list(range = c(-2,2)))) %>%
   animation_opts(1000/fps)
p

htmlwidgets::saveWidget(as_widget(p), file = "/assets/gabryxx7/plots/wave.html", selfcontained = TRUE)
~~~

## [[JS/Plotly] Plotly animation and 3D data visualisation](/assets/gabryxx7/html/plotly.html)

<img src='/assets/gabryxx7/img/plotly_test.PNG'  width='300' height='200'/>


## [[WebGL] Cubes recursion generator](/assets/gabryxx7/html/cubes.html)

<img src='/assets/gabryxx7/img/cubes_webgl.PNG'  width='300' height='200'/>


## [[WebGL] Globe Data Visualisation](/assets/gabryxx7/html/globe.html)

<img src='/assets/gabryxx7/img/miscellaneous.PNG'  width='300' height='200'/>


## [[JS] Canvas JSON marker rendering](/assets/gabryxx7/html/map_markers.html)

<img src='/assets/gabryxx7/img/canvas-markers.PNG'  width='300' height='200'/>
