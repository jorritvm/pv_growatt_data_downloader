# Fri Feb 26 19:45:45 2021 ------------------------------
# read excel data downloads into flat table
# jvm

rm(list = ls())
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# library(here)
library(data.table)
library(readxl)
library(stringr)
library(lubridate)
library(jrutils)

filelist = list.files(path = "../data_download/maandrapport/", 
                      pattern = "my plant", 
                      full.names = TRUE,
                      recursive = FALSE)

all_data_list = list()
i = 0
for (fpfn in filelist) {
  print(paste("collecting data from", basename(fpfn)))
  i = i + 1
  
  # year & month
  yyyy = as.numeric(str_extract(string =  basename(fpfn), pattern = "[[:digit:]]{4}"))
  mm = as.numeric(gsub(".xls", "", str_extract(string =  basename(fpfn), pattern = "[[:digit:]]{1,2}.xls")))

  # read daily data file
  dt = as.data.table(
          read_xls(path = fpfn, range = "D17:AL18")
       )
  
  # cleanup
  last_data_col = grep("Total", names(dt)) - 1
  dt = dt[, 1:last_data_col]
  dt[is.na(dt)] = 0 
  
  all_data_list[[i]] = data.table(year = yyyy, month = mm, day = as.numeric(names(dt)), solar = as.numeric(unlist(dt[1])))
  
}

dt = rbindlist(all_data_list)
dt[, date := ymd(paste(year, month, day, sep = "-"))]
dt = dt[order(date)]
setcolorder(dt, "date")

str(dt)
wtf(dt)
