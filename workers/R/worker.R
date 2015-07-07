#!/usr/bin/env Rscript

# Simple worker for CI services.
library(logging)
library(jsonlite)

basicConfig()

args <- commandArgs(trailingOnly=TRUE)

loginfo("-------------- R Worker Started ------------------------------")

# Load R driver
library(rzmq)

pullPort = toString(args[3])
pushPort = toString(args[4])

context = init.context()
socketPull = init.socket(context,"ZMQ_PULL")
socketPush = init.socket(context,"ZMQ_PUSH")

pullUrl = paste("tcp://", toString(args[1]), ":", pullPort, sep = "")
pushUrl = paste("tcp://", toString(args[2]), ":", pushPort, sep = "")

loginfo(paste("PULL is ", pullUrl, sep = " = "))
loginfo(paste("PUSH is ", pushUrl, sep = " = "))

connect.socket(socketPull, pullUrl)
connect.socket(socketPush, pushUrl)

while(1) {
  loginfo('Loop start')
  msg = receive.string(socketPull)
  data = fromJSON(msg)
  print(msg)
  print(data)
  
  # Process the data here:
  job_id = data["job_id"]
  
  print("JOBID")
  print(job_id[[1]])
  result = list(job_id=c(job_id[[1]]), result=list())
  result.json <- toJSON(result)
  print(result.json)
  send.socket(socketPush, result.json);
}

processData <- function(data) {
  
}