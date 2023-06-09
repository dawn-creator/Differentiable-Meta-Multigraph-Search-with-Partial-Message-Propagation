archs = {
#Multigraph
"Amazon_M" :
 {
    "source" : ([[[4], [3], [2], [0]]], [[[1], [1, 2, 4, 7, 9], [1, 4, 5, 6, 7, 9], [9], [0], [8]]]), 
    "target" : ([[[5], [4], [2], [1]]], [[[3, 5, 6, 8, 9], [2, 9], [0, 4, 7, 9], [6, 8, 9], [8, 9], [2, 6, 8, 9]]])
 },
"Yelp_M" : 
 {
    "source" : ([[[6], [5], [4], [3]]], [[[2, 3, 5, 8, 9], [2, 3, 4, 5, 6, 7], [1, 2, 4, 6, 8, 9, 10], [0, 3, 10], [1, 3, 9], [1, 9]]]),
    "target" : ([[[4], [5], [9], [2]]], [[[3, 4, 5, 6, 10], [0, 1, 2, 4, 5, 8], [0, 5, 6, 8, 9, 10], [2, 9, 10], [2, 5, 10], [9, 10]]])
 },
"Douban_Movie_M":
 {
    "source" : ([[[5], [7], [0], [1]]], [[[6, 11], [0, 6, 8, 9, 10, 11, 12], [0, 1, 2, 3, 7, 10, 11], [11, 12], [3, 11, 12], [11]]]),
    "target" : ([[[10], [0], [8], [2]]], [[[2, 5, 7, 9, 11, 12], [1, 4, 5, 6, 7, 8, 11, 12], [2, 4, 6, 7, 9, 12], [2, 5, 11, 12], [11], [2, 5, 7]]])
 },
###PMMM
"Amazon" :
 {
    "source": ([[[2, 5], [2], [1, 2], [0]]], [[[6], [4], [1, 3, 6], [8], [8], [9]]]),
    "target": ([[[0], [2], [4], [1]]], [[[8], [5, 7], [9], [8], [8], [1, 6]]])
 },
"Yelp" :
 {
    "source": [[[[4],[3],[4],[1]]],[[[1,2,4,5,6,8,10],[1,2,4,6,7,10],[1,2,4],[0,1,9],[1,9],[0,1,9]]]],
    "target": [[[[8],[7],[8],[2]]],[[[3,4,5,6,7],[3,5,7,8,9],[0,2,3,5,8],[5,9],[2,5,10],[2,5,9]]]]
 },
"Douban_Movie" : 
 {
    "source": [[[[6],[3],[9],[11]]],[[[0,2,8,9,10,11],[2,5,8,9,10,11,12],[3,4,6,8,9],[12],[0,3,12],[0,3]]]],
    "target": [[[[6],[10],[2],[2]]],[[[0,2,3,4,5,6,8,11],[1,2,5,6,7,10,11,12],[4,5,8,9,10,12],[2,5,7,12],[2,9,11],[9,11]]]]
 },
}