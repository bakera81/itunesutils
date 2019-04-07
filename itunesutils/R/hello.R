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

# lib <- read_xml("~/Documents/itunesutils/data/Library.xml")
lib <- read_xml("~/Documents/libpytunes/libpytunes/tests/Test Library.xml")

playlists_root <- lib %>%
  xml_nodes(xpath = "//key[text() = 'Playlists']/following-sibling::array")

# dict <- playlists_root %>%
#   xml_child(search = 13)

# Takes a single playlist dict as an XML node and returns a df
playlist_node_to_df <- function(node) {
  # Convert the node to a list
  l <- node %>%
    xml_children() %>%
    as_list()

  # Convert the node list to df
  keys <- unlist(l[c(T, F)])
  values <- l[c(F, T)]
  meta <- tibble(
    keys = keys,
    values = values
  )

  # Helper function: extract data out of meta$values
  expand_playlists <- function(x) {
    if (length(x) == 0) {
      NA_character_
    } else if (length(x) == 1) {
      unlist(x)
    } else {
      map_chr(x, ~.$integer[[1]])
    }
  }

  # Convert the meta df into a properly formatted df
  meta %>%
    mutate(values = map(values, expand_playlists)) %>%
    # Unlist any keys that should not be lists
    mutate(keys = paste0(keys, "..unlist=", lengths(values) <= 1)) %>% # Hack to identify which cols to unlist
    spread(keys, values) %>%
    # Need to do this step in wide format because each col must have a consistend data type
    mutate_at(vars(ends_with("..unlist=TRUE")), unlist) %>%
    # Undo our column renames
    rename_all(~str_remove(., "\\.\\.unlist=.*$"))
}

node <- playlists_root %>%
  xml_child(search = 6)

playlist_node_to_df(node)

playlists_root %>%
  xml_children() %>%
  map_df(playlist_node_to_df)













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
