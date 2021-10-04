# content = [{
#             'Name': 'sdddd',
#             'CreationDate': "d",
#             'Key': "a"
#         },
#         {
#             'Name': 'rerere',
#             'CreationDate': "c",
#             'Key': "b"
#         }]
# resrc={}
        
# if (len(content) != 0):
#     s3=[]
#     ec2=[]
#     for cont in content:
#         s3.append(cont["Name"])
#     resrc["s3"] = s3
    
#     for cont in content:
#         ec2.append(cont["Key"])
#     resrc["ec2"] = ec2

# Reservations= [
#         {
#             'Groups': [
#                 {
#                     'GroupName': 'string',
#                     'GroupId': 'string'
#                 },
#             ],
#             'Instances': [
#                 {
#                     'AmiLaunchIndex': 123,
#                     'ImageId': 'string',
#                     'InstanceId': 'string' 
#                 }]}]
# print(Reservations[0]['Instances'][0]['InstanceId'])

# x = {'Name': 'aaaaaassssssss1', 'CreationDate': "xxxx"}

# import xlsxwriter
# all_resources={
#     "s3": ["a", "b", "c", "e"],
#     "ec2": ["aa", "bb", "cc"],
#     "lambda":["ss", "ff", "vv", "df"],
#     "test": ["tt", "gg", "gf", "dd", "dd"]
# }

# def excel_file():
#     workbook = xlsxwriter.Workbook('test.xlsx')
#     worksheet = workbook.add_worksheet()
#     bold = workbook.add_format({'bold': True})

#     i=0
#     row = 0
#     col = 0
#     while(i<len(all_resources)):
#         worksheet.write(row, col, "Resource name", bold)
#         worksheet.write(row, col+1, "No of resources", bold)
#         for key,value in all_resources.items():
#             worksheet.write(row+1, col, key)
#             worksheet.write(row+1, col+1, len(value))
#             row+=1
#             i+=1
    
#     j=0
#     while(j<len(all_resources)):
#         for key,value in all_resources.items():
#             row = len(all_resources)
#             worksheet.write(row+2, col+j, key, bold)
#             for v in value:
#                 worksheet.write(row+3, col+j, v)
#                 row+=1
#             j+=1

#     workbook.close()

# excel_file()
txt = ["aaa","ahad", "ddd"]

for item in txt:
    if item.startswith("aa") or item.startswith("ahad"):
        print(f"{item}: True")
    else:
        print(False)

