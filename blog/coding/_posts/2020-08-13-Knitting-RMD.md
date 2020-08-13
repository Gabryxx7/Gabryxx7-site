---
title: Knitting RMarkdown to Jekyll post
output:
  md_document:
    variant: gfm
    preserve_yaml: TRUE
knit: (function(inputFile, encoding) {
  rmarkdown::render(paste(format(Sys.time(), "%Y-%m-%d"), "-",inputFile, sep = " ", collapse = NULL), encoding = encoding, output_dir = "../_posts/") })
---

One thing I would love to do with this blog is to post data anlysis done in R (or Python sometimes). They can be a lot of fun and I would prefer to spend the time writing the R notebook rather than converting it afterward to pure Markdown for Jekyll.
So here is a few tips for an easy R Markdown to Jekyll Markdown port (Thanks to [this guide](http://svmiller.com/blog/2019/08/two-helpful-rmarkdown-jekyll-tips/) ).
Another interesting package is `blogdown` whith has Jekyll [support](https://bookdown.org/yihui/blogdown/jekyll.html). The most interesting part was their code for generating markdown files and figures in different folders

```r
local({
  # fall back on "/" if baseurl is not specified
  baseurl = blogdown:::get_config2("baseurl", default = "/")
  knitr::opts_knit$set(base.url = baseurl)
  knitr::render_jekyll()  # set output hooks

  # input/output filenames as two arguments to Rscript
  a = commandArgs(TRUE)
  d = gsub("^_|[.][a-zA-Z]+$", "", a[1])
  knitr::opts_chunk$set(
    fig.path   = sprintf("figure/%s/", d),
    cache.path = sprintf("cache/%s/", d)
  )
  knitr::knit(
    a[1], a[2], quiet = TRUE, encoding = "UTF-8",
    envir = globalenv()
  )
})
```

So I understood that the knitr options called `base.url` is a prefix to `fig.path`, while `base.dir` is the actual directory where the images will be genereated, `base.url` is pretty much an alias.

For instance by setting `base.url='/'`, `fig.path='assets/r_figures/'` and `base.dir='C:\Users\Gabryxx7\Documents\GitHub\blog\' ` the final markdown for a figure will look something like this:

```markdown
![](/assets/r_figures/nice_plot.png)<!-- -->
```

And `nice_plot.png` will actually be located at `C:\Users\Gabryxx7\Documents\GitHub\blog\assets\r_figures\nice_plot.png`.

This is awesome since Jekyll will interpret the first `/` as the website root folder where the `assets` folder actually is!


From the `knitr` [documentation](https://yihui.org/knitr/objects/):
> Knitr’s settings must be set in a chunk before any chunks which rely on those settings to be active. It is recommended to create a knit configuration chunk as the first chunk in a script with cache = FALSE and include = FALSE options set. This chunk must not contain any commands which expect the settings in the configuration chunk to be in effect at the time of execution.

Another interesting feature is the possibility to set up parameters into the `yaml` header and use them withing your code. This makes up for [parameterized reports](https://rmarkdown.rstudio.com/developer_parameterized_reports.html)

So with all this knowledge, let's get started.

## Setting up the R Markdown file

When on RStudio the first thing you should do is to create a new R Markdown file. So `File -> New File -> R Markdown`.

Once you get your file, you can add the following lines to your heading and as the first chunk of your markdown file:

{% highlight yaml %}
---
title: "R Markdown and jekyll"
output:
  md_document:
    variant: gfm
    preserve_yaml: TRUE
params: 
  fig_base_path: "C:\\Users\\Gabryxx7\\Documents\\GitHub\\blog\\assets\\gabryxx7\\r_figures"
knit: (function(input, ...) {
  rmarkdown::render(input=input,
    output_file=paste0(Sys.Date(),'-',xfun::sans_ext(basename(input)),'.md'),
    encoding = encoding,
    output_dir="C:\\Users\\Gabryxx7\\Documents\\GitHub\\blog\\blog\\coding\\_posts")
  })
---

```{r setup, include=FALSE}
knitr::opts_knit$set( base.dir=params$fig_base_path, base.url="/assets/gabryxx7/r_figures/")
knitr::opts_chunk$set(echo = TRUE, fig.path = "")

```
{% endhighlight %}

**HEADS UP**: If you get an error saying `Error in setwd(...): cannot change the working directory` you probably mispelled the path or pointed at a non existing directory. R Will only create directories specified under `opts_chunk$set` but anything else (for instance `fig_base_path`) will be expected to exist already.
{:.message}


So connecting back to `blogdown`  I found out that you can override the [`rmarkdown::render()`](https://rmarkdown.rstudio.com/docs/reference/render.html) function in R Markdown and R Notebook files.
The render function takes as parameters an input file path and an encoding string (here it's included in `...`).

By overriding the function we can tell it to render the .rmd `input` file to a new file with `.md` extension and the proper Jekyll's post markdown formatting. The part `xfun::sans_ext(basename(input))` is just getting the filename from the `input` file path and removing its extension.
Finally just set the `output_dir` to be whatever your Jekyll post folder is (some extra freedom for you! Decoupling is always the key!).

A bit of an annoying thing is that you cannot just use a base path and then concatenate the twos since `rmarkdown::render()` will be called before the `YAML` header is processed. I mean, `params` is literally in the same header, unless `YAML` is interpreted which is not, there is no way for `knit` to know what other variables are in the yaml header.

For this reason you will have to copy-paste your folder path twice, once as the `output_dir` parameter in the `rmarkdown::render()` function and another time as a parameter in your `YAML` header. But that's actually not all bad, as I said before now you can output your figures to whatever folder you prefer.
This is especially useful in my case where I work on different machines (develope my blog on Windows/Macbook and depploy on Linux server).

So as you can see here:
- The `.md` markdown file will be generated in `C:\Users\Gabryxx7\Documents\GitHub\blog\blog\coding\_posts`
- The figure files will be generated in: `C:\Users\Gabryxx7\Documents\GitHub\blog\assets\gabryxx7\r_figures`
- The figures in the markdown file will all have `/assets/gabryxx7/r_figures/` as base url so that jekyll will know where to get the files starting from the root of your website.

We can actually take it a step further and put the figures in each post's separate folder in the `r_figures` base folder:
```r
knitr::opts_chunk$set(echo = TRUE,
                      strip.white=TRUE,
                      message=FALSE,
                      warning=FALSE,
                      results="markup",
                      out.format="jekyll",
                      class.output="plaintext",
                      out.extra = "",
                      fig.path = paste0(Sys.Date(),'-',xfun::sans_ext(basename(knitr::current_input())),"/"))
```

In this way:
- The final path will be `C:\Users\Gabryxx7\Documents\GitHub\blog\assets\gabryxx7\r_figures\2020-08-13-ggantt`
- The images url will be `/assets/gabryxx7/r_figures/2020-08-13-ggantt/nice_plot.png`
- Message and warnings won't be included in the code output. The code output will be wrapped in a code chunk with language `plaintext` so that we can capture it with javascript and do something with it
- **DO NOT FORGET to add `out.extra = ""` otherwise knitr will add images with an ending comment like `![](/assets/gabryxx7/r_figures/2020-08-13-ggantt/test.png)<!-- -->` completely messing up the `html` page

## Knitting it!
Well there is not much left to do, just press `knit` on RStudio with your `.rmd` file opened and you're good to go!

Alternatively you can call the knit function from the console but be careful as this won't call the `markdown::render()` method in the `yaml` header so the `.md` file will be generated in the working directory unless you specify the output file path:

```r
setwd("C:\\Users\\Gabryxx7\\Documents\\GitHub\\whatever\\") # adjust to your preferences.
knitr::knit("rmarkdown_file.rmd") # Generate to working directory
knitr::knit("ggantt.rmd", output = "C:\\Users\\Gabryxx7\\Documents\\GitHub\\blog\\blog\\coding\\_posts\\2020-08-13-rmarkdown_file.md") # Generate to Jekyll's post directory
```

You can also make your own function in case you have multiple files:
```r
knit_to_jekyll <- function(input, ...) {
  rmarkdown::render(input=input,
    output_file=paste0(Sys.Date(),'-',xfun::sans_ext(basename(input)),'.md'),
    encoding = encoding,
    output_dir="C:\\Users\\Gabryxx7\\Documents\\GitHub\\blog\\blog\\coding\\_posts")
  }
knit_to_jekyll("r_notebook_markdown.rmd")
```
