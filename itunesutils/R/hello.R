# Hello, world!
#
# This is an example function named 'hello'
# which prints 'Hello, world!'.
#
# You can learn more about package authoring with RStudio at:
#
#   http://r-pkgs.had.co.nz/
#
# Some useful keyboard shortcuts for package authoring:
#
#   Build and Reload Package:  'Cmd + Shift + B'
#   Check Package:             'Cmd + Shift + E'
#   Test Package:              'Cmd + Shift + T'


library(xml2)
library(rvest)
library(tidyverse)
library(purrr)
library(tictoc)

lib <- read_xml("~/Documents/itunesutils/data/Library.xml")
lib <- read_xml("~/Documents/libpytunes/libpytunes/tests/Test Library.xml")

playlists_root <- lib %>%
  xml_nodes(xpath = "//key[text() = 'Playlists']/following-sibling::array")

# dict <- playlists_root %>%
#   xml_child(search = 13)

# This works but is god-awful slow
dict_to_list <- function(dict) {
  # profvis::profvis({
  playlist <- list()
  for (node in dict %>% xml_children()) {
    if (node %>% xml_name() == "key") {
      key <- node %>% xml_text()
      next_sibling <- node %>% xml_node(xpath = "./following-sibling::*")
      if (next_sibling %>% xml_name() == "array") {
        value <- c()
        for (n in next_sibling %>% xml_children()) {
          # browser()
          value <- c(value, dict_to_list(n))
        }
      } else {
        value <- next_sibling %>% xml_text()
      }
      # print(paste0(key, ": ", value))
      if (key == "Name" & value %in% c("Library", "Music")) {
        return(NA)
      }
      if (key == "Name") {
        print(paste0("Parsing ", value, "..."))
      }
      playlist[[key]] <- value
    }
  }
  playlist
  # })
}

# Experimental version of above
# dict_to_list <- function(dict) {
  # profvis::profvis({
  playlist <- list()

  dict <- playlists_root %>%
    xml_child()

  l <- dict %>%
    xml_children() %>%
    as_list()

  keys <- unlist(l[c(T, F)])
  values <- unlist(l[c(F, T)], recursive = F)
  values_raw <- l[c(F, T)]


  names(values) <- keys

  # Create a meta df
  meta <- tibble(
    keys = keys,
    values = values_raw,
    lengths = lengths(values_raw)
  )



  expand_playlists <- function(x) {
    # browser()
    if (length(x) == 0) {
      NA_character_
    } else if (length(x) == 1) {
      unlist(x)
    } else {
      # browser()
      # expand_track_ids(x)
      map_chr(x, fetch_int_value)
    }
  }

  expand_track_ids <- function(x) {
    # browser()
    map_chr(x, fetch_int_value)
    # map_chr(x, ~ .$dict$integer[[1]])
  }

  fetch_int_value <- function(x) {
    # browser()
    # x$integer[[1]]
    x$integer[[1]]
  }

  playlist <- meta %>%
    mutate(values = map(values, expand_playlists)) %>%
    unnest()

  playlist %>%
    group_by(keys) %>%
    nest(values) %>%
    spread(keys, data) %>%
    mutate_at(vars(-`Playlist Items`), ~.[[1]]$values)

  meta %>%
    mutate(v2 = map(values, ~expand_playlists(values, lengths)))

  playlist <- list()
  for (i in length(keys)) {
    if ()
    playlist[[keys[i]]] <- unlist(values_raw[i])
  }


  for (node in dict %>% xml_children()) {
    if (node %>% xml_name() == "key") {
      key <- node %>% xml_text()
      next_sibling <- node %>% xml_node(xpath = "./following-sibling::*")
      if (next_sibling %>% xml_name() == "array") {
        value <- c()
        for (n in next_sibling %>% xml_children()) {
          # browser()
          value <- c(value, dict_to_list(n))
        }
      } else {
        value <- next_sibling %>% xml_text()
      }
      # print(paste0(key, ": ", value))
      if (key == "Name" & value %in% c("Library", "Music")) {
        return(NA)
      }
      if (key == "Name") {
        print(paste0("Parsing ", value, "..."))
      }
      playlist[[key]] <- value
    }
  }
  playlist
  # })
}




dict_to_df <- function(dict) {
  l <- dict_to_list(dict)

  as_tibble(l) #%>%
    # unnest() %>%
    # nest(`Playlist Items`,
    #      .key = `Playlist Items`)
}

p <- dict_to_list(dict)

df <- dict_to_df(dict)

for(i in 1:20) {
  print(
    playlists_root %>%
    xml_child(search = i) %>%
    xml_child(search = 2) %>%
    xml_text()
  )
}

dict <- playlists_root %>%
  xml_child(search = 14)

profvis::profvis({
  dict_to_df(dict)
})

tic()
playlists_df <- playlists_root %>%
  xml_children() %>% head(2) %>%
  map_dfr(dict_to_df)
toc()
