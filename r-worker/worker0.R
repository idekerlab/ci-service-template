library(logging)


args <- commandArgs(trailingOnly = TRUE)

basicConfig()
addHandler(writeToConsole)

print("----------R worker")
logwarn("Started------------------------------")
loginfo(args[1])
loginfo(args[2])
loginfo(args[3])
loginfo(args[4])

while(1) {
  Sys.sleep(2)
  loginfo('Looping...')
}
