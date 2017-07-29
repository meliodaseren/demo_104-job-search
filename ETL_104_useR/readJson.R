# install.packages("rjson")
# install.packages("jsonlite")

# library(rjson)
library(jsonlite)

job_data <- fromJSON("./Job_104_clean.json")
class(job_data)  # list
str(job_data)    # 28541 obs. of  8 variables

job_lists_data <- subset(job_data$job_lists)
View(job_lists_data)
class(job_lists_data)  # data.frame
str(job_lists_data)    # 28541 obs. of  8 variables

# Clean Data
# Remove duplicated [url] rows
str(job_lists_data$url)          # 28541
str(unique(job_lists_data$url))  # 16747

job_lists_data <- job_lists_data[!duplicated(job_lists_data$url), ]

