library("stringr")

make_snippets <- function(tb, ...){
  out <- c()
  for(i in 1:nrow(tb)){
    #for(i in 1:3){
    out <- c(out, make_one_snippet(tb[i,], ...) )
  }

  XX <- paste0(out, collapse = '')
  return(XX)
}

#make_one_snippet(term=d1[1,], col='blue', letter='P')
make_one_snippet <- function(term, col, letter){

  color <- paste0('<span style="color:', col, '">', letter, '</span>')

  iid <- strsplit(term$ID, '[.]')[[1]][2]
  url <- paste0('http://purl.obolibrary.org/obo/', iid)

  url.pattern <- 'obo\\.[:alpha:]+_\\d+'
  url.ex <-str_detect(term$ID, url.pattern)
  #url.ex <- url.exists(url)

  if (url.ex==FALSE){
    out <- paste0('  \'', term$ID, '\':\n',
                  '   \'prefix\': ', '\'',term$label.final, '\'', '\n', #was term$label.final: no . in terms
                  '   \'body\': ', '\'', term$label.nospace, '\'', '\n',
                  '   \'description\': ', '\'', term$Defs, '\'', '\n',
                  '   \'leftLabelHTML\': ', '\'', color, '\'', '\n\n'
                  #'   \'descriptionMoreURL\': ', '\'', url, '\'', '\n\n'
    )
  }

  if (url.ex==TRUE){
    out <- paste0('  \'', term$ID, '\':\n',
                  '   \'prefix\': ', '\'',term$label.final, '\'', '\n', #was term$label.final: no . in terms
                  '   \'body\': ', '\'', term$label.nospace, '\'', '\n',
                  '   \'description\': ', '\'', term$Defs, '\'', '\n',
                  '   \'leftLabelHTML\': ', '\'', color, '\'', '\n',
                  '   \'descriptionMoreURL\': ', '\'', url, '\'', '\n\n'
    )
  }


  return(out)

}
