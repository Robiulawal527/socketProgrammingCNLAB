# socketProgrammingCNLAB
socket programming CN Lab


kill the localhost server: 

lsof -i tcp:8080

lsof -ti tcp:8080 | xargs -r kill -9