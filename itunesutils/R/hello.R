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

lib <- read_xml("../Library.xml")

playlists_root <- lib %>%
  xml_nodes(xpath = "//key[text() = 'Playlists']/following-sibling::array")

dict <- playlists_root %>%
  xml_child(search = 13)
  # as_list()

parse_dict <- function(dict) {
  playlist <- list()
  for (node in dict %>% xml_children()) {
    if (node %>% xml_name() == "key") {
      key <- node %>% xml_text()
      next_sibling <- node %>% xml_node(xpath = "./following-sibling::*")
      if (next_sibling %>% xml_name() == "array") {
        value <- c()
        for (n in next_sibling %>% xml_children()) {
          # browser()
          value <- c(value, parse_dict(n))
        }
      } else {
        value <- next_sibling %>% xml_text()
      }
      print(paste0(key, ": ", value))
      playlist[[key]] <- value
    }
  }
  playlist
}

p <- parse_dict(dict)

as.data.frame(p) %>%
  tibble() %>%
  View()

    # xpath <- paste0("/key[text() = '", key, "']/following-sibling")
    # dict %>% xml_children() %>% xml_nodes(xpath = xpath)

    # next_sibling <- (node %>% xml_siblings())[[1]]
    # next_sibling %>% xml_remove()
    # node %>% xml_remove()



    # list(node %>% xml_text() = node %>% xml_node(xpath = "following-sibling")
    # node %>% xml_node(xpath = "following-sibling")


# parse_xml <- function(path) {
  root <- xml2::read_xml(path)
  top_level <- xml_children(root)
  top_level <- xml_children(top_level)

tracks_index <- which(xml_text(top_level) == "Tracks") + 1
playlists_index <- which(xml_text(top_level) == "Playlists") + 1

playlists <- xml_children(top_level[playlists_index])

p <- playlists[1]

schema <- list(
  playlists = c("Name", "Description", "Master", "Playlist ID", "Playlist Persistent ID", "Visible", "All Items", "Playlist Items")
)

parse_playlist <- function(p) {
  # names <- xml_text(xml_find_all(p, "key"))
  # values <- xml_text()
  # xml_children(p)[xml_name(xml_children(p)) == "key"]
  names <- xml_text(xml_children(p)[which(xml_name(xml_children(p)) == "key")])
  values <- xml_children(p)[which(xml_name(xml_children(p)) != "key")]

  names() <- names
  values
}


doc <- read_xml(path)
p2 <- xml_ns_strip(playlists)
doc <- xml_ns_strip()
