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
lib <- read_xml("~/Documents/itunesutils/data/Test Library.xml")

playlists_root <- lib %>%
  xml_nodes(xpath = "//key[text() = 'Playlists']/following-sibling::array")

tracks_root <- lib %>%
  xml_nodes(xpath = "//key[text() = 'Tracks']/following-sibling::dict")

# dict <- playlists_root %>%
#   xml_child(search = 13)

# Helper function: extract data out of meta$values
expand_playlists <- function(x) {
  if (length(x) == 0) {
    NA_character_
  } else if (length(x) == 1) {
    unlist(x)
  } else {
    # TODO: if this isn't an integer, still grab it
    map_chr(x, ~.$integer[[1]])
  }
}

# Takes a single playlist dict as an XML node and returns a df
playlist_node_to_df <- function(node) {
  # Convert the node to a list
  l <- node %>%
    xml_children() %>%
    as_list()

  # Convert the node list to df
  keys <- unlist(l[c(T, F)]) # Key/value pairs alternate
  values <- l[c(F, T)]
  meta <- tibble(
    keys = keys,
    values = values
  )

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

playlists <- playlists_root %>%
  xml_children() %>%
  map_df(playlist_node_to_df)

# To unnest, replace any NULLs with NA or list()
playlists_long <- playlists %>%
  mutate(playlist_length = lengths(`Playlist Items`),
         `Playlist Items` = ifelse(
           playlist_length == 0,
           NA,
           `Playlist Items`)) %>%
  unnest()


track_node_to_df <- function(node) {
  # Convert the node to a list
  l <- node %>%
    xml_children() %>%
    as_list()

  # Convert the node list to df
  keys <- unlist(l[c(T, F)]) # Key/value pairs alternate
  values <- l[c(F, T)]
  meta <- tibble(
    keys = keys,
    values = values
  )

  meta %>%
    unnest() %>%
    mutate(values = unlist(values)) %>%
    spread(keys, values)
}

node <- tracks_root %>%
  # TODO: the tracks root can be either a dict or an array
  xml_child(search = 2)

tracks <- tracks_root %>%
  xml_find_all("dict") %>%
  map_df(track_node_to_df)

