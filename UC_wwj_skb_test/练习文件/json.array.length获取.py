# # from builtins import function
# import function
# # from django.core.mail.backends import console
# # # from numpy import var
# # from numpy.ma import var
# #
# # var pBzjtJson ={"SORT":1,"TITLE":"12324","RANK":1,"TYPE_TAG":"班子集体责任","SR_CLASS_ID":"a2bdfa5b5f684d5d9da5c055117c94c5"};
# # var length = Object.keys(pBzjtJson).length;
# # console.log(length);
#
# function getJsonLength(jsonData){
#     var jsonLength = 0;
#     for(var item in jsonData){
#         jsonLength++;
#     }
#     return jsonLength;
# }
a = ['this', 'test', 4.56, ['inner', 'list']]
if 'inner'  in a :
    print(False)
else:
    print(a[3][0])
