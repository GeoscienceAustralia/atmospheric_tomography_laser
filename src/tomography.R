library(ggplot2)
library(plyr)
library(dplyr)
library(magrittr)
library(lubridate)
ginninderra.tz = "Australia/Canberra"
infile = "data/kaggle/150601_GA_GasFinder2_filteredR95v2.csv"
gasfinder = read.csv(infile) %>% .[, c("Date","Hour", "Reflector", "PPM")]
gasfinder$Date = paste(gasfinder$Date, gasfinder$Hour, sep=" ")
gasfinder %<>% .[,! names(.) %in% c("Hour")]
gasfinder %<>% mutate(Date = Date %>% parse_date_time(c("%d/%m/%Y %I:%M:%S %p"), exact=T, tz=ginninderra.tz))
gasfinder$Reflector = factor(gasfinder$Reflector)
levels(gasfinder$Reflector)

# Time based filters to be applied
start.high = as.POSIXct("2015-05-12 11:56:00", tz=ginninderra.tz)
end.high = as.POSIXct("2015-05-12 12:02:00", tz=ginninderra.tz)
gasfinder %<>% .[(.$Date < start.high | .$Date > end.high),]
# 138407 observations after this filter is applied.

start.high = as.POSIXct("2015-05-13 14:13:00", tz=ginninderra.tz)
end.high = as.POSIXct("2015-05-13 14:36:00", tz=ginninderra.tz)
gasfinder %<>% .[(.$Date < start.high | .$Date > end.high),]
# 138120 after this one.

#### Another visual inspection
# cbPalette= c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
#p = ggplot() + geom_point(data=gasfinder, mapping = aes(Date, PPM, color=Reflector)) + scale_colour_manual(values=cbPalette)
#p = p + theme_bw() + theme(
#  plot.background = element_blank()
#  ,panel.grid.major = element_blank()
#  ,panel.grid.minor = element_blank()
#  ,panel.border = element_blank()
#) + ggtitle("Concentration Data from 08-05 to 13-05 with periods of high release rate filtered out")
# print(p)
####
thirty.mins = cut(gasfinder$Date, breaks="30 min")
gasfinder.avg = gasfinder %>% split(thirty.mins) %>% 
               ldply(function(dat) {ddply(dat, .(Reflector), function(x) mean(x$PPM))}) %>%
               plyr::rename(c(".id"="Date", "V1"="PPM")) %<>% 
               reshape2::dcast(Date ~ Reflector, value.var="PPM")
gasfinder.avg$Date = as.POSIXct(gasfinder.avg$Date, tz = ginninderra.tz)

##
mean.smallest.n = function(row, n){
  bg = row  %>% sort(na.last = NA) %>% .[1:min(n, dim(.)[2])] %>% .[which(. > 0)] %>% mean
  return(bg)
}
bg= apply(gasfinder.avg[,2:8], MARGIN = 1, FUN = mean.smallest.n, n=5)
gasfinder.avg %<>% cbind(.,Background=bg)

gasfinder.avg[, 2:8] =  gasfinder.avg[, 2:8] - bg
gasfinder.avg %<>% .[,!names(.) %in% c("Background")]


weather.file = "data/unprocessed/0805-1305/0805-1305-weather.csv"
weather = read.csv(weather.file) %>% 
         mutate(Date = Date %>% parse_date_time(c("%Y-%m-%d %H:%M:%S"), exact=T, tz=ginninderra.tz))

collated = merge(weather, gasfinder.avg)
id.cols = c("Date","Temperature", "WindSpeed", "WindDirection", "MO_Length","P_EC100_mean")
collated %<>% 
  reshape2::melt(id.var = id.cols) %<>% 
  .[.$value >0,] %<>%
  .[complete.cases(.),] %<>%
   plyr::rename(c("variable"="Reflector", "value"="PPM"))
  
filter_sd = function(x){return(x[x$PPM > sd(x$PPM) ,])}
collated %<>% 
  ddply( .(Reflector), filter_sd) %<>%
  .[.$WindSpeed > 1.5 & .$WindSpeed < 9,]


collated.op = "0805-1305-collated.csv"
cols.order = c("Temperature", "P_EC100_mean", "WindSpeed", "WindDirection", "MO_Length", "Reflector", "PPM")
collated %>% .[, cols.order] %>%
  write.csv(file=collated.op, row.names=F, quote=F)